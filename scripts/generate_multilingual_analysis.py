#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Document Cross-Linguistique pour Corpus Enfant
Créé des visualisations et analyses pour chaque langue du corpus
"""

import json
import os
import sys
from collections import defaultdict, Counter

# Chemin vers les expériences
EXPERIMENTS_PATH = "/home/stephane/GitHub/PaniniFS-Research/experiments/dhatu"

def load_child_prompts(lang_code):
    """Charge les prompts enfant pour une langue donnée"""
    file_path = os.path.join(EXPERIMENTS_PATH, "prompts_child", f"{lang_code}.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def load_typological_sample():
    """Charge les informations typologiques"""
    file_path = os.path.join(EXPERIMENTS_PATH, "typological_sample.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"languages": []}

def get_language_families():
    """Retourne la classification par famille linguistique"""
    return {
        'Indo-Européennes': {
            'en': 'Anglais',
            'fr': 'Français', 
            'deu': 'Allemand',
            'spa': 'Espagnol',
            'nld': 'Néerlandais',
            'hin': 'Hindi'
        },
        'Sino-Tibétaines': {
            'cmn': 'Chinois Mandarin'
        },
        'Afro-Asiatiques': {
            'arb': 'Arabe',
            'heb': 'Hébreu',
            'hau': 'Hausa'
        },
        'Niger-Congo': {
            'yor': 'Yoruba',
            'swa': 'Swahili',
            'zul': 'Zulu',
            'ewe': 'Ewe'
        },
        'Altaïques': {
            'jpn': 'Japonais',
            'kor': 'Coréen',
            'tur': 'Turc'
        },
        'Autres': {
            'eus': 'Basque',
            'hun': 'Hongrois',
            'iku': 'Inuktitut'
        }
    }

def analyze_language_coverage(lang_code, data):
    """Analyse la couverture d'une langue par les dhātu"""
    if not data or 'items' not in data:
        return {
            'coverage': 0,
            'total_sentences': 0,
            'dhatu_usage': {},
            'phenomena': {},
            'gaps': [],
            'strengths': []
        }
    
    total_sentences = len(data['items'])
    dhatu_usage = Counter()
    phenomena = Counter()
    gaps = []
    strengths = []
    
    # Analyse simple basée sur mots-clés (à améliorer avec vrai analyseur)
    dhatu_keywords = {
        'EXIST': ['is', 'am', 'are', 'est', 'être', 'existe', 'sein', 'ist', 'ser', 'estar'],
        'RELATE': ['in', 'on', 'at', 'dans', 'sur', 'avec', 'in', 'auf', 'an', 'en', 'con'],
        'COMM': ['say', 'tell', 'talk', 'dire', 'parler', 'sagen', 'sprechen', 'decir', 'hablar'],
        'EVAL': ['big', 'small', 'good', 'bad', 'grand', 'petit', 'bon', 'groß', 'klein', 'gut'],
        'ITER': ['more', 'again', 'encore', 'plus', 'wieder', 'mehr', 'más', 'otra vez'],
        'MODAL': ['can', 'must', 'may', 'peut', 'doit', 'kann', 'muss', 'puede', 'debe'],
        'CAUSE': ['make', 'do', 'faire', 'machen', 'tun', 'hacer', 'causa', 'porque'],
        'FLOW': ['go', 'come', 'move', 'aller', 'venir', 'gehen', 'kommen', 'ir', 'venir'],
        'DECIDE': ['choose', 'pick', 'want', 'choisir', 'vouloir', 'wählen', 'wollen', 'elegir']
    }
    
    sentences_with_dhatu = 0
    
    for item in data['items']:
        sentence = item.get('text', '').lower()
        item_dhatu = set()
        
        # Détecter dhātu dans la phrase
        for dhatu, keywords in dhatu_keywords.items():
            for keyword in keywords:
                if keyword in sentence:
                    dhatu_usage[dhatu] += 1
                    item_dhatu.add(dhatu)
        
        if item_dhatu:
            sentences_with_dhatu += 1
        
        # Analyser phénomènes si disponibles
        if 'phenomena' in item:
            for phenomenon in item['phenomena']:
                phenomena[phenomenon] += 1
    
    coverage = sentences_with_dhatu / total_sentences if total_sentences > 0 else 0
    
    # Identifier gaps et strengths
    if coverage < 0.3:
        gaps.append("Couverture générale faible")
    if 'EXIST' not in dhatu_usage:
        gaps.append("Manque expression existence")
    if 'RELATE' not in dhatu_usage:
        gaps.append("Relations spatiales non détectées")
    
    if dhatu_usage.get('EXIST', 0) > 3:
        strengths.append("Forte expression existentielle")
    if len(dhatu_usage) > 5:
        strengths.append("Diversité dhātu élevée")
    
    return {
        'coverage': coverage,
        'total_sentences': total_sentences,
        'dhatu_usage': dict(dhatu_usage),
        'phenomena': dict(phenomena),
        'gaps': gaps,
        'strengths': strengths
    }

