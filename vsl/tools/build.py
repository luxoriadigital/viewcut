"""Build the Viewcut VSL: TTS (male) -> timeline -> chapters -> HTML compositions.

Usage:  py tools/build.py            (both languages)
        py tools/build.py fr         (one language)
Outputs:
  build/slides-{lang}.json
  index.html            (FR composition)
  compositions/en.html   (EN composition)
  ../chapters-fr.txt ../chapters-en.txt ../assets/chapters.json
"""
import html
import json
import re
import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent
GAP = 0.8

TONES = {
    "HOOK": "blue", "MECHANISM": "blue", "PRICE": "blue", "CTA": "blue",
    "PROBLEM": "red", "COST": "red", "OBJECTION": "red", "TURNAROUND": "red",
    "PROOF": "green", "PROCESS": "green", "FORMATS": "green",
    "LANGUAGES": "green", "WHO IT'S FOR": "green",
}
TOPBAR = {
    "fr": "Résultat &middot; 10 &euro;/h &middot; FR + EN",
    "en": "Output &middot; &euro;10/h &middot; FR + EN",
}
SITE = {"fr": "viewcut &middot; envoie tes images", "en": "viewcut &middot; send one clip"}
# FR kickers: no English words on a French screen
DISP_FR = {"HOOK": "ACCROCHE", "PROCESS": "ÉTAPES", "OBJECTION": "DOUTES ?", "CTA": "QUE FAIRE ?"}
TOTALS = {}

# Human prosody patterns (research-backed: lower base pitch + wider range,
# variable pace, slow/low on money facts, high/brisk on hook & proof, energy on CTA).
# rate: momentum vs weight · pitch: authority (-) vs excitement (+)
PROSODY = {
    "HOOK":         ("+10%", "+1Hz"),
    "PROBLEM":      ("+0%",  "-2Hz"),
    "COST":         ("-4%",  "-3Hz"),
    "MECHANISM":    ("+4%",  "-1Hz"),
    "PROOF":        ("+8%",  "+1Hz"),
    "PRICE":        ("-4%",  "-2Hz"),
    "PROCESS":      ("+4%",  "-1Hz"),
    "FORMATS":      ("+6%",  "+0Hz"),
    "OBJECTION":    ("+6%",  "+1Hz"),
    "TURNAROUND":   ("+2%",  "-2Hz"),
    "WHO IT'S FOR": ("+4%",  "+0Hz"),
    "POUR QUI":     ("+4%",  "+0Hz"),
    "DÉLAIS":       ("+2%",  "-2Hz"),
    "CTA":          ("+8%",  "+1Hz"),
}

def esc(s):
    return html.escape(s, quote=False)

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)

def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.strip())

GAP_MS = 140  # breath between sentences (robotic -> human pacing)

def _edge(voice, text, dest, rate="+0%", pitch="+0Hz"):
    exe = shutil.which("edge-tts") or "edge-tts"
    base = ["--voice", voice, "--text", text, "--write-media", str(dest),
            f"--rate={rate}", f"--pitch={pitch}"]
    r = run([exe] + base)
    if r.returncode != 0 or not dest.exists():
        r = run(["cmd", "/c", "edge-tts"] + base)
    if not dest.exists() or dest.stat().st_size < 2000:
        raise SystemExit(f"TTS failed: {dest}\n{r.stdout}\n{r.stderr}")

def _gap_file():
    g = ROOT / "assets" / "vo" / "_gap.mp3"
    if not g.exists():
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", f"{GAP_MS/1000:.3f}", "-c:a", "libmp3lame", "-b:a", "48k", str(g)])
    return g

def _split_sentences(text):
    text = " ".join(text.split())
    parts = re.split(r"(?<=[.!?…])\s+", text)
    out = [p.strip() for p in parts if p.strip()]
    # drop punctuation-only fragments ("…", "-") that TTS refuses to speak
    return [p for p in out if re.sub(r"[^\w]", "", p, flags=re.UNICODE)]

def _sent_prosody(base, s, i):
    """Wide, alternating sentence-to-sentence motion: kills the monotone read.
    Momentum flips each sentence; questions lift; money slows down and drops."""
    rate = int(base[0].rstrip("%")) + (5 if i % 2 == 0 else -5)
    pitch = int(base[1].replace("Hz", "")) + (3 if i % 2 == 0 else -3)
    if s.rstrip().endswith("?"):
        pitch += 5
        rate += 3
    if re.search(r"\d", s) or re.search(r"euros?|\bdollars?\b|€", s, re.I):
        rate -= 7
        pitch -= 3
    rate = max(-45, min(45, rate))
    pitch = max(-15, min(15, pitch))
    return f"{rate:+d}%", f"{pitch:+d}Hz"

