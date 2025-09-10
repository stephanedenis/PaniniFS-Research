#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation Phase 1 : Extension Multi-Scripts pour Corpus Multilingue
Solution immédiate aux gaps identifiés (coverage 0% → 30-50%)
"""

import json
import os
import unicodedata
from collections import defaultdict, Counter

class MultilingualDhatuAnalyzer:
    """Analyseur dhātu multilingue avec support scripts non-latins"""
    
    def __init__(self):
        self.dhatu_multilingual = {
            'EXIST': {
                'latin': ['is', 'am', 'are', 'être', 'est', 'sein', 'ist', 'ser', 'estar', 'zijn', 'on', 'sono'],
                'arabic': ['يكون', 'كان', 'هو', 'هي', 'يوجد', 'في', 'كائن'],
                'chinese': ['是', '有', '在', '存在', '为', '乃'],
                'devanagari': ['है', 'हैं', 'था', 'होना', 'अस्ति'],
                'hebrew': ['הוא', 'היא', 'יש', 'קיים', 'נמצא'],
                'japanese': ['だ', 'です', 'ある', 'いる', 'である'],
                'korean': ['이다', '있다', '존재하다', '되다']
            },
            'RELATE': {
                'latin': ['in', 'on', 'at', 'dans', 'sur', 'avec', 'in', 'auf', 'an', 'en', 'sobre', 'con', 'di', 'su'],
                'arabic': ['في', 'على', 'عند', 'مع', 'إلى', 'من', 'بين'],
                'chinese': ['在', '上', '里', '中', '的', '与', '和'],
                'devanagari': ['में', 'पर', 'के साथ', 'से', 'को'],
                'hebrew': ['ב', 'על', 'עם', 'אצל', 'של', 'אל'],
                'japanese': ['に', 'で', 'と', 'から', 'まで', 'の'],
                'korean': ['에', '에서', '와', '과', '의', '로']
            },
            'COMM': {
                'latin': ['say', 'tell', 'talk', 'speak', 'dire', 'parler', 'sagen', 'sprechen', 'decir', 'hablar'],
                'arabic': ['قال', 'يقول', 'تكلم', 'حديث', 'كلام'],
                'chinese': ['说', '讲', '话', '言', '谈'],
                'devanagari': ['कहना', 'बोलना', 'बात', 'कह'],
                'hebrew': ['אמר', 'דבר', 'מדבר', 'אמרה'],
                'japanese': ['言う', '話す', 'いう', 'はなす'],
                'korean': ['말하다', '이야기하다', '얘기']
            },
            'EVAL': {
                'latin': ['big', 'small', 'good', 'bad', 'grand', 'petit', 'bon', 'groß', 'klein', 'gut', 'grande'],
                'arabic': ['كبير', 'صغير', 'جيد', 'سيء', 'أكبر'],
                'chinese': ['大', '小', '好', '坏', '很'],
                'devanagari': ['बड़ा', 'छोटा', 'अच्छा', 'बुरा'],
                'hebrew': ['גדול', 'קטן', 'טוב', 'רע'],
                'japanese': ['大きい', '小さい', 'いい', '悪い'],
                'korean': ['크다', '작다', '좋다', '나쁘다']
            },
            'ITER': {
                'latin': ['more', 'again', 'encore', 'plus', 'wieder', 'mehr', 'más', 'otra vez', 'ancora'],
                'arabic': ['أكثر', 'مرة', 'ثانية', 'زيادة'],
                'chinese': ['更', '再', '又', '多'],
                'devanagari': ['फिर', 'और', 'अधिक'],
                'hebrew': ['עוד', 'שוב', 'יותר'],
                'japanese': ['また', 'もう', 'もっと'],
                'korean': ['더', '다시', '또']
            },
            'MODAL': {
                'latin': ['can', 'must', 'may', 'should', 'peut', 'doit', 'kann', 'muss', 'puede', 'debe'],
                'arabic': ['يمكن', 'يجب', 'ممكن', 'لازم'],
                'chinese': ['能', '可以', '应该', '必须'],
                'devanagari': ['सकना', 'चाहिए', 'होगा'],
                'hebrew': ['יכול', 'צריך', 'אפשר'],
                'japanese': ['できる', 'べき', 'かもしれない'],
                'korean': ['할 수 있다', '해야 하다', '아마']
            },
            'CAUSE': {
                'latin': ['make', 'do', 'cause', 'faire', 'machen', 'tun', 'hacer', 'causa'],
                'arabic': ['يفعل', 'سبب', 'عمل', 'صنع'],
                'chinese': ['做', '让', '使', '造成'],
                'devanagari': ['करना', 'बनाना', 'कारण'],
                'hebrew': ['עושה', 'גורם', 'עשה'],
                'japanese': ['する', 'させる', '作る'],
                'korean': ['하다', '만들다', '시키다']
            },
            'FLOW': {
                'latin': ['go', 'come', 'move', 'aller', 'venir', 'gehen', 'kommen', 'ir', 'venir', 'andare'],
                'arabic': ['يذهب', 'يأتي', 'حركة', 'ذهاب'],
                'chinese': ['去', '来', '走', '移动'],
                'devanagari': ['जाना', 'आना', 'चलना'],
                'hebrew': ['הולך', 'בא', 'זז'],
                'japanese': ['行く', '来る', '動く'],
                'korean': ['가다', '오다', '움직이다']
            },
            'DECIDE': {
                'latin': ['choose', 'pick', 'want', 'decide', 'choisir', 'vouloir', 'wählen', 'wollen', 'elegir'],
                'arabic': ['يختار', 'يريد', 'قرار', 'اختيار'],
                'chinese': ['选择', '要', '决定', '想'],
                'devanagari': ['चुनना', 'चाहना', 'फैसला'],
                'hebrew': ['בוחר', 'רוצה', 'החליט'],
                'japanese': ['選ぶ', 'ほしい', '決める'],
                'korean': ['선택하다', '원하다', '결정하다']
            }
        }
        
        # Mapping des scripts Unicode vers nos catégories
        self.script_mapping = {
            'ARABIC': 'arabic',
            'HAN': 'chinese',
            'HIRAGANA': 'japanese',
            'KATAKANA': 'japanese',
            'DEVANAGARI': 'devanagari',
            'HEBREW': 'hebrew',
            'HANGUL': 'korean',
            'LATIN': 'latin'
        }
    
    def detect_script(self, text):
        """Détecte le script principal du texte"""
        scripts = defaultdict(int)
        for char in text:
            if char.isalpha():
                try:
                    script = unicodedata.name(char).split()[0]
                    scripts[script] += 1
                except ValueError:
                    continue
        
        if not scripts:
            return 'latin'
        
        main_script = max(scripts.items(), key=lambda x: x[1])[0]
        return self.script_mapping.get(main_script, 'latin')
    
    def get_dhatu_keywords(self, dhatu, script):
        """Retourne keywords appropriés selon script détecté"""
        return self.dhatu_multilingual.get(dhatu, {}).get(script, [])
    
    def analyze_sentence_multilingual(self, sentence, language_hint=None):
        """Analyse multilingue d'une phrase"""
        # Détecter script automatiquement ou utiliser hint
        if language_hint:
            script = self.get_script_from_language(language_hint)
        else:
            script = self.detect_script(sentence)
        
        sentence_lower = sentence.lower()
        dhatu_counts = Counter()
        
        # Pour chaque dhātu, chercher ses keywords dans le script approprié
        for dhatu in self.dhatu_multilingual.keys():
            keywords = self.get_dhatu_keywords(dhatu, script)
            for keyword in keywords:
                if keyword in sentence_lower:
                    dhatu_counts[dhatu] += 1
        
        return {
            'detected_script': script,
            'dhatu_usage': dict(dhatu_counts),
            'total_dhatu': sum(dhatu_counts.values()),
            'coverage': len(dhatu_counts) / 9  # 9 dhātu total
        }
    
    def get_script_from_language(self, lang_code):
        """Mapping codes langue vers scripts"""
        lang_script_map = {
            'arb': 'arabic', 'ar': 'arabic',
            'cmn': 'chinese', 'zh': 'chinese',
            'heb': 'hebrew', 'he': 'hebrew',
            'hin': 'devanagari', 'hi': 'devanagari',
            'jpn': 'japanese', 'ja': 'japanese',
            'kor': 'korean', 'ko': 'korean'
        }
        return lang_script_map.get(lang_code, 'latin')