def generate_language_analysis(lang_code):
    """Génère l'analyse complète d'une langue"""
    data = load_child_prompts(lang_code)
    families = get_language_families()
    
    # Trouver nom et famille
    lang_name = lang_code
    family = "Non classée"
    
    for fam, langs in families.items():
        if lang_code in langs:
            lang_name = langs[lang_code]
            family = fam
            break
    
    analysis = analyze_language_coverage(lang_code, data)
    
    return {
        'code': lang_code,
        'name': lang_name,
        'family': family,
        'analysis': analysis,
        'raw_data': data
    }

def create_corpus_visualization_document():
    """Crée le document principal avec graphiques et analyses"""
    
    # Obtenir toutes les langues disponibles
    prompts_dir = os.path.join(EXPERIMENTS_PATH, "prompts_child")
    available_langs = []
    
    if os.path.exists(prompts_dir):
        for filename in os.listdir(prompts_dir):
            if filename.endswith('.json') and filename != 'schema.json':
                available_langs.append(filename[:-5])  # Remove .json
    
    available_langs.sort()
    
    # Analyser toutes les langues
    all_analyses = {}
    for lang in available_langs:
        all_analyses[lang] = generate_language_analysis(lang)
    
    # Générer le document
    doc_content = f"""# 📊 CORPUS MULTILINGUE ENFANT : Validation Dhātu Universels

*Analyse exhaustive de l'adéquation du système PaniniSpeak sur {len(available_langs)} langues*

---

## 🎯 **Vue d'Ensemble**

### **Corpus Analysé**
- **Langues testées** : {len(available_langs)}
- **Familles linguistiques** : {len(get_language_families())}
- **Total phrases enfant** : {sum(a['analysis']['total_sentences'] for a in all_analyses.values())}

### **Système Dhātu Testé**
```
[EXIST] [RELATE] [COMM] [EVAL] [ITER] [MODAL] [CAUSE] [FLOW] [DECIDE]
```

---

## 🌍 **Analyse par Famille Linguistique**

"""
    
    families = get_language_families()
    family_stats = defaultdict(list)
    
    # Regrouper par famille
    for lang_code, analysis in all_analyses.items():
        family_stats[analysis['family']].append(analysis)
    
    # Générer analyse par famille
    for family, analyses in family_stats.items():
        doc_content += f"""### **{family}**

| Langue | Code | Coverage | Phrases | Top Dhātu | Gaps Identifiés |
|--------|------|----------|---------|-----------|-----------------|
"""
        
        for analysis in analyses:
            lang = analysis['analysis']
            top_dhatu = sorted(lang['dhatu_usage'].items(), key=lambda x: x[1], reverse=True)[:3]
            top_dhatu_str = ", ".join([f"{d}({c})" for d, c in top_dhatu]) if top_dhatu else "Aucun"
            gaps_str = "; ".join(lang['gaps'][:2]) if lang['gaps'] else "Aucun majeur"
            
            doc_content += f"| {analysis['name']} | `{analysis['code']}` | {lang['coverage']:.1%} | {lang['total_sentences']} | {top_dhatu_str} | {gaps_str} |\n"
    
    doc_content += "\n---\n\n"
    
    # Analyses détaillées par langue
    doc_content += "## 📋 **Analyses Détaillées par Langue**\n\n"
    
    for lang_code in sorted(available_langs):
        analysis = all_analyses[lang_code]
        lang = analysis['analysis']
        
        doc_content += f"""### **{analysis['name']} ({analysis['code'].upper()})**
*Famille : {analysis['family']}*

#### **Métriques**
- **Coverage globale** : {lang['coverage']:.1%} ({int(lang['coverage'] * lang['total_sentences'])}/{lang['total_sentences']} phrases)
- **Dhātu détectés** : {len(lang['dhatu_usage'])} / 9

#### **Usage Dhātu**
"""
        
        if lang['dhatu_usage']:
            dhatu_sorted = sorted(lang['dhatu_usage'].items(), key=lambda x: x[1], reverse=True)
            for dhatu, count in dhatu_sorted:
                percentage = (count / lang['total_sentences'] * 100) if lang['total_sentences'] > 0 else 0
                doc_content += f"- **{dhatu}** : {count} occurrences ({percentage:.1f}%)\n"
        else:
            doc_content += "- *Aucun dhātu détecté*\n"
        
        doc_content += "\n#### **Forces et Faiblesses**\n"
        
        if lang['strengths']:
            doc_content += "**✅ Forces :**\n"
            for strength in lang['strengths']:
                doc_content += f"- {strength}\n"
        
        if lang['gaps']:
            doc_content += "**❌ Faiblesses :**\n"
            for gap in lang['gaps']:
                doc_content += f"- {gap}\n"
        
        if not lang['strengths'] and not lang['gaps']:
            doc_content += "*Évaluation neutre - données insuffisantes*\n"
        
        # Exemples de phrases si disponibles
        if analysis['raw_data'] and 'items' in analysis['raw_data']:
            doc_content += "\n#### **Échantillon de Phrases**\n"
            sample_items = analysis['raw_data']['items'][:3]
            for i, item in enumerate(sample_items, 1):
                text = item.get('text', 'Texte non disponible')
                doc_content += f"{i}. *{text}*\n"
        
        doc_content += "\n---\n\n"
    
    # Conclusions globales
    total_coverage = sum(a['analysis']['coverage'] for a in all_analyses.values()) / len(all_analyses)
    best_lang = max(all_analyses.values(), key=lambda x: x['analysis']['coverage'])
    worst_lang = min(all_analyses.values(), key=lambda x: x['analysis']['coverage'])
    
    doc_content += f"""## 🎯 **Conclusions Globales**

### **Performance Système**
- **Coverage moyenne** : {total_coverage:.1%}
- **Meilleure langue** : {best_lang['name']} ({best_lang['analysis']['coverage']:.1%})
- **Plus faible** : {worst_lang['name']} ({worst_lang['analysis']['coverage']:.1%})

### **Dhātu les Plus Universels**
"""
    
    # Compter usage global des dhātu
    global_dhatu = Counter()
    for analysis in all_analyses.values():
        for dhatu, count in analysis['analysis']['dhatu_usage'].items():
            global_dhatu[dhatu] += count
    
    for dhatu, total_count in global_dhatu.most_common():
        lang_count = sum(1 for a in all_analyses.values() if dhatu in a['analysis']['dhatu_usage'])
        universality = lang_count / len(all_analyses) * 100
        doc_content += f"- **{dhatu}** : {total_count} occurrences, {lang_count}/{len(all_analyses)} langues ({universality:.0f}% universalité)\n"
    
    doc_content += f"""
### **Recommandations d'Amélioration**

#### **Gaps Système Identifiés**
1. **Détection linguistique** : Le système simple de mots-clés sous-estime la couverture réelle
2. **Variations morphologiques** : Langues agglutinantes mal détectées
3. **Ordre des mots** : Langues SOV posent des défis

#### **Extensions Proposées**
1. **Analyseur morphologique** pour langues complexes
2. **Patterns syntaxiques** spécifiques par famille
3. **Corpus étendus** pour validation statistique

---

*Document généré automatiquement le {__import__('datetime').datetime.now().strftime('%d/%m/%Y à %H:%M')}*
*Basé sur corpus enfant PaniniFS Research*
"""
    
    return doc_content