def synth(voice, text, dest, rate="+0%", pitch="+0Hz"):
    if dest.exists() and dest.stat().st_size > 2000:
        return
    sents = _split_sentences(text)
    if len(sents) < 2:
        _edge(voice, text, dest, rate=rate, pitch=pitch)
        return
    parts = ROOT / "assets" / "vo" / "_parts" / dest.stem
    parts.mkdir(parents=True, exist_ok=True)
    gap = _gap_file()
    files = []
    for i, s in enumerate(sents):
        f = parts / f"{i:02d}.mp3"
        sr, sp = _sent_prosody((rate, pitch), s, i)
        _edge(voice, s, f, rate=sr, pitch=sp)
        files.append(f)
        if i < len(sents) - 1:
            files.append(gap)
    lst = parts / "list.txt"
    lst.write_text(
        "\n".join("file '" + str(f).replace("\\", "/") + "'" for f in files) + "\n",
        encoding="utf-8")
    r = run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
             "-ar", "24000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "64k",
             str(dest)])
    if not dest.exists() or dest.stat().st_size < 2000:
        raise SystemExit(f"concat failed: {dest}\n{r.stdout}\n{r.stderr}")

def tc(seconds):
    m = int(seconds // 60)
    s = int(round(seconds - m * 60))
    if s == 60:
        m, s = m + 1, 0
    return f"{m}:{s:02d}"

def build(lang):
    data = json.loads((ROOT / "scripts" / f"{lang}.json").read_text(encoding="utf-8"))
    voice, slides = data["voice"], data["slides"]
    (ROOT / "assets" / "vo").mkdir(parents=True, exist_ok=True)

    t = 0.0
    rows = []
    for i, sl in enumerate(slides, 1):
        mp3 = ROOT / "assets" / "vo" / f"{lang}-{i:02d}.mp3"
        rate, pitch = PROSODY.get(sl["label"], ("+0%", "-1Hz"))
        synth(voice, sl["vo"], mp3, rate=rate, pitch=pitch)
        adur = probe(mp3)
        sdur = round(adur + GAP, 3)
        tone = TONES.get(sl["label"], "blue")
        rows.append({
            "n": i, "id": f"s{i:02d}", "label": sl["label"],
            "disp": DISP_FR.get(sl["label"], sl["label"]) if lang == "fr" else sl["label"], "chapter": sl["chapter"],
            "start": round(t, 3), "dur": sdur, "audio": round(adur, 3),
            "title": sl["title"], "bullets": sl["bullets"], "tone": tone,
            "tc": tc(t),
        })
        t += sdur
    total = round(t, 3)
    TOTALS[lang] = total

    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / f"slides-{lang}.json").write_text(
        json.dumps({"lang": lang, "voice": voice, "total": total, "slides": rows},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    chapters = [{"t": r["start"], "tc": tc(r["start"]), "title": r["chapter"]}
                for r in rows if r["chapter"]]
    txt = "\n".join(f"{c['tc']} {c['title']}" for c in chapters) + "\n"
    (OUT / f"chapters-{lang}.txt").write_text(txt, encoding="utf-8")
    return rows, total, chapters

def render_slide(r, n_total):
    tone = r["tone"]
    lines = r["title"]
    if len(lines[0]) <= 14:
        title_html = (f'<div class="t-accent">{esc(lines[0])}</div>'
                      f'<div class="t-sub">{esc(lines[1])}</div>')
    else:
        title_html = (f'<div class="t-lead">{esc(lines[0])}</div>'
                      f'<div class="t-accent">{esc(lines[1])}</div>')
    disp = r.get("disp", r["label"])
    ghost = f'{esc(disp)} &middot; {esc(disp)} &middot; {esc(disp)}'
    bullets = "\n".join(
        f'            <li><span class="tick"></span>{esc(b)}</li>'
        for b in r["bullets"])
    return f'''      <section class="slide clip tone-{tone}" id="{r["id"]}" data-start="{r["start"]:.3f}" data-duration="{r["dur"]:.3f}" data-track-index="0">
        <div class="ghost" data-layout-allow-overflow="true" aria-hidden="true">{ghost}</div>
        <div class="rule-top"></div>
        <div class="kicker mono"><span class="kick-label">{esc(disp)}</span><span class="kick-sep">/</span><span class="kick-tc">{r["tc"]}</span></div>
        <div class="title">
{title_html}
        </div>
        <ul class="bullets">
{bullets}
        </ul>
        <div class="counter mono">{r["n"]}<span class="cnt-total"> / {n_total}</span></div>
        <div class="rule-bottom"></div>
      </section>'''

def render_js(rows, total):
    out = ['      const tl = gsap.timeline({ paused: true });',
           '      tl.fromTo("#glow", { scale: 1, opacity: .55 }, { scale: 1.08, opacity: .78, duration: 7, ease: "sine.inOut", yoyo: true, repeat: -1 }, 0);',
           f'      tl.fromTo("#progress", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {total:.3f}, ease: "none" }}, 0);']
    for r in rows:
        s, d, i = r["start"], r["dur"], r["id"]
        out.append(f'      tl.fromTo("#{i} .kicker", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: .4, ease: "power3.out" }}, {s:.3f});')
        if len(r["title"][0]) > 14:
            out.append(f'      tl.fromTo("#{i} .t-lead", {{ opacity: 0, y: 44 }}, {{ opacity: 1, y: 0, duration: .55, ease: "power4.out" }}, {s + 0.05:.3f});')
        out.append(f'      tl.fromTo("#{i} .t-accent, #{i} .t-sub", {{ opacity: 0, y: 44 }}, {{ opacity: 1, y: 0, duration: .55, ease: "power4.out" }}, {s + 0.16:.3f});')
        out.append(f'      tl.fromTo("#{i} .bullets li", {{ opacity: 0, x: -26 }}, {{ opacity: 1, x: 0, duration: .45, ease: "back.out(1.6)", stagger: .09 }}, {s + 0.34:.3f});')
        out.append(f'      tl.fromTo("#{i} .counter", {{ opacity: 0 }}, {{ opacity: 1, duration: .5, ease: "power2.out" }}, {s + 0.6:.3f});')
        out.append(f'      tl.fromTo("#{i} .ghost", {{ opacity: 0, x: -40 }}, {{ opacity: .05, x: 40, duration: {d:.3f}, ease: "none" }}, {s:.3f});')
    out.append('      window.__timelines["main"] = tl;')
    out.append('      tl.seek(0);')
    return "\n".join(out)

def build_html(lang, rows, total, dest):
    n = len(rows)
    sections = "\n".join(render_slide(r, n) for r in rows)
    audios = "\n".join(
        f'      <audio id="vo-{r["n"]:02d}" src="assets/vo/{lang}-{r["n"]:02d}.mp3" data-start="{r["start"]:.3f}" data-duration="{r["audio"]:.3f}" data-track-index="1" data-volume="1"></audio>'
        for r in rows)
    js = render_js(rows, total)
    doc = f'''<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1920px; height: 1080px; overflow: hidden;
        background: #0b0f1a; -webkit-font-smoothing: antialiased;
      }}
      :root {{
        --bg: #0b0f1a; --panel: #141b2e; --fg: #e9eef9; --mute: #93a0bd;
        --line: rgba(147, 160, 189, .22); --blue: #4d84ff; --blue-solid: #0055ff;
        --green: #34d399; --red: #ff7a7a; --amber: #f59e0b;
      }}
      #root {{
        position: relative; width: 100%; height: 100%;
        background: var(--bg); overflow: hidden;
        font-family: Montserrat, "Segoe UI", Arial, sans-serif; color: var(--fg);
      }}
      .mono {{ font-family: "IBM Plex Mono", Consolas, "Courier New", monospace; }}
      #bg-layer {{ position: absolute; inset: 0; }}
      #glow {{
        position: absolute; width: 1400px; height: 1400px; left: -320px; top: -520px; opacity: .55;
        background: radial-gradient(circle at 50% 50%, rgba(0, 85, 255, .34) 0%, rgba(0, 85, 255, .10) 42%, rgba(11, 15, 26, 0) 70%);
      }}
      #grid {{
        position: absolute; inset: 0; opacity: .5;
        background-image:
          linear-gradient(to right, rgba(147,160,189,.07) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(147,160,189,.07) 1px, transparent 1px);
        background-size: 160px 160px;
      }}
      #topbar {{
        position: absolute; top: 44px; left: 130px; right: 130px;
        display: flex; justify-content: space-between; align-items: center;
        font-size: 22px; letter-spacing: .34em; color: var(--mute); text-transform: uppercase;
      }}
      #topbar .mark {{ color: var(--fg); font-weight: 700; }}
      #topbar .mark b {{ color: var(--blue); font-weight: 700; }}
      #progress-wrap {{ position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: rgba(147, 160, 189, .12); }}
      #progress {{ position: absolute; inset: 0; transform-origin: left center; background: linear-gradient(90deg, var(--blue-solid), var(--green)); }}
      .slide {{ position: absolute; inset: 0; padding: 148px 130px 96px; display: flex; flex-direction: column; justify-content: center; }}
      .ghost {{
        position: absolute; left: -40px; bottom: 60px; font-size: 190px; font-weight: 900;
        letter-spacing: -.04em; white-space: nowrap; opacity: .05; color: var(--fg); pointer-events: none;
      }}
      .rule-top, .rule-bottom {{ position: absolute; left: 130px; right: 130px; height: 2px; background: var(--line); }}
      .rule-top {{ top: 116px; }}
      .rule-bottom {{ bottom: 74px; }}
      .kicker {{
        font-size: 24px; letter-spacing: .3em; text-transform: uppercase; color: var(--mute);
        margin-bottom: 40px; display: flex; gap: 26px; align-items: baseline;
      }}
      .kick-label {{ color: var(--blue); font-weight: 700; }}
      .tone-red .kick-label {{ color: var(--red); }}
      .tone-green .kick-label {{ color: var(--green); }}
      .tone-amber .kick-label {{ color: var(--amber); }}
      .kick-sep {{ color: #6b7a99; }}
      .kick-tc {{ color: var(--mute); letter-spacing: .18em; }}
      .title {{ margin-bottom: 54px; }}
      .title div {{ font-weight: 900; letter-spacing: -.035em; line-height: 1.04; font-size: 92px; color: var(--fg); }}
      .title .t-accent {{ color: var(--green); font-size: 108px; }}
      .tone-red .title .t-accent {{ color: var(--red); }}
      .tone-amber .title .t-accent {{ color: var(--amber); }}
      .tone-blue .title .t-accent {{ color: var(--blue); }}
      .title .t-sub {{ color: var(--mute); }}
      .bullets {{ list-style: none; max-width: 1420px; }}
      .bullets li {{
        display: flex; align-items: center; gap: 28px; font-size: 36px; font-weight: 400;
        color: var(--fg); line-height: 1.3; padding: 22px 0; border-bottom: 1px solid var(--line);
      }}
      .bullets li:first-child {{ border-top: 1px solid var(--line); }}
      .tick {{ width: 16px; height: 16px; flex: 0 0 16px; background: var(--blue); border-radius: 3px; }}
      .tone-red .tick {{ background: var(--red); }}
      .tone-green .tick {{ background: var(--green); }}
      .tone-amber .tick {{ background: var(--amber); }}
      .counter {{ position: absolute; right: 130px; bottom: 92px; font-size: 22px; color: var(--fg); letter-spacing: .1em; }}
      .cnt-total {{ color: var(--mute); }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total:.3f}"
      data-fps="30"
      data-width="1920"
      data-height="1080"
    >
      <div id="bg-layer" aria-hidden="true">
        <div id="glow"></div>
        <div id="grid"></div>
        <div id="topbar"><span class="mark">View<b>cut</b></span><span>{TOPBAR[lang]}</span></div>
        <div id="progress-wrap"><div id="progress"></div></div>
      </div>

{sections}
{audios}
    </div>
    <script>
{js}
    </script>
  </body>
</html>
'''
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")

def main():
    langs = sys.argv[1:] or ["fr", "en"]
    built = {}
    for lang in langs:
        rows, total, chapters = build(lang)
        built[lang] = {"rows": rows, "total": total, "chapters": chapters}
        dest = ROOT / "index.html" if lang == "fr" else ROOT / "compositions" / "en.html"
        build_html(lang, rows, total, dest)
        print(f"[{lang}] {len(rows)} slides, {total:.1f}s -> {dest}")

    # merged chapter data for the landing page
    merged = {}
    for lang, b in built.items():
        merged[lang] = {
            "total": b["total"],
            "duration": tc(b["total"]),
            "chapters": b["chapters"],
            "slides": [{"t": r["start"], "label": r["label"]} for r in b["rows"]],
        }
    (OUT / "assets" / "chapters.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print("chapters:", {k: len(v["chapters"]) for k, v in merged.items()})

if __name__ == "__main__":
    main()
