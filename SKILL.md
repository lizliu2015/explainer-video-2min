---
name: "explainer-video-2min"
description: "把任何话题、文章、链接或文件做成约2分钟、简单易懂的中文讲解短视频（口播配音+动态图卡+字幕，竖屏/横屏）。用于“做成讲解视频”“两分钟讲清楚X”等请求。"
---

# 两分钟讲解短视频

输入：一个话题 / 一篇文章 / 链接 / 附件。输出：`<标题>.mp4`（约2:00）+ `<标题>_脚本.md`（逐场景口播稿+画面说明）。

## 0. 默认参数（用户没说就用这些，不追问）
- 画幅：竖屏 1080×1920（抖音/视频号/Shorts）。用户说 YouTube/横屏 → 1920×1080。
- 语言：跟随输入；简繁跟随用户（繁体 `"script":"tc"`）。
- 配音：**必须用 ElevenLabs 声音 `E3IuT6dcpXhUwXqAw9Or`（Dennis - Warm & Clear，男声）**，流程见第 4 节。用户本次指定别的声音或给了配音文件（`voice_file`）时才换。
- 主题色：`ink`（深蓝+金）/`paper`（米白+朱红）/`jade`（墨绿+金），按话题气质选。玄学/传统文化优先 `jade` 或 `paper`。
- 时长目标 110–130 秒。

## 1. 吃透材料
- 只给话题 → 先 WebSearch 3–6 次，取事实、数字、一个好例子；数字必须有出处，写进脚本 md 末尾“来源”。
- 给文章/链接/文件 → 全文读完（链接用 WebFetch）。不加原文没有的观点；原文有错或过时，在脚本 md 里标注。
- 写下三样东西再动笔：
  1. **一句话核心**（≤25字，观众看完只记得住这一句）
  2. **最大误解/反常识点**（做开头钩子）
  3. **一个生活化比喻**（把抽象概念换成日常物件：钥匙和锁、水管、排队……）
- 材料太大装不进2分钟 → 只讲一个主线，其余放进脚本 md 的“未展开”清单，不硬塞。

## 1.5 八字/命理类视频：专业排盘（话题涉及八字、四柱、大运、某人命盘时必做）
- **自己重新排盘，不照抄原文**：把下方 `bazi.py` 原样写入工作目录，`pip install --break-system-packages -q lunar_python`，然后：
  `python3 bazi.py --solar "1898-03-04 12:00" --gender F [--lon 出生地经度] [--no-hour] [--sect 2]`（只有农历日期就用 `--lunar "1898-02-12 12:00"`）。
  会打印文字命盘（贴进脚本 md），并写出 `bazi_scenes.json`，里面有两个现成场景：`bazi`（命盘）和 `dayun`（大运）。
- **逐项核对原文**：四柱、十神、藏干、日空、大运干支、起运岁数和交运年份、顺排还是逆排（阳男阴女顺排，阴男阳女逆排）。原文写错就在脚本 md 的“核对”里标出来，口播以复算结果为准。
- **专业细节**：
  - 换年换月以节气为准（立春换年、节令换月），不按正月初一换年。出生日期靠近节气交接时，在 md 里提示边界。
  - 给了出生地就加 `--lon`，按真太阳时排（经度差＋均时差），命盘下方会注明校正了几分钟。
  - 子时流派默认 `--sect 2`（晚子时日柱不换日），23–24 点出生的要在 md 里说明用的是哪派。
  - 时辰不详时用 `--no-hour`，只排三柱，时柱显示“不详”。原文自己推出来的时辰，在 heading 或口播里说明是“推定时辰”。
  - 有生年争议的，每个版本各排一张命盘。
- **分镜**：至少放一个 `bazi` 命盘场景，原文讲大运时再放一个 `dayun` 场景，代替纯文字卡片。用 `hl` 跟着口播圈出被讲到的字（透干、合冲、空亡等）：
  - `bazi`：`"hl":[{"cells":[[1,"天干"],[3,"天干"]],"label":"偏印双透","cue":1}]`（列号 0 年、1 月、2 日、3 时；行可选 `柱`/`十神`/`天干`/`地支`/`藏干`）。圈注框画在格子上，标签排成表下一行的药丸，不压盘面。
  - `dayun`：`"hl":[{"i":2,"label":"嫁蒋","cue":0}]`（i 是第几步大运，从 0 数）。
  - 命盘场景不受“屏幕文字≤12字”的限制，但 heading 要短，比如“1898年 坤造”。
