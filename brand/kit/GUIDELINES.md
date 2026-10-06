# Viewcut — Guide du logo (version compact)

> Pour non-designers. Une à deux pages. Les « à faire » d'abord.

## 1. Le logo
- **Idée** : un cadre arrondi tranché en deux par une coupe à 30° — le geste du montage, les deux moitiés glissent comme une image à la cisaille.
- **Versions** : horizontal (principal) · empilé · symbole seul · logotype seul.
- **Fichiers** : `kit/*.svg` + PNG écrans · favicon et jeu d'icônes dans `kit/web/` · écrans en RGB ; pour l'imprimeur, faire exporter le SVG en PDF CMJN par le fournisseur (aucun PDF n'est fourni ici).
- Le logotype est un **contour** (Inter 900 vectorisé) : ne jamais le retaper au clavier, ni le remplacer par une police installée.

## 2. Zone de protection
Garder autour du logo un vide d'**¼ de la hauteur du symbole** sur les quatre côtés. La zone grandit avec le logo — jamais une distance fixe.

## 3. Tailles minimales
| Version | Écran | Impression |
|---|---|---|
| Horizontal | 160 px de large | 40 mm de large |
| Symbole | 16 px (fichier `viewcut-symbol-favicon.svg`) | 6 mm |
| Logotype seul | 240 px de large | 60 mm de large |

En dessous de 24 px d'icône, utiliser impérativement le fichier `-favicon` (coupe élargie à 24 unités, dessiné pour l'onglet).

## 4. Couleur
| Nom | HEX | RGB | CMJN | Pantone |
|---|---|---|---|---|
| Bleu Viewcut | #0055ff | 0, 85, 255 | 100 / 67 / 0 / 0 (approx.) | à confirmer avec l'imprimeur |
| Encre | #0b0f1a | 11, 15, 26 | 58 / 42 / 0 / 90 (approx.) | à confirmer avec l'imprimeur |
| Blanc | #ffffff | 255, 255, 255 | 0 / 0 / 0 / 0 | — |

**Combinaisons validées** : couleur sur blanc · blanc sur bleu · blanc sur encre · noir sur blanc.
Sur photo : version blanche ou noire sur une zone calme, sinon poser le logo dans un conteneur plein (tuile ou plaque).

## 5. Typographie
- Titres : **Inter 900/700** · Texte : **Inter 400/500** · Repli web : `-apple-system, 'Segoe UI', Roboto, Arial, sans-serif`.
- Licence : Inter, **SIL Open Font License 1.1** (Google Fonts) — usage commercial autorisé.

## 6. À ne pas faire
Ne pas étirer ni aplatir · ne pas recolorer hors palette · ne pas tourner le logo ni l'angle de la coupe ·
ni ombres, dégradés, contours ou effets · ne pas déplacer les pièces d'un lockup · ne pas poser sur fond
chargé sans conteneur · ne pas retaper le logotype.

## 7. Contact
Questions d'usage : *à compléter (identité légale Viewcut)*. Fichiers maîtres : `viewcut/brand/kit/`
(masters `viewcut-symbol.svg`, `viewcut-horizontal.svg`, `viewcut-stacked.svg`, `viewcut-wordmark.svg` ;
script de reconstruction `make_kit.py` à côté).

**Pièces jointes du kit** : `presentation.html` + `slides/` (planche finale), `preview/` (rendus de contrôle),
variantes `-black` / `-white` / `-mono-0055ff` / `-app-icon` / `-favicon` / `-square`, `web/` (favicon.ico,
apple-touch, icônes 192/512, maskable, `site.webmanifest`, `head-snippet.html`).
