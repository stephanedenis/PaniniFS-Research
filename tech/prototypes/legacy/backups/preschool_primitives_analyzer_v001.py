#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧸 ANALYSE CORPUS PRÉSCOLAIRE MULTILINGUE
====================================================================
Recherche des primitives nécessaires pour atteindre 100% de couverture
sur les dialogues préscolaires dans toutes les langues.

Auteur: Assistant IA PaniniFS Research
Version: 0.0.1 - Recherche Primitives Préscolaires
Date: 08/09/2025
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
import json
from pathlib import Path

class PreschoolCorpusAnalyzer:
    """Analyseur spécialisé corpus préscolaire"""
    
    def __init__(self):
        print("🧸 INITIALISATION ANALYSEUR CORPUS PRÉSCOLAIRE")
        
        # Corpus dialogues préscolaires typiques
        self.preschool_corpus = {
            'FRENCH': [
                "Maman, j'ai faim",
                "Je veux jouer avec mes jouets",
                "Le chat mange ses croquettes",
                "Papa lit une histoire",
                "Je suis content aujourd'hui",
                "Mon frère pleure",
                "La voiture rouge roule vite",
                "Je dors dans mon lit",
                "Tu viens jouer avec moi ?",
                "Regarde mon dessin !",
                "J'aime les bonbons",
                "Où est ma poupée ?",
                "Il fait beau dehors",
                "Je me lave les mains",
                "Bonne nuit papa",
                "Maman chante une chanson",
                "Mon chien aboie fort",
                "Je mets mes chaussures",
                "C'est l'heure du goûter",
                "Je cours dans le jardin"
            ],
            
            'ENGLISH': [
                "Mommy, I'm hungry",
                "I want to play with my toys",
                "The cat eats its food",
                "Daddy reads a story",
                "I am happy today",
                "My brother is crying",
                "The red car goes fast",
                "I sleep in my bed",
                "Do you want to play with me?",
                "Look at my drawing!",
                "I love candy",
                "Where is my doll?",
                "It's sunny outside",
                "I wash my hands",
                "Good night daddy",
                "Mommy sings a song",
                "My dog barks loudly",
                "I put on my shoes",
                "It's snack time",
                "I run in the garden"
            ],
            
            'CHINESE': [
                "妈妈，我饿了",
                "我想玩玩具",
                "猫咪吃食物",
                "爸爸读故事",
                "我今天很开心",
                "我哥哥在哭",
                "红色汽车跑得快",
                "我在床上睡觉",
                "你想和我一起玩吗？",
                "看我的画！",
                "我喜欢糖果",
                "我的娃娃在哪里？",
                "外面天气很好",
                "我洗手",
                "晚安爸爸",
                "妈妈唱歌",
                "我的狗叫得很大声",
                "我穿鞋子",
                "零食时间到了",
                "我在花园里跑步"
            ],
            
            'ARABIC': [
                "ماما، أنا جائع",
                "أريد أن ألعب بألعابي",
                "القطة تأكل طعامها",
                "بابا يقرأ قصة",
                "أنا سعيد اليوم",
                "أخي يبكي",
                "السيارة الحمراء تسير بسرعة",
                "أنام في سريري",
                "هل تريد أن تلعب معي؟",
                "انظر إلى رسمتي!",
                "أحب الحلوى",
                "أين دميتي؟",
                "الطقس جميل في الخارج",
                "أغسل يدي",
                "تصبح على خير بابا",
                "ماما تغني أغنية",
                "كلبي ينبح بصوت عالي",
                "ألبس حذائي",
                "حان وقت الوجبة الخفيفة",
                "أجري في الحديقة"
            ]
        }
        
        # Dhātu actuels (base v0.0.1)
        self.current_dhatus = {
            'EXIST', 'RELATE', 'COMM', 'EVAL', 'ITER', 
            'MODAL', 'CAUSE', 'FLOW', 'DECIDE'
        }
        
        # Primitives préscolaires candidates
        self.preschool_primitives = {
            # Actions corporelles essentielles
            'EAT': {
                'french': ['manger', 'mange', 'boire', 'boit', 'avaler', 'goûter'],
                'english': ['eat', 'eats', 'drink', 'drinks', 'taste', 'swallow'],
                'chinese': ['吃', '喝', '品尝', '吞咽'],
                'arabic': ['يأكل', 'تأكل', 'يشرب', 'تشرب', 'يتذوق']
            },
            
            'SLEEP': {
                'french': ['dormir', 'dors', 'dort', 'sieste', 'repos', 'se reposer'],
                'english': ['sleep', 'sleeps', 'nap', 'rest', 'lie down'],
                'chinese': ['睡觉', '休息', '躺下', '小憩'],
                'arabic': ['ينام', 'تنام', 'يستريح', 'يرقد', 'قيلولة']
            },
            
            'PLAY': {
                'french': ['jouer', 'joue', 'joues', 'jeu', 's\'amuser', 'amuser'],
                'english': ['play', 'plays', 'game', 'fun', 'toy'],
                'chinese': ['玩', '游戏', '娱乐', '玩具'],
                'arabic': ['يلعب', 'تلعب', 'لعبة', 'يستمتع', 'لعب']
            },
            
            'WASH': {
                'french': ['laver', 'lave', 'nettoyer', 'bain', 'douche', 'propre'],
                'english': ['wash', 'clean', 'bath', 'shower', 'soap'],
                'chinese': ['洗', '清洁', '洗澡', '肥皂'],
                'arabic': ['يغسل', 'تغسل', 'ينظف', 'حمام', 'صابون']
            },
            
            # Émotions de base
            'HAPPY': {
                'french': ['content', 'heureux', 'joyeux', 'sourire', 'rire'],
                'english': ['happy', 'glad', 'joy', 'smile', 'laugh'],
                'chinese': ['开心', '高兴', '快乐', '微笑', '笑'],
                'arabic': ['سعيد', 'فرح', 'مسرور', 'يبتسم', 'يضحك']
            },
            
            'SAD': {
                'french': ['triste', 'pleurer', 'pleure', 'chagrin', 'larme'],
                'english': ['sad', 'cry', 'tears', 'upset', 'unhappy'],
                'chinese': ['伤心', '哭', '眼泪', '难过'],
                'arabic': ['حزين', 'يبكي', 'تبكي', 'دموع', 'متضايق']
            },
            
            # Relations familiales
            'FAMILY': {
                'french': ['maman', 'papa', 'frère', 'sœur', 'grand-mère', 'grand-père'],
                'english': ['mommy', 'daddy', 'brother', 'sister', 'grandma', 'grandpa'],
                'chinese': ['妈妈', '爸爸', '哥哥', '姐姐', '奶奶', '爷爷'],
                'arabic': ['ماما', 'بابا', 'أخ', 'أخت', 'جدة', 'جد']
            },
            
            # Actions quotidiennes
            'WEAR': {
                'french': ['porter', 'mettre', 'habiller', 'vêtement', 'chaussure'],
                'english': ['wear', 'put on', 'dress', 'clothes', 'shoes'],
                'chinese': ['穿', '戴', '衣服', '鞋子', '穿戴'],
                'arabic': ['يلبس', 'تلبس', 'يرتدي', 'ملابس', 'حذاء']
            },
            
            'LOOK': {
                'french': ['regarder', 'voir', 'observer', 'yeux', 'regarde'],
                'english': ['look', 'see', 'watch', 'eyes', 'observe'],
                'chinese': ['看', '观察', '眼睛', '看见'],
                'arabic': ['ينظر', 'تنظر', 'يرى', 'عيون', 'يراقب']
            },
            
            # Sensations physiques  
            'HUNGRY': {
                'french': ['faim', 'j\'ai faim', 'affamé', 'appétit'],
                'english': ['hungry', 'appetite', 'starving'],
                'chinese': ['饿', '饥饿', '食欲'],
                'arabic': ['جائع', 'جوع', 'شهية']
            },
            
            'FAST': {
                'french': ['vite', 'rapide', 'rapidement', 'vitesse'],
                'english': ['fast', 'quick', 'speed', 'rapidly'],
                'chinese': ['快', '迅速', '速度'],
                'arabic': ['سريع', 'بسرعة', 'سرعة']
            }
        }
    
    def analyze_coverage_current_dhatus(self) -> Dict:
        """Analyse couverture dhātu actuels sur corpus préscolaire"""
        print("\n🔍 ANALYSE COUVERTURE DHĀTU ACTUELS")
        
        # Mapping dhātu actuels pour préscolaire
        current_mapping = {
            'EXIST': ['是', 'est', 'are', 'is', 'être', 'avoir', 'il y a', 'there', 'موجود', 'يوجد'],
            'RELATE': ['dans', 'avec', 'sur', 'in', 'with', 'at', '在', '和', 'في', 'مع'],
            'COMM': ['dit', 'parle', 'says', 'talk', 'tell', '说', '讲', 'يقول', 'يتكلم'],
            'EVAL': ['bon', 'beau', 'good', 'nice', '好', 'جيد', 'جميل'],
            'FLOW': ['va', 'vient', 'go', 'come', '去', '来', 'يذهب', 'يأتي'],
            'MODAL': ['veux', 'peut', 'want', 'can', '想', '能', 'أريد', 'يمكن'],
            'CAUSE': ['fait', 'crée', 'make', 'do', '做', '创造', 'يفعل', 'يصنع'],
            'ITER': ['encore', 'again', '再', 'مرة أخرى'],
            'DECIDE': ['choisit', 'choose', '选择', 'يختار']
        }
        
        results = {}
        total_detected = 0
        total_sentences = 0
        
        for language, sentences in self.preschool_corpus.items():
            detected_count = 0
            language_results = []
            
            for sentence in sentences:
                sentence_dhatus = []
                sentence_lower = sentence.lower()
                
                for dhatu, patterns in current_mapping.items():
                    for pattern in patterns:
                        if pattern.lower() in sentence_lower:
                            sentence_dhatus.append(dhatu)
                            break
                
                detected_count += len(sentence_dhatus)
                total_detected += len(sentence_dhatus)
                language_results.append({
                    'sentence': sentence,
                    'dhatus': sentence_dhatus,
                    'coverage': len(sentence_dhatus) > 0
                })
            
            total_sentences += len(sentences)
            
            results[language] = {
                'sentences': language_results,
                'coverage_rate': sum(1 for r in language_results if r['coverage']) / len(sentences) * 100,
                'avg_dhatus_per_sentence': detected_count / len(sentences)
            }
            
            print(f"   {language}: {results[language]['coverage_rate']:.1f}% couverture")
        
        overall_coverage = total_detected / total_sentences
        print(f"\n📊 Couverture globale: {overall_coverage:.1f} dhātu/phrase")
        
        return results
    
    def identify_missing_primitives(self) -> Dict:
        """Identification primitives manquantes critiques"""
        print("\n🧬 IDENTIFICATION PRIMITIVES MANQUANTES")
        
        # Analyse fréquence actions préscolaires manquantes
        missing_actions = defaultdict(int)
        
        for language, sentences in self.preschool_corpus.items():
            for sentence in sentences:
                sentence_lower = sentence.lower()
                
                # Recherche primitives préscolaires dans chaque phrase
                for primitive, patterns in self.preschool_primitives.items():
                    lang_key = {
                        'FRENCH': 'french',
                        'ENGLISH': 'english', 
                        'CHINESE': 'chinese',
                        'ARABIC': 'arabic'
                    }.get(language, 'french')
                    
                    if lang_key in patterns:
                        for pattern in patterns[lang_key]:
                            if pattern.lower() in sentence_lower:
                                missing_actions[primitive] += 1
                                break
        
        # Tri par fréquence
        sorted_missing = sorted(missing_actions.items(), key=lambda x: x[1], reverse=True)
        
        print("   Primitives manquantes par fréquence:")
        for primitive, count in sorted_missing[:10]:
            print(f"     {primitive}: {count} occurrences")
            
        return dict(sorted_missing)
    
    def explore_primitive_assemblies(self) -> Dict:
        """Exploration assemblages primitives composées"""
        print("\n🔧 EXPLORATION ASSEMBLAGES PRIMITIVES")
        
        # Règles d'assemblage candidates
        assembly_rules = {
            'EAT': {
                'components': ['CAUSE', 'RELATE', 'FLOW'],
                'description': 'CAUSE (action) + RELATE (bouche) + FLOW (nourriture vers intérieur)',
                'confidence': 0.9
            },
            
            'SLEEP': {
                'components': ['EXIST', 'RELATE', 'MODAL'],
                'description': 'EXIST (état) + RELATE (lit/lieu) + MODAL (besoin)',
                'confidence': 0.8
            },
            
            'PLAY': {
                'components': ['CAUSE', 'EVAL', 'ITER'],
                'description': 'CAUSE (action) + EVAL (plaisir) + ITER (répétition)',
                'confidence': 0.7
            },
            
            'WASH': {
                'components': ['CAUSE', 'FLOW', 'RELATE'],
                'description': 'CAUSE (action) + FLOW (eau) + RELATE (corps)',
                'confidence': 0.85
            },
            
            'HAPPY': {
                'components': ['EVAL', 'EXIST'],
                'description': 'EVAL (positif) + EXIST (état émotionnel)',
                'confidence': 0.9
            },
            
            'SAD': {
                'components': ['EVAL', 'EXIST', 'FLOW'],
                'description': 'EVAL (négatif) + EXIST (état) + FLOW (larmes)',
                'confidence': 0.85
            },
            
            'WEAR': {
                'components': ['CAUSE', 'RELATE'],
                'description': 'CAUSE (action mettre) + RELATE (vêtement sur corps)',
                'confidence': 0.8
            },
            
            'LOOK': {
                'components': ['RELATE', 'FLOW'],
                'description': 'RELATE (direction regard) + FLOW (information visuelle)',
                'confidence': 0.75
            },
            
            'HUNGRY': {
                'components': ['MODAL', 'EAT'],
                'description': 'MODAL (besoin) + EAT (nourriture) - Circulaire!',
                'confidence': 0.6
            },
            
            'FAST': {
                'components': ['FLOW', 'EVAL'],
                'description': 'FLOW (mouvement) + EVAL (intensité élevée)',
                'confidence': 0.8
            }
        }
        
        print("   Assemblages analysés:")
        reducible_count = 0
        
        for primitive, rule in assembly_rules.items():
            components = rule['components']
            description = rule['description']
            confidence = rule['confidence']
            
            # Vérification circularité
            circular = any(comp not in self.current_dhatus for comp in components)
            
            if not circular and confidence > 0.7:
                reducible_count += 1
                status = "✅ RÉDUCTIBLE"
            else:
                status = "❌ PRIMITIF"
                
            print(f"     {primitive}: {components} ({confidence:.1f}) - {status}")
            print(f"       → {description}")
        
        print(f"\n📊 Réductions possibles: {reducible_count}/{len(assembly_rules)}")
        
        return assembly_rules
    
    def test_preschool_coverage_with_primitives(self, include_assemblies=True) -> Dict:
        """Test couverture avec nouvelles primitives"""
        print(f"\n🧪 TEST COUVERTURE AVEC PRIMITIVES {'+ ASSEMBLAGES' if include_assemblies else 'BRUTES'}")
        
        # Dhātu étendus
        extended_dhatus = self.current_dhatus.copy()
        
        if include_assemblies:
            # Ajout primitives non-réductibles seulement
            irreducible = {'FAMILY', 'HUNGRY'}  # Exemples
            extended_dhatus.update(irreducible)
        else:
            # Ajout toutes les primitives préscolaires
            extended_dhatus.update(self.preschool_primitives.keys())
        
        # Mapping étendu
        extended_mapping = {
            'EXIST': ['是', 'est', 'are', 'is', 'être', 'avoir', 'il y a', 'there', 'موجود', 'يوجد'],
            'RELATE': ['dans', 'avec', 'sur', 'in', 'with', 'at', '在', '和', 'في', 'مع'],
            'COMM': ['dit', 'parle', 'says', 'talk', 'tell', '说', '讲', 'يقول', 'يتكلم'],
            'EVAL': ['bon', 'beau', 'good', 'nice', '好', 'جيد', 'جميل'],
            'FLOW': ['va', 'vient', 'go', 'come', '去', '来', 'يذهب', 'يأتي'],
            'MODAL': ['veux', 'peut', 'want', 'can', '想', '能', 'أريد', 'يمكن'],
            'CAUSE': ['fait', 'crée', 'make', 'do', '做', '创造', 'يفعل', 'يصنع'],
            'ITER': ['encore', 'again', '再', 'مرة أخرى'],
            'DECIDE': ['choisit', 'choose', '选择', 'يختار']
        }
        
        # Ajout mappings primitives préscolaires
        for primitive, patterns in self.preschool_primitives.items():
            if primitive in extended_dhatus:
                combined_patterns = []
                for lang_patterns in patterns.values():
                    combined_patterns.extend(lang_patterns)
                extended_mapping[primitive] = combined_patterns
        
        results = {}
        total_coverage = 0
        
        for language, sentences in self.preschool_corpus.items():
            covered_sentences = 0
            
            for sentence in sentences:
                sentence_dhatus = []
                sentence_lower = sentence.lower()
                
                for dhatu, patterns in extended_mapping.items():
                    for pattern in patterns:
                        if pattern.lower() in sentence_lower:
                            sentence_dhatus.append(dhatu)
                            break
                
                if sentence_dhatus:
                    covered_sentences += 1
            
            coverage_rate = covered_sentences / len(sentences) * 100
            total_coverage += coverage_rate
            
            results[language] = coverage_rate
            print(f"   {language}: {coverage_rate:.1f}% couverture")
        
        average_coverage = total_coverage / len(self.preschool_corpus)
        print(f"\n🎯 Couverture moyenne: {average_coverage:.1f}%")
        
        return {
            'by_language': results,
            'average': average_coverage,
            'dhatu_count': len(extended_dhatus)
        }
    
    def generate_preschool_primitives_report(self) -> str:
        """Génération rapport complet"""
        print("\n📄 GÉNÉRATION RAPPORT PRIMITIVES PRÉSCOLAIRES")
        
        report_path = Path("data/references_cache/RAPPORT_PRIMITIVES_PRESCOLAIRE_v0.0.1.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Analyse complète
        current_coverage = self.analyze_coverage_current_dhatus()
        missing_primitives = self.identify_missing_primitives()
        assemblies = self.explore_primitive_assemblies()
        coverage_brute = self.test_preschool_coverage_with_primitives(include_assemblies=False)
        coverage_assemblies = self.test_preschool_coverage_with_primitives(include_assemblies=True)
        
        report_content = f"""# 🧸 RAPPORT PRIMITIVES PRÉSCOLAIRES v0.0.1

## 🎯 **Objectif: 100% Couverture Dialogues Préscolaires**

### **Corpus Analysé**
- **4 langues**: Français, Anglais, Chinois, Arabe
- **80 phrases**: 20 par langue (dialogues typiques préscolaires)
- **Thèmes**: Actions quotidiennes, émotions, famille, jeu

## 📊 **Couverture Actuelle (9 Dhātu)**

### **Performance par Langue**
- **Français**: {current_coverage['FRENCH']['coverage_rate']:.1f}% 
- **Anglais**: {current_coverage['ENGLISH']['coverage_rate']:.1f}%
- **Chinois**: {current_coverage['CHINESE']['coverage_rate']:.1f}%
- **Arabe**: {current_coverage['ARABIC']['coverage_rate']:.1f}%

**Insuffisant pour niveau préscolaire!**

## 🧬 **Primitives Manquantes Identifiées**

### **Top 10 Primitives Critiques**
{chr(10).join(f"- **{prim}**: {count} occurrences" for prim, count in list(missing_primitives.items())[:10])}

### **Catégories Manquantes**
1. **Actions corporelles**: EAT, SLEEP, WASH, WEAR
2. **Émotions de base**: HAPPY, SAD  
3. **Actions quotidiennes**: PLAY, LOOK
4. **Relations familiales**: FAMILY
5. **Sensations**: HUNGRY, FAST

## 🔧 **Exploration Assemblages**

### **Primitives Réductibles via Assemblages**
{chr(10).join(f"- **{prim}**: {rule['components']} (conf: {rule['confidence']:.1f})" 
             for prim, rule in assemblies.items() 
             if rule['confidence'] > 0.7 and all(comp in self.current_dhatus for comp in rule['components']))}

### **Primitives Irréductibles** 
{chr(10).join(f"- **{prim}**: {rule['description']}" 
             for prim, rule in assemblies.items() 
             if rule['confidence'] <= 0.7 or any(comp not in self.current_dhatus for comp in rule['components']))}

## 📈 **Projections Couverture**

### **Avec Toutes Primitives** ({coverage_brute['dhatu_count']} dhātu)
- **Couverture moyenne**: {coverage_brute['average']:.1f}%
{chr(10).join(f"- {lang}: {cov:.1f}%" for lang, cov in coverage_brute['by_language'].items())}

### **Avec Assemblages Optimisés** ({coverage_assemblies['dhatu_count']} dhātu)
- **Couverture moyenne**: {coverage_assemblies['average']:.1f}%
{chr(10).join(f"- {lang}: {cov:.1f}%" for lang, cov in coverage_assemblies['by_language'].items())}

## 🎯 **Recommandations**

### **Stratégie Tableau Périodique Optimisé**
1. **Conserver 9 dhātu de base** (universels validés)
2. **Ajouter 3-5 primitives irréductibles** pour préscolaire
3. **Implémenter assemblages** pour primitives complexes
4. **Validation 100%** sur corpus étendu

### **Primitives Prioritaires à Ajouter**
1. **EAT** (si non-réductible après test)
2. **FAMILY** (concepts relationnels spécifiques)
3. **HUNGRY** (sensation physiologique de base)

### **Assemblages à Implémenter**
1. **PLAY** = CAUSE + EVAL + ITER
2. **WASH** = CAUSE + FLOW + RELATE  
3. **HAPPY** = EVAL + EXIST

---

**Prochaine étape**: Implémentation assemblages et test 100% préscolaire

---
*Rapport généré - {__import__('time').strftime('%d/%m/%Y %H:%M')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        return str(report_path)

def run_preschool_primitives_analysis():
    """Analyse complète primitives préscolaires"""
    print("🧸 ANALYSE PRIMITIVES PRÉSCOLAIRES MULTILINGUES")
    print("=" * 80)
    
    analyzer = PreschoolCorpusAnalyzer()
    
    # Analyse complète
    report_path = analyzer.generate_preschool_primitives_report()
    
    print(f"\n📄 Rapport complet: {report_path}")
    print("\n✅ ANALYSE PRIMITIVES PRÉSCOLAIRES TERMINÉE!")

if __name__ == "__main__":
    run_preschool_primitives_analysis()