- **口播**：干支照字读（“戊戌年，甲寅月”）。术语第一次出现时用一句大白话带过，比如“偏印就是生你、护你的那股力量”。合冲刑害要说清是哪两个字，比如“丙辛合，寅亥合”。
- 涉及真实人物的争议史料（贪腐、政治指控等），与命理主线无关的放进“未展开”，不进口播。

## 2. 写口播稿（最关键）
**字数**：ElevenLabs Dennis 首次实测约 300 字/分钟（不含场景间停顿）。2 分钟 = **500–540 个有效汉字**（不算标点）。超了就删，不要靠加速。生成配音后以渲染器打印的 `TOTAL` 为准，只重做超长/过短的场景。
- narration 里不要写 ElevenLabs 语气标签（如 `[excited]`）：字幕直接取自 narration，标签会出现在字幕里。

**结构（6–8 个场景）**
| 段 | 秒数 | 内容 | 常用版式 |
|---|---|---|---|
| 钩子 | 0–10 | 反常识 / 提问 / 结果前置，第一句就抛冲突；第二句预告“两分钟讲清楚” | hook |
| 定义 | 10–25 | 关键概念 + 比喻 | big |
| 机制 | 25–70 | 2–3 个要点，或因果步骤 | list / steps / compare |
| 例子/应用 | 70–100 | 一个具体场景，解释开头的现象 | steps / compare |
| 金句 | 100–110 | 一句话核心的口语版 | big |
| 总结 | 110–125 | 重复核心 + 一句可行动的建议或余味 | end |

**易懂规则**
- 每句 ≤20 字，口语，能大声念顺。多用“你”。
- 一个场景只讲一件事。
- 每个术语出现时立刻用比喻或大白话解释；能不用术语就不用。
- 数字只留 1–3 个最有冲击力的，并四舍五入成好记的说法（“一半”“五六个小时”）。
- 用“第一、第二、第三”“所以”“但是”给听觉路标。
- 结尾回扣开头的钩子。
- 禁：书面连接词（“此外”“综上所述”）、长定语、括号、英文缩写不解释。

**节奏（停顿要落在画面变化上）**
- 一个场景 = 一段话 = 一个画面，3–5 句。画面变化只发生在句首：用 `cue` 把每张卡片绑到讲它的那一句。
- 每个场景说完后画面停约 1 秒（`scene_tail`，默认 1.0）；金句、总结场景设 1.5。
- 列表的最后一张卡片至少在场景结束前 2 秒出现，不要让卡片刚出来就切走。

**TTS 朗读修正**（写进 narration 前处理）
- 数字/年份/单位写成要读的样子：`2027年`→`二〇二七年`，`50%`→`百分之五十`，`3:1`→`三比一`。
- 多音字有歧义时换同义词（如“行”“重”“长”）。
- 英文、符号、表情不要进 narration；屏幕文字可以有。
- 用“，”控制停顿，用“。？！”断句（字幕和画面切换都按句子走）。

## 3. 分镜 storyboard.json
```json
{
  "title": "标题", "size": [1080,1920], "theme": "ink", "script": "sc", "speed": 0.95,
  "bgm": null, "bgm_volume": 0.12, "voice_file": null,
  "scenes": [
    {"layout":"hook","kicker":"两分钟讲清楚","heading":"咖啡其实不会\n给你能量","narration":"……"},
    {"layout":"big","heading":"腺苷","items":["大脑里的「疲劳计数器」"],"narration":"……"},
    {"layout":"list","heading":"三步","items":[{"title":"堆积","text":"醒得越久积得越多","cue":1}],"narration":"……"},
    {"layout":"compare","heading":"A vs B","items":[{"title":"A","text":"…\n…"},{"title":"B","text":"…","cue":0}],"narration":"……"},
    {"layout":"steps","heading":"过程","items":[{"title":"…","text":"…"}],"narration":"……"},
    {"layout":"end","heading":"一句话总结","items":["…","…"],"narration":"……"}
  ]
}
```
- 版式：`hook`（大标题+小眉题）、`big`（金色大字，单个概念/数字/金句，`size` 可调字号）、`list`（编号卡片≤3）、`steps`（带箭头的流程≤3）、`compare`（左右两栏，恰好2项）、`end`；八字类另有 `bazi`（四柱命盘：十神/天干/地支/藏干/纳音/长生，五行着色）和 `dayun`（大运 2×4 格），由 `bazi.py` 生成，见 1.5 节。
- 屏幕文字是**关键词，不是字幕**：heading ≤12字，卡片 title ≤6字、text ≤14字。`\n` 手动换行。
- `cue`：该卡片在第几句口播（从0数）开始时出现；不写则按句子均匀分配。也可用 `at`（秒）。让画面和“第一、第二”同步。
- 外部配音：设 `voice_file`，并给每个场景填 `dur`（秒），字幕按字数比例分配。

