# Spécification Préliminaire Avatar 3D Linguistique & Langues Signées

Statut: Ébauche (Phase de recherche – aucune implémentation encore)
Version: 0.1
Responsable: Recherche interne

## 1. Objectif
Définir les exigences anatomiques, linguistiques, phonétiques et techniques pour un avatar 3D modulaire capable de simuler fidèlement:
- Langues signées (ASL, LSQ, extension multilingue)
- Communication orale / articulatoire (zones IPA pertinentes pour co‐articulation ou pointage facial)
- Expressions faciales (émotion, grammaticales, adverbiales)
- Variantes développement (adulte / enfant / bébé)

## 2. Portée
Inclut: rig mains haute précision, tête/visage articulé (FACS + visèmes), bras avec cinématique physiologique, interop glTF, pipeline test poses linguistiques.
Exclut (phase 0): simulation musculaire complète, tissus mous dynamiques, capture temps réel.

## 3. Anatomie Main & Exigences de Rig
Objectif: Reproduire de façon paramétrable les configurations manuelles contrastives nécessaires à la phonologie des langues signées (handshapes) tout en respectant les limites physiologiques pour éviter des poses irréalistes.

### 3.1 Segmentation osseuse / joints
- Carpe traité comme un bloc rigide (ancrage poignet) pour Phase 0.
- Métacarpiens: possibilité de légère rotation / écartement (splay) contrôlée (Index & Auriculaire plus mobiles; Major quasi fixe) pour affiner arch transverse.
- Phalanges: 
  - Doigts II–V: 3 phalanges (prox / interm / dist) → Joints: MCP, PIP, DIP.
  - Pouce: 2 phalanges + 1 métacarpien → Joints: CMC (selle), MCP, IP.

### 3.2 Degrés de liberté (DoF) cibles
- MCP (II–V): Flex/Ext (~0–90° utile), Abd/Add (±15–20°) mais bloqué automatiquement quand Flexion > 60° (couplage physiologique). Pas de rotation axiale indépendante Phase 0.
- PIP: Flex/Ext ~0–100° (index un peu moins 0–95°). Pas d’Abd/Add.
- DIP: Flex/Ext ~0–80° (index ~0–70°). Hyperextension passive légère (+10°) optionnelle (contrainte douce).
- CMC Pouce: 
  - Flex/Ext (Plano-frontal) ~45° flex / 15° ext.
  - Abd/Add (Palmo-radial) ~50° abd / 15° add.
  - Opposition: axe composé (rotation interne + flex + abd). Implémentation Phase 0: paramètre unique Opposition 0–1 pilotant combinaison (courbe).
- MCP Pouce: Flex/Ext 0–60° (base neutre 10° flex), légère Abd/Add ±10° (optionnel).
- IP Pouce: Flex/Ext 0–80° (hyperext +20° possible).
- Splay métacarpien (Index ↔ Auriculaire): paramètre global -1..+1 appliquant micro-rotations yaw (±8° périphérie) + translation minime pour conserver arc.

### 3.3 Contraintes / couplages
- Limiter Abd/Add MCP proportionnel à (1 - flex_norm). Exemple: abd_effective = abd_target * (1 - clamp(flex/60°,0,1)).
- Opposition pouce force: verrouiller Abd quand Opposition > 0.8 pour éviter sur-extension irréaliste.
- Préserver alignement ongles: orientation distale dérivée de chaîne (roll minimal) sauf lorsque paramètre TwistDistal appliqué (±10°) pour variantes handshape spécifiques.

### 3.4 Handshapes prioritaires (inventaire minimal Phase 0)
Couverture ~80% fréquence ASL/LSQ commune:
- A, S, B (plat), 5 (ouvert), C, O, 1 (index), L, V, 3, 4, I, Y, F (pinch), Relaxed-5, Flat-O.
Paramétrisation: chaque handshape = preset (ensemble d’angles & splay) + éventuelles courbes d’opposition pouce.

### 3.5 Niveaux de détail (LOD) main
- LOD0 (Haute fidélité): Joints listés + blendshapes micro-ajustements pulpe (contact, écrasement léger), ongles séparés.
- LOD1 (Standard): Retirer Abd/Add MCP (poser neutralisée), pas de twist distal.
- LOD2 (Basique): Doigts groupes (courbes anim simultanées), pouce opposition simplifiée binaire.

### 3.6 Cibles morphologiques (blendshapes) proposées
- ContactCompressionFingerPad (param par doigt)
- ThumbPadFlatten
- KnuckleBulge (MCP flexion extrême)
- DorsalVeinAccent (option esthétique)

### 3.7 Données métriques de référence
Objectif: fournir un jeu de mesures normalisées permettant (a) le positionnement cohérent des contacts (paume / pulpe / articulation), (b) la génération de seuils collision, (c) l’adaptation à des morphologies (adulte / enfant / bébé) par simple application de facteurs d’échelle.

Format général: toutes les longueurs sont exprimées en millimètres pour la main adulte moyenne (population mixte occidentale) puis normalisées par la Longueur Paume (LP = distance pli proximal poignet → base doigts au niveau des MCP). Les ratios sont préférés aux valeurs absolues pour portabilité.

Sources principales: [S:HAND_ANTHRO], [S:ANTHRO_MODERN] (valeurs agrégées; affiner avec échantillon interne ultérieur). Les écarts-types sont indicatifs (σ) pour définir marges de tolérance contact (typiquement 0.5σ).

#### 3.7.1 Longueurs segmentaires (adulte)
Mesure | Valeur mm | Ratio / LP | σ approx
------ | --------- | ---------- | --------
Longueur Paume (LP) | 95 | 1.00 | 4.0
Largeur Paume (base MCP II–V) | 82 | 0.86 | 3.5
Index (MCP→Tip) | 70 | 0.74 | 3.0
Majeur (MCP→Tip) | 78 | 0.82 | 3.2
Annulaire (MCP→Tip) | 73 | 0.77 | 3.1
Auriculaire (MCP→Tip) | 60 | 0.63 | 2.8
Pouce (CMC→Tip) | 60 | 0.63 | 3.0

