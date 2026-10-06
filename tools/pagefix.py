# -*- coding: utf-8 -*-
"""Landing FR: prix 35 -> 50 (marché 2026) + dé-anglicisation."""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "index.html")
t = io.open(p, encoding="utf-8").read()

reps = [
    ("contre ~35 €/h de temps facturé", "contre ~50 €/h de temps facturé"),
    ("Tu envoies le rush.", "Tu envoies tes images."),
    ("<b>35 <span style=\"font-size:20px\">€/h</span></b>", "<b>50 <span style=\"font-size:20px\">€/h</span></b>"),
    ("3 à 5 jours pour un premier cut", "3 à 5 jours pour une première version"),
    ("<h4>35 €/h de temps facturé</h4>", "<h4>50 €/h de temps facturé</h4>"),
    ("Je vends l'output.<br />Pas l'outil.", "Je vends le résultat.<br />Pas l'outil."),
    ("Un lien vers tes rushs (Drive", "Un lien vers tes images (Drive"),
    ("<div class=\"num\" style=\"font-size:26px\">1:1</div><p>Feed</p>",
     "<div class=\"num\" style=\"font-size:26px\">1:1</div><p>Fil d'actualité</p>"),
    ("<div class=\"num\" style=\"font-size:26px\">CC</div>",
     "<div class=\"num\" style=\"font-size:26px\">ST</div>"),
    ("<s>10 €</s>&nbsp;au lieu d'environ 35 €/h de temps facturé",
     "<s>10 €</s>&nbsp;au lieu d'environ 50 €/h de temps facturé"),
    ("<td>~35 €/h de temps</td>", "<td>~50 €/h de temps</td>"),
    ("tu n'as pas encore de rushs", "tu n'as pas encore de plans tournés"),
    ("tu as déjà tes rushs", "tu as déjà tes images"),
    ("Tu envoies un rush et l'extrait qui t'intéresse",
     "Tu envoies tes images et l'extrait qui t'intéresse"),
    ("il y a un brief, un montage, et une validation",
     "il y a une demande, un montage, et une validation"),
    ("Comment je t'envoie mes rushs ?", "Comment je t'envoie mes images ?"),
    ("Envoie un rush.<br />Reçois 30 secondes gratuites.",
     "Envoie tes images.<br />Reçois 30 secondes gratuites."),
]
missing = []
for a, b in reps:
    if a not in t:
        missing.append(a)
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="").write(t)

low = t.lower()
checks = {
    "35": t.count("35"),
    "rush": low.count("rush"),
    "output": low.count("output"),
    "feed": low.count("feed"),
    "brief": low.count("brief"),
    "cut": low.count("cut"),
    "50 €/h": t.count("50 €/h"),
    "50 <span": t.count("50 <span"),
}
print("MISSING:", missing)
print("CHECKS:", checks)
