#!/usr/bin/env python3
"""render.py storyboard.json out.mp4  —  2分钟讲解短视频渲染器
TTS(逐句) -> 每场景一段mp4(Pillow逐帧 → ffmpeg) -> concat -> 混音频。"""
import json, os, re, subprocess, sys, glob, math
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

SB = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
W, H = SB.get("size", [1080, 1920])
FPS = 30
WORK = os.path.join(os.path.dirname(os.path.abspath(OUT)), "_build")
os.makedirs(WORK, exist_ok=True)
VERT = H > W
S = min(W, H) / 1080  # 尺寸基准

# ---------- 字体 ----------
TC = SB.get("script", "sc") == "tc"
FIDX = 3 if TC else 2  # Noto CJK ttc: 0JP 1KR 2SC 3TC 4HK
FD = "/usr/share/fonts/opentype/noto/"
BOLD = next((FD + f for f in ["NotoSansCJK-Bold.ttc", "NotoSansCJK-Black.ttc"] if os.path.exists(FD + f)))
REG = FD + "NotoSansCJK-Regular.ttc"
_fc = {}
def font(sz, bold=True):
    k = (sz, bold)
    if k not in _fc: _fc[k] = ImageFont.truetype(BOLD if bold else REG, int(sz * S), index=FIDX)
    return _fc[k]

# ---------- 配色 ----------
THEMES = {
    "ink":   dict(bg1=(18, 24, 38), bg2=(32, 44, 70), fg=(245, 245, 240), sub=(170, 182, 205), acc=(255, 196, 61), card=(40, 54, 86)),
    "paper": dict(bg1=(250, 246, 238), bg2=(238, 230, 214), fg=(34, 34, 34), sub=(110, 104, 96), acc=(200, 60, 45), card=(255, 255, 255)),
    "jade":  dict(bg1=(14, 40, 36), bg2=(24, 66, 58), fg=(240, 248, 244), sub=(160, 200, 188), acc=(240, 200, 110), card=(30, 80, 70)),
}
T = THEMES[SB.get("theme", "ink")]

# ---------- TTS ----------
_tts = None
def tts_engine():
    global _tts
    if _tts: return _tts
    import sherpa_onnx as so
    M = os.environ.get("TTS_DIR", "/tmp/tts") + "/matcha-icefall-zh-baker"
    V = os.environ.get("TTS_DIR", "/tmp/tts") + "/vocos.onnx"
    cfg = so.OfflineTtsConfig(model=so.OfflineTtsModelConfig(
        matcha=so.OfflineTtsMatchaModelConfig(acoustic_model=M + "/model-steps-3.onnx", vocoder=V,
            lexicon=M + "/lexicon.txt", tokens=M + "/tokens.txt", dict_dir=M + "/dict"), num_threads=4),
        rule_fsts=f"{M}/phone.fst,{M}/date.fst,{M}/number.fst")
    _tts = so.OfflineTts(cfg)
    return _tts

SR = 22050
AUDIO_DIR = SB.get("audio_dir")  # 预生成配音：<audio_dir>/<场景号>.mp3（整场景）或 <场景号>_<句号>.mp3（逐句）
def say(text, speed, key=None):
    if AUDIO_DIR:
        fn = f"{AUDIO_DIR}/{key}.mp3"
        if not os.path.exists(fn): sys.exit(f"缺少配音文件 {fn}")
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", fn, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        return np.frombuffer(raw, dtype=np.float32).copy()
    a = tts_engine().generate(text, sid=0, speed=speed)
    x = np.asarray(a.samples, dtype=np.float32)
    if a.sample_rate != SR:  # 简单重采样
        idx = np.linspace(0, len(x) - 1, int(len(x) * SR / a.sample_rate)); x = np.interp(idx, np.arange(len(x)), x).astype(np.float32)
    return x

def sentences(t):
    parts = re.findall(r"[^。！？!?]+[。！？!?」”]*", t.strip())
    return [p.strip() for p in parts if p.strip()]

def sub_lines(sent, maxc):
    """一句拆成若干字幕行（按逗号），每行≤maxc字"""
    bits = re.findall(r"[^，,；;：:、]+[，,；;：:、]?", sent)
    lines, cur = [], ""
    for b in bits:
        if cur and len(cur) + len(b) > maxc: lines.append(cur); cur = b
        else: cur += b
    if cur: lines.append(cur)
    out = []
    for l in lines:
        while len(l) > maxc: out.append(l[:maxc]); l = l[maxc:]
        out.append(l)
    return out