def test_multilingual_improvements():
    """Test des améliorations sur phrases problématiques"""
    
    analyzer = MultilingualDhatuAnalyzer()
    
    test_cases = [
        # Cas qui échouaient avant (0% coverage)
        {'text': 'القطة في البيت', 'lang': 'arb', 'description': 'Arabe: Chat dans maison'},
        {'text': '猫在房子里', 'lang': 'cmn', 'description': 'Chinois: Chat dans maison'},
        {'text': 'החתול בבית', 'lang': 'heb', 'description': 'Hébreu: Chat dans maison'},
        {'text': 'बिल्ली घर में है', 'lang': 'hin', 'description': 'Hindi: Chat dans maison'},
        {'text': '猫は家にいます', 'lang': 'jpn', 'description': 'Japonais: Chat dans maison'},
        {'text': '고양이는 집에 있다', 'lang': 'kor', 'description': 'Coréen: Chat dans maison'},
        
        # Cas de contrôle (déjà bons)
        {'text': 'The cat is in the house', 'lang': 'en', 'description': 'Anglais: Chat dans maison'},
        {'text': 'Le chat est dans la maison', 'lang': 'fr', 'description': 'Français: Chat dans maison'}
    ]
    
    print("🧪 TEST AMÉLIORATIONS MULTILINGUES")
    print("=" * 50)
    
    for case in test_cases:
        result = analyzer.analyze_sentence_multilingual(case['text'], case['lang'])
        
        print(f"\n📝 {case['description']}")
        print(f"   Texte: {case['text']}")
        print(f"   Script détecté: {result['detected_script']}")
        print(f"   Coverage: {result['coverage']:.1%}")
        print(f"   Dhātu détectés: {result['dhatu_usage']}")
        print(f"   Total dhātu: {result['total_dhatu']}")

