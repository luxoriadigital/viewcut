# BRIEF — Viewcut VSL (FR + EN)

## Product
**Viewcut** — video editing **service** sold on **output**: `€10 per finished video hour` (edited, captioned, ready to publish) vs market average `€35/h` of editing time. No subscription, no tool to learn. Deliverables: vertical (9:16 Reels/Shorts), wide (16:9), 1:1, burned-in captions, **timed YouTube chapters**, French **and** English versions (same script, rewritten, two voices).

## Audience
Creators posting weekly (drowning in editing), e-commerce brands needing monthly variations, agencies reselling video to clients without hiring another editor. Time-pressed, skeptical of SaaS subscriptions, wants a price per result.

## Promise of this video
In ~3–4 minutes: show the price gap (35 → 10), name the real cost (weeks without publishing), explain the mechanism (you buy the file, not the tool), show the proof (1,000,000+ views, screenshots on the page), then send one CTA: **send one clip, receive one edited video**.

## Tone
Direct, commercial, confident, plain French / plain English. No jargon, no hype words, no fake numbers. Market-rate and view-count figures are the only claims — they come from the client.

## Structure (13 slides, both languages)
HOOK → PROBLEM → COST → MECHANISM → PROOF → PRICE → PROCESS → FORMATS → (LANGUAGES) → OBJECTION → (TURNAROUND) → WHO IT'S FOR → CTA.
Slides in parentheses are not YouTube chapters. 10 chapters per language.

## Visual system
- Canvas 1920×1080, 30 fps. Dark deck: bg `#0b0f1a`, panel `#141b2e`, fg `#e9eef9`, mute `#93a0bd`, line `rgba(147,160,189,.22)`, accent blue `#0055ff` / `#4d84ff`, secondary green `#34d399`, red `#ff7a7a`.
- Per-slide `tone-blue` / `tone-green` / `tone-red` kickers; persistent grid + radial glow + top bar wordmark `Viewcut` + bottom progress bar.
- Type: heavy tight-tracked display (Montserrat/Arial stack), mono kickers with timecode, one accent line per title, 3 bullets max, slide counter `n / 13`.
- Deterministic only: GSAP paused root timeline registered on `window.__timelines["main"]`, every timed element `class="clip"` with `data-start` + `data-duration`.

## Audio
- VO only, one `<audio>` clip per slide, male voices: **FR `fr-FR-HenriNeural`**, **EN `en-US-AndrewNeural`**.
- 0.8 s silence after each slide; audio duration = slide duration − 0.8.
- No music (keeps render simple and avoids licensing questions).

## Outputs
- `renders/viewcut-vsl-fr.mp4` (composition `index.html`)
- `renders/viewcut-vsl-en.mp4` (composition `compositions/en.html`)
- `../chapters-fr.txt` / `../chapters-en.txt` (paste-ready YouTube description chapters) + `../assets/chapters.json` for the landing page.

## Rules
- No invented testimonials, client names, logos, or metrics.
- Every number visible on screen must exist in `scripts/fr.json` / `scripts/en.json`.
- UI language of each render matches its script language (labels, bullets, counters).