Décomposition phalanges (ratios par doigt, somme ≈ longueur doigt):
Doigt | Prox (% doigt) | Interm (% doigt) | Dist (% doigt)
----- | -------------- | ---------------- | -------------
Index | 46% | 30% | 24%
Majeur | 45% | 32% | 23%
Annulaire | 46% | 31% | 23%
Auriculaire | 48% | 30% | 22%
Pouce (MC + Phal 1 + Phal 2) | 42% (MC) | 34% (Prox) | 24% (Dist)

Conversion absolue exemple (Index): MCP→PIP ≈ 32 mm, PIP→DIP ≈ 21 mm, DIP→Tip ≈ 17 mm.

#### 3.7.2 Largeurs / épaisseurs clés
Mesure | Valeur mm | Ratio / LP | Usage
------ | --------- | ---------- | -----
Épaisseur pulpe distale index | 14 | 0.147 | Rayon collision pulpe-contact
Largeur distal index | 11 | 0.116 | Ajustement silhouette handshape « B »
Largeur MCP index | 18 | 0.189 | Positionnement knuckle bulge morph
Largeur pouce (phalange distale) | 16 | 0.168 | Zone contact pinch « F »
Distance centre CMC pouce → centre MCP index | 45 | 0.474 | Paramètre opposition géométrique

#### 3.7.3 Spreads & arcs
Paramètre | Valeur (deg ou mm) | Note
--------- | ------------------ | ----
Splay maximal Index (abduction MCP) | 20° | Limite physiologique neutre
Splay maximal Auriculaire | 25° | Plus mobile latéralement
Arc transverse paume (creux) flèche | 8 mm | Courbure pour posing naturel
Arc longitudinal (courbure MCP→Tip majeur) flèche | 12 mm | Affecte alignement DIP
Opposition pouce angle combiné (abd+flex+rot) | 110° équivalent | Pour paramètre Opposition=1

#### 3.7.4 Normalisation & dérivation runtime
Variables de base: LP, largeur_paume, longueur_majeur.
Ratios stockés: r_index = 0.74, r_majeur = 0.82, etc. Les sous-segments utilisent pourcentages internes.

Algorithme reconstruction absolue (pseudo):
1. Input: LP_user (profil), scale_global.
2. length_index = r_index * LP_user.
3. index_prox = 0.46 * length_index, index_inter = 0.30 * length_index, index_dist = 0.24 * length_index.
4. Générer positions joints en chaîne sur axe doigt local; appliquer arc longitudinal via offset z suivant courbe paramétrée (flèche 12 mm * (LP_user / 95)).
5. Calculer rayonCollisionPulpe = 0.147 * LP_user.
6. OppositionMapping: angleOpposition = 110° * oppositionParam (0..1).
7. Contraintes Abd/Add adaptatives: abdMaxIndex = 20° * clamp(LP_user/95, 0.9, 1.1).

Tolérances collisions: seuil pénétration autorisé < 0.5 * rayonCollisionPulpe.

#### 3.7.5 Marges enfant / bébé (référence croisée Section 11)
Avant application Section 11, on définit placeholders facteurs d’échelle (seront détaillés Section 11.1):
- enfant_scale_longueurs ≈ 0.92 (6 ans)
- enfant_scale_pulpe ≈ 0.90
- bebe_scale_longueurs ≈ 0.75
- bebe_scale_pulpe ≈ 0.78

Les ROM réduites pour bébé (ex: DIP flexion max 0.80 adulte) se calculeront après reconstitution des longueurs.

#### 3.7.6 Données à affiner
Marqués pour future révision (R1): écarts-types précis par segment, covariance splay vs flexion, anisotropie pulpe.

Notes: Les valeurs mm approximatives servent d’ancrage initial — seront remplacées par moyenne agrégée (N≥30) interne.

### 3.8 Validation
Tests: 
- Range Sweep automatisé par joint vérifiant absence d’interpénétration maillage.
- Set de handshapes exporté → comparaison capture image à gabarits (tolerance angle ≤ 5°).

Sources primaires: [S:HAND_WIKI], [S:PIP_DIP_WIKI], [S:MCP_WIKI].

## 4. Anatomie Bras & Cinématique
Objectif: Garantir trajectoires naturelles pour positionnement des mains dans l’espace de signature (signing space) sans singularités ni poses anatomiquement impossibles.

### 4.1 Segments & Joints
- Clavicule (éventuel contrôleur pour élévation épaule) – Phase 0 optionnel (peut être baked dans animation).
- Scapula (glissement scapulo-thoracique) – Phase 0: approximé par rotation additionnelle sur joint épaule.
- Épaule (Glenohuméral): 3 DoF (pitch, yaw, roll). Limites simplifiées.
- Coude (Huméro-ulnaire / radio-ulnaire prox.): Flex/Ext + pronation/supination radius autour ulna.
- Poignet (Radio-carpien + midcarpien agrégé): Flex/Ext + Deviation Radiale/Ulnar + contribution pronation/supination visible via alignement main.

### 4.2 Ranges de mouvement cibles (adulte sain)
- Épaule: 
  - Flexion 0–170° (utilisé typiquement ≤150° en signature)
  - Extension 0–50°
  - Abduction 0–160° (utilisé ≤140°)
  - Rotation interne/ externe (bras à 90° abd): ~80° / 90° (simplification en ±85° autour neutre).
