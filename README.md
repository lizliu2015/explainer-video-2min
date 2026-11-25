# explainer-video-2min

Claude skill：把任何话题 / 文章 / 链接 / 文件做成约 2 分钟、简单易懂的中文讲解短视频（口播配音 + 动态图卡 + 字幕，竖屏 9:16 或横屏 16:9）。

## 文件
- `SKILL.md` — skill 本体（流程、脚本写作规则、分镜格式；内嵌 render.py）
- `scripts/render.py` — 渲染器（与 SKILL.md 内嵌版本一致）
- `scripts/bazi.py` — 八字排盘（lunar_python；真太阳时、子时流派、时辰不详），输出 `bazi` 命盘与 `dayun` 大运场景（与 SKILL.md 内嵌版本一致）
- `examples/coffee_storyboard.json` — 样例分镜（咖啡为什么让你清醒）
- `examples/bazi_storyboard.json` — 八字样例分镜（命盘 + 大运，带圈注）
- `examples/fengfei_storyboard.json` — 人物八字样例（印章钩子、精简命盘 `compact`、时间轴 `timeline`），对应《锋菲恋八字》

## 配音
默认用 ElevenLabs 声音 `E3IuT6dcpXhUwXqAw9Or`（Dennis - Warm & Clear），通过 ElevenLabs 连接器按场景生成，下载到 `audio/01.mp3…`，分镜里设 `"audio_dir": "audio"`。不设 `audio_dir` 时用离线 sherpa-onnx 女声作后备。

## 用法
```bash
pip install sherpa-onnx soundfile pillow numpy   # 另需 ffmpeg、Noto Sans CJK 字体
# 下载离线中文 TTS 模型到 /tmp/tts（见 SKILL.md 第 4 节）
PREVIEW=1 python3 scripts/render.py examples/coffee_storyboard.json out.mp4   # 预览帧 + 时长
python3 scripts/render.py examples/coffee_storyboard.json out.mp4             # 完整渲染
```

## 渲染器功能
- `stamp`：任何场景可加的印章（判词 / 反转），在指定句子时“盖”下。
- `timeline` 版式：竖向时间轴，逐条弹出；用于“预测 vs 现实”、事件经过、年表。
- `bazi` 的 `"compact": true`：只留柱 / 十神 / 天干 / 地支四行，大字，面向大众。
- 自动推镜：场景缓慢推近；`bazi`/`dayun` 的 `hl` 圈注出现时推到被圈格子（`"zoom": false` 关闭）。
- `squeeze`（默认 0.26 秒）：压缩 ElevenLabs 配音里的长停顿；字幕吸附在压缩后的音频上进行。
- 竖屏字幕上移到约 2/3 高度，避开抖音 / 视频号底部遮挡区。
