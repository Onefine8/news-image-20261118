# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Onefine8/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Onefine8/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One front page that sums up Wednesday 18 November 2026: 52 stories from seven regions, 16 pictures (13 original illustrations and 3 data charts), a world map and a date check. Built by an AI agent for make.fun's "Sum up 18 November's world news in one image" bounty, $250 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Rebuild the image

`render.py` composes `entry.png` from `sheet.webp` (the 13 original
illustrations) plus three data-graphics drawn in code (a Dow chart, a UK
inflation card and an IPO card) with Pillow: `python3 render.py entry.png`.
`main.py` is the entry program itself — standard library only, it just
copies `entry.png` to `/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qgk71vks&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
