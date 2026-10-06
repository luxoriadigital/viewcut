# -*- coding: utf-8 -*-
"""PREUVE -> autorité (pas « vues générées avec la méthode) + nouvelles voix."""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    return json.load(open(p, encoding="utf-8"))


def save(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# ---------- FR : voix + slide PREUVE ----------
p = os.path.join(BASE, "scripts", "fr.json")
d = load(p)
d["voice"] = "fr-FR-RemyMultilingualNeural"
for s in d["slides"]:
    if s["label"] == "PREUVE":
        s["title"] = ["1M+ de vues.", "Sur mes publications."]
        s["bullets"] = ["Mes Reels · Shorts · TikTok",
                        "Captures Instagram sur la page",
                        "À vérifier par toi-même"]
        s["vo"] = ("Plus d'un million de vues cumulées sur l'ensemble de mes publications. "
                   "Les captures d'écran Instagram sont sur la page, pas dans une présentation. "
                   "Ouvrez-les, comptez-les : c'est mon travail qui parle, pas une promesse.")
save(p, d)

# ---------- EN : voix + slide PROOF ----------
p = os.path.join(BASE, "scripts", "en.json")
d = load(p)
d["voice"] = "en-US-BrianNeural"
for s in d["slides"]:
    if s["label"] == "PROOF":
        s["title"] = ["1M+ views.", "On my own posts."]
        s["bullets"] = ["My Reels, Shorts and TikTok",
                        "Instagram screenshots on the page",
                        "Check it yourself"]
        s["vo"] = ("Over a million views across all my own posts. "
                   "The Instagram screenshots are on the page, not in a deck. "
                   "Open them, count them: the work speaks, not a promise.")
save(p, d)

# checks
for name in ("fr", "en"):
    d = load(os.path.join(BASE, "scripts", name + ".json"))
    t = json.dumps(d, ensure_ascii=False).lower()
    print(name, "voice:", d["voice"],
          "| 'generated/générées/produites de la même':",
          t.count("generated") + t.count("générées") + t.count("produites de la m"),
          "| proof title:", [s["title"] for s in d["slides"] if s["label"] in ("PREUVE", "PROOF")])
