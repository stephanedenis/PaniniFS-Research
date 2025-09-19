# PaniniFS - Deux Implémentations

PaniniFS propose deux versions complémentaires pour l'analyse sémantique et l'organisation de fichiers basée sur les universaux dhātu de Panini.

## 🦀 PaniniFS-Core (Rust)

**Objectif**: Système de fichiers natif Linux avec intégration FUSE pour un accès transparent.

### Fonctionnalités
- **FUSE Integration**: Mount point transparent dans Linux
- **Index sémantique**: Calcul dhātu vectoriel sur tout type de fichier
- **Performance**: Traitement rapide en Rust natif
- **CLI intégré**: `paninifs analyze`, `paninifs index`, `paninifs mount`

### Installation & Usage
```bash
# Depuis tech/rust/
cargo build --release

# Analyser un fichier
./target/release/paninifs analyze README.md

# Indexer un répertoire  
./target/release/paninifs index /path/to/dir

# (Future) Monter un filesystem
sudo ./target/release/paninifs mount /mnt/paninifs /path/to/source
```

### Architecture
- `src/lib.rs`: Types core (Dhatu, DhatuVector, SemanticFile, SemanticIndex)
- `src/main.rs`: CLI et commandes
- Support FUSE (à implémenter): fichiers virtuels basés sur signatures dhātu

## 📦 PaniniFS-Git (TypeScript/npm)

**Objectif**: Interface Git dynamique avec génération de fichiers à la volée et navigation sémantique.

### Fonctionnalités
- **Git Integration**: Analyse de repos Git avec historique
- **Dynamic Files**: Génération de vues sémantiques (ex: `/by-dhatu/EVAL.json`)
- **Web Interface**: API REST pour browsing sémantique
- **npm Package**: Installation et usage simple

### Installation & Usage
```bash
# Depuis tech/node/packages/paninifs-git/
npm install
npm run build

# Analyser un repo Git
node bin/cli.js browse /path/to/repo

# Créer un index sémantique
node bin/cli.js index /path/to/repo output.json

# (Future) Serveur web
npm run serve -- --port 3001
```

### Architecture
- `src/types.ts`: Types partagés (compatibles avec Rust)
- `bin/cli.js`: Interface ligne de commande
- `bin/server.js` (à implémenter): Serveur web pour API REST

## 🔗 Interopérabilité

### Format commun
Les deux versions utilisent le même format de signature dhātu:
```json
{
  "path": "README.md",
  "signature": "472c97ef52703003", 
  "topDhatus": [
    {"dhatu": "EVAL", "weight": 0.147},
    {"dhatu": "EXIST", "weight": 0.145}
  ]
}
```

### Use Cases Complémentaires

**Rust Version**:
- Intégration système profonde
- Performance pour gros volumes
- Filesystem transparent
- Indexation batch rapide

**TypeScript Version**:
- Intégration Git native
- Interface web moderne
- Développement rapide de prototypes
- API REST pour applications

## 🎯 Roadmap

### Court terme
- [x] Core dhātu codec (Rust + TS)
- [x] CLI de base pour analyse/indexation
- [x] Demo Git browsing
- [ ] FUSE filesystem (Rust)
- [ ] API REST server (TS)

### Moyen terme
- [ ] Compression sémantique (déduplication par signature)
- [ ] Fichiers virtuels dynamiques (agrégations par dhātu)
- [ ] Interface web pour exploration
- [ ] Plugin VS Code

### Long terme
- [ ] Cache distribué basé signatures
- [ ] Sync entre instances PaniniFS
- [ ] ML pour améliorer projection dhātu
- [ ] Intégration cloud (S3, Git repos)

## 🧬 Universaux Dhātu

Les 9 dhātu universels utilisés:
- **RELATE**: Relations, connexions, liens
- **MODAL**: Modalités, possibilités, nécessités
- **EXIST**: Existence, états, être
- **EVAL**: Évaluations, jugements, mesures
- **COMM**: Communication, expressions, langages
- **CAUSE**: Causalités, actions, changements
- **ITER**: Itérations, répétitions, cycles
- **DECIDE**: Décisions, choix, déterminations
- **FEEL**: Sentiments, perceptions, ressentis

Chaque fichier reçoit un vecteur 9D normalisé, une signature stable, et un classement par dhātu dominant.