- Coude: Flex/Ext 0–145° (repos physiologique ~5–10° flexion). Hyperext -5° optionnel.
- Pronation/Supination: ~80° / 80° autour neutre (paume latérale). Limiter en fonction de flexion coude (option Phase 1).
- Poignet: 
  - Flexion 0–70°
  - Extension 0–60°
  - Déviation radiale 0–20°
  - Déviation ulnaire 0–30°
  - Couplage: extrêmes de déviation réduisent flexion maximale (ellipse ergonomique).

### 4.3 Contraintes & Couplages
- IK chaîne bras: prioriser orientation main (handshape lisible) sur alignement exact coude.
- Correction automatique when ShoulderAbduction >130° → réduction CoudeFlexion pour éviter intersection torse.
- Limiter pronation extrême quand Poignet en flexion >50° (facteur 0.6).
- Préservation espace Signing Space: volume devant torse (boîte heuristique) – détecter collisions (torse, tête) et appliquer offset micro-translation ou compensation épaule.

### 4.4 Niveaux de détail cinématique
- Phase 0: IK simple 2 segments + orient wrist joint.
- Phase 1: Ajout clavicle auto (driven par distance main-milieu sternum).
- Phase 2: Scapula slide approximatif (blendshapes ou joint supplémentaire).

### 4.5 Paramètres de contrôle utilisateur
- ShoulderFK/IK Blend (0–1)
- ElbowPin (cible optionnelle pour orientation plan)
- WristSpace Switch (Local / World / Chest) pour orientation stable pendant mouvements larges.

### 4.6 Validation
Tests scriptés:
- Grille de points volumétrique (cube devant torse) → Reach Test: doit atteindre ≥95% points accessibles sans dépasser limites articulaires.
- Stress Test trajectoires (courbes spline) comparant jitter orientation main (<2° variation frame-to-frame en trajectoire lisse).

Sources primaires: [S:HAND_WIKI] (supination/pronation mention), [S:WRIST_WIKI].

## 5. Tête & Visage (FACS / Phonétique)
Objectif: Supporter simultanément expressions linguistiques (questions, topicalisation), émotions de base et articulation labiale/mandibulaire pour synchronisation multimodale.

### 5.1 Ensemble minimal AUs (priorité Phase 0)
AU1 Inner Brow Raiser  
AU2 Outer Brow Raiser  
AU4 Brow Lowerer  
AU5 Upper Lid Raiser  
AU6 Cheek Raiser  
AU7 Lid Tightener  
AU9 Nose Wrinkler (option)  
AU10 Upper Lip Raiser  
AU12 Lip Corner Puller  
AU14 Dimpler (option)  
AU15 Lip Corner Depressor  
AU17 Chin Raiser  
AU20 Lip Stretcher  
AU23 Lip Tightener  
AU24 Lip Pressor  
AU25 Lips Part  
AU26 Jaw Drop  
AU27 Mouth Stretch  
AU28 Lip Suck (option)  
AU45 Blink  
Head Pitch / Yaw / Roll (mouvements non‐manuels)  
Eye Gaze (target vector)

### 5.2 Mapping interne → ARKit (exemples)
FACS_AU01 ↔ browInnerUp  
FACS_AU02 ↔ browOuterUp_[L/R]  
FACS_AU12 ↔ mouthSmile_[L/R]  
FACS_AU15 ↔ mouthFrown_[L/R]  
FACS_AU17 ↔ chinRaise  
FACS_AU26 ↔ jawOpen  
FACS_AU20 ↔ mouthStretch  
FACS_AU25 ↔ jawOpen *et* lipsPart (interne fusion)  
Blink ↔ eyeBlink_[L/R]
(Le reste défini dans table d’expansion future.)

### 5.3 Visèmes (Set initial)
Code | Catégorie | Description | Exemples phonèmes
---- | --------- | ----------- | -----------------
VIS_PBM | Bilabiale fermée | Lèvres jointes | /p b m/
VIS_FV | Labio-dentale | Dents sur lèvre inférieure | /f v/
VIS_TH | Interdentale | Langue visible entre incisives | /θ ð/
VIS_TDN | Alvéolaire | Légère ouverture, langue derrière incisives | /t d n l/
VIS_SZX | Fricative alv. | Lèvres étirées, dents visibles | /s z/
VIS_SH | Post-alv./palato-alv. | Lèvres légèrement arrondies, ouverture réduite | /ʃ ʒ tʃ dʒ/
VIS_KG | Vélaire | Ouverture médiane, langue postérieure | /k g ŋ/
VIS_R | Rhotic | Lèvres neutres/légère protrusion | /ɹ r/
VIS_W | Labiovélaire | Arrondissement modéré | /w/
VIS_J | Palatale | Lèvres neutres | /j/
VIS_A | Ouverte | Large ouverture | /a ɑ/
VIS_E | Mi-ouverte | Ouverture moyenne | /e ɛ ə/
VIS_I | Étirée | Lèvres latéralement | /i ɪ/
VIS_U | Arrondie fermée | Forte protrusion | /u ʊ o/
VIS_NEUTRAL | Repos | Léger contact lèvres | (silence)

### 5.4 Zones articulatoires 3D (ancres)
Ancres (repères) définies comme points ou plans relatifs au crâne:  
- Glabella, Nasion (référence verticale sourcils)  
- CommissureLabiale_[L/R]  
- MidUpperIncisor / MidLowerIncisor  
- PalateAnterior (alvéolaire), PalateMid (palatal), PalatePosterior (vélaire)  
- UvulaApprox (uvulaire)  
- LipUpperMid, LipLowerMid  
- JawHinge_[L/R]  
- TongueTip, TongueBlade, TongueDorsum (si langue modélisée Phase 1)

### 5.5 Blendshapes / morph naming
Préfixes: FACS_, VIS_, SIGN_NMF_, EMO_. Exemple: FACS_AU01, VIS_PBM, SIGN_NMF_BrowsQuestion, EMO_SmileSoft.