## 4. 配音（ElevenLabs，声音 ID `E3IuT6dcpXhUwXqAw9Or`）
固定用这个声音。ElevenLabs 不可用时停下告诉用户原因，**不要自行换成离线声音**；用户同意后才用下方离线后备。

**工具**：ElevenLabs 连接器的 `creative_create_flow`、`creative_generate_speech`、`creative_get_flow_run_status`。不在工具列表里 → 先用 ToolSearch 搜 `ElevenLabs generate speech`；仍没有 → 请用户在 claude.ai 连接 ElevenLabs 连接器，然后开新对话。

**确认点（花积分之前）**
- 用户在场：先用 SendUserMessage 发出完整口播稿（按场景分段，标出总字数和预估时长），等用户回“好/可以”或改稿后再配音。用户只改个别场景，就只改那几场。
- 用户不在场（定时任务、说过稍后回来、问题没人回）：直接按稿配音，交付时说明稿子没经过确认。
- 配音后先跑 PREVIEW 看 `TOTAL` 和关键帧；需要整片重配时先告诉用户，不要悄悄重配。

**流程**（每次生成都扣积分）：
1. `creative_create_flow`（name = 视频标题）→ 记下 `flow_id`，本视频所有配音都放这个 flow。
2. 每个场景调用一次 `creative_generate_speech`：`prompt` = 该场景 narration 全文，`voice_id` = `E3IuT6dcpXhUwXqAw9Or`，`model_id` = `eleven_v4`，`generations_count` = 1，`flow_id` = 上一步的。各场景可在同一轮并发发出。**绝不重复调用来重试**（会再扣一次）。
3. 等约 10 秒，用 `creative_get_flow_run_status`（flow_id + 全部 session_ids）取每个生成的 `media[].url`，按 prompt 对应回场景。
4. 下载：`curl -sS -o audio/01.mp3 "<url>"`（场景号两位数）。下载被拒（403 / CONNECT tunnel failed）→ 告诉用户：在 claude.ai 的 设置 → Capabilities 允许的域名里加上 `elevenlabsusercontent.com`，加好后再继续。不要换别的方式绕过。
5. storyboard.json 加 `"audio_dir": "audio"`。渲染器读 `audio/<场景号>.mp3`，先按字数估算字幕边界，再自动吸附到配音里的真实停顿（实测误差约 0.03 秒）；卡片按 `cue` 在对应句子开口时出现。
6. 改稿时只重新生成改动的场景，覆盖对应 mp3。

**成本**：约 1 积分/字（实测 30 字 = 31 积分），2 分钟视频约 520–560 积分。

### 离线后备（仅用户同意时；不设 `audio_dir` 即用离线女声）
```bash
pip install --break-system-packages -q sherpa-onnx soundfile
mkdir -p /tmp/tts && cd /tmp/tts
[ -d matcha-icefall-zh-baker ] || (curl -sSL -o m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/matcha-icefall-zh-baker.tar.bz2 && tar xjf m.tar.bz2)
[ -f vocos.onnx ] || curl -sSL -o vocos.onnx https://github.com/k2-fsa/sherpa-onnx/releases/download/vocoder-models/vocos-22khz-univ.onnx
```
字体用系统 Noto Sans CJK（`/usr/share/fonts/opentype/noto/`）。若 GitHub 下载失败：告诉用户，并改为请用户提供配音文件（`voice_file`），其余流程不变。

