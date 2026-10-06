# -*- coding: utf-8 -*-
import io
t = io.open("index.html", encoding="utf-8").read()
print("side panel:", t.count('class="chapters"'),
      "| ch-toggle:", t.count("ch-toggle"),
      "| chbar:", t.count('id="chbar"'),
      "| panel:", t.count("chapters-panel"),
      "| tools:", t.count("vsl-tools"))
ids = [i for i in ("vsl-duration", "ch-duration", "copy-chapters",
                   "chapters-btn", "chtip", "chbar", "chapters") if 'id="%s"' % i in t]
print("ids:", ids)
js = io.open("assets/app.js", encoding="utf-8").read()
print("app.js chseg:", js.count("chseg"), "| tries:", js.count("tries"),
      "| closePanel:", js.count("closePanel"), "| seekTo:", js.count("seekTo"))
css = io.open("assets/style.css", encoding="utf-8").read()
print("css ch-panel:", css.count(".ch-panel"), "| chseg:", css.count(".chseg"),
      "| hero-vsl single:", ".hero-vsl{margin:34px 0 6px;max-width:760px}" in css)