### 5.6 Priorités LOD visage
- LOD0: AUs listés + visèmes séparés + micro-asymétries (gauche/droite).  
- LOD1: Fusionne certains AUs (1+2 → browUp, 15+17 → mouthLowerSet).  
- LOD2: 6 expressions macro + 5 visèmes regroupés.

### 5.7 Validation
Metrics: Erreur projection silhouette vs gabarit, collision lèvres/dents évitée, séquence co‐articulation visèmes (latence max 2 frames entre audio marker et morph >0.5).

Sources: [S:FACS_BASE], [S:IPA_CHART], [S:ARKit_BLEND].

## 6. Phonologie des Langues Signées

### 6.1 Paramètres principaux
- Handshape (inventaire Section 3.4)  
- Orientation: palmNormal (vec3), fingerDirection (vec3)  
- Location: bodyRegion (enum), offset3D (cm relatif sternum ou repère tête)  
- Movement: pathType (line, arc, circle, oscillation), plane (sagittal / frontal / transverse), repetition (count), directionality  
- Non-manual features (NMF): {faceAUs subset, headMovement, eyeGaze pattern}  
- Contact: {targetRegion, contactType(tap, hold, brush), durationMs}  
- Dominance: {pattern: symmetric / alternating / dominant-nondominant / independent}  
- Timing: {holdMs, transitionMs, overlapRatio}

### 6.2 BodyRegion enum (initial)
HEAD_FOREHEAD, HEAD_CHEEK_L/R, HEAD_CHIN, HEAD_MOUTH, TORSO_UPPER, TORSO_CENTER, SHOULDER_L/R, NEUTRAL_SPACE_FRONT, NEUTRAL_SPACE_HIGH, NEUTRAL_SPACE_LOW, ARM_L/R, HAND_L/R.

### 6.3 Modèle de données (pseudo-schema JSON)
{
  "sign": {
    "id": "STRING",
    "gloss": "STRING",
    "hands": [
      {
        "role": "dominant|non_dominant",
        "handshape": "CODE",
        "orientation": {"palm": [x,y,z], "finger": [x,y,z]},
        "location": {"region": "ENUM", "offset": [x,y,z]},
        "movement": {"path": "line|arc|circle|osc", "plane": "frontal", "repetition": 1, "amplitude": "cm"},
        "contact": {"region": "ENUM", "type": "tap", "duration": 120},
        "timing": {"start": 0, "transition": 180, "hold": 300},
        "constraints": {"avoid": ["FACE_COLLISION"], "symmetryRef": true}
      }
    ],
    "nmf": {"AUs": [1,2], "head": {"pitch": -10}, "gaze": "addressee"}
  }
}

### 6.4 Contraintes / règles
- Symétrie: si pattern symmetric → main non-dominante dérive angles du dominant avec miroirs (axe sagittal).  
- Orientation vs Location: interdiction palmNormal pointer vers visage à <2 cm sans contact déclaré.  
- Timing: overlap gestures successifs ≤30% pour éviter flou signifiant (phase 0 heuristique).  
- Collision résolution: ajustement micro-translation (<1 cm) priorisant conservation handshape.

### 6.5 NMF prioritaires
BrowRaiseQuestion (AU1+2), BrowLowerWH (AU4), HeadTiltTopic, HeadNodYes, HeadShakeNo, MouthAdverbial (pursed), EyeWide (AU5), BlinkEmphatic (AU45 intensité >0.7).

Sources: [S:SL_BATTISON], [S:SL_BRENTARI], [S:SL_ASL_REF].

### 6.6 Règles Formelles NMF
Objectif: définir un sous-ensemble de contraintes logiques pour valider combinaisons d’unités faciales et mouvements de tête pendant un signe.

Syntaxe expressions:
- Identifiants: FACS_AU01, FACS_AU04, HEAD_PITCH, HEAD_YAW.
- Littéraux numériques intensité (0..1) ou angles (°).
- Opérateurs: AND, OR, NOT, >, <, >=, <=, + (somme intensités), IN_RANGE(x,a,b).
- Règle = condition → effet (WARNING|ERROR) + message.

Table règles (exemples):
ID | Expression | Effet | Message
---|-----------|-------|--------
RULE_AU1_AU4_CONFLICT | (FACS_AU01 > 0.5) AND (FACS_AU04 > 0.5) | ERROR | "Brow raise & lower conflict" 
RULE_EXCESS_BLINK | (BlinkEmphatic > 0.9) AND (durationBlink < 80) | WARNING | "Blink too short for emphasis" 
RULE_HEAD_SHAKE_NOD | (HeadNodYes > 0.3) AND (HeadShakeNo > 0.3) | ERROR | "Nod & shake simultaneous" 
RULE_BROW_QUESTION_INTENSITY | (BrowRaiseQuestion + BrowLowerWH > 0.9) | WARNING | "Mixed question/WH signal" 

JSON structure (nmf_rules.v0.1.json) proposée:
{
  "version": "0.1",
  "rules": [
    {
      "id": "RULE_AU1_AU4_CONFLICT",
      "if": "(FACS_AU01 > 0.5) AND (FACS_AU04 > 0.5)",
      "level": "ERROR",
      "message": "Brow raise & lower conflict"
    },
    {
      "id": "RULE_HEAD_SHAKE_NOD",
      "if": "(HeadNodYes > 0.3) AND (HeadShakeNo > 0.3)",
      "level": "ERROR",
      "message": "Nod & shake simultaneous"
    }
  ]
}

Évaluation: parse expression → AST → évaluation sur frame ou intervalle (agrégation max intensité). Violations collectées pour test_nmf_rules.

## 7. Articulation Orale / IPA (Support Linguistique)
Objectif: uniformiser ancrages spatiaux pour pointer, classifier co‐articulation ou gestes métalinguistiques (ex: indiquer lieu d’articulation).