## 5. 渲染
把下方 `render.py` 原样写入工作目录（八字类再写入 `bazi.py`），然后：
1. **先预览**：`PREVIEW=1 python3 render.py storyboard.json out.mp4` → 生成配音、打印每场景秒数和 `TOTAL`，输出 `_build/preview_XX.png`（每场景 85% 时刻的满屏帧）。
   - `TOTAL` 不在 110–130s → 改稿（增删字），不要改 speed 超出 0.85–1.05。
   - 拼一张缩略总览看：`ffmpeg -i _build/preview_%02d.png -vf "scale=360:-1,tile=4x2" sheet.png`，用 Read 检查：文字溢出、卡片挤、字幕遮挡、空场景。
2. **全量渲染**：`python3 render.py storyboard.json <标题>.mp4`（2分钟竖屏约1分钟）。
3. 只改某场景画面：`ONLY=3,5 python3 render.py …`（其他场景复用已有片段）。改了 narration 则全量重跑。
4. 抽 2–3 帧（`ffmpeg -ss <秒> -i out.mp4 -frames:v 1 f.png`）在元素最多的时刻复查，`ffprobe` 确认时长。

## 6. 交付
- SendUserFile 发 mp4 + `<标题>_脚本.md`（场景表：时间码 / 口播 / 屏幕文字 / 来源）。
- 回复里只说：时长、一句话核心、可调项（换声音/横屏/主题色/加BGM）。
- 用户要改：改稿 → 只重渲受影响场景。

