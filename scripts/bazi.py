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