### 7.1 Lieux d’articulation (mapping ID → repère)
ID_BILABIAL → midpoint(LipUpperMid, LipLowerMid)  
ID_LABIODENTAL → plane formé par bord incisives supérieures + lèvre inférieure  
ID_DENTAL → bord incisives supérieures  
ID_ALVEOLAR → PalateAnterior  
ID_POSTALVEOLAR → milieu entre PalateAnterior et PalateMid  
ID_PALATAL → PalateMid  
ID_VELAR → PalatePosterior  
ID_UVULAR → UvulaApprox  
ID_GLOTTAL → plan approximé (trachée entrée) (visualisation stylisée)  

### 7.2 Utilisation dans moteur
- Permet attaches de trajectoires de pointe (index) pour gestes explicatifs.  
- Permet colorisation contextuelle (overlay translucide) pour didactique.  
- Stocké dans glTF extras: nodes["Head"].extras.articulationAnchors.

### 7.3 Co‐articulation baseline
Fenêtre anticipatoire visème: 80 ms avant phonème cible (peut être paramétrable).  
Interpolation morph pondérée par importance (bilabial > arrondi > voyelle ouverte).

Sources: [S:IPA_CHART], [S:PHONETICS_STD].

## 8. Architecture Rig Modulaire

### 8.1 Modules
- CoreSkeleton (corps + bras L/R + base cou)  
- HighFidelityHand (remplaçable par variant – doit garder mêmes joint names: hand.L, index1.L …)  
- FaceModule (blendshapes + joints mâchoire, langue optionnelle)  
- Accessory (cheveux, vêtements – hors scope Phase 0)  

### 8.2 Conventions nommage joints (glTF nodes)
root → hips → spine → chest → neck → head  
chest → shoulder.L → upperArm.L → lowerArm.L → hand.L → index1.L → index2.L → index3.L → indexTip.L  
(analogue côté R)  
Pouce: thumb1.L (CMC), thumb2.L (MCP), thumb3.L (IP), thumbTip.L.

### 8.3 Swappabilité main
Condition: mêmes noms de joints + mêmes bind poses; géométrie alternative fournie via second mesh + skin différent; sélection runtime (variant) KHR_materials_variants ou extension custom EXT_hand_variants.

### 8.4 Blendshape namespace
Groupes: FACS_, VIS_, SIGN_, UTIL_. Interdiction collisions noms; mapping table exportée JSON.

### 8.5 LOD stratégie
LOD tag dans node.extras.lod = 0|1|2; moteur charge filtré selon budget (tri global surfaces + morph count).  

### 8.6 Extensions / extras custom (proposées)
- EXT_avatar_phonology: { handshapesPreset, articulationAnchors, nmfDefinitions }  
- EXT_rig_metadata: { version, jointOrientationStandard: "Y-up X-right Z-forward" }

### 8.7 Extension EXT_avatar_phonology (Schéma conceptuel)
Objectif: Encapsuler métadonnées phonologiques nécessaires à la reconstruction d’un signe sans dépendre d’un format externe.

Structure (JSON Schema abrégée):
{
  "$id": "https://example.org/schemas/ext_avatar_phonology.schema.json",
  "type": "object",
  "properties": {
    "version": {"type": "string"},
    "handshapesPreset": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["code","description","angles"],
        "properties": {
          "code": {"type": "string"},
          "description": {"type": "string"},
          "angles": {"type": "object", "description": "Joint local target angles (deg)"},
          "metadata": {"type": "object"}
        }
      }
    },
    "articulationAnchors": {
      "type": "object",
      "patternProperties": {
        "^ID_[A-Z_]+$": {
          "type": "object",
          "required": ["position"],
          "properties": {"position": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3}}
        }
      }
    },
    "nmfDefinitions": {
      "type": "array",
      "items": {"type": "object", "required": ["id","facial"], "properties": {"id": {"type": "string"}, "facial": {"type": "array", "items": {"type": "string"}}, "constraints": {"type": "object"}}}
    },
    "signEntries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id","hands"],
        "properties": {
          "id": {"type": "string"},
          "gloss": {"type": "string"},
          "hands": {"type": "array", "items": {"type": "object", "required": ["role","handshape","orientation","location","movement","timing"], "properties": {"role": {"type": "string"}, "handshape": {"type": "string"}, "orientation": {"type": "object"}, "location": {"type": "object"}, "movement": {"type": "object"}, "contact": {"type": "object"}, "timing": {"type": "object"}}}},
          "nmf": {"type": "object"}
        }
      }
    }
  },
  "required": ["version","handshapesPreset"]
}

Exemple minimal (embeddé dans glTF: asset.extensions.EXT_avatar_phonology):
{
  "version": "0.1",
  "handshapesPreset": [
    {"code": "A", "description": "Poing fermé, pouce sur côté index", "angles": {"index.MCP": 75, "thumb.CMC": 30}}
  ],
  "articulationAnchors": {
    "ID_ALVEOLAR": {"position": [0.0, 0.065, 0.09]}
  },
  "nmfDefinitions": [
    {"id": "BrowRaiseQuestion", "facial": ["FACS_AU01","FACS_AU02"], "constraints": {"intensityRange": [0.4,0.9]}}
  ],
  "signEntries": [
    {"id": "SIGN_HELLO_ASL", "gloss": "HELLO", "hands": [{"role": "dominant", "handshape": "B", "orientation": {"palm": [0,0,1], "finger": [0,1,0]}, "location": {"region": "HEAD_FOREHEAD", "offset": [0.05,0.02,0]}, "movement": {"path": "line", "plane": "frontal", "amplitude": 0.08, "repetition": 1}, "timing": {"start":0, "transition":180, "hold": 260}}], "nmf": {"head": {"yaw": 5}}}
  ]
}

