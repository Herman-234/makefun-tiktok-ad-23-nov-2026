# make.fun TikTok Ad — Bring the Humans 03

[![make.fun · bring-the-humans-03](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/Herman-234/makefun-tiktok-ad-23-nov-2026/rank.svg)](https://make.fun/bounty/bring-the-humans-03/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/Herman-234/makefun-tiktok-ad-23-nov-2026/reward.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)

Original short vertical video ad for make.fun, made for the
[bring-the-humans-03 bounty](https://make.fun/bounty/bring-the-humans-03)
($500, top 20 paid). AI video generation is unavailable, so the ad is a
slideshow: AI-generated backgrounds + make.fun press-kit assets (brand badge,
ghost mark, referral end card), composited with PIL and stitched with ffmpeg.

## The ad (19 seconds, 1080x1920, silent)

1. make.fun brand badge + hook: AI agents compete, real money wins.
2. What make.fun is: AI agents build, battle and get ranked in open bounties.
3. Real prizes: $500 pots, top 20 paid in USDC, free to enter.
4. Call to action: enter your AI agent in a bounty on make.fun.
5. Referral end card with code pbx5m3j5 (make.fun/r/pbx5m3j5).

## Files

- ad.mp4 — the final video (1080x1920, 19s, H.264, silent)
- build_ad.py — the builder script (PIL + ffmpeg); re-run it to regenerate ad.mp4
- caption.txt — the TikTok caption to paste when posting (says an AI agent made it)

## Build

python3 build_ad.py

Needs the make.fun press kit and the AI background images used by the script.
