#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👶 ÉVALUATEUR DÉVELOPPEMENT ÉMOTIONNEL PERSONNALISÉ
====================================================================
Outil d'évaluation et de recommendation pour le développement 
émotionnel basé sur le modèle évolutif par paliers intégrant
Panksepp, trinaire et besoins expressifs.

Auteur: Assistant IA PaniniFS Research  
Version: 0.0.1 - Évaluateur Développement Émotionnel
Date: 08/09/2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolutionary_emotional_model_v001 import EvolutionaryEmotionalModel, AcquisitionStage
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, date
import json
from pathlib import Path

@dataclass
class ChildProfile:
    """Profil d'enfant pour évaluation développementale"""
    name: str
    birth_date: date
    current_age_months: int
    current_observations: Dict[str, bool] = field(default_factory=dict)
    environmental_factors: List[str] = field(default_factory=list)
    special_needs: List[str] = field(default_factory=list)
    cultural_context: str = "western_standard"
    language_exposure: List[str] = field(default_factory=list)

@dataclass 
class DevelopmentalAssessment:
    """Évaluation développementale complète"""
    child_profile: ChildProfile
    assessment_date: date
    current_stage: AcquisitionStage
    mastered_emotions: List[str]
    emerging_emotions: List[str] 
    delayed_emotions: List[str]
    advanced_emotions: List[str]
    trinaire_readiness: Dict[str, str]
    recommendations: Dict[str, List[str]]
    next_review_date: date
    developmental_score: float

