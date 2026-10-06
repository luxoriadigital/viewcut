# -*- coding: utf-8 -*-
"""Page : preuve -> autorité (mes publications, pas vues générées),
copie parlée au client, bouton plein écran VSL, messages propres."""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "index.html")
t = io.open(p, encoding="utf-8").read()

# ---------- 1. section PREUVES -> autorité, copie client ----------
start = t.find("  <!-- PREUVES -->")
end = t.find("  <!-- PRIX -->")
if start < 0 or end < 0:
    sys.exit("markers not found")
new_section = """  <!-- PREUVES : autorité — mes publications, pas un résultat du service -->
  <section class="alt" id="proof">
    <div class="wrap">
      <div class="eyebrow">Mes publications</div>
      <h2 class="h2">1M+ de vues,<br />capture par capture.</h2>
      <p class="sub">Ci-dessous, mes captures Instagram, telles quelles : environ 700 000 vues visibles d'un coup d'œil. Le cumul de l'ensemble de mes contenus dépasse le million. Ce sont mes propres publications — le montage derrière Viewcut, à vérifier avant qu'on se parle.</p>

      <div class="proof-grid">
        <div class="shot" data-src="assets/proof/proof-1.png"><div class="ph"><b>Capture Instagram</b><span>Clique pour agrandir</span></div></div>
        <div class="shot" data-src="assets/proof/proof-2.png"><div class="ph"><b>Capture Instagram</b><span>Clique pour agrandir</span></div></div>
        <div class="shot" data-src="assets/proof/proof-3.png"><div class="ph"><b>Capture Instagram</b><span>Clique pour agrandir</span></div></div>
        <div class="shot" data-src="assets/proof/proof-4.png"><div class="ph"><b>Capture Instagram</b><span>Clique pour agrandir</span></div></div>
      </div>

      <div class="proof-bar">
        <div class="pb">
          <b>≈ 700 000</b>
          <span>vues visibles sur les captures</span>
        </div>
        <div class="pb plus">
          <b>+ le reste</b>
          <span>tous les contenus confondus</span>
        </div>
        <div class="pb hl">
          <b>1M+</b>
          <span>de vues sur l'ensemble de mes publications</span>
        </div>
        <p class="pb-note">
          Clique sur une capture pour l'ouvrir en plein écran et lire les chiffres en entier.
        </p>
      </div>
    </div>
  </section>

"""
t = t[:start] + new_section + t[end:]

# ---------- 2. remplacements client / autorité ----------
reps = [
    ("1M+ de vues cumulées · Reels, Shorts, TikTok",
     "1M+ de vues sur mes publications · Reels, Shorts, TikTok"),
    ("Et pour commencer sans risque&nbsp;: <b>30 secondes de vidéo test gratuites</b>.",
     "Et pour commencer&nbsp;: <b>30 secondes de vidéo test gratuites</b>, jugées sur le rendu."),
    ('<div class="stat"><b>1M+</b><span>de vues cumulées</span></div>',
     '<div class="stat"><b>1M+</b><span>de vues sur mes publications</span></div>'),
    ("<b>MP4 introuvable</b>",
     "<b>La vidéo ne se charge pas</b>"),
    ("<span>Lance le rendu dans le dossier vsl/ puis recharge.</span>",
     "<span>Réessaie dans un instant, ou écris-moi sur WhatsApp.</span>"),
    ("<h4>Test avant d'engager</h4>",
     "<h4>Tester avant de payer</h4>"),
    ("<s>30 s</s>&nbsp;<b>de vidéo test gratuites</b> avant tout engagement",
     "<s>30 s</s>&nbsp;<b>de vidéo test gratuites</b> avant de payer"),
    (">Réserver les 30 s gratuites<",
     ">Je veux mes 30 s gratuites<"),
    ("Sans risque : 30 secondes de vidéo test montées et sous-titrées, avant tout engagement. Ensuite, tu décides.",
     "30 secondes de ta vidéo, montées et sous-titrées, avant de payer quoi que ce soit. Ensuite, tu décides."),
    ("— gratuit, sans engagement.", "— gratuit."),
    ("Chiffres affichés : prix de service communiqué par le client, ~700 000 vues visibles sur les captures et cumul déclaré au-delà de 1M de vues (captures dans la section Preuves).",
     "Chiffres affichés : prix du service, ≈700 000 vues visibles sur les captures Instagram et cumul de l'ensemble des publications au-delà de 1M (section Preuves)."),
]
missing = [a for a, b in reps if a not in t]
for a, b in reps:
    t = t.replace(a, b)

# ---------- 3. bouton plein écran sur le lecteur VSL ----------
old_video = '<video id="vsl-video" src="assets/vsl-fr.mp4" controls preload="metadata" playsinline></video>'
new_video = old_video + '\n          <button class="vsl-fs" type="button" id="vsl-fs" aria-label="Plein écran">⛶ Plein écran</button>'
if old_video in t:
    t = t.replace(old_video, new_video)
else:
    missing.append("video-tag")

io.open(p, "w", encoding="utf-8", newline="").write(t)

# ---------- vérifs ----------
low = t.lower()
print("MISSING:", missing)
print("CHECKS:", {
    "mp4 introuvable": low.count("mp4 introuvable"),
    "dossier vsl": low.count("dossier vsl"),
    "sans risque": low.count("sans risque"),
    "réserver": low.count("réserver"),
    "engagement": low.count("engagement"),
    "cumul declaré": low.count("déclaré"),
    "par le client": low.count("par le client"),
    "1m+ de vues": low.count("1m+ de vues"),
    "sur mes publications": low.count("sur mes publications"),
    "vsl-fs": t.count('id="vsl-fs"'),
    "note owner": t.count("À faire avant publication"),
})
