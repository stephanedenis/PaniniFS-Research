# Node Workspace

Organisation du code Node/JS pour PaniniFS.

## Structure
- `package.json` (workspace root) : scripts proxy et configuration workspaces.
- `packages/test-runner` : exécution Playwright des tests JS.
- `node_modules/` : dépendances partagées (installées à la racine du workspace `tech/node`).

## Utilisation
Depuis la racine du repo (ou `tech/node`):

```bash
cd tech/node
npm install
npm test
npm run test:firefox
```

Pour lancer l’UI Playwright:
```bash
npm run test:ui
```

## Ajout d’un nouveau package
Créer un dossier sous `packages/mon-package` avec son propre `package.json`. Il sera automatiquement inclus.

## Raison de la migration
- Évite le bruit Node à la racine.
- Prépare l’évolution multi-paquets (générateurs, outils de build, analyseurs).
- Simplifie le `verify_layout.sh` (whitelist racine stricte).

## Prochaines améliorations possibles
- Conversion vers PNPM/Yarn si besoin de hoisting optimisé.
- Ajout d’un package `@paninifs/generators` pour scripts de génération.
- Intégration d’un linter/formatter partagé (`eslint`, `prettier`).