def create_graphical_summary():
    """Crée un résumé graphique des résultats"""
    # Obtenir toutes les langues disponibles
    prompts_dir = os.path.join(EXPERIMENTS_PATH, "prompts_child")
    available_langs = []
    
    if os.path.exists(prompts_dir):
        for filename in os.listdir(prompts_dir):
            if filename.endswith('.json') and filename != 'schema.json':
                available_langs.append(filename[:-5])
    
    # Analyser toutes les langues
    all_analyses = {}
    for lang in available_langs:
        all_analyses[lang] = generate_language_analysis(lang)
    
    # Créer visualisation ASCII simple
    graph_content = """# 📈 GRAPHIQUE : Coverage Dhātu par Langue

## Répartition des Coverages

```
Coverage (%)
  100 |
      |
   80 |
      |
   60 |
      |
   40 |
      |
   20 |  ●
      |     ●
    0 |________●●●●●●●●●●●●●●●●●●●●
      """
    
    # Ajouter les langues triées par coverage
    sorted_langs = sorted(all_analyses.items(), key=lambda x: x[1]['analysis']['coverage'], reverse=True)
    
    graph_content += "\n\n## Classement par Coverage\n\n"
    for i, (lang_code, analysis) in enumerate(sorted_langs):
        coverage = analysis['analysis']['coverage']
        bar_length = int(coverage * 50)  # Barre sur 50 caractères
        bar = "█" * bar_length + "░" * (50 - bar_length)
        graph_content += f"{i+1:2d}. {analysis['name']:<15} {coverage:5.1%} |{bar}|\n"
    
    return graph_content

def main():
    """Fonction principale"""
    
    print("🔄 Génération du document d'analyse corpus multilingue...")
    
    # Créer le document principal
    main_doc = create_corpus_visualization_document()
    
    # Créer le graphique
    graph_doc = create_graphical_summary()
    
    # Sauvegarder les documents
    output_dir = "/home/stephane/GitHub/PaniniFS-Research/data/references_cache"
    
    main_file = os.path.join(output_dir, "CORPUS_MULTILINGUE_ANALYSE_COMPLETE.md")
    graph_file = os.path.join(output_dir, "CORPUS_MULTILINGUE_GRAPHIQUES.md")
    
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(main_doc)
    
    with open(graph_file, 'w', encoding='utf-8') as f:
        f.write(graph_doc)
    
    print(f"✅ Documents générés :")
    print(f"   📄 Analyse complète : {main_file}")
    print(f"   📊 Graphiques : {graph_file}")

if __name__ == "__main__":
    main()