## render.py
```python
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

def silences(fn):
    """返回配音里每个停顿结束、下一句开口前的时刻（秒）。用于把句子/字幕边界吸附到真实停顿上。"""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", fn, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return [max(a, b - 0.05) for a, b in zip(st, en)]

def snap(expected, sil, win):
    """把预估边界吸附到最近的停顿（窗口内、单调递增），否则保留预估值。"""
    out, used, last = [], set(), -1
    for e in expected:
        best = None
        for i, x in enumerate(sil):
            if i in used or x <= last or abs(x - e) > win: continue
            if best is None or abs(x - e) < abs(sil[best] - e): best = i
        v = sil[best] if best is not None else max(e, last + 0.05)
        if best is not None: used.add(best)
        out.append(v); last = v
    return out

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

# ---------- 八字命盘 / 大运 ----------
WX = {}
for chs, col in (("甲乙寅卯", (46, 139, 87)), ("丙丁巳午", (205, 50, 40)), ("戊己辰戌丑未", (156, 102, 31)),
                 ("庚辛申酉", (196, 150, 20)), ("壬癸亥子", (30, 90, 170))):
    for c in chs: WX[c] = col
def wx(c): return WX.get(c, T["sub"])

def cue_time(sc, k):
    st = sc.get("_starts") or [0.6]
    return max(0.6, st[min(k, len(st) - 1)])

def hl_box(d, box, k, label=None):
    if k <= 0: return
    x0, y0, x1, y1 = box; pad = 6 * S * k
    d.rounded_rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], radius=int(18 * S), outline=T["acc"], width=max(2, int(6 * S * k)))
    if label:
        f = font(34); tw = d.textlength(label, font=f)
        d.rounded_rectangle([(x0 + x1) / 2 - tw / 2 - 14 * S, y1 + pad + 6 * S, (x0 + x1) / 2 + tw / 2 + 14 * S, y1 + pad + 56 * S], radius=int(12 * S), fill=T["acc"])
        d.text(((x0 + x1) / 2 - tw / 2, y1 + pad + 10 * S), label, font=f, fill=T["bg1"])

def draw_bazi(sc, t, img):
    """四柱命盘：十神/天干/地支/藏干(带十神)/纳音/十二长生，五行着色；hl 按 cue 圈出要点"""
    d = ImageDraw.Draw(img); ch = sc["chart"]; cols = ch["cols"]; base = T["bg1"]
    k_head = ease(t / 0.5)
    hh = text_block(d, (W / 2, TOP + (1 - k_head) * 30 * S), sc.get("heading", ""), font(64), T["fg"], W - 2 * M, alpha=k_head, base=base)
    y = TOP + hh + 50 * S
    lw = 120 * S; cw = (W - 2 * M - lw) / len(cols)
    rows = [("", 64), ("十神", 64), ("天干", 150), ("地支", 150), ("藏干", 168), ("纳音", 62), ("长生", 62)]
    top = y; ys = {}
    for name, h in rows: ys[name or "柱"] = (y, y + h * S); y += h * S
    d.rounded_rectangle([M - 10 * S, top - 10 * S, W - M + 10 * S, y + 10 * S], radius=int(24 * S), fill=blend(T["card"], base, k_head))
    for name, _ in rows[1:]:
        y0, y1 = ys[name]; f = font(34, False)
        d.text((M + 18 * S, (y0 + y1) / 2 - f.size * 0.62), name, font=f, fill=blend(T["sub"], T["card"], k_head))
        d.line([M + 10 * S, y0, W - M - 10 * S, y0], fill=blend(T["bg2"], T["card"], k_head), width=max(1, int(2 * S)))
    cell = {}
    for i, c in enumerate(cols):
        k = ease((t - 0.4 - i * 0.3) / 0.45)
        x0 = M + lw + i * cw; cx = x0 + cw / 2
        for name in ys: cell[(i, name)] = (x0 + 8 * S, ys[name][0] + 4 * S, x0 + cw - 8 * S, ys[name][1] - 4 * S)
        if k <= 0: continue
        def ctext(name, s, f, col):
            y0, y1 = ys[name]; tw = d.textlength(s, font=f)
            d.text((cx - tw / 2, (y0 + y1) / 2 - f.size * 0.62), s, font=f, fill=blend(col, T["card"], k))
        ctext("柱", c["name"], font(38), T["sub"])
        ctext("十神", c["ss"], font(40), T["acc"] if c["ss"] == "日主" else T["fg"])
        ctext("天干", c["gan"], font(118), wx(c["gan"]))
        ctext("地支", c["zhi"], font(118), wx(c["zhi"]))
        y0, y1 = ys["藏干"]; f = font(36, False); n = max(1, len(c["hide"]))
        for j, (hg, hs) in enumerate(c["hide"]):
            yy = y0 + (y1 - y0) * (j + 0.5) / 3 - f.size * 0.62 + (3 - n) * (y1 - y0) / 6
            s1 = hg; s2 = hs; w1 = d.textlength(s1, font=font(36)); w2 = d.textlength(s2, font=f)
            xx = cx - (w1 + 8 * S + w2) / 2
            d.text((xx, yy), s1, font=font(36), fill=blend(wx(hg), T["card"], k)); d.text((xx + w1 + 8 * S, yy), s2, font=f, fill=blend(T["sub"], T["card"], k))
        ctext("纳音", c["nayin"], font(34, False), T["sub"])
        ctext("长生", c["dishi"], font(34, False), T["sub"])
    ny = y + 40 * S
    for line in ch.get("notes", []):
        ny += text_block(d, (W / 2, ny), line, font(36, False), T["sub"], W - 2 * M, alpha=k_head, base=base) + 6 * S
    # hl: {"cells":[[列,"天干"|"地支"|"十神"|"藏干"|"柱"],...], "label":"丙辛合", "cue":句号}
    # 圈注框画在格子上；标签不压盘面，按出现顺序排成表下一行药丸
    tags = []
    for h in sc.get("hl", []):
        k = ease((t - cue_time(sc, h.get("cue", 0))) / 0.4)
        for ci, rn in h["cells"]: hl_box(d, cell[(ci, rn)], k)
        if h.get("label") and k > 0: tags.append((h["label"], k))
    if tags:
        f = font(40); pw = [d.textlength(s, font=f) + 44 * S for s, _ in tags]
        x = W / 2 - (sum(pw) + 20 * S * (len(tags) - 1)) / 2; ty = ny + 30 * S
        for (s, k), w in zip(tags, pw):
            d.rounded_rectangle([x, ty + (1 - k) * 20 * S, x + w, ty + 70 * S + (1 - k) * 20 * S], radius=int(35 * S), fill=blend(T["acc"], base, k))
            d.text((x + 22 * S, ty + 12 * S + (1 - k) * 20 * S), s, font=f, fill=blend(T["bg1"], T["acc"], k)); x += w + 20 * S

def draw_dayun(sc, t, img):
    """大运：2×4 格，干支五行着色 + 起运年/岁；hl 列出要圈的步序 {"i":2,"label":"嫁蒋","cue":0}"""
    d = ImageDraw.Draw(img); base = T["bg1"]; k_head = ease(t / 0.5)
    hh = text_block(d, (W / 2, TOP + (1 - k_head) * 30 * S), sc.get("heading", "大运"), font(64), T["fg"], W - 2 * M, alpha=k_head, base=base)
    y0 = TOP + hh + 60 * S; dy = sc["dayun"][:8]; per = 4 if VERT else 8
    gap = 22 * S; bw = (W - 2 * M - gap * (per - 1)) / per; bh = 300 * S
    boxes = []
    for i, x in enumerate(dy):
        r, c = divmod(i, per); bx = M + c * (bw + gap); by = y0 + r * (bh + 110 * S)
        boxes.append((bx, by, bx + bw, by + bh)); k = ease((t - 0.4 - i * 0.12) / 0.4)
        if k <= 0: continue
        d.rounded_rectangle(boxes[-1], radius=int(20 * S), fill=blend(T["card"], base, k))
        f = font(92); cx = bx + bw / 2
        for j, chh in enumerate(x["gz"]):
            tw = d.textlength(chh, font=f); d.text((cx - tw / 2, by + 20 * S + j * 100 * S), chh, font=f, fill=blend(wx(chh), T["card"], k))
        s = f"{x['year']}·{x['age']}岁"; fs = font(30, False); tw = d.textlength(s, font=fs)
        d.text((cx - tw / 2, by + bh - 50 * S), s, font=fs, fill=blend(T["sub"], T["card"], k))
    if sc.get("note"):
        rows = (len(dy) + per - 1) // per
        text_block(d, (W / 2, y0 + rows * (bh + 110 * S) - 40 * S), sc["note"], font(36, False), T["sub"], W - 2 * M, alpha=k_head, base=base)
    for h in sc.get("hl", []):
        if h["i"] < len(boxes): hl_box(d, boxes[h["i"]], ease((t - cue_time(sc, h.get("cue", 0))) / 0.4), h.get("label"))

def draw_scene(sc, t, dur, img):
    d = ImageDraw.Draw(img)
    lay = sc.get("layout", "big")
    if lay == "bazi": return draw_bazi(sc, t, img)
    if lay == "dayun": return draw_dayun(sc, t, img)
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
scene_tail = SB.get("scene_tail", 1.0)  # 整场景配音模式：说完后画面再停留的秒数
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
        # 字幕行 + 句首标记；按字数估边界，再吸附到配音的真实停顿上
        lines, heads = [], []
        for x in sents:
            ls = sub_lines(x, 16 if VERT else 22); heads.append(len(lines)); lines += ls
        w = [len(re.sub(r"[，。,\.；;：:、！？!?「」“”]", "", l)) or 1 for l in lines]
        cum = np.cumsum(w) / sum(w) * dl
        sil = silences(scene_mp3)
        edges = snap(list(cum[:-1]), [x for x in sil if 0.2 < x < dl - 0.2], 0.9)
        b = [0.0] + edges + [dl]
        for k, l in enumerate(lines): cues.append((t + b[k], t + b[k + 1], clean(l)))
        sc["_starts"] = [t + b[h] for h in heads]
        chunks.append(a); t += dl
        dur = t + scene_tail; chunks.append(np.zeros(int(SR * scene_tail), np.float32))
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
```