def clean(s): return re.sub(r"[，。,\.；;：:、！？!?]+$", "", s)

# ---------- 绘图工具 ----------
def bg_base():
    g = np.linspace(0, 1, H)[:, None, None]
    a = np.array(T["bg1"])[None, None]; b = np.array(T["bg2"])[None, None]
    img = (a * (1 - g) + b * g).repeat(W, 1).astype(np.uint8)
    return Image.fromarray(img, "RGB")
BG = bg_base()

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n": lines.append(cur); cur = ""; continue
        if d.textlength(cur + ch, font=f) > maxw and cur: lines.append(cur); cur = ch
        else: cur += ch
    if cur: lines.append(cur)
    # 避免行首标点
    for i in range(1, len(lines)):
        if lines[i] and lines[i][0] in "，。、！？；：,.!?」”）)":
            lines[i - 1] += lines[i][0]; lines[i] = lines[i][1:]
    return [l for l in lines if l]

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3

def text_block(d, xy, text, f, fill, maxw, align="center", lh=1.3, alpha=1.0, base=None):
    lines = wrap(d, text, f, maxw); x, y = xy
    asc = f.size * lh
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=f)
        lx = x - tw / 2 if align == "center" else x
        col = blend(fill, base, alpha) if base else fill
        d.text((lx, y + i * asc), l, font=f, fill=col)
    return len(lines) * asc

def blend(c, base, a): return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))

# ---------- 版式 ----------
M = int(80 * S)  # 边距
TOP = int((260 if VERT else 90) * S)
SUB_Y = H - int((430 if VERT else 150) * S)  # 字幕区顶