class PersonalizedEmotionalEvaluator:
    """Évaluateur personnalisé de développement émotionnel"""
    
    def __init__(self):
        print("👶 ÉVALUATEUR DÉVELOPPEMENT ÉMOTIONNEL PERSONNALISÉ")
        
        # Initialisation modèle évolutif
        self.model = EvolutionaryEmotionalModel()
        
        # Base de données observations comportementales
        self._build_behavioral_checklist()
        
        # Facteurs environnementaux et culturels
        self._build_environmental_factors()
    
    def _build_behavioral_checklist(self):
        """Construction checklist observations comportementales"""
        print("   📋 Construction checklist comportementale...")
        
        self.behavioral_checklist = {
            # NÉONATAL (0-2 mois)
            "comfort_distress_cycles": "Pleurs/apaisement cycles réguliers",
            "visual_tracking": "Suit objets/visages du regard", 
            "startle_response": "Réactions sursaut normales",
            "sleep_wake_cycles": "Cycles veille-sommeil établis",
            
            # PETIT ENFANT PRÉCOCE (2-6 mois)  
            "social_smile": "Sourire en réponse interactions",
            "vocal_play": "Babillage et vocalises joyeuses",
            "emotional_contagion": "Réagit émotions des autres",
            "stranger_interest": "Intérêt pour nouveaux visages",
            
            # PETIT ENFANT TARDIF (6-12 mois)
            "stranger_wariness": "Méfiance avec inconnus",
            "separation_anxiety": "Détresse séparation figure attachment",
            "anger_frustration": "Colère quand objectifs bloqués", 
            "fear_avoidance": "Évitement situations inquiétantes",
            
            # BAMBIN PRÉCOCE (12-18 mois)
            "curiosity_exploration": "Exploration active environnement",
            "empathic_concern": "Inquiétude pour détresse autres",
            "object_sharing": "Partage spontané objets",
            "imitation_emotional": "Imite expressions émotionnelles",
            
            # BAMBIN TARDIF (18-36 mois)
            "pride_achievement": "Fierté lors réussites",
            "shame_failure": "Embarras lors échecs publics",
            "guilt_transgression": "Remords après transgression règles",
            "emotional_labeling": "Nomme émotions propres/autres"
        }
    
    def _build_environmental_factors(self):
        """Construction facteurs environnementaux"""
        print("   🌍 Construction facteurs environnementaux...")
        
        self.environmental_factors = {
            "family_structure": ["nucléaire", "monoparentale", "recomposée", "élargie"],
            "caregiver_sensitivity": ["très_sensible", "sensible", "modérément_sensible", "peu_sensible"],
            "socioeconomic_status": ["élevé", "moyen", "modeste", "précaire"],
            "cultural_context": ["occidental", "collectiviste", "mixte", "traditionnel"],
            "language_environment": ["monolingue", "bilingue", "multilingue"],
            "special_circumstances": ["prématurité", "hospitalisation", "trauma", "handicap", "aucun"]
        }
    
    def create_child_profile(self, name: str, birth_date: date, 
                           observations: Dict[str, bool] = None,
                           env_factors: List[str] = None,
                           special_needs: List[str] = None) -> ChildProfile:
        """Création profil enfant"""
        
        # Calcul âge en mois
        today = date.today()
        age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        if today.day < birth_date.day:
            age_months -= 1
        
        profile = ChildProfile(
            name=name,
            birth_date=birth_date,
            current_age_months=age_months,
            current_observations=observations or {},
            environmental_factors=env_factors or [],
            special_needs=special_needs or []
        )
        
        print(f"   👶 Profil créé pour {name} ({age_months} mois)")
        return profile
    
    def conduct_assessment(self, child_profile: ChildProfile) -> DevelopmentalAssessment:
        """Conduite évaluation développementale complète"""
        print(f"\n📊 ÉVALUATION DÉVELOPPEMENTALE - {child_profile.name}")
        
        # Évaluation développementale de base
        base_assessment = self.model.generate_developmental_assessment(child_profile.current_age_months)
        
        # Analyse observations comportementales
        emotional_analysis = self._analyze_emotional_behaviors(child_profile)
        
        # Évaluation influence facteurs environnementaux
        environmental_impact = self._assess_environmental_impact(child_profile)
        
        # Détection retards/avances développementales
        developmental_variations = self._detect_developmental_variations(
            child_profile, base_assessment, emotional_analysis
        )
        
        # Recommandations personnalisées
        personalized_recommendations = self._generate_personalized_recommendations(
            child_profile, base_assessment, emotional_analysis, environmental_impact
        )
        
        # Score développemental global
        dev_score = self._calculate_developmental_score(
            child_profile, emotional_analysis, developmental_variations
        )
        
        # Prochaine évaluation 
        next_review = self._calculate_next_review_date(child_profile, dev_score)
        
        assessment = DevelopmentalAssessment(
            child_profile=child_profile,
            assessment_date=date.today(),
            current_stage=base_assessment['current_stage'],
            mastered_emotions=[em.concept for em in base_assessment['expected_acquisitions']],
            emerging_emotions=[em.concept for em in base_assessment['emerging_acquisitions']],
            delayed_emotions=developmental_variations['delayed'],
            advanced_emotions=developmental_variations['advanced'],
            trinaire_readiness=self._assess_trinaire_readiness(child_profile, base_assessment),
            recommendations=personalized_recommendations,
            next_review_date=next_review,
            developmental_score=dev_score
        )
        
        return assessment
    
    def _analyze_emotional_behaviors(self, profile: ChildProfile) -> Dict:
        """Analyse comportements émotionnels observés"""
        
        observed_behaviors = []
        missing_behaviors = []
        concerning_behaviors = []
        
        # Analyse selon âge attendu
        expected_stage = self.model._determine_current_stage(profile.current_age_months)
        
        for behavior_key, behavior_desc in self.behavioral_checklist.items():
            if behavior_key in profile.current_observations:
                if profile.current_observations[behavior_key]:
                    observed_behaviors.append(behavior_key)
                else:
                    missing_behaviors.append(behavior_key)
        
        # Détection comportements préoccupants selon âge
        age_appropriate_expectations = self._get_age_appropriate_behaviors(profile.current_age_months)
        
        for expected_behavior in age_appropriate_expectations:
            if expected_behavior in missing_behaviors:
                concerning_behaviors.append(expected_behavior)
        
        return {
            "observed": observed_behaviors,
            "missing": missing_behaviors, 
            "concerning": concerning_behaviors,
            "total_expected": len(age_appropriate_expectations),
            "percent_observed": len(observed_behaviors) / len(age_appropriate_expectations) * 100 if age_appropriate_expectations else 0
        }
    
    def _get_age_appropriate_behaviors(self, age_months: int) -> List[str]:
        """Obtention comportements appropriés selon âge"""
        
        behaviors = []
        
        if age_months >= 2:  # Néonatal passé
            behaviors.extend(["comfort_distress_cycles", "visual_tracking", "startle_response", "sleep_wake_cycles"])
        
        if age_months >= 6:  # Petit enfant précoce  
            behaviors.extend(["social_smile", "vocal_play", "emotional_contagion", "stranger_interest"])
        
        if age_months >= 12:  # Petit enfant tardif
            behaviors.extend(["stranger_wariness", "separation_anxiety", "anger_frustration", "fear_avoidance"])
        
        if age_months >= 18:  # Bambin précoce
            behaviors.extend(["curiosity_exploration", "empathic_concern", "object_sharing", "imitation_emotional"])
        
        if age_months >= 36:  # Bambin tardif
            behaviors.extend(["pride_achievement", "shame_failure", "guilt_transgression", "emotional_labeling"])
        
        return behaviors
    
    def _assess_environmental_impact(self, profile: ChildProfile) -> Dict:
        """Évaluation impact facteurs environnementaux"""
        
        # Facteurs de risque et de protection
        risk_factors = []
        protective_factors = []
        
        # Analyse facteurs familiaux
        if "famille_monoparentale" in profile.environmental_factors:
            risk_factors.append("stress_parental_potentiel")
        if "famille_nucléaire_stable" in profile.environmental_factors:
            protective_factors.append("stabilité_attachment")
        
        # Analyse facteurs socioéconomiques
        if "précarité" in profile.environmental_factors:
            risk_factors.append("stress_chronique")
        if "ressources_éducatives" in profile.environmental_factors:
            protective_factors.append("stimulation_cognitive")
        
        # Besoins spéciaux
        if profile.special_needs:
            risk_factors.extend([f"adaptation_{need}" for need in profile.special_needs])
        
        return {
            "risk_factors": risk_factors,
            "protective_factors": protective_factors,
            "risk_score": len(risk_factors),
            "protection_score": len(protective_factors),
            "overall_impact": "positive" if len(protective_factors) > len(risk_factors) else "neutral" if len(protective_factors) == len(risk_factors) else "challenging"
        }
    
    def _detect_developmental_variations(self, profile: ChildProfile, 
                                       base_assessment: Dict, 
                                       emotional_analysis: Dict) -> Dict:
        """Détection variations développementales"""
        
        delayed = []
        advanced = []
        
        # Analyse retards basés sur observations manquantes
        expected_emotions = [em.concept for em in base_assessment['expected_acquisitions']]
        concerning_missing = emotional_analysis['concerning']
        
        # Émotions en retard (devraient être acquises)
        for emotion_concept in expected_emotions:
            # Mapping concept vers comportement observable
            if self._is_emotion_delayed(emotion_concept, profile, concerning_missing):
                delayed.append(emotion_concept)
        
        # Émotions avancées (acquises précocement)
        future_emotions = [em.concept for em in base_assessment['future_acquisitions']]
        observed_behaviors = emotional_analysis['observed']
        
        for emotion_concept in future_emotions:
            if self._is_emotion_advanced(emotion_concept, profile, observed_behaviors):
                advanced.append(emotion_concept)
        
        return {
            "delayed": delayed,
            "advanced": advanced,
            "typical": len(expected_emotions) - len(delayed)
        }
    
    def _is_emotion_delayed(self, emotion_concept: str, profile: ChildProfile, concerning_missing: List[str]) -> bool:
        """Vérification si émotion en retard"""
        
        emotion_behavior_mapping = {
            "COMFORT": ["comfort_distress_cycles"],
            "JOY": ["social_smile", "vocal_play"],
            "FEAR": ["stranger_wariness", "fear_avoidance"],
            "ANGER": ["anger_frustration"],
            "CURIOSITY": ["curiosity_exploration"],
            "EMPATHY": ["empathic_concern", "object_sharing"],
            "PRIDE": ["pride_achievement"],
            "GUILT": ["guilt_transgression"]
        }
        
        expected_behaviors = emotion_behavior_mapping.get(emotion_concept, [])
        return any(behavior in concerning_missing for behavior in expected_behaviors)
    
    def _is_emotion_advanced(self, emotion_concept: str, profile: ChildProfile, observed_behaviors: List[str]) -> bool:
        """Vérification si émotion avancée"""
        
        emotion_behavior_mapping = {
            "COMFORT": ["comfort_distress_cycles"],
            "JOY": ["social_smile", "vocal_play"],
            "FEAR": ["stranger_wariness", "fear_avoidance"],
            "ANGER": ["anger_frustration"],
            "CURIOSITY": ["curiosity_exploration"],
            "EMPATHY": ["empathic_concern", "object_sharing"],
            "PRIDE": ["pride_achievement"],
            "GUILT": ["guilt_transgression"]
        }
        
        expected_behaviors = emotion_behavior_mapping.get(emotion_concept, [])
        return any(behavior in observed_behaviors for behavior in expected_behaviors)
    
    def _generate_personalized_recommendations(self, profile: ChildProfile,
                                             base_assessment: Dict,
                                             emotional_analysis: Dict,
                                             environmental_impact: Dict) -> Dict[str, List[str]]:
        """Génération recommandations personnalisées"""
        
        recommendations = {
            "immediate_focus": [],
            "trinaire_activities": [],
            "environmental_supports": [], 
            "monitoring_priorities": [],
            "professional_referrals": []
        }
        
        # Focus immédiat basé sur retards détectés
        if emotional_analysis['concerning']:
            recommendations["immediate_focus"].extend([
                f"Stimuler {behavior.replace('_', ' ')}" for behavior in emotional_analysis['concerning'][:3]
            ])
        
        # Activités trinaires selon stade
        recommendations["trinaire_activities"].extend(base_assessment['trinaire_recommendations'])
        
        # Supports environnementaux
        if environmental_impact['risk_score'] > environmental_impact['protection_score']:
            recommendations["environmental_supports"].extend([
                "Renforcer stabilité routines quotidiennes",
                "Augmenter interactions positives parent-enfant",
                "Créer environnement prévisible et sécurisant"
            ])
        
        # Priorités monitoring 
        if emotional_analysis['percent_observed'] < 70:
            recommendations["monitoring_priorities"].append("Évaluation développementale approfondie recommandée")
        
        # Orientation professionnelle si nécessaire
        if emotional_analysis['percent_observed'] < 50:
            recommendations["professional_referrals"].append("Consultation pédopsychologie recommandée")
        
        return recommendations
    
    def _assess_trinaire_readiness(self, profile: ChildProfile, base_assessment: Dict) -> Dict[str, str]:
        """Évaluation préparation système trinaire"""
        
        readiness = {}
        
        current_stage = base_assessment['current_stage']
        
        # Préparation selon stade développemental
        if current_stage in [AcquisitionStage.NEONATAL, AcquisitionStage.EARLY_INFANT]:
            readiness = {
                "complexity_level": "simple",
                "recommended_forms": "KA/KE (comfort), RA/RE (arousal)",
                "learning_approach": "association_directe",
                "parental_modeling": "essentiel"
            }
        elif current_stage == AcquisitionStage.LATE_INFANT:
            readiness = {
                "complexity_level": "intermediate", 
                "recommended_forms": "JA/JE/JI, FA/FE/FI",
                "learning_approach": "imitation_et_jeu",
                "parental_modeling": "important"
            }
        else:  # Bambin
            readiness = {
                "complexity_level": "complex",
                "recommended_forms": "toutes_primitives_disponibles",
                "learning_approach": "symbolique_et_narratif",
                "parental_modeling": "guide_et_facilite"
            }
        
        return readiness
    
    def _calculate_developmental_score(self, profile: ChildProfile,
                                     emotional_analysis: Dict,
                                     variations: Dict) -> float:
        """Calcul score développemental global"""
        
        base_score = emotional_analysis['percent_observed']
        
        # Bonus pour émotions avancées
        advanced_bonus = len(variations['advanced']) * 5
        
        # Pénalité pour retards significatifs  
        delay_penalty = len(variations['delayed']) * 10
        
        # Ajustement facteurs environnementaux
        env_adjustment = 0
        if len(profile.special_needs) > 0:
            env_adjustment = -5  # Ajustement compatissant
        
        final_score = max(0, min(100, base_score + advanced_bonus - delay_penalty + env_adjustment))
        
        return round(final_score, 1)
    
    def _calculate_next_review_date(self, profile: ChildProfile, dev_score: float) -> date:
        """Calcul date prochaine évaluation"""
        
        today = date.today()
        
        # Fréquence selon âge et score
        if profile.current_age_months < 12:
            interval_months = 2  # Tous les 2 mois première année
        elif profile.current_age_months < 24:
            interval_months = 3  # Tous les 3 mois deuxième année  
        else:
            interval_months = 6  # Tous les 6 mois après 2 ans
        
        # Ajustement selon score développemental
        if dev_score < 60:
            interval_months = max(1, interval_months - 1)  # Plus fréquent si préoccupations
        
        # Calcul date approximative (simplifié)
        next_month = today.month + interval_months
        next_year = today.year + (next_month - 1) // 12
        next_month = ((next_month - 1) % 12) + 1
        
        try:
            next_date = date(next_year, next_month, today.day)
        except ValueError:
            # Ajustement pour mois avec moins de jours
            next_date = date(next_year, next_month, min(today.day, 28))
        
        return next_date
    
    def generate_assessment_report(self, assessment: DevelopmentalAssessment) -> str:
        """Génération rapport d'évaluation complet"""
        
        report_path = Path(f"/home/stephane/GitHub/PaniniFS-Research/data/references_cache/EVALUATION_{assessment.child_profile.name}_{assessment.assessment_date.strftime('%Y%m%d')}.md")
        
        report_content = f"""# 👶 ÉVALUATION DÉVELOPPEMENT ÉMOTIONNEL - {assessment.child_profile.name}

## 📋 **Profil Enfant**
- **Nom**: {assessment.child_profile.name}
- **Date naissance**: {assessment.child_profile.birth_date.strftime('%d/%m/%Y')}
- **Âge actuel**: {assessment.child_profile.current_age_months} mois
- **Date évaluation**: {assessment.assessment_date.strftime('%d/%m/%Y')}

## 📊 **Résultats Évaluation**

### **🎯 Stade Développemental Actuel**
**{assessment.current_stage.value}** - {self._get_stage_description(assessment.current_stage)}

### **📈 Score Développemental Global: {assessment.developmental_score}/100**
{self._interpret_developmental_score(assessment.developmental_score)}

### **✅ Émotions Maîtrisées ({len(assessment.mastered_emotions)})**
{chr(10).join(f"- {emotion}" for emotion in assessment.mastered_emotions)}

### **🌱 Émotions Émergentes ({len(assessment.emerging_emotions)})**  
{chr(10).join(f"- {emotion}" for emotion in assessment.emerging_emotions)}

### **⚠️ Émotions en Retard ({len(assessment.delayed_emotions)})**
{chr(10).join(f"- {emotion}" for emotion in assessment.delayed_emotions) if assessment.delayed_emotions else "Aucune émotion en retard détectée"}

### **🚀 Émotions Avancées ({len(assessment.advanced_emotions)})**
{chr(10).join(f"- {emotion}" for emotion in assessment.advanced_emotions) if assessment.advanced_emotions else "Développement typique selon âge"}

## 🔤 **Préparation Système Trinaire**

### **Niveau de Complexité Recommandé**
**{assessment.trinaire_readiness['complexity_level'].upper()}**

### **Formes Trinaires Adaptées**
{assessment.trinaire_readiness['recommended_forms']}

### **Approche d'Apprentissage**
{assessment.trinaire_readiness['learning_approach'].replace('_', ' ').title()}

### **Rôle Parental**
{assessment.trinaire_readiness['parental_modeling'].replace('_', ' ').title()}

## 🎯 **Recommandations Personnalisées**

### **🔥 Focus Immédiat**
{chr(10).join(f"- {rec}" for rec in assessment.recommendations['immediate_focus']) if assessment.recommendations['immediate_focus'] else "Développement dans la norme, continuer stimulation régulière"}

### **🎲 Activités Trinaires**
{chr(10).join(f"- {rec}" for rec in assessment.recommendations['trinaire_activities'])}

### **🏠 Supports Environnementaux**
{chr(10).join(f"- {rec}" for rec in assessment.recommendations['environmental_supports']) if assessment.recommendations['environmental_supports'] else "Environnement actuel approprié"}

### **📊 Priorités Monitoring**
{chr(10).join(f"- {rec}" for rec in assessment.recommendations['monitoring_priorities']) if assessment.recommendations['monitoring_priorities'] else "Suivi développemental standard suffisant"}

### **👩‍⚕️ Orientations Professionnelles**
{chr(10).join(f"- {rec}" for rec in assessment.recommendations['professional_referrals']) if assessment.recommendations['professional_referrals'] else "Aucune orientation spécialisée nécessaire actuellement"}

## 📅 **Suivi**

### **Prochaine Évaluation Recommandée**
**{assessment.next_review_date.strftime('%d/%m/%Y')}**

### **Points de Vigilance**
{self._generate_vigilance_points(assessment)}

### **Objectifs Développementaux**
{self._generate_developmental_goals(assessment)}

---

**Évaluation réalisée via Modèle Évolutif Émotionnel v0.0.1** ✓  
*Intégration Panksepp + Trinaire + Paliers développementaux*

---
*Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)
    
    def _get_stage_description(self, stage: AcquisitionStage) -> str:
        """Description stade développemental"""
        descriptions = {
            AcquisitionStage.NEONATAL: "Réflexes de base et régulation somatique",
            AcquisitionStage.EARLY_INFANT: "Émotions primaires et engagement social", 
            AcquisitionStage.LATE_INFANT: "Différenciation émotionnelle et conscience sociale",
            AcquisitionStage.EARLY_TODDLER: "Émotions sociales et conscience de soi",
            AcquisitionStage.LATE_TODDLER: "Complexité émotionnelle et émotions morales",
            AcquisitionStage.PRESCHOOL: "Régulation émotionnelle et métacognition"
        }
        return descriptions.get(stage, "Stade développemental avancé")
    
    def _interpret_developmental_score(self, score: float) -> str:
        """Interprétation score développemental"""
        if score >= 85:
            return "🟢 **EXCELLENT** - Développement optimal ou avancé"
        elif score >= 70:
            return "🟡 **BON** - Développement dans la norme, quelques aspects à stimuler"
        elif score >= 55:
            return "🟠 **PRÉOCCUPANT** - Retards légers, intervention recommandée" 
        else:
            return "🔴 **ALARMANT** - Retards significatifs, évaluation spécialisée urgente"
    
    def _generate_vigilance_points(self, assessment: DevelopmentalAssessment) -> str:
        """Génération points de vigilance"""
        points = []
        
        if assessment.delayed_emotions:
            points.append(f"Surveiller progression {', '.join(assessment.delayed_emotions[:2])}")
        
        if assessment.developmental_score < 70:
            points.append("Monitoring rapproché développement émotionnel")
        
        if assessment.child_profile.special_needs:
            points.append("Adaptation interventions selon besoins spéciaux")
        
        return chr(10).join(f"- {point}" for point in points) if points else "- Développement typique, vigilance standard"
    
    def _generate_developmental_goals(self, assessment: DevelopmentalAssessment) -> str:
        """Génération objectifs développementaux"""
        goals = []
        
        # Objectifs basés sur émotions émergentes
        for emotion in assessment.emerging_emotions[:3]:
            goals.append(f"Consolider acquisition {emotion}")
        
        # Objectifs basés sur retards
        for emotion in assessment.delayed_emotions[:2]:
            goals.append(f"Rattraper retard {emotion}")
        
        # Objectif trinaire
        trinaire_level = assessment.trinaire_readiness['complexity_level']
        goals.append(f"Progresser système trinaire niveau {trinaire_level}")
        
        return chr(10).join(f"- {goal}" for goal in goals) if goals else "- Maintenir progression développementale actuelle"

def run_example_evaluation():
    """Exemple d'évaluation complète"""
    print("👶 EXEMPLE ÉVALUATION DÉVELOPPEMENT ÉMOTIONNEL")
    print("=" * 60)
    
    evaluator = PersonalizedEmotionalEvaluator()
    
    # Création profils exemples
    profiles = [
        # Profil 1: Développement typique
        evaluator.create_child_profile(
            name="Emma",
            birth_date=date(2023, 3, 15),  # ~18 mois
            observations={
                "comfort_distress_cycles": True,
                "social_smile": True,
                "stranger_wariness": True,
                "anger_frustration": True,
                "curiosity_exploration": True,
                "empathic_concern": True,
                "object_sharing": False,  # En émergence
                "pride_achievement": False  # Pas encore
            },
            env_factors=["famille_nucléaire_stable", "ressources_éducatives"],
            special_needs=[]
        ),
        
        # Profil 2: Quelques retards
        evaluator.create_child_profile(
            name="Lucas", 
            birth_date=date(2022, 8, 20),  # ~24 mois
            observations={
                "comfort_distress_cycles": True,
                "social_smile": True,
                "stranger_wariness": False,  # Retard
                "anger_frustration": True,
                "curiosity_exploration": True,
                "empathic_concern": False,  # Retard
                "object_sharing": False,
                "pride_achievement": True,  # Avancé
                "guilt_transgression": False
            },
            env_factors=["famille_monoparentale", "stress_environnemental"],
            special_needs=["retard_langage_léger"]
        )
    ]
    
    # Conduite évaluations
    for profile in profiles:
        print(f"\n🔍 Évaluation {profile.name}...")
        assessment = evaluator.conduct_assessment(profile)
        
        print(f"   Score développemental: {assessment.developmental_score}/100")
        print(f"   Stade: {assessment.current_stage.value}")
        print(f"   Émotions maîtrisées: {len(assessment.mastered_emotions)}")
        print(f"   Émotions en retard: {len(assessment.delayed_emotions)}")
        print(f"   Prochaine évaluation: {assessment.next_review_date.strftime('%d/%m/%Y')}")
        
        # Génération rapport
        report_path = evaluator.generate_assessment_report(assessment)
        print(f"   📄 Rapport: {Path(report_path).name}")
    
    print(f"\n✅ EXEMPLES ÉVALUATIONS TERMINÉS!")
    print(f"📄 Rapports disponibles dans data/references_cache/")

if __name__ == "__main__":
    run_example_evaluation()
