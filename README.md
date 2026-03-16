# 🔭 Fink/LSST — Notebooks d'exploration

Collection de notebooks Jupyter pour explorer les alertes du survey **LSST/Rubin Observatory**
via l'API du portail [Fink](https://lsst.fink-portal.org).

Fink est un broker d'alertes astronomiques qui enrichit les alertes LSST avec des scores de
classification ML, des cross-matches avec des catalogues externes (Gaia DR3, TNS, SIMBAD…)
et des tags scientifiques.

**API base URL :** `https://api.lsst.fink-portal.org`

---

## 📋 Notebooks

### 👻 `fink_lsst_hostless.ipynb` — Objets sans galaxie hôte
Explore les alertes taguées **`hostless_candidate`**, sélectionnées par l'algorithme ELEPHANT
([arXiv:2404.18165](https://arxiv.org/abs/2404.18165)) lorsqu'aucune galaxie hôte n'est détectée.
Ces objets peuvent être des supernovae dans des galaxies naines, des transitoires dans des halos
galactiques, ou des événements extragalactiques lointains.

- Distribution spatiale (carte Mollweide) comparée aux `sn_near_galaxy_candidate`
- Comparaison des propriétés photométriques (flux, magnitude, déclinaison)
- Courbes de lumière + cutouts Science/Template/Difference
- Comparaison des scores de classification Fink entre les deux populations

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/cutouts` · `/api/v1/schema`

---

### ⚡ `fink_lsst_new_transients.ipynb` — Nouveaux transitoires extragalactiques
Cible le tag **`extragalactic_new_candidate`** qui sélectionne les alertes dont la première
détection date de moins de 48h. Outil de veille pour identifier rapidement les nouveaux
transitoires candidats à un suivi spectroscopique.

- Calcul de l'âge depuis la première détection (en heures)
- Distribution des âges et magnitude au pic
- Carte Mollweide colorée par âge
- Courbes de lumière précoces + cutouts
- Tableau récapitulatif trié par âge croissant

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/cutouts` · `/api/v1/schema`

---

### 🤖 `fink_lsst_scores.ipynb` — Scores de classification Fink
Exploration systématique des **scores et valeurs ajoutées** par les modules de science Fink
pour un tag donné. Les colonnes Fink sont organisées en familles : `f:clf.*` (classifieurs ML),
`f:xm.*` (cross-matches), `f:lc_features.*` (features de courbe de lumière), `f:misc.*`.

- Découverte automatique des colonnes `f:` disponibles via le schéma
- Distributions des scores de classification (`clf.*`)
- Heatmap objet × score (score médian par objet)
- Évolution temporelle des scores pour les meilleurs candidats
- Tableau récapitulatif trié par score

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/schema`

---

### 🏷️ `fink_lsst_tns.ipynb` — Cross-match TNS
Analyse des alertes ayant une contrepartie dans le **Transient Name Server (TNS)**
via le tag `in_tns`. Compare les objets confirmés TNS avec les autres tags.

- Distribution des types TNS (AT, SN Ia, SN II, SN Ib/c…)
- Comparaison des scores Fink entre objets TNS et non-confirmés
- Carte Mollweide colorée par type TNS
- Courbes de lumière des objets les mieux classifiés
- Tableau avec liens TNS + portail Fink

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/schema`

---

### 🔭 `fink_lsst_conesearch.ipynb` — Recherche par position
Recherche de tous les objets Fink dans un **champ circulaire** défini par un centre
(RA, Dec) et un rayon en arcsecondes. Le centre peut être saisi en coordonnées décimales,
sexagésimales, ou résolu par nom d'objet (ex. `"NGC 1365"`) via l'API Fink.

- Carte locale en projection gnomonique centrée sur la cible
- Courbes de lumière de chaque objet trouvé
- Cutouts Science/Template/Difference
- Scores de classification Fink
- Tableau récapitulatif avec liens portail

**Endpoints :** `/api/v1/conesearch` · `/api/v1/sources` · `/api/v1/cutouts` · `/api/v1/resolver`

---

### 🌙 `fink_lsst_nightcurve.ipynb` — Suivi temporel nuit par nuit
Trace l'**évolution temporelle** du flux d'alertes Fink/LSST nuit par nuit pour un
ou plusieurs tags.

- Nombre d'alertes et d'objets nouveaux par nuit
- Décomposition par filtre LSST (u, g, r, i, z, y)
- Courbe cumulative du nombre d'objets découverts
- Heatmap nuit × filtre
- Détection des nuits les plus actives

**Endpoints :** `/api/v1/tags` · `/api/v1/sources`

---

### 🌍 `fink_lsst_skymap.ipynb` — Carte céleste (Mollweide)
Affiche la **distribution spatiale** des alertes d'un tag donné sur une projection
de Mollweide, avec superposition du plan galactique et de l'écliptique.

- Carte Mollweide avec plan galactique et écliptique
- Coloration par filtre dominant ou par propriété photométrique
- Annotations optionnelles (`diaObjectId`, coordonnées)
- Grille RA/Dec

**Endpoints :** `/api/v1/tags` · `/api/v1/sources`

---

### 📊 `fink_lsst_multitag_stats.ipynb` — Comparaison multi-tags
Récupère **tous les tags disponibles** via l'API et produit une figure de synthèse
comparative.

- Nombre d'alertes et d'objets uniques par tag
- Distribution par filtre LSST
- Distribution en flux PSF (nJy)
- Distribution spatiale (RA, Dec)
- Figure de synthèse comparant tous les tags côte à côte

**Endpoints :** `/api/v1/tags` · `/api/v1/sources`

---

### 🌌 `fink_lsst_alert_summary.ipynb` — Résumé par objet (LC + cutouts)
Génère une **figure de synthèse par objet** pour un tag donné, combinant courbe de
lumière et cutouts d'imagerie.

- Courbe de lumière en flux PSF (nJy)
- Courbe de lumière en magnitude AB
- Cutouts Science / Template / Difference de la dernière alerte
- Titre avec `diaObjectId`, `diaSourceId`, filtre et date

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/cutouts`

---

### 📡 `fink_lsst_forced_photometry.ipynb` — Photométrie forcée
Exploite l'endpoint `/api/v1/fp` pour récupérer la **photométrie forcée** des objets
les plus brillants d'un tag. La photométrie forcée mesure le flux à une position fixe
indépendamment d'une détection, permettant de remonter à l'évolution **pré-détection**
du transitoire.

- Courbe de lumière combinée : détections officielles (points pleins) + photométrie
  forcée (points creux)
- Flux PSF et magnitude AB sur le même axe
- Mise en évidence de la date de première détection officielle
- Tableau récapitulatif avec liens portail

**Endpoints :** `/api/v1/tags` · `/api/v1/sources` · `/api/v1/fp`

---

## ⚙️ Prérequis

```bash
pip install requests numpy pandas matplotlib astropy Pillow tqdm
```

Python ≥ 3.9, pandas ≥ 2.0.

## 🔗 Ressources

- [Portail Fink/LSST](https://lsst.fink-portal.org)
- [Documentation API Fink](https://api.lsst.fink-portal.org)
- [Article ELEPHANT](https://arxiv.org/abs/2404.18165)
- [Transient Name Server](https://www.wis-tns.org)
