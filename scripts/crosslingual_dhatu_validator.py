#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation Cross-Linguistique avec 9 Dhātu Optimaux
Test sur les 20 langues du dossier experiments/
"""
import json
import os
import sys
from optimal_dhatu_analyzer import OptimalDhatuAnalyzer

def load_child_prompts(lang_code):
    """Charge les prompts d'une langue spécifique"""
    prompts_path = f"../experiments/dhatu/prompts_child/{lang_code}.json"
    try:
        with open(prompts_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Language file not found: {lang_code}")
        return None

def test_language_coverage(lang_code, analyzer):
    """Teste la couverture pour une langue donnée"""
    prompts_data = load_child_prompts(lang_code)
    if not prompts_data:
        return None
    
    results = []
    total_coverage = 0
    dhatu_usage = {}
    
    for item in prompts_data['items']:
        text = item['text']
        phenomena = item['phenomena']
        
        analysis = analyzer.analyze_text(text)
        coverage = analysis['coverage_stats']['semantic_coverage']
        total_coverage += coverage
        
        # Compter usage dhātu
        for dhatu, count in analysis['dhatu_distribution'].items():
            dhatu_usage[dhatu] = dhatu_usage.get(dhatu, 0) + count
        
        results.append({
            'id': item['id'],
            'text': text,
            'phenomena': phenomena,
            'coverage': coverage,
            'dhatu_found': list(analysis['dhatu_distribution'].keys()),
            'gaps': [gap.text for gap in analysis['semantic_gaps'][:3]]
        })
    
    avg_coverage = total_coverage / len(results) if results else 0
    
    return {
        'lang': lang_code,
        'avg_coverage': avg_coverage,
        'total_sentences': len(results),
        'dhatu_usage': dhatu_usage,
        'results': results
    }

def run_crosslingual_validation():
    """Validation complète sur toutes les langues"""
    
    # 20 langues disponibles dans experiments/dhatu/prompts_child/
    languages = [
        'arb', 'cmn', 'deu', 'en', 'eus', 'ewe', 'fr', 'hau', 
        'heb', 'hin', 'hun', 'iku', 'jpn', 'kor', 'nld', 
        'spa', 'swa', 'tur', 'yor', 'zul'
    ]
    
    analyzer = OptimalDhatuAnalyzer()
    all_results = {}
    
    print("🌍 VALIDATION CROSS-LINGUISTIQUE - 9 DHĀTU OPTIMAUX")
    print("=" * 60)
    
    total_global_coverage = 0
    successful_langs = 0
    global_dhatu_usage = {}
    
    for lang in languages:
        print(f"\n🔍 Testing {lang.upper()}...")
        result = test_language_coverage(lang, analyzer)
        
        if result:
            all_results[lang] = result
            total_global_coverage += result['avg_coverage']
            successful_langs += 1
            
            # Agrégation usage dhātu global
            for dhatu, count in result['dhatu_usage'].items():
                global_dhatu_usage[dhatu] = global_dhatu_usage.get(dhatu, 0) + count
            
            print(f"   ✅ Coverage: {result['avg_coverage']:.3f} ({result['total_sentences']} sentences)")
            print(f"   🧬 Top Dhātu: {sorted(result['dhatu_usage'].items(), key=lambda x: x[1], reverse=True)[:3]}")
        else:
            print(f"   ❌ Failed to load language data")
    
    # Statistiques globales
    global_avg_coverage = total_global_coverage / successful_langs if successful_langs > 0 else 0
    
    print(f"\n🏆 RÉSULTATS GLOBAUX")
    print(f"=" * 30)
    print(f"📊 Langues testées: {successful_langs}/{len(languages)}")
    print(f"🎯 Couverture moyenne globale: {global_avg_coverage:.3f} ({global_avg_coverage:.1%})")
    print(f"🧬 Dhātu les plus utilisés:")
    
    sorted_dhatu = sorted(global_dhatu_usage.items(), key=lambda x: x[1], reverse=True)
    for dhatu, count in sorted_dhatu:
        percentage = count / sum(global_dhatu_usage.values()) * 100
        print(f"   {dhatu}: {count} ({percentage:.1f}%)")
    
    # Comparaison avec baseline
    baseline_coverage = 0.367  # Baseline du système original (3.7 primitives moyenne)
    improvement = global_avg_coverage - baseline_coverage
    
    print(f"\n📈 COMPARAISON AVEC BASELINE")
    print(f"🎯 Baseline (système original): {baseline_coverage:.3f}")
    print(f"🆕 9 Dhātu optimaux: {global_avg_coverage:.3f}")
    print(f"📊 Amélioration: {improvement:+.3f} ({improvement/baseline_coverage:+.1%})")
    
    # Évaluation par famille linguistique
    language_families = {
        'Indo-European': ['en', 'fr', 'deu', 'spa', 'nld', 'hin'],
        'Sino-Tibetan': ['cmn'],
        'Afro-Asiatic': ['arb', 'heb', 'hau'],
        'Niger-Congo': ['yor', 'swa', 'zul', 'ewe'],
        'Altaic': ['jpn', 'kor', 'tur'],
        'Other': ['eus', 'hun', 'iku']
    }
    
    print(f"\n🌍 PERFORMANCE PAR FAMILLE LINGUISTIQUE")
    print(f"=" * 40)
    
    for family, langs in language_families.items():
        family_results = [all_results[lang]['avg_coverage'] for lang in langs if lang in all_results]
        if family_results:
            family_avg = sum(family_results) / len(family_results)
            print(f"{family}: {family_avg:.3f} ({len(family_results)} langues)")
    
    return all_results, global_avg_coverage

if __name__ == "__main__":
    results, coverage = run_crosslingual_validation()
    
    print(f"\n✅ VALIDATION TERMINÉE")
    print(f"🎯 Couverture globale 9 dhātu: {coverage:.1%}")
    print(f"📊 Objectif >70%: {'✅ ATTEINT' if coverage > 0.70 else '⚠️ En cours'}")
