# Règles de Copilotage PaniniFS Research
# Version 2.0 - Septembre 2025
# Stratégies obligatoires pour assurer la qualité des livrables

## 🎯 STRATÉGIE 1: VALIDATION AUTOMATIQUE OBLIGATOIRE

### Principe Fondamental
**AVANT TOUT LIVRABLE WEB**: Exécution obligatoire du validateur de navigation automatisé

### Implémentation Requise
```bash
python3 validate_navigation.py
```

### Critères de Validation
- ✅ **Taux de réussite ≥ 90%** des tests automatisés
- ✅ **Temps de chargement < 3s** par page
- ✅ **Éléments UI requis** présents et fonctionnels
- ✅ **Liens de navigation** opérationnels
- ✅ **Contenu textuel** conforme aux spécifications

### Tests Obligatoires Automatisés
1. **Hub Principal** (`/hub.html`)
   - Éléments: `.hub-container`, `.access-grid`, `.access-card`
   - Contenu: "PaniniFS Research Hub", "Validateur Interactif"

2. **Validateur Interactif** (`/interactive-validator/`)
   - Éléments: `.app-container`, `.nav-tabs`, `.dhatu-grid`
   - Contenu: "PaniniFS Research", "Dhātu"

3. **Galerie Gestes** (`/interactive-validator/gesture-gallery.html`)
   - Éléments: `.gesture-gallery`, `.gesture-showcase`
   - Contenu: "Galerie des Gestes", "Anatomiques"

4. **Tests Techniques** (`/interactive-validator/test-gestures.html`)
   - Éléments: `.gesture-grid`, `.controls`
   - Contenu: "Test des Gestes", "Baby Sign"

5. **Documentation** (`/production/documents/`)
   - Navigation fonctionnelle
   - Fichiers PDF accessibles

### Actions en Cas d'Échec
- 🛑 **ARRÊT du livrable** si taux < 90%
- 🔧 **Correction obligatoire** avant continuation
- 📸 **Screenshots automatiques** pour debugging
- 📋 **Rapport JSON détaillé** généré

---

## 🎯 STRATÉGIE 2: ARCHITECTURE LIENS ROBUSTE

### Principes Obligatoires
- **Chemins absolus** depuis racine serveur (`/path/file.html`)
- **Fallback intelligent** pour ressources manquantes
- **Tests de connectivité** avant déploiement
- **Structure hiérarchique** claire et documentée

### Structure Serveur Requis
```
/home/stephane/GitHub/PaniniFS-Research/  (racine serveur)
├── hub.html                              (navigation principale)
├── navigation-test.html                  (tests diagnostiques)
├── interactive-validator/
│   ├── index.html                       (validateur principal)
│   ├── gesture-gallery.html            (galerie anatomique)
│   ├── test-gestures.html              (tests techniques)
│   ├── app.js                          (logique application)
│   ├── dhatu-data.js                   (base données)
│   └── enhanced-baby-sign-gestures.js  (animations)
└── production/documents/                (corpus PDF)
```

---

## 🎯 STRATÉGIE 3: GESTION SERVEUR AUTOMATISÉE

### Serveur HTTP Obligatoire
- **Python HTTP Server**: `python3 -m http.server 8081`
- **Répertoire racine**: `/home/stephane/GitHub/PaniniFS-Research/`
- **Port standard**: 8081
- **Démarrage automatique** par le validateur

### Gestion des Erreurs
- **Auto-détection** serveur existant
- **Démarrage automatique** si nécessaire
- **Arrêt propre** après validation
- **Gestion timeout** et récupération d'erreurs

---

## 🎯 STRATÉGIE 4: DOCUMENTATION CONTINUE

### Métadonnées Obligatoires
- **Timestamp** de chaque validation
- **Métriques performance** (temps chargement, First Paint)
- **Screenshots** automatiques de toutes les pages
- **Rapport JSON** détaillé avec erreurs

### Archivage Requis
```bash
/tmp/paniniFS_validation_report_YYYYMMDD_HHMMSS.json
/tmp/paniniFS_screenshot_*.png
```

---

## 🎯 STRATÉGIE 5: QUALITÉ INTERFACE UTILISATEUR

### Standards Visuels
- **Design responsive** testé automatiquement
- **Animations SVG** fonctionnelles (baby sign)
- **Navigation intuitive** validée
- **Temps de réponse** < 3 secondes

### Accessibilité
- **Contraste** suffisant
- **Éléments interactifs** identifiables
- **Navigation clavier** supportée
- **Fallbacks** pour échecs JavaScript

---

## 🎯 STRATÉGIE 6: INTÉGRATION CONTINUE

### Workflow Obligatoire
1. **Développement** → Modification code/contenu
2. **Validation automatique** → `python3 validate_navigation.py`
3. **Correction** → Si échec, correction obligatoire
4. **Re-validation** → Jusqu'à succès ≥ 90%
5. **Livrable** → Seulement après validation complète

### Outils Requis
- **Playwright** pour automation navigateur
- **Python 3.7+** pour scripts validation
- **HTTP Server** pour tests locaux
- **JSON reporting** pour traçabilité

---

## 🎯 EXÉCUTION DE LA STRATÉGIE

### Commande de Validation Complète
```bash
cd /home/stephane/GitHub/PaniniFS-Research

# Launcher intelligent (recommandé - choisit automatiquement)
python3 validate.py

# Versions spécifiques (si besoin)
python3 validate_navigation.py          # Version complète avec Playwright
python3 validate_navigation_basic.py    # Version basique HTTP/urllib
```

### Codes de Sortie
- `0`: Validation réussie (≥90%)
- `1`: Validation partiellement échouée (<90%)
- `2`: Erreur critique durant validation
- `3`: Interruption utilisateur
- `4`: Erreur inattendue

### Intégration CI/CD Future
```yaml
# Exemple pour GitHub Actions
- name: Validate PaniniFS Navigation
  run: |
    cd /home/stephane/GitHub/PaniniFS-Research
    python3 validate_navigation.py
  env:
    HEADLESS: true
```

---

## 📋 CHECKLIST DE LIVRABLE

### Avant Chaque Livrable
- [ ] Serveur HTTP fonctionnel port 8081
- [ ] Tous les fichiers présents et accessibles
- [ ] Liens de navigation testés manuellement
- [ ] **Validation automatique exécutée et réussie**
- [ ] Screenshots générées et vérifiées
- [ ] Rapport JSON archivé
- [ ] Performance acceptable (<3s par page)
- [ ] Fonctionnalités JavaScript opérationnelles

### Critères d'Acceptation
- **90% minimum** des tests automatisés passent
- **Navigation complète** fonctionnelle
- **Gestes baby sign** animés correctement
- **Export de données** opérationnel
- **Documentation** accessible et complète

---

*Ces règles constituent le standard minimal obligatoire pour tout livrable PaniniFS Research impliquant des interfaces web. Aucune exception n'est autorisée sans validation automatique préalable.*
