# explainer-video-2min

Claude skill：把任何话题 / 文章 / 链接 / 文件做成约 2 分钟、简单易懂的中文讲解短视频（口播配音 + 动态图卡 + 字幕，竖屏 9:16 或横屏 16:9）。

## 文件
- `SKILL.md` — skill 本体（流程、脚本写作规则、分镜格式；内嵌 render.py）
- `scripts/render.py` — 渲染器（与 SKILL.md 内嵌版本一致）
- `examples/coffee_storyboard.json` — 样例分镜（咖啡为什么让你清醒）

## 配音
默认用 ElevenLabs 声音 `E3IuT6dcpXhUwXqAw9Or`（Dennis - Warm & Clear），通过 ElevenLabs 连接器按场景生成，下载到 `audio/01.mp3…`，分镜里设 `"audio_dir": "audio"`。不设 `audio_dir` 时用离线 sherpa-onnx 女声作后备。

## 用法
```bash
pip install sherpa-onnx soundfile pillow numpy   # 另需 ffmpeg、Noto Sans CJK 字体
# 下载离线中文 TTS 模型到 /tmp/tts（见 SKILL.md 第 4 节）
PREVIEW=1 python3 scripts/render.py examples/coffee_storyboard.json out.mp4   # 预览帧 + 时长
python3 scripts/render.py examples/coffee_storyboard.json out.mp4             # 完整渲染
```