## bazi.py
```python
#!/usr/bin/env python3
"""bazi.py — 排盘 → 命盘场景 JSON（供 render.py 的 bazi / dayun 版式）
用法：
  python3 bazi.py --solar "1898-03-04 12:00" --gender F [--lon 121.47] [--no-hour] [--sect 2]
  python3 bazi.py --lunar "1898-02-12 12:00" --gender F ...
输出：stdout 打印文字命盘（贴进脚本md）；写 bazi_scenes.json（两个场景：bazi 命盘 + dayun 大运）。
--lon  出生地经度，换算真太阳时（经度差 + 均时差）；不给则按北京时间。
--no-hour  时辰不详：只排三柱，时柱显示「不详」。
--sect 1|2  子时流派：2=晚子时日柱不换日（默认），1=23点即换日。"""
import argparse, json, math, datetime as dt
from lunar_python import Solar, Lunar

ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--solar"); g.add_argument("--lunar")
ap.add_argument("--gender", choices=["M", "F"], required=True)
ap.add_argument("--lon", type=float); ap.add_argument("--no-hour", action="store_true")
ap.add_argument("--sect", type=int, default=2, choices=[1, 2]); ap.add_argument("--out", default="bazi_scenes.json")
A = ap.parse_args()

def parse(s):
    d, t = (s.split() + ["12:00"])[:2]; y, m, dd = map(int, d.split("-")); hh, mm = map(int, t.split(":")); return y, m, dd, hh, mm
if A.solar:
    s0 = dt.datetime(*parse(A.solar))
else:
    y, m, d, hh, mm = parse(A.lunar); so = Lunar.fromYmdHms(y, m, d, hh, mm, 0).getSolar()
    s0 = dt.datetime(so.getYear(), so.getMonth(), so.getDay(), hh, mm)
note_t = ""
if A.lon is not None and not A.no_hour:
    n = s0.timetuple().tm_yday; B = 2 * math.pi * (n - 81) / 364
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    off = 4 * (A.lon - 120) + eot; s1 = s0 + dt.timedelta(minutes=off)
    note_t = f"真太阳时 {s1:%H:%M}（经度{A.lon}°，校正{off:+.0f}分）"; s0 = s1
sol = Solar.fromYmdHms(s0.year, s0.month, s0.day, s0.hour, s0.minute, 0)
ec = sol.getLunar().getEightChar(); ec.setSect(A.sect)
P = [("年柱", "Year"), ("月柱", "Month"), ("日柱", "Day"), ("时柱", "Time")]
cols = []
for i, (nm, k) in enumerate(P):
    if k == "Time" and A.no_hour:
        cols.append(dict(name=nm, ss="", gan="?", zhi="?", hide=[], nayin="时辰不详", dishi="")); continue
    gz = getattr(ec, f"get{k}")()
    ss = "日主" if k == "Day" else getattr(ec, f"get{k}ShiShenGan")()
    hide = list(zip(getattr(ec, f"get{k}HideGan")(), getattr(ec, f"get{k}ShiShenZhi")()))
    cols.append(dict(name=nm, ss=ss, gan=gz[0], zhi=gz[1], hide=[list(h) for h in hide],
                     nayin=getattr(ec, f"get{k}NaYin")(), dishi=getattr(ec, f"get{k}DiShi")()))
yun = ec.getYun(1 if A.gender == "M" else 0)
dys = [d for d in yun.getDaYun()[1:9]]
qy = f"{yun.getStartYear()}岁{yun.getStartMonth()}个月起运（{yun.getStartSolar().toYmd()}交运）"
zao = "乾造" if A.gender == "M" else "坤造"
notes = [f"{zao} · 公历 {sol.toYmd()}" + ("" if A.no_hour else f" {s0:%H:%M}") + f" · 农历 {sol.getLunar().getYearInGanZhi()}年{sol.getLunar().getMonthInChinese()}月{sol.getLunar().getDayInChinese()}",
         f"日空 {ec.getDayXunKong()} · {qy}"]
if note_t: notes.append(note_t)
scenes = [
    {"layout": "bazi", "heading": f"{sol.getYear()}年 {zao}", "chart": {"cols": cols, "notes": notes}, "hl": [], "narration": ""},
    {"layout": "dayun", "heading": "大运", "dayun": [{"gz": d.getGanZhi(), "year": d.getStartYear(), "age": d.getStartAge()} for d in dys],
     "note": qy + ("，顺排" if yun.isForward() else "，逆排"), "hl": [], "narration": ""},
]
json.dump(scenes, open(A.out, "w"), ensure_ascii=False, indent=1)
# 文字命盘
print(notes[0]); print("      " + "  ".join(c["name"] for c in cols))
print("十神  " + "  ".join(f"{c['ss']:<4}" for c in cols))
print("天干  " + "    ".join(c["gan"] for c in cols)); print("地支  " + "    ".join(c["zhi"] for c in cols))
for r in range(3): print(("藏干  " if r == 0 else "      ") + "  ".join((f"{c['hide'][r][0]}{c['hide'][r][1]}" if r < len(c['hide']) else "    ").ljust(4) for c in cols))
print("纳音  " + "  ".join(c["nayin"] for c in cols)); print("长生  " + "  ".join(f"{c['dishi']:<4}" for c in cols))
for n in notes[1:]: print(n)
print("大运  " + "  ".join(f"{d['gz']}{d['year']}" for d in scenes[1]["dayun"]))
print(f"→ {A.out}")
```
