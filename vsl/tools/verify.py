# -*- coding: utf-8 -*-
import io, re
t = io.open("index.html", encoding="utf-8").read()
print("kick-labels:", re.findall(r'kick-label">([^<]+)', t))
print("Output:", t.count("Output"), "| Resultat:", t.count("Résultat"),
      "| rush:", t.lower().count("rush"), "| 35:", t.count("35"),
      "| topbar:", re.search(r'<span>.{0,60}</span></div>', t).group(0)[:90])
t2 = io.open("compositions/en.html", encoding="utf-8").read()
print("EN Output:", t2.count("Output"), "| 35:", t2.count("35"),
      "| kick:", re.findall(r'kick-label">([^<]+)', t2))