### 8.8 Extension EXT_rig_metadata (Ébauche)
Objectif: fournir des métadonnées techniques de rig facilitant validation, interchange et adaptation LOD sans heuristiques externes.

Champs principaux (JSON Schema abrégé):
{
  "$id": "https://example.org/schemas/ext_rig_metadata.schema.json",
  "type": "object",
  "properties": {
    "version": {"type": "string"},
    "jointOrientationStandard": {"type": "string", "enum": ["Y-up X-right Z-forward"]},
    "skeleton": {
      "type": "object",
      "properties": {
        "joints": {"type": "array", "items": {"type": "string"}},
        "restPoseHash": {"type": "string", "description": "SHA256 des matrices bind concaténées"}
      },
      "required": ["joints","restPoseHash"]
    },
    "lod": {
      "type": "array",
      "items": {"type": "object", "required": ["level","nodes","maxMorphTargets"], "properties": {"level": {"type": "integer"}, "nodes": {"type": "array", "items": {"type": "string"}}, "maxMorphTargets": {"type": "integer"}, "budgetMs": {"type": "number"}}}
    },
    "constraints": {
      "type": "object",
      "properties": {
        "jointLimits": {"type": "object", "description": "Map joint -> {min:[deg],max:[deg]} par axe"},
        "couplings": {"type": "array", "items": {"type": "object", "properties": {"driver": {"type": "string"}, "driven": {"type": "string"}, "expression": {"type": "string"}}}}
      }
    },
    "handshapePresetRef": {"type": "string", "description": "Lien vers extension EXT_avatar_phonology.version"}
  },
  "required": ["version","skeleton"]
}

Exemple embedding glTF (asset.extensions.EXT_rig_metadata):
{
  "version": "0.1",
  "jointOrientationStandard": "Y-up X-right Z-forward",
  "skeleton": {"joints": ["root","hips","spine","chest","shoulder.L", "upperArm.L"], "restPoseHash": "5f2a..."},
  "lod": [
    {"level":0, "nodes":["faceMesh","handHigh.L","handHigh.R"], "maxMorphTargets": 80, "budgetMs": 4.0},
    {"level":1, "nodes":["faceMeshLOD1","handStd.L","handStd.R"], "maxMorphTargets": 40, "budgetMs": 2.0},
    {"level":2, "nodes":["faceMeshLOD2","handLow.L","handLow.R"], "maxMorphTargets": 20, "budgetMs": 1.0}
  ],
  "constraints": {
    "jointLimits": {"index1.L": {"flex": {"min":0, "max":90}}},
    "couplings": [{"driver": "index1.L.flex", "driven": "index1.L.abd", "expression": "abd = (1 - flex/60) * abd_target"}]
  },
  "handshapePresetRef": "EXT_avatar_phonology@0.1"
}

## 9. Formats & Interopérabilité

### 9.1 glTF 2.0 utilisation
- Mesh séparé par module (corps, mains, visage option)  
- Skins: 1 skin global ou skins distincts (face micro-joints)  
- Morph Targets: list ordonnée; indices stables entre versions mineures.  
- Animations: canaux séparés (facial, mains, corps) pour recomposition.

### 9.2 Mapping FACS ↔ Interne ↔ ARKit (extraits)
AU1 → FACS_AU01 → browInnerUp  
AU2 → FACS_AU02 → browOuterUp_[L/R]  
AU12 → FACS_AU12 → mouthSmile_[L/R]  
AU26 → FACS_AU26 → jawOpen  
VIS_PBM → (N/A FACS) → combined lipsClosed morph (ou derive d’inversion jawOpen)  

### 9.3 Compression / performance
- Quantisation positions 14 bits, normales 12 bits (KHR_mesh_quantization).  
- Animations: interpolation cubic spline pour facial, linear pour corps.  
- Option Draco pour meshes statiques (pas sur morph heavy faces).  

### 9.4 Sécurité régression
Versionnement semver dans asset.extras.avatarSpecVersion.

Sources: [S:FORMAT_GLTF], [S:FORMAT_KHR], [S:ARKit_BLEND].

## 10. Jeu de Tests (Validation Linguistique & Anatomique)

Catégorie | Objectif | Métrique clé
--------- | -------- | ------------
Hand ROM | Respect limites articulaires | Diff max angle >limite ? (FAIL)
Handshape Presets | Conformité | Erreur RMS angles <5°
Symétrie | Signes biman. | Δ orientation paumes <7° (si symmetric)
Collision | Pas d’interpénétration | Nombre frames collision = 0
Visèmes Sync | Alignement audio | Décalage pic morph ≤ 40 ms
NMF Intégrité | Combinaison autorisée | Règles conflit (ex AU1+AU4 > intensité seuil) absentes
Performance | Budget morph | < 60 morph actifs (LOD0 bureau), < 25 (mobile)
LOD Fallback | Dégradation progressive | Score lisibilité ≥0.9 (heuristique silhouette)
Reach Space | Couverture espace signature | ≥95% points test accessibles
Stabilité IK | Lissage orientation main | Variation frame-to-frame <2°

Scripts prévus: test_hand_rom, test_handshape_presets, test_viseme_sync, test_nmf_rules, test_reach_volume.

### 10.1 Pseudo-algorithmes détaillés

test_hand_rom:
1. Charger limites articulaires (EXT_rig_metadata.constraints.jointLimits).
2. Pour chaque joint et axe pertinent: échantillonner N steps (ex: 10) entre min→max.
3. Appliquer rotation, résoudre couplages; mettre à jour scène (sans IK corps si main isolée).
4. Vérifier: (a) pas de collision mesh self/inter (bounding volumes ou distance surfaces), (b) angle appliqué ≤ limite+tol (1°).
5. Enregistrer angle_max_effectif; calculer diff = max_effectif - limite_théorique.
6. FAIL si diff > 1° ou collision détectée.

