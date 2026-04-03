# 🔭 Fink/LSST — Exploration


Fink est un broker d'alertes astronomiques qui enrichit les alertes LSST avec des scores de
classification ML, des cross-matches avec des catalogues externes (Gaia DR3, TNS, SIMBAD…)
et des tags scientifiques.

Ci-dessous vous trouverez une appication Web pour montrer la localisation des alertes du survey **LSST/Rubin Observatory** 
ainsi qu'une collection de notebooks Jupyter pour explorer ces alertes.


**API base URL :** `https://api.lsst.fink-portal.org`

**Pour ZTF portal (non couvert ici) :** `https://ztf.fink-portal.org/`

---
## Web application

 🗺️ `fink_lsst_skymap_portal.html` — Navigateur de ciel interactif (Aladin Lite v3)
Application web **standalone** (un seul fichier HTML, aucune dépendance serveur)
affichant les alertes FINK/LSST sur une carte du ciel interactive temps-réel,
construite sur [Aladin Lite v3](https://aladin.cds.unistra.fr/AladinLite/).

**Fonctionnalités principales :**
- Carte en **projection Mollweide** (basculable AIT) avec zoom molette et panoramique souris
- **Fond de ciel HiPS** sélectionnable : Mellinger RGB, PanSTARRS, DSS2, 2MASS, WISE, XMM X-ray
- **Multi-tags simultanés** : jusqu'à 5 tags FINK affichés en couleurs distinctes,
  activables/désactivables individuellement
- **Grille de coordonnées** RA/Dec toggle ON/OFF (bouton sidebar + contrôle natif Aladin)
- **Clic sur une alerte** → panneau de détail : `diaObjectId` (64-bit précis), RA/Dec,
  tag, filtre, MJD, nombre de sources, **lien direct vers le portail Fink**
- **Copie en un clic** du `diaObjectId` dans le presse-papier
- Barre de coordonnées temps-réel (RA, Dec, FoV) en bas de carte
- Contrôle du nombre d'alertes par tag (slider 50–500)
- Log d'activité en temps réel dans la sidebar
- Plein écran natif
- Aucun serveur requis : ouvrir directement dans un navigateur moderne

**Endpoints :** `/api/v1/tags`


## 📋 Notebooks

### `FINK_schema_dump.ipynb`  
Cree un fichier json à partir des schemas de diffrents endpoints de l'API V1 en cours, ex. `all_schema_api_v1_20260403.json` 

### `Fink_schema_inspector.ipynb`
Permet de chercher dans all_schema JSON  des patterns dans les variables. 
Par exemple
`print_df(search(df, tag="detec"),nrows=None)` donne avec l'API V1 

|     | endpoint/var          | doc                                                                                                                                  |
|----:|:----------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
|  31 | tags/r:detector       | Id of the detector where this diaSource was measured. Datatype short instead of byte because of DB concerns about unsigned bytes.    |
| 163 | conesearch/r:detector | Id of the detector where this diaSource was measured. Datatype short instead of byte because of DB concerns about unsigned bytes.    |
| 468 | sources/r:detector    | Id of the detector where this diaSource was measured. Datatype short instead of byte because of DB concerns about unsigned bytes.    |
| 593 | fp/r:detector         | Id of the detector where this forcedSource was measured. Datatype short instead of byte because of DB concerns about unsigned bytes. |


### 🌍 `fink_lsst_skymap.ipynb` — Carte céleste statique (Mollweide + 3D)
Affiche la **distribution spatiale** des alertes d'un tag donné sur une projection
de Mollweide matplotlib, avec une vue 3D interactive Plotly en bonus.

- Carte de Mollweide avec superposition du **plan galactique** et de l'**écliptique**
  (calculés via Astropy en coordonnées ICRS)
- **Coloration par filtre dominant** (u/g/r/i/z/y) ou par flux PSF maximum (colormap continue)
- Annotations optionnelles : `diaObjectId` et/ou coordonnées α/δ par point
- Grille RA/Dec configurable
- **Vue 3D interactive** (Plotly `Scatter3d`) sur sphère céleste, exportée en HTML autonome
- Distributions marginales RA et Dec (histogrammes)
- Tableau récapitulatif avec liens directs vers le portail Fink/LSST
- Sauvegarde automatique des figures en PDF et PNG

**Endpoints :** `/api/v1/tags` · `/api/v1/sources`


---

### 📈 `fink_lsst_lightcurves.ipynb` — Courbes de lumière multi-bandes
Génère une **figure de courbe de lumière par objet** pour un tag donné, avec toutes les
bandes `ugrizy` superposées sur un même graphe.

- Courbe de lumière en **flux PSF (nJy)** — toutes bandes superposées (panneau haut)
- Courbe de lumière en **magnitude AB** — toutes bandes superposées (panneau bas)
- Axes temporels partagés et synchronisés
- Couleurs LSST standards par filtre (`u`/`g`/`r`/`i`/`z`/`y`)
- Non-détections représentées par des flèches ▼ à la limite 3σ
- Titre avec `diaObjectId`, bandes présentes et date de la dernière alerte
- Lien cliquable vers le portail Fink/LSST pour chaque objet
- Tableau récapitulatif (bandes, MJD, flux max, dernier filtre)
- Sauvegarde automatique PDF + PNG dans `lightcurves/`

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

### 🔭 `fink_lsst_conesearch_nsources.ipynb` — Recherche par position avec filtrage qualité
Extension de `fink_lsst_conesearch.ipynb` ajoutant un **filtrage par qualité** des objets
et un seuil sur le nombre d'objets traités, utile pour les grands champs ou les requêtes
à fort rayon.

**Paramètres supplémentaires :**
- `MIN_NUMBER_SOURCES` — exclut les objets avec moins de N alertes (`nDiaSources`)
- `MAX_OBJECTS` — limite le nombre d'objets traités (évite les longues boucles)

**Différences avec `fink_lsst_conesearch.ipynb` :**
- La colonne `nDiaSources` est demandée à l'API et affichée dans le tableau de prévisualisation
- Le filtrage `MIN_NUMBER_SOURCES` est appliqué avant la carte et les courbes de lumière
- Les courbes de lumière adoptent le style **`fink_lsst_lightcurves_ddf`** :
  panneaux flux (haut) et magnitude (bas) empilés, axe X partagé (`sharex`),
  bandes dans l'ordre LSST `ugrizy`, fonction `fetch_lightcurve()` encapsulée
- La boucle de tracé est limitée à `MAX_OBJECTS` objets

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
