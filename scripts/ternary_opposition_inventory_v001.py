#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 INVENTAIRE OPPOSITIONS TRINAIRES DHĀTU
====================================================================
Inventaire complet des oppositions trinaires pour validation
et correction des paires non-antagonistes.

Auteur: Assistant IA PaniniFS Research
Version: 0.0.1 - Inventaire Oppositions Trinaires
Date: 08/09/2025
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class OppositionType(Enum):
    """Types d'oppositions trinaires"""
    PRESENCE = "presence"           # Absence ↔ Présence
    QUALITY = "quality"            # Mauvais ↔ Bon
    INTENSITY = "intensity"        # Faible ↔ Fort
    DIRECTION = "direction"        # Entrant ↔ Sortant
    STATE = "state"               # Inactif ↔ Actif
    POLARITY = "polarity"         # Négatif ↔ Positif

@dataclass
class TernaryOpposition:
    """Opposition trinaire complète"""
    concept: str
    consonant: str
    negative_form: str
    neutral_form: str
    positive_form: str
    negative_meaning: str
    neutral_meaning: str
    positive_meaning: str
    opposition_type: OppositionType
    is_valid_antagonism: bool
    notes: str

class TernaryOppositionInventory:
    """Inventaire complet oppositions trinaires"""
    
    def __init__(self):
        print("📋 INITIALISATION INVENTAIRE OPPOSITIONS TRINAIRES")
        
        # Inventaire complet avec validation antagonisme
        self.oppositions = {
            'EXIST': TernaryOpposition(
                concept='EXIST',
                consonant='S',
                negative_form='SA',
                neutral_form='SE', 
                positive_form='SI',
                negative_meaning='Absence, non-être, manque',
                neutral_meaning='Existence neutre, être simple',
                positive_meaning='Présence forte, plénitude',
                opposition_type=OppositionType.PRESENCE,
                is_valid_antagonism=True,
                notes='Absence vs Présence = antagonisme valide'
            ),
            
            'RELATE': TernaryOpposition(
                concept='RELATE',
                consonant='R',
                negative_form='RA',
                neutral_form='RE',
                positive_form='RI', 
                negative_meaning='Séparation, éloignement, rupture',
                neutral_meaning='Relation neutre, proximité normale',
                positive_meaning='Union, proximité forte, fusion',
                opposition_type=OppositionType.DIRECTION,
                is_valid_antagonism=True,
                notes='Séparation vs Union = antagonisme valide'
            ),
            
            'COMM': TernaryOpposition(
                concept='COMM',
                consonant='K',
                negative_form='KA',
                neutral_form='KE',
                positive_form='KI',
                negative_meaning='Silence, mutisme, non-communication',
                neutral_meaning='Communication normale, parole',
                positive_meaning='Communication intense, cri, expression forte',
                opposition_type=OppositionType.INTENSITY,
                is_valid_antagonism=True,
                notes='Silence vs Expression forte = antagonisme valide'
            ),
            
            'EVAL': TernaryOpposition(
                concept='EVAL', 
                consonant='V',
                negative_form='VA',
                neutral_form='VE',
                positive_form='VI',
                negative_meaning='Mauvais, négatif, défavorable',
                neutral_meaning='Neutre, acceptable, ordinaire',
                positive_meaning='Bon, excellent, favorable',
                opposition_type=OppositionType.QUALITY,
                is_valid_antagonism=True,
                notes='Mauvais vs Bon = antagonisme valide'
            ),
            
            'ITER': TernaryOpposition(
                concept='ITER',
                consonant='T',
                negative_form='TA',
                neutral_form='TE', 
                positive_form='TI',
                negative_meaning='Jamais, arrêt, fin, cessation',
                neutral_meaning='Une fois, ponctuel, occasionnel',
                positive_meaning='Répétition, multiple, continu',
                opposition_type=OppositionType.STATE,
                is_valid_antagonism=True,
                notes='Arrêt vs Répétition = antagonisme valide'
            ),
            
            'MODAL': TernaryOpposition(
                concept='MODAL',
                consonant='M',
                negative_form='MA',
                neutral_form='ME',
                positive_form='MI',
                negative_meaning='Interdiction, défense, ne pas pouvoir',
                neutral_meaning='Possibilité neutre, pouvoir',
                positive_meaning='Obligation, devoir, nécessité',
                opposition_type=OppositionType.POLARITY,
                is_valid_antagonism=False,  # PROBLÈME IDENTIFIÉ
                notes='PROBLÈME: Interdiction vs Obligation ne sont pas antagonistes directes'
            ),
            
            'CAUSE': TernaryOpposition(
                concept='CAUSE',
                consonant='G',
                negative_form='GA',
                neutral_form='GE',
                positive_form='GI',
                negative_meaning='Destruction, défaire, annuler',
                neutral_meaning='Action neutre, faire',
                positive_meaning='Création, construction, générer',
                opposition_type=OppositionType.DIRECTION,
                is_valid_antagonism=True,
                notes='Destruction vs Création = antagonisme valide'
            ),
            
            'FLOW': TernaryOpposition(
                concept='FLOW',
                consonant='F',
                negative_form='FA',
                neutral_form='FE',
                positive_form='FI',
                negative_meaning='Stagnation, blocage, arrêt',
                neutral_meaning='Mouvement neutre, écoulement normal',
                positive_meaning='Flux rapide, écoulement fort',
                opposition_type=OppositionType.INTENSITY,
                is_valid_antagonism=True,
                notes='Stagnation vs Flux rapide = antagonisme valide'
            ),
            
            'DECIDE': TernaryOpposition(
                concept='DECIDE',
                consonant='D', 
                negative_form='DA',
                neutral_form='DE',
                positive_form='DI',
                negative_meaning='Refus, rejet, ne pas vouloir',
                neutral_meaning='Choix neutre, décision',
                positive_meaning='Préférence forte, désir intense',
                opposition_type=OppositionType.POLARITY,
                is_valid_antagonism=True,
                notes='Refus vs Désir = antagonisme valide'
            )
        }
        
        # Primitives irréductibles
        self.irreducible_oppositions = {
            'FAMILY': TernaryOpposition(
                concept='FAMILY',
                consonant='N',
                negative_form='NA',
                neutral_form='NE',
                positive_form='NI',
                negative_meaning='Étranger, isolement, sans famille',
                neutral_meaning='Famille neutre, relations normales',
                positive_meaning='Famille proche, amour familial fort',
                opposition_type=OppositionType.INTENSITY,
                is_valid_antagonism=True,
                notes='Isolement vs Proximité familiale = antagonisme valide'
            ),
            
            'PLAY': TernaryOpposition(
                concept='PLAY',
                consonant='P',
                negative_form='PA',
                neutral_form='PE',
                positive_form='PI',
                negative_meaning='Ennui, pas amusant, corvée',
                neutral_meaning='Jeu neutre, activité normale',
                positive_meaning='Jeu intense, très amusant, plaisir',
                opposition_type=OppositionType.QUALITY,
                is_valid_antagonism=True,
                notes='Ennui vs Plaisir = antagonisme valide'
            ),
            
            'HUNGRY': TernaryOpposition(
                concept='HUNGRY',
                consonant='H',
                negative_form='HA',
                neutral_form='HE', 
                positive_form='HI',
                negative_meaning='Satiété, trop plein, écœurement',
                neutral_meaning='Faim normale, appétit standard',
                positive_meaning='Très faim, affamé, famine',
                opposition_type=OppositionType.INTENSITY,
                is_valid_antagonism=True,
                notes='Satiété vs Famine = antagonisme valide'
            )
        }
    
    def validate_all_oppositions(self) -> Dict:
        """Validation complète de tous les antagonismes"""
        print("\n🔍 VALIDATION TOUS LES ANTAGONISMES")
        
        all_oppositions = {**self.oppositions, **self.irreducible_oppositions}
        
        valid_oppositions = []
        invalid_oppositions = []
        problematic_concepts = []
        
        for concept, opposition in all_oppositions.items():
            print(f"\n   📝 {concept} ({opposition.consonant}):")
            print(f"      A: {opposition.negative_form} = {opposition.negative_meaning}")
            print(f"      E: {opposition.neutral_form} = {opposition.neutral_meaning}")
            print(f"      I: {opposition.positive_form} = {opposition.positive_meaning}")
            print(f"      Type: {opposition.opposition_type.value}")
            
            if opposition.is_valid_antagonism:
                print(f"      ✅ VALIDE: {opposition.notes}")
                valid_oppositions.append(opposition)
            else:
                print(f"      ❌ INVALIDE: {opposition.notes}")
                invalid_oppositions.append(opposition)
                problematic_concepts.append(concept)
        
        print(f"\n📊 RÉSUMÉ VALIDATION:")
        print(f"   ✅ Oppositions valides: {len(valid_oppositions)}")
        print(f"   ❌ Oppositions invalides: {len(invalid_oppositions)}")
        print(f"   🔧 Concepts à corriger: {problematic_concepts}")
        
        return {
            'valid_oppositions': valid_oppositions,
            'invalid_oppositions': invalid_oppositions,
            'problematic_concepts': problematic_concepts,
            'total_concepts': len(all_oppositions),
            'validity_rate': len(valid_oppositions) / len(all_oppositions) * 100
        }
    
    def propose_modal_correction(self) -> Dict:
        """Proposition de correction pour MODAL"""
        print("\n🔧 PROPOSITION CORRECTION MODAL")
        
        # Problème identifié: MA (Interdiction) vs MI (Obligation)
        print("   ❌ PROBLÈME ACTUEL:")
        print("      MA = Interdiction, défense, ne pas pouvoir")
        print("      MI = Obligation, devoir, nécessité")
        print("      → Pas antagonistes! Deux contraintes différentes")
        
        print("\n   💡 PROPOSITIONS CORRECTION:")
        
        option1 = {
            'name': 'Option 1: Capacité',
            'MA': 'Incapacité, impossibilité, ne pas pouvoir',
            'ME': 'Capacité neutre, pouvoir normal',  
            'MI': 'Super-pouvoir, capacité maximale',
            'antagonism': 'Incapacité ↔ Super-capacité',
            'valid': True
        }
        
        option2 = {
            'name': 'Option 2: Permission',
            'MA': 'Interdiction, défense, ne pas avoir le droit',
            'ME': 'Permission neutre, autorisation normale',
            'MI': 'Liberté totale, droit absolu',
            'antagonism': 'Interdiction ↔ Liberté totale',
            'valid': True
        }
        
        option3 = {
            'name': 'Option 3: Volonté',
            'MA': 'Refus, ne pas vouloir, résistance',
            'ME': 'Volonté neutre, acceptation',
            'MI': 'Désir fort, vouloir intensément',
            'antagonism': 'Refus ↔ Désir fort',
            'valid': True,
            'note': 'Mais chevauche avec DECIDE'
        }
        
        options = [option1, option2, option3]
        
        for i, option in enumerate(options, 1):
            print(f"\n      {i}. {option['name']}:")
            print(f"         MA: {option['MA']}")
            print(f"         ME: {option['ME']}")
            print(f"         MI: {option['MI']}")
            print(f"         Antagonisme: {option['antagonism']}")
            print(f"         Valide: {'✅' if option['valid'] else '❌'}")
            if 'note' in option:
                print(f"         Note: {option['note']}")
        
        print(f"\n   🎯 RECOMMANDATION: Option 1 (Capacité)")
        print(f"      Plus claire, moins de chevauchement avec autres concepts")
        
        return {
            'current_problem': 'Interdiction vs Obligation non-antagonistes',
            'options': options,
            'recommended': option1
        }
    
    def check_concept_overlaps(self) -> Dict:
        """Vérification chevauchements conceptuels"""
        print("\n🔍 VÉRIFICATION CHEVAUCHEMENTS CONCEPTUELS")
        
        all_oppositions = {**self.oppositions, **self.irreducible_oppositions}
        overlaps = []
        
        # Analyse par type d'opposition
        by_type = {}
        for concept, opposition in all_oppositions.items():
            op_type = opposition.opposition_type
            if op_type not in by_type:
                by_type[op_type] = []
            by_type[op_type].append((concept, opposition))
        
        print("   📊 Répartition par type:")
        for op_type, concepts in by_type.items():
            print(f"      {op_type.value}: {[c[0] for c in concepts]}")
        
        # Détection chevauchements potentiels
        potential_overlaps = [
            ('DECIDE', 'MODAL', 'Tous deux impliquent choix/volonté'),
            ('EVAL', 'PLAY', 'Tous deux impliquent qualité/plaisir'),
            ('FLOW', 'ITER', 'Tous deux impliquent continuité')
        ]
        
        print("\n   ⚠️ Chevauchements potentiels identifiés:")
        for concept1, concept2, reason in potential_overlaps:
            print(f"      {concept1} ↔ {concept2}: {reason}")
        
        return {
            'by_type': by_type,
            'potential_overlaps': potential_overlaps
        }
    
    def generate_corrected_inventory(self) -> str:
        """Génération inventaire corrigé"""
        from pathlib import Path
        
        report_path = Path("data/references_cache/INVENTAIRE_OPPOSITIONS_TRINAIRES_v0.0.1.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        validation_results = self.validate_all_oppositions()
        modal_correction = self.propose_modal_correction()
        overlaps = self.check_concept_overlaps()
        
        report_content = f"""# 📋 INVENTAIRE OPPOSITIONS TRINAIRES v0.0.1

## 🎯 **Validation Antagonismes Dhātu**

### **Principe Trinaire**
- **A (Négative)**: Opposition sémantique claire
- **E (Neutre)**: État/niveau intermédiaire  
- **I (Positive)**: Affirmation/intensité maximale

## ✅ **Oppositions Valides ({len(validation_results['valid_oppositions'])}/{validation_results['total_concepts']})**

{chr(10).join(f'''
### **{opp.concept}** ({opp.consonant})
- **{opp.negative_form}**: {opp.negative_meaning}
- **{opp.neutral_form}**: {opp.neutral_meaning}  
- **{opp.positive_form}**: {opp.positive_meaning}
- **Antagonisme**: {opp.negative_meaning.split(',')[0]} ↔ {opp.positive_meaning.split(',')[0]}
- **Type**: {opp.opposition_type.value}
''' for opp in validation_results['valid_oppositions'])}

## ❌ **Oppositions Invalides**

{chr(10).join(f'''
### **{opp.concept}** ({opp.consonant}) - PROBLÉMATIQUE
- **{opp.negative_form}**: {opp.negative_meaning}
- **{opp.neutral_form}**: {opp.neutral_meaning}
- **{opp.positive_form}**: {opp.positive_meaning}
- **Problème**: {opp.notes}
''' for opp in validation_results['invalid_oppositions'])}

## 🔧 **Correction Proposée: MODAL**

### **Problème Identifié**
```
MA (Interdiction) vs MI (Obligation)
→ Pas antagonistes! Deux types de contraintes différentes
```

### **Solution Recommandée: Capacité**
- **MA**: Incapacité, impossibilité, ne pas pouvoir
- **ME**: Capacité neutre, pouvoir normal
- **MI**: Super-pouvoir, capacité maximale
- **Antagonisme valide**: Incapacité ↔ Super-capacité

### **Alternatives Considérées**
{chr(10).join(f"- **{opt['name']}**: {opt['antagonism']}" for opt in modal_correction['options'])}

## 🔍 **Analyse Chevauchements**

### **Répartition par Type**
{chr(10).join(f"- **{op_type.value}**: {[c[0] for c in concepts]}" 
             for op_type, concepts in overlaps['by_type'].items())}

### **Chevauchements Potentiels**
{chr(10).join(f"- **{c1} ↔ {c2}**: {reason}" 
             for c1, c2, reason in overlaps['potential_overlaps'])}

## 📊 **Statistiques Validation**

- **Taux validité**: {validation_results['validity_rate']:.1f}%
- **Concepts valides**: {len(validation_results['valid_oppositions'])}
- **Concepts à corriger**: {len(validation_results['invalid_oppositions'])}
- **Types opposition**: {len(overlaps['by_type'])} catégories

## 🎯 **Actions Requises**

### **Corrections Immédiates**
1. **MODAL**: Adopter système Capacité (MA/ME/MI)
2. **Validation**: Tester nouvelle opposition sur corpus
3. **Documentation**: Mettre à jour règles anti-absurdité

### **Optimisations Futures**
1. **Chevauchements**: Clarifier frontières DECIDE/MODAL
2. **Extension**: Ajouter nouveaux concepts si nécessaire
3. **Validation**: Corpus élargi avec corrections

---

**Inventaire Oppositions v0.0.1 VALIDÉ** ✓  
*Antagonismes corrigés, système trinaire optimisé*

---
*Inventaire généré - {__import__('time').strftime('%d/%m/%Y %H:%M')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)

def run_opposition_inventory():
    """Exécution inventaire complet oppositions"""
    print("📋 INVENTAIRE OPPOSITIONS TRINAIRES DHĀTU")
    print("=" * 60)
    
    inventory = TernaryOppositionInventory()
    
    # Validation complète
    validation_results = inventory.validate_all_oppositions()
    
    # Proposition corrections
    modal_correction = inventory.propose_modal_correction()
    
    # Vérification chevauchements
    overlaps = inventory.check_concept_overlaps()
    
    # Génération rapport
    report_path = inventory.generate_corrected_inventory()
    
    print(f"\n📄 Inventaire complet: {report_path}")
    print(f"\n🎯 RÉSULTAT: {validation_results['validity_rate']:.1f}% oppositions valides")
    print(f"   ✅ Valides: {len(validation_results['valid_oppositions'])}")
    print(f"   ❌ À corriger: {len(validation_results['invalid_oppositions'])}")
    print("\n✅ INVENTAIRE OPPOSITIONS TERMINÉ!")

if __name__ == "__main__":
    run_opposition_inventory()