def draw_scene(sc, t, dur, img):
    d = ImageDraw.Draw(img)
    lay = sc.get("layout", "big")
    items = sc.get("items", [])
    n = max(1, len(items))
    # 元素出现时刻：显式at(秒) / cue(第几句) / 按句子均匀分配
    st = sc.get("_starts") or [0.6]
    def at_of(i, it):
        if isinstance(it, dict) and it.get("at") is not None: return it["at"]
        k = it.get("cue") if isinstance(it, dict) and it.get("cue") is not None else int(i * len(st) / n)
        return max(0.6, st[min(k, len(st) - 1)])
    ats = [at_of(i, it) for i, it in enumerate(items)]
    k_head = ease(t / 0.5)
    base = T["bg1"]
    if lay in ("hook", "big", "end"):
        hy = H * (0.30 if VERT else 0.28)
        if sc.get("kicker"):
            hy += text_block(d, (W / 2, hy - 90 * S), sc["kicker"], font(40), T["acc"], W - 2 * M, alpha=k_head, base=base) - 60 * S
        f = font(sc.get("size", 96 if lay == "hook" else 120 if lay == "big" else 84))
        dy = (1 - k_head) * 40 * S
        h = text_block(d, (W / 2, hy + dy), sc.get("heading", ""), f, T["acc"] if lay == "big" else T["fg"], W - 2 * M, alpha=k_head, base=base)
        y = hy + h + 40 * S
        for i, it in enumerate(items):
            k = ease((t - ats[i]) / 0.45)
            if k <= 0: continue
            txt = it["text"] if isinstance(it, dict) else it
            y += text_block(d, (W / 2, y + (1 - k) * 30 * S), txt, font(52, False), T["sub"], W - 2 * M, alpha=k, base=base) + 18 * S
        return
    # 卡片类：list / steps / compare
    f_h = font(64)
    hh = text_block(d, (W / 2, TOP + (1 - k_head) * 30 * S), sc.get("heading", ""), f_h, T["fg"], W - 2 * M, alpha=k_head, base=base)
    d.rectangle([W / 2 - 60 * S, TOP + hh + 14 * S, W / 2 + 60 * S, TOP + hh + 22 * S], fill=blend(T["acc"], base, k_head))
    y0 = TOP + hh + 80 * S
    avail = SUB_Y - 40 * S - y0
    if lay == "compare" and len(items) == 2:
        cw = (W - 2 * M - 40 * S) / 2
        for i, it in enumerate(items):
            k = ease((t - ats[i]) / 0.45)
            if k <= 0: continue
            x0 = M + i * (cw + 40 * S); yy = y0 + (1 - k) * 40 * S
            d.rounded_rectangle([x0, yy, x0 + cw, yy + min(avail, 620 * S)], radius=int(28 * S), fill=blend(T["card"], base, k))
            text_block(d, (x0 + cw / 2, yy + 50 * S), it.get("title", ""), font(56), blend(T["acc"], T["card"], k), cw - 60 * S)
            text_block(d, (x0 + cw / 2, yy + 160 * S), it.get("text", ""), font(50, False), blend(T["fg"], T["card"], k), cw - 60 * S, lh=1.45)
        return
    gap = 28 * S
    ch = min((avail - gap * (n - 1)) / n, 300 * S)
    for i, it in enumerate(items):
        k = ease((t - ats[i]) / 0.45)
        if k <= 0: continue
        it = it if isinstance(it, dict) else {"text": it}
        yy = y0 + i * (ch + gap) + (1 - k) * 40 * S
        d.rounded_rectangle([M, yy, W - M, yy + ch], radius=int(24 * S), fill=blend(T["card"], base, k))
        badge = it.get("icon") or (str(i + 1))
        r = 46 * S; cx = M + 40 * S + r; cy = yy + ch / 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=blend(T["acc"], T["card"], k))
        bf = font(48); bw = d.textlength(badge, font=bf)
        d.text((cx - bw / 2, cy - bf.size * 0.62), badge, font=bf, fill=blend(T["bg1"], T["acc"], k))
        tx = cx + r + 36 * S; tw = W - M - 40 * S - tx
        title = it.get("title"); body = it.get("text", "")
        ft, fb = font(54), font(46, False)
        tl = wrap(d, title, ft, tw) if title else []
        bl = wrap(d, body, fb, tw) if body else []
        th = len(tl) * ft.size * 1.25 + (12 * S if tl and bl else 0) + len(bl) * fb.size * 1.4
        ty = cy - th / 2
        for l in tl: d.text((tx, ty), l, font=ft, fill=blend(T["fg"], T["card"], k)); ty += ft.size * 1.25
        if tl and bl: ty += 12 * S
        for l in bl: d.text((tx, ty), l, font=fb, fill=blend(T["sub"], T["card"], k)); ty += fb.size * 1.4
        if lay == "steps" and i < n - 1 and k > 0.9:
            ax = cx; d.polygon([(ax - 16 * S, yy + ch + 4 * S), (ax + 16 * S, yy + ch + 4 * S), (ax, yy + ch + gap - 2 * S)], fill=T["acc"])

def draw_sub(img, line):
    if not line: return
    d = ImageDraw.Draw(img); f = font(54 if VERT else 46)
    lines = wrap(d, line, f, W - 2 * M - 40 * S)
    lh = f.size * 1.35; boxh = len(lines) * lh + 36 * S
    y = SUB_Y + (60 * S if VERT else 0)
    widest = max(d.textlength(l, font=f) for l in lines)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([W / 2 - widest / 2 - 30 * S, y, W / 2 + widest / 2 + 30 * S, y + boxh], radius=int(18 * S), fill=(0, 0, 0, 150))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=f)
        d.text((W / 2 - tw / 2, y + 18 * S + i * lh), l, font=f, fill=(255, 255, 255))

def progress(img, frac):
    d = ImageDraw.Draw(img); h = int(8 * S)
    d.rectangle([0, H - h, int(W * frac), H], fill=T["acc"])

