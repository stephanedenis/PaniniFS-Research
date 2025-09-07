# Migration Log

## 2025-09-07 - Initialisation du submodule Research

### Contenu migré depuis le repository principal PaniniFS :

1. **Dossier `.seed_research/`** → racine du repository
   - `cloud-processing/` - Stratégies de calcul cloud
   - `discoveries/` - Découvertes scientifiques (Dhātu, baby sign language, etc.)
   - `methodology/protocols/` - Protocoles de publication et méthodologies
   - `publications/articles/` - Articles en préparation
   - `docs/` - Documentation de recherche
   - `.vscode/` - Configuration VSCode pour la recherche

2. **Scripts** → `scripts/`
   - `generate_research_rss.py` - Génération RSS pour les mises à jour recherche

### Actions post-migration à effectuer dans le repository principal :

- [ ] Supprimer `.seed_research/` après validation
- [ ] Mettre à jour les références dans les scripts
- [ ] Ajouter le submodule dans `.gitmodules`
- [ ] Mettre à jour la documentation

### Structure finale :

```
RESEARCH/
├── README.md
├── MIGRATION.md (ce fichier)
├── scripts/
│   └── generate_research_rss.py
├── cloud-processing/
├── discoveries/
├── methodology/
├── publications/
└── docs/
```