def update_existing_corpus_analysis():
    """Met à jour l'analyse du corpus avec le nouveau système"""
    
    analyzer = MultilingualDhatuAnalyzer()
    experiments_path = "/home/stephane/GitHub/PaniniFS-Research/experiments/dhatu"
    
    # Langues à tester
    languages = ['arb', 'cmn', 'heb', 'hin', 'jpn', 'kor']
    
    results = {}
    
    print("\n🔄 MISE À JOUR ANALYSE CORPUS")
    print("=" * 40)
    
    for lang in languages:
        # Charger données existantes
        file_path = os.path.join(experiments_path, "prompts_child", f"{lang}.json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'items' not in data:
                print(f"❌ {lang}: Pas de données 'items'")
                continue
            
            total_sentences = len(data['items'])
            total_coverage = 0
            global_dhatu = Counter()
            
            # Analyser chaque phrase avec nouveau système
            for item in data['items']:
                sentence = item.get('text', '')
                if sentence:
                    result = analyzer.analyze_sentence_multilingual(sentence, lang)
                    total_coverage += result['coverage']
                    
                    for dhatu, count in result['dhatu_usage'].items():
                        global_dhatu[dhatu] += count
            
            avg_coverage = total_coverage / total_sentences if total_sentences > 0 else 0
            
            results[lang] = {
                'avg_coverage': avg_coverage,
                'total_sentences': total_sentences,
                'dhatu_usage': dict(global_dhatu),
                'improvement': avg_coverage  # Comparé à 0% avant
            }
            
            print(f"✅ {lang.upper()}: {avg_coverage:.1%} coverage ({total_sentences} phrases)")
            if global_dhatu:
                top_dhatu = global_dhatu.most_common(3)
                print(f"   Top dhātu: {top_dhatu}")
        
        except FileNotFoundError:
            print(f"❌ {lang}: Fichier non trouvé")
        except Exception as e:
            print(f"❌ {lang}: Erreur {e}")
    
    return results

def generate_improvement_report(results):
    """Génère rapport d'amélioration"""
    
    report_content = f"""# 📈 RAPPORT D'AMÉLIORATION : Extension Multilingue Phase 1

*Résultats après implémentation détecteur multi-scripts*

## 🎯 **Améliorations Mesurées**

### **Avant vs Après (Coverage %)**

| Langue | Famille | Avant | Après | Amélioration | Status |
|--------|---------|-------|-------|--------------|--------|
"""
    
    for lang, data in results.items():
        lang_names = {
            'arb': 'Arabe',
            'cmn': 'Chinois', 
            'heb': 'Hébreu',
            'hin': 'Hindi',
            'jpn': 'Japonais',
            'kor': 'Coréen'
        }
        
        families = {
            'arb': 'Afro-Asiatique',
            'cmn': 'Sino-Tibétaine',
            'heb': 'Afro-Asiatique', 
            'hin': 'Indo-Européenne',
            'jpn': 'Altaïque',
            'kor': 'Altaïque'
        }
        
        lang_name = lang_names.get(lang, lang)
        family = families.get(lang, 'Autre')
        before = 0.0
        after = data['avg_coverage']
        improvement = after - before
        
        status = "🚀 Succès" if after > 0.2 else "⚠️ Partiel" if after > 0.05 else "❌ Échec"
        
        report_content += f"| {lang_name} | {family} | {before:.1%} | {after:.1%} | +{improvement:.1%} | {status} |\n"
    
    # Calculs globaux
    total_improvement = sum(r['avg_coverage'] for r in results.values()) / len(results)
    
    report_content += f"""
## 📊 **Statistiques Globales**

- **Coverage moyenne** : 0.0% → {total_improvement:.1%}
- **Langues améliorées** : {sum(1 for r in results.values() if r['avg_coverage'] > 0.05)}/{len(results)}
- **Meilleure performance** : {max(results.items(), key=lambda x: x[1]['avg_coverage'])[0].upper()} ({max(r['avg_coverage'] for r in results.values()):.1%})

## 🧬 **Dhātu les Plus Détectés**

"""
    
    # Agréger usage dhātu global
    global_dhatu_usage = Counter()
    for data in results.values():
        for dhatu, count in data['dhatu_usage'].items():
            global_dhatu_usage[dhatu] += count
    
    for dhatu, count in global_dhatu_usage.most_common():
        lang_count = sum(1 for r in results.values() if dhatu in r['dhatu_usage'])
        universality = lang_count / len(results) * 100
        report_content += f"- **{dhatu}** : {count} occurrences, {lang_count}/{len(results)} langues ({universality:.0f}%)\n"
    
    report_content += f"""
## 🎯 **Évaluation Phase 1**

### **✅ Succès**
- Détection automatique scripts Unicode
- Keywords multilingues opérationnels
- Amélioration mesurable langues problématiques

### **⚠️ Limitations Persistantes**
- Algorithme keywords simple (pas d'analyse morphologique)
- Couverture encore faible (<30% pour la plupart)
- Manque validation linguistes natifs

### **🚀 Prochaines Étapes**
1. **Phase 2** : Analyseur morphologique (racines sémitiques, agglutination)
2. **Validation humaine** : Échantillons contrôlés par linguistes
3. **Corpus étendus** : Plus de phrases par langue

---

*Rapport généré automatiquement - {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}*
"""
    
    return report_content

def main():
    """Fonction principale de test"""
    
    print("🚀 DÉMARRAGE SOLUTION PHASE 1 : Extension Multilingue")
    print("=" * 60)
    
    # Test améliorations
    test_multilingual_improvements()
    
    # Analyse corpus mis à jour
    results = update_existing_corpus_analysis()
    
    # Générer rapport
    if results:
        report = generate_improvement_report(results)
        
        # Sauvegarder rapport
        output_path = "/home/stephane/GitHub/PaniniFS-Research/data/references_cache/RAPPORT_AMELIORATION_PHASE1.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Rapport d'amélioration généré: {output_path}")
    
    print("\n✅ Solution Phase 1 terminée!")

if __name__ == "__main__":
    main()