# ---------- 主流程 ----------
speed = SB.get("speed", 0.95)
gap_s, tail_s = 0.25, 0.45
voice_file = SB.get("voice_file")  # 外部整段配音时，场景时长取 sc["dur"]
all_audio, plan, total = [], [], 0.0
for si, sc in enumerate(SB["scenes"]):
    cues, t = [], 0.25 if si == 0 else 0.1
    chunks = [np.zeros(int(SR * t), np.float32)]
    scene_mp3 = f"{AUDIO_DIR}/{si+1:02d}.mp3" if AUDIO_DIR else None
    if scene_mp3 and os.path.exists(scene_mp3):
        # 整场景一段配音（ElevenLabs）：字幕/卡片按字数比例分配时间
        a = say(None, speed, f"{si+1:02d}"); dl = len(a) / SR
        sents = sentences(sc.get("narration", ""))
        tot = sum(len(x) for x in sents) or 1; c = t; sc["_starts"] = []
        for x in sents:
            sc["_starts"].append(c)
            ls = sub_lines(x, 16 if VERT else 22); xl = dl * len(x) / tot; lt = sum(len(l) for l in ls) or 1
            for l in ls:
                ld = xl * len(l) / lt; cues.append((c, c + ld, clean(l))); c += ld
        chunks.append(a); t += dl
        dur = t + tail_s; chunks.append(np.zeros(int(SR * tail_s), np.float32))
    elif voice_file:
        dur = float(sc["dur"])
        lines = [l for s in sentences(sc.get("narration", "")) for l in sub_lines(s, 16 if VERT else 22)]
        tot = sum(len(l) for l in lines) or 1; cur = 0.1
        for l in lines:
            dl = (dur - 0.3) * len(l) / tot; cues.append((cur, cur + dl, clean(l))); cur += dl
    else:
        sc["_starts"] = []
        for j, s in enumerate(sentences(sc.get("narration", ""))):
            sc["_starts"].append(t)
            a = say(s, speed, f"{si+1:02d}_{j+1:02d}"); dl = len(a) / SR
            lines = sub_lines(s, 16 if VERT else 22); tot = sum(len(l) for l in lines)
            c = t
            for l in lines:
                ld = dl * len(l) / tot; cues.append((c, c + ld, clean(l))); c += ld
            chunks += [a, np.zeros(int(SR * gap_s), np.float32)]; t += dl + gap_s
        dur = t + tail_s; chunks.append(np.zeros(int(SR * tail_s), np.float32))
    nf = int(round(dur * FPS)); dur = nf / FPS
    if not voice_file:
        a = np.concatenate(chunks); a = np.pad(a, (0, max(0, int(dur * SR) - len(a))))[: int(dur * SR)]; all_audio.append(a)
    plan.append((sc, dur, cues, total)); total += dur
    print(f"scene {si+1}: {dur:.1f}s", flush=True)
print(f"TOTAL {total:.1f}s", flush=True)
if not voice_file: sf.write(f"{WORK}/voice.wav", np.concatenate(all_audio), SR)

only = set(int(x) for x in os.environ.get("ONLY", "").split(",") if x)
preview = os.environ.get("PREVIEW")  # PREVIEW=1 → 只出每场景关键帧PNG
files = []
for si, (sc, dur, cues, t0) in enumerate(plan):
    fn = f"{WORK}/s{si+1:02d}.mp4"; files.append(fn)
    if preview:
        t = dur * 0.85; img = BG.copy(); draw_scene(sc, t, dur, img)
        draw_sub(img, next((c[2] for c in cues if c[0] <= t < c[1]), cues[-1][2] if cues else "")); progress(img, (t0 + t) / total)
        img.save(f"{WORK}/preview_{si+1:02d}.png"); continue
    if only and (si + 1) not in only and os.path.exists(fn): continue
    tmp = fn[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    nf = int(round(dur * FPS))
    for fi in range(nf):
        t = fi / FPS; img = BG.copy(); draw_scene(sc, t, dur, img)
        draw_sub(img, next((c[2] for c in cues if c[0] <= t < c[1]), ""))
        progress(img, (t0 + t) / total)
        if t > dur - 0.2: img = Image.blend(img, BG, (t - (dur - 0.2)) / 0.2 * 0.6)
        p.stdin.write(img.tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, fn)
    print(f"rendered {fn}", flush=True)
if preview: sys.exit(0)

with open(f"{WORK}/list.txt", "w") as f:
    for fn in files: f.write(f"file '{fn}'\n")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt", "-c", "copy", f"{WORK}/video.mp4"], check=True)
aud = voice_file or f"{WORK}/voice.wav"
cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", f"{WORK}/video.mp4", "-i", aud]
bgm = SB.get("bgm")
if bgm:
    cmd += ["-stream_loop", "-1", "-i", bgm, "-filter_complex",
            f"[2:a]volume={SB.get('bgm_volume', 0.12)}[b];[1:a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]", "-map", "0:v", "-map", "[a]"]
else:
    cmd += ["-filter:a", "loudnorm=I=-16:TP=-1.5", "-map", "0:v", "-map", "1:a"]
cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT]
subprocess.run(cmd, check=True)
print("DONE", OUT)
