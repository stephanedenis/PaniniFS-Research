#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit détaillé du corpus existant pour identifier lacunes et besoins d'expansion
"""

import json
from pathlib import Path

def audit_corpus():
    """Analyser le corpus existant"""
    
    # Analyser le corpus existant
    corpus_file = Path('./corpus_simple/corpus.json')
    math_file = Path('./corpus_simple/mathematical_analysis.json')

    print('AUDIT CORPUS EXISTANT')
    print('=' * 50)

    with open(corpus_file, 'r') as f:
        papers = json.load(f)

    with open(math_file, 'r') as f:
        math_analysis = json.load(f)

    print('STATISTIQUES GENERALES')
    print(f'   Total articles: {len(papers)}')

    # Analyse langues
    languages = {}
    categories = {}
    math_densities = []

    for paper in papers:
        lang = paper.get('language', 'unknown')
        languages[lang] = languages.get(lang, 0) + 1
        
        cat = paper.get('primary_category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
        
        math_dens = paper.get('mathematical_analysis', {}).get('math_density', 0)
        math_densities.append(math_dens)

    print('\nDISTRIBUTION LANGUES:')
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        print(f'   {lang}: {count} articles ({count/len(papers)*100:.1f}%)')

    print('\nDISTRIBUTION CATEGORIES:')
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f'   {cat}: {count} articles')

    print('\nANALYSE MATHEMATIQUE:')
    avg_density = sum(math_densities) / len(math_densities)
    print(f'   Densite math moyenne: {avg_density:.3f}')
    papers_with_math = math_analysis["corpus_info"]["papers_with_math"]
    print(f'   Articles avec math: {papers_with_math}/{len(papers)}')
    unique_notations = math_analysis["notation_statistics"]["total_unique"]
    print(f'   Notations uniques: {unique_notations}')

    print('\nLACUNES IDENTIFIEES:')
    print('   X Monolingue (100% anglais)')
    print('   X Sources limitees (ArXiv uniquement)')
    print('   X Notations simples (=, >, < seulement)')
    print('   X Pas de dialectes mathematiques regionaux')
    print('   X Corpus trop petit pour analyses robustes')
    
    print('\nBESOINS EXPANSION:')
    print('   + Corpus multilingue (francais HAL, allemand, etc.)')
    print('   + Sources diversifiees (DBLP, Semantic Scholar)')
    print('   + Notations avancees (pour tout, existe, integral, etc.)')
    print('   + Dialectes regionaux math (notation francaise vs anglo-saxonne)')
    print('   + Corpus >1000 articles pour robustesse statistique')

if __name__ == "__main__":
    audit_corpus()