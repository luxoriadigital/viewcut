# -*- coding: utf-8 -*-
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(BASE, "scripts", "fr.json")
d = json.load(open(p, encoding="utf-8"))
for s in d["slides"]:
    if s["label"] == "MÉCANISME":
        s["title"] = ["Je vends le résultat.", "Pas l'outil."]
    if s["label"] == "CTA":
        s["title"] = ["Envoie tes images.", "Reçois une vidéo."]
    s["vo"] = " ".join(s["vo"].split())
    s["vo"] = s["vo"].replace("Envoyez-moi un rush", "Envoyez-moi vos images")
    s["vo"] = s["vo"].replace("un rush", "tes images").replace("votre rush", "vos images")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
t = io.open(p, encoding="utf-8").read()
print("FR restes rush:", t.lower().count("rush"), "output:", t.lower().count("output"),
      "35:", t.count("35"), "50:", t.count("50 €/h"))

p = os.path.join(BASE, "scripts", "en.json")
d = json.load(open(p, encoding="utf-8"))
for s in d["slides"]:
    if s["label"] == "CTA":
        s["title"] = [t2 for t2 in s["title"]]
t = json.dumps(d, ensure_ascii=False)
print("EN 35:", t.count("35"), "rush:", t.lower().count("rush"),
      "output:", t.lower().count("output"), "fifty:", t.lower().count("fifty"),
      "euro50:", t.count("€50/h"))
