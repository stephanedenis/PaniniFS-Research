# Aide-mémoire : Éviter les blocages de pager

## 🚨 Problème courant
Les commandes Git et GitHub CLI peuvent parfois ouvrir un pager (less, vi) qui bloque la session.

## ✅ Solutions préventives

### Commandes Git
```bash
# Au lieu de : git log
git --no-pager log --oneline -10

# Au lieu de : git status  
git status --porcelain

# Au lieu de : git diff
git --no-pager diff

# Au lieu de : git show
git --no-pager show
```

### Commandes GitHub CLI
```bash
# Au lieu de : gh repo view
gh repo view --json name,url | cat

# Au lieu de : gh pr list
gh pr list --json number,title | cat

# Au lieu de : gh issue list  
gh issue list --json number,title | cat
```

### Configuration globale (optionnel)
```bash
# Désactiver le pager pour toutes les commandes git
git config --global core.pager ""

# Ou définir un pager qui n'interrompt pas
git config --global core.pager "cat"
```

### Variables d'environnement
```bash
# Désactiver temporairement les pagers
export GIT_PAGER=cat
export PAGER=cat
```

## 🔧 Si vous êtes déjà bloqué
- Appuyez sur `q` pour quitter less
- Appuyez sur `:q` puis `Enter` pour quitter vi/vim
- `Ctrl+C` en dernier recours

---
*Généré pour éviter les blocages lors de l'automatisation*