test_handshape_presets:
1. Lire presets (EXT_avatar_phonology.handshapesPreset).
2. Pour chaque preset P: appliquer angles cibles sur joints.
3. Mesurer erreur_angle_j = |angle_actuel - angle_cible|.
4. RMS_P = sqrt(sum(erreur_angle_j^2)/countJointsCiblés).
5. Capturer image OR silhouette binaire → comparer vs référence (optionnel R2) via IoU.
6. FAIL si RMS_P > 5° ou IoU < 0.92 (si référence dispo).

test_reach_volume:
1. Définir grille points uniformes dans volume signing space (ex: 9x7x5 points).
2. Pour chaque point: résoudre IK bras (ou planificateur) pour amener centre paume.
3. Marquer succès si distance paume→point < seuil (2 cm) ET aucune collision torse/tête.
4. Calculer couverture = succès / total.
5. FAIL si couverture < 0.95.

test_viseme_sync:
1. Charger séquence phonèmes avec timestamps audio.
2. Générer timeline visèmes cibles (anticipation 80 ms; Section 7.3).
3. Jouer animation ou simuler interpolation morph (cubic spline pour AUs).
4. Pour chaque phonème: trouver frame pic morph visème associé.
5. latence = |t_pic - (t_phoneme - anticip)|.
6. FAIL si latence moyenne > 40 ms ou latence max > 60 ms.

test_nmf_rules:
1. Charger nmfDefinitions & règles conflits (ex: AU1+AU4 intensité >0.5 interdit).
2. Générer combinaisons aléatoires (Monte Carlo M=200) d’AUs dans plages intensityRange.
3. Pour chaque combinaison: évaluer règles (expressions logiques) → collecter violations.
4. FAIL si violations > 0 ou couverture de chaque règle <100% testée.

### 10.2 Format rapport JSON
Schéma conceptuel:
{
  "version": "0.1",
  "avatarVersion": "0.1.0",
  "tests": [
    {
      "id": "test_hand_rom",
      "metrics": {"joints_tested": 42, "max_angle_diff_deg": 0.8},
      "thresholds": {"max_angle_diff_deg": 1.0},
      "status": "PASS",
      "failures": []
    }
  ],
  "summary": {"pass": 5, "fail": 0, "coverage_reach": 0.97}
}

Règles:
- status PASS si toutes les métriques respectent leurs seuils.
- failures liste objets {"metric","value","threshold","detail"}.
- Ajout champ "durationMs" par test recommandé.

Exemple minimal (test_handshape_presets):
{
  "id": "test_handshape_presets",
  "metrics": {"presets": 14, "rms_mean_deg": 2.9, "rms_max_deg": 4.7},
  "thresholds": {"rms_mean_deg": 5, "rms_max_deg": 5},
  "status": "PASS",
  "failures": []
}

## 11. Variantes Développement (Bébé / Enfant)

Aspect | Enfant (≈6 ans) | Bébé (≈12-18 mois)
------ | --------------- | ------------------
ROM Doigts | ~90–95% adulte | 70–80% adulte (réduction flex DIP)
Handshape Maîtrise | Simplifications (A,B,5) | Préhension globale (gross grasp)
Vitesse Transition | -10% | -25% / + latence réaction
NMF Contrôle Sourcils | Partiel | Minimal
Coordination Biman. | Majorité symétrique | Principalement unimanuel

Paramètres d’adaptation: scaleAmplitude (<1), jitterTemporal (ajout ±30 ms), limitation inventaire handshape.

### 11.1 Paramètres numériques dérivés
Objectif: chiffrer adaptations morphologiques et fonctionnelles en se basant sur les ratios Section 3.7.

Facteurs d’échelle longueur (appliqués à LP et dérivés segmentaires):
- Enfant (6 ans): 0.92
- Bébé (12–18 mois): 0.75

Facteurs de largeur/épaisseur pulpe:
- Enfant: 0.90
- Bébé: 0.78

Réduction ROM (multiplie limites adultes):
Joint | Enfant | Bébé
----- | ------ | ----
MCP Flex | 0.95 | 0.85
PIP Flex | 0.95 | 0.80
DIP Flex | 0.92 | 0.75
Pouce Opposition | 0.95 | 0.80

Vitesse transition gestes (facteur temps → augmente durée):
- Enfant: *1.10
- Bébé: *1.25

Jitter temporel (ajout bruit gaussien σ):
- Enfant: 15 ms
- Bébé: 30 ms

Script adaptation pseudo:
1. Input profil {ageClass}.
2. scaleL = lookupScaleLength(ageClass).
3. Recalculer longueurs segmentaires = ratios * (LP_adulte * scaleL).
4. Appliquer facteur pulpe sur rayonCollisionPulpe.
5. Limiter ROM = ROM_adulte * factorROM[ageClass][joint].
6. Ajuster temps transitions = baseTransition * speedFactor[ageClass].
7. Si ageClass == bebe, réduire inventaire handshape à {A, B, 5, S, C}.
8. Appliquer jitter gaussien sur start/hold (σ défini) pour micro-variabilité.

Validation: recalculer test_hand_rom avec nouveaux plafonds → tous angles doivent rester ≤ limites réduites; vérifier absence d’échec collision (rayons modifiés).

