# -*- coding: utf-8 -*-
"""Prix 35 -> 50 (marché FR 2026) + dé-anglicisation FR/EN."""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def main():
    # ---------- FR ----------
    p = os.path.join(BASE, "scripts", "fr.json")
    d = load(p)
    vo_reps = [
        ("Le marché facture en moyenne trente-cinq euros de l'heure de montage",
         "Le marché facture en moyenne cinquante euros de l'heure de montage"),
        ("freelance à trente-cinq euros de l'heure", "freelance à cinquante euros de l'heure"),
        ("freelance à trente-cinq euros", "freelance à cinquante euros"),
        ("Le rush part le mardi", "Les images partent le mardi"),
        ("Vous envoyez votre rush, vous recevez la vidéo finie",
         "Vous envoyez vos images, vous recevez la vidéo finie"),
        ("Vous envoyez vos rushes et votre intention",
         "Vous envoyez vos images et votre intention"),
        ("avant de prendre votre rush", "avant de prendre vos images"),
        ("Il y a un brief, un humain qui monte", "Il y a une demande, un humain qui monte"),
        ("Trente-cinq euros de l'heure de montage", "Cinquante euros de l'heure de montage"),
        ("trente-cinq euros", "cinquante euros"),
    ]
    for s in d["slides"]:
        s["vo"] = " ".join(s["vo"].split())
        for a, b in vo_reps:
            s["vo"] = s["vo"].replace(a, b)
        s["title"] = [t.replace("35 €/h", "50 €/h").replace("35 €", "50 €") for t in s["title"]]
        s["bullets"] = [b.replace("35 €/h", "50 €/h").replace("35 €", "50 €") for b in s["bullets"]]
        lab = s["label"]
        if lab == "MECHANISM":
            s["title"] = ["Je vends le résultat.", "Pas l'outil."]
        if lab == "FORMATS":
            s["bullets"] = ["Chapitres horodatés inclus", "Accroches et titres à l'écran", "Un fichier par format"]
        if lab == "PROCESS":
            s["bullets"] = ["1. Tu envoies tes images", "2. Je monte et je livre", "3. Tu publies"]
        if lab == "CTA":
            s["bullets"] = ["30 s de vidéo test gratuites", "Tes images = ton essai", "Le lien est sous cette vidéo"]
        if lab == "POUR QUI":
            s["bullets"] = [b.replace("rushs", "images") for b in s["bullets"]]
            s["vo"] = s["vo"].replace("rushs", "images")
        s["vo"] = s["vo"].replace("ton rush", "tes images").replace("votre rush", "vos images")
    save(p, d)

    # ---------- EN ----------
    p = os.path.join(BASE, "scripts", "en.json")
    d = load(p)
    vo_reps = [
        ("around thirty-five euros an hour", "around fifty euros an hour"),
        ("The freelancer at thirty-five euros an hour", "The freelancer at fifty euros an hour"),
        ("thirty-five euros", "fifty euros"),
        ("I sell the output", "I sell the result"),
    ]
    for s in d["slides"]:
        s["vo"] = " ".join(s["vo"].split())
        for a, b in vo_reps:
            s["vo"] = s["vo"].replace(a, b)
        s["title"] = [t.replace("€35/h", "€50/h") for t in s["title"]]
        s["bullets"] = [b.replace("€35/h", "€50/h") for b in s["bullets"]]
        if s["label"] == "MECHANISM":
            s["title"] = ["I sell the result.", "Not the tool."]
    save(p, d)

    # ---------- checks ----------
    for name in ("fr", "en"):
        txt = json.dumps(load(os.path.join(BASE, "scripts", name + ".json")), ensure_ascii=False)
        low = txt.lower()
        print(name, "| '35':", txt.count("35"), "| rush:", low.count("rush"),
              "| output:", low.count("output"), "| brief:", low.count("brief"),
              "| hook:", txt.count("Hook"), "| feed:", low.count("feed"),
              "| 'CC':", txt.count("CC"), "| 50 €/h:", txt.count("50 €/h") + txt.count("€50/h"),
              "| cinquante/fifty:", low.count("cinquante") + low.count("fifty"))


if __name__ == "__main__":
    main()
