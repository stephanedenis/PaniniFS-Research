# Copilotage Setup - Documentation

## 📋 Résumé

Ce script a configuré avec succès le système de copilotage en :

1. **Copiant la configuration** depuis `../PaniniFS/copilotage`
2. **Configurant un sous-module Git** pointant vers `https://github.com/stephanedenis/PaniniFS-CopilotageShared.git`

## 📁 Structure créée

```
copilotage/
├── config.yml          # Configuration locale du projet
├── README.md           # Documentation du copilotage
└── shared/             # Sous-module Git (PaniniFS-CopilotageShared)
    ├── config.yml
    ├── README.md
    └── .github/
```

## 🔧 Commandes utiles

### Mettre à jour le sous-module shared
```bash
git submodule update --remote copilotage/shared
```

### Initialiser le sous-module dans un nouveau clone
```bash
git submodule update --init --recursive
```

### Vérifier l'état des sous-modules
```bash
git submodule status
```

### Travailler dans le sous-module
```bash
cd copilotage/shared
git checkout main
# Faire des modifications
git add .
git commit -m "Update shared configuration"
git push origin main
cd ../..
git add copilotage/shared
git commit -m "Update shared submodule reference"
```

## 🚀 Prochaines étapes

1. **Pousser les changements** vers le repository distant :
   ```bash
   git push origin main
   ```

2. **Personnaliser la configuration** dans `copilotage/config.yml` selon vos besoins

3. **Contribuer au repository partagé** dans `copilotage/shared/` pour bénéficier à tous les projets

## 📝 Notes importantes

- Le sous-module `copilotage/shared` pointe vers un repository Git séparé
- Les modifications dans `shared/` doivent être commitées dans ce sous-module
- Pensez à mettre à jour la référence du sous-module dans le projet principal après modification

---

*Généré automatiquement par le script setup_copilotage.sh*