## 12. Bibliographie & Sources (Première liste)
ID | Référence | Type | Remarque
-- | --------- | ---- | --------
S:HAND_WIKI | "Hand" Wikipedia (2025-07-19) | Anatomie | CC-BY-SA 4.0
S:PIP_DIP_WIKI | "Interphalangeal joints of the hand" Wikipedia (2025-08-28) | Anatomie | CC-BY-SA 4.0
S:MCP_WIKI | "Metacarpophalangeal joint" Wikipedia (2025-08-28) | Anatomie | CC-BY-SA 4.0
S:WRIST_WIKI | "Wrist" Wikipedia (2025-08-28) | Anatomie | CC-BY-SA 4.0
S:FACS_BASE | Ekman & Friesen (1978) FACS Manual | FACS | Référence descriptive (licence propriétaire – résumé seul)
S:IPA_CHART | International Phonetic Association (2023) IPA Chart | Phonétique | Usage académique
S:PHONETICS_STD | Ladefoged & Johnson (2021) A Course in Phonetics | Phonétique | Ouvrage
S:SL_BATTISON | Battison (1978) Lexical Borrowing in ASL | Phonologie | Paramètres
S:SL_BRENTARI | Brentari (1998) A Prosodic Model of Sign Language Phonology | Phonologie | Modèle
S:SL_ASL_REF | Valli et al. (2011) Linguistics of ASL | Phonologie | Inventaire
S:FORMAT_GLTF | glTF 2.0 Spec (Khronos) | Format | Technique
S:FORMAT_KHR | KHR_mesh_quantization & autres | Extension | Optimisation
S:ARKit_BLEND | Apple ARKit Face Tracking BlendShapes | Format | Mapping AUs
S:HAND_ANTHRO | NASA Anthropometric Source Book (1978) | Anthropométrie | Tailles mains | 
S:ANTHRO_MODERN | Gerstman (2020) Anthropometric Data | Anthropométrie | Mise à jour | 
S:MBLAB | MB-Lab Project Documentation | Rigging | Open-source base human | 
S:MAKEHUMAN | MakeHuman Docs | Rigging | Variation morphologique | 
S:OPENPOSE | Cao et al. (2017) OpenPose | Vision | Données articulation | 
S:MEDIAPIPE_HAND | Google MediaPipe Hands | Vision | Landmarks utilisables | 

(Ajouts futurs: sources LSQ spécifiques, anthropométrie main, développement moteur, corpus NMF.)

## 13. Cache Références Téléchargeables (Initial)
ID | Type | URL | Licence | Hash(SHA256) | Note
-- | ---- | --- | ------- | ------------ | ----
S:HAND_WIKI | html | https://en.wikipedia.org/wiki/Hand | CC-BY-SA 4.0 | (à générer) | Snapshot
S:WRIST_WIKI | html | https://en.wikipedia.org/wiki/Wrist | CC-BY-SA 4.0 | (à générer) | Snapshot
S:PIP_DIP_WIKI | html | https://en.wikipedia.org/wiki/Interphalangeal_joints_of_the_hand | CC-BY-SA 4.0 | (à générer) | Snapshot
S:MCP_WIKI | html | https://en.wikipedia.org/wiki/Metacarpophalangeal_joint | CC-BY-SA 4.0 | (à générer) | Snapshot
S:FORMAT_GLTF | pdf/html | https://registry.khronos.org/glTF/specs/2.0 | Apache-2.0 | (à générer) | Spec
S:FORMAT_KHR | html | https://github.com/KhronosGroup/glTF | Various | (à générer) | Extensions
S:IPA_CHART | pdf | https://www.internationalphoneticassociation.org/ipachart | © IPA | (à générer) | Educational
S:MBLAB | git | https://github.com/animate1978/MB-Lab | AGPL-3.0 | (à générer) | Rig base
S:MAKEHUMAN | site | http://www.makehumancommunity.org/ | CC-BY | (à générer) | Générateur
S:MEDIAPIPE_HAND | doc | https://developers.google.com/mediapipe/solutions/vision/hand_landmarker | Apache-2.0 | (à générer) | Landmarks

Procédure hash (exemple): sha256sum fichier > store.

Workflow recommandé (automatisé):
1. Créer dossier `cache_downloads/` contenant les ressources téléchargées (noms stables).
2. Maintenir fichier liste `cache_sources.txt` lignes: `ID URL TYPE(optional)`.
3. Exécuter script `scripts/generate_cache_hashes.py --input cache_sources.txt --out cache_manifest.json`.
4. Commit `cache_manifest.json` (traçabilité des versions). Ne pas modifier manuellement les hash.
5. Lors mise à jour source, retélécharger fichier → relancer script → nouvelle empreinte.

Schéma sortie (extrait):
{
  "version": "0.1",
  "generated": "UTC ISO8601",
  "items": [ {"id":"S:HAND_WIKI","url":"...","filename":"S_HAND_WIKI.html","sha256":"<hex>","size":12345} ]
}

Politique intégrité: build / CI échoue si une ressource listée manque ou si une modification fichier locale n'est pas reflétée par manifest (hash recalculé ≠ stocké).

## 14. Roadmap Technique (Itération 0 → v1)
Étape | Contenu | Sortie | Statut
----- | ------- | ------ | ------
R0 | Spécification initiale (présent document) | v0.1 doc | En cours
R1 | Inventaire complet handshapes + tests ROM | Presets + script test_hand_rom | À faire
R2 | Prototype rig mains HF (glTF) | hand_rig_v0.glb | À faire
R3 | Intégration visage (AUs + visèmes) | face_module_v0.glb | À faire
R4 | Système animation combinatoire (sign + visèmes + NMF) | player prototype | À faire
R5 | Test suite automatisée (Section 10) | rapports JSON | À faire
R6 | Optimisation LOD + quantisation | glb optimisés | À faire
R7 | Variantes enfant/bébé paramétriques | profils config | À faire
R8 | Publication Avatar Spec v1.0 | doc + assets | À faire

Critère passage v1: 95% handshape fréquence couverte, >90% tests OK, mapping FACS ↔ ARKit stable, latence morph <50 ms (réf moteur interne).

---
*Document généré (squelette enrichi – premier tour de remplissage).*
