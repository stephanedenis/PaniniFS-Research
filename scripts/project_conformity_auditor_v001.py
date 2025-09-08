#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 AUDITEUR CONFORMITÉ PROJET
====================================================================
Vérification complète de la conformité du projet PaniniFS-Research
aux règles de copilotage consolidées.

Auteur: Assistant IA PaniniFS Research
Version: 0.0.1 - Audit Conformité Projet
Date: 08/09/2025
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConformityIssue:
    """Issue de conformité identifiée"""
    file_path: str
    issue_type: str
    severity: str  # "critical", "major", "minor"
    description: str
    expected: str
    current: str
    fix_suggestion: str

@dataclass
class DirectoryAnalysis:
    """Analyse d'un répertoire"""
    path: str
    expected_content: List[str]
    actual_content: List[str]
    missing_files: List[str]
    unexpected_files: List[str]
    naming_issues: List[str]

class ProjectConformityAuditor:
    """Auditeur conformité projet"""
    
    def __init__(self):
        print("🔍 AUDIT CONFORMITÉ PROJET PANINIFIX-RESEARCH")
        
        self.project_root = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.issues = []
        
        # Règles de nommage selon REGLES_COPILOTAGE_v0.0.1.md
        self.naming_rules = {
            "rapport": r"^RAPPORT_[A-Z_]+_v\d+\.\d+\.\d+\.md$",
            "analyse": r"^ANALYSE_[A-Z_]+[A-Z0-9_]*\.md$",
            "cache": r"^CACHE_[A-Z_]+_[A-Z0-9_]*\.json$",
            "validation": r"^VALIDATION_[A-Z_]+[A-Z0-9_]*\.md$",
            "recherche": r"^RECHERCHE_[A-Z_]+_v\d+\.\d+\.\d+\.md$",
            "tableau": r"^TABLEAU_[A-Z_]+_v\d+\.\d+\.\d+\.(md|csv)$",
            "regles": r"^REGLES_[A-Z_]+_v\d+\.\d+\.\d+\.md$",
            "verification": r"^VERIFICATION_[A-Z_]+_v\d+\.\d+\.\d+\.md$"
        }
        
        # Structure attendue
        self.expected_structure = {
            "data/corpus_babillage": ["Corpus d'analyse linguistique"],
            "data/references_cache": ["Cache références + rapports"],
            "scripts": ["Scripts Python d'analyse"],
            "discoveries": ["Découvertes recherche"],
            "publications": ["Articles et livres"],
            "methodology": ["Protocoles méthodologiques"],
            "docs": ["Documentation projet"]
        }
    
    def check_directory_structure(self) -> Dict:
        """Vérification structure répertoires"""
        print("\n📁 VÉRIFICATION STRUCTURE RÉPERTOIRES")
        
        structure_issues = []
        
        for expected_dir, description in self.expected_structure.items():
            dir_path = self.project_root / expected_dir
            
            if not dir_path.exists():
                structure_issues.append(ConformityIssue(
                    file_path=str(dir_path),
                    issue_type="missing_directory",
                    severity="major",
                    description=f"Répertoire manquant: {expected_dir}",
                    expected=f"Répertoire {expected_dir} doit exister",
                    current="Répertoire inexistant",
                    fix_suggestion=f"Créer: mkdir -p {dir_path}"
                ))
            else:
                print(f"   ✅ {expected_dir} - {description[0]}")
        
        return {
            "issues": structure_issues,
            "directories_checked": len(self.expected_structure),
            "missing_directories": len(structure_issues)
        }
    
    def check_file_naming_conventions(self) -> Dict:
        """Vérification conventions nommage"""
        print("\n📝 VÉRIFICATION CONVENTIONS NOMMAGE")
        
        naming_issues = []
        files_checked = 0
        
        # Vérification data/references_cache
        cache_dir = self.project_root / "data/references_cache"
        if cache_dir.exists():
            for file_path in cache_dir.iterdir():
                if file_path.is_file():
                    files_checked += 1
                    filename = file_path.name
                    
                    # Déterminer type attendu
                    file_type = self._determine_file_type(filename)
                    
                    if file_type and file_type in self.naming_rules:
                        pattern = self.naming_rules[file_type]
                        if not re.match(pattern, filename):
                            naming_issues.append(ConformityIssue(
                                file_path=str(file_path),
                                issue_type="naming_convention",
                                severity="minor",
                                description=f"Nom fichier non-conforme: {filename}",
                                expected=f"Pattern: {pattern}",
                                current=filename,
                                fix_suggestion=f"Renommer selon convention {file_type}"
                            ))
                        else:
                            print(f"   ✅ {filename} - conforme")
                    elif filename not in ["metadata.json", "references_cache.json"]:
                        naming_issues.append(ConformityIssue(
                            file_path=str(file_path),
                            issue_type="unknown_file_type",
                            severity="minor",
                            description=f"Type fichier non-identifié: {filename}",
                            expected="Type fichier reconnu",
                            current="Type inconnu",
                            fix_suggestion="Vérifier si fichier nécessaire ou renommer"
                        ))
        
        # Vérification scripts
        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            for file_path in scripts_dir.iterdir():
                if file_path.suffix == ".py":
                    files_checked += 1
                    filename = file_path.name
                    
                    # Convention scripts: [nom]_v[version].py
                    script_pattern = r"^[a-z_]+_v\d{3}\.py$"
                    if not re.match(script_pattern, filename):
                        naming_issues.append(ConformityIssue(
                            file_path=str(file_path),
                            issue_type="script_naming",
                            severity="minor",
                            description=f"Script mal nommé: {filename}",
                            expected="Pattern: [nom]_v[version].py",
                            current=filename,
                            fix_suggestion="Renommer avec version 3 chiffres"
                        ))
                    else:
                        print(f"   ✅ {filename} - script conforme")
        
        return {
            "issues": naming_issues,
            "files_checked": files_checked,
            "naming_violations": len(naming_issues)
        }
    
    def _determine_file_type(self, filename: str) -> str:
        """Détermine le type d'un fichier"""
        filename_upper = filename.upper()
        
        if filename_upper.startswith("RAPPORT_"):
            return "rapport"
        elif filename_upper.startswith("ANALYSE_"):
            return "analyse"  
        elif filename_upper.startswith("CACHE_"):
            return "cache"
        elif filename_upper.startswith("VALIDATION_"):
            return "validation"
        elif filename_upper.startswith("RECHERCHE_"):
            return "recherche"
        elif filename_upper.startswith("TABLEAU_"):
            return "tableau"
        elif filename_upper.startswith("REGLES_"):
            return "regles"
        elif filename_upper.startswith("VERIFICATION_"):
            return "verification"
        
        return None
    
    def check_metadata_completeness(self) -> Dict:
        """Vérification complétude métadonnées"""
        print("\n📊 VÉRIFICATION MÉTADONNÉES")
        
        metadata_issues = []
        
        # Vérification metadata.json principal
        metadata_path = self.project_root / "data/references_cache/metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                required_fields = [
                    "cache_metadata.created",
                    "cache_metadata.last_updated", 
                    "cache_metadata.version",
                    "cache_metadata.purpose"
                ]
                
                for field in required_fields:
                    if not self._check_nested_field(metadata, field):
                        metadata_issues.append(ConformityIssue(
                            file_path=str(metadata_path),
                            issue_type="missing_metadata_field",
                            severity="major",
                            description=f"Champ manquant: {field}",
                            expected=f"Champ {field} présent",
                            current="Champ absent",
                            fix_suggestion=f"Ajouter champ {field}"
                        ))
                
                print(f"   ✅ metadata.json - {len(required_fields) - len(metadata_issues)} champs sur {len(required_fields)}")
                
            except json.JSONDecodeError:
                metadata_issues.append(ConformityIssue(
                    file_path=str(metadata_path),
                    issue_type="invalid_json",
                    severity="critical",
                    description="Fichier JSON invalide",
                    expected="JSON valide",
                    current="JSON corrompu",
                    fix_suggestion="Corriger syntaxe JSON"
                ))
        else:
            metadata_issues.append(ConformityIssue(
                file_path=str(metadata_path),
                issue_type="missing_file",
                severity="critical",
                description="Fichier metadata.json manquant",
                expected="Fichier metadata.json présent",
                current="Fichier absent",
                fix_suggestion="Créer metadata.json avec structure requise"
            ))
        
        # Vérification references_cache.json
        ref_cache_path = self.project_root / "data/references_cache/references_cache.json"
        if ref_cache_path.exists():
            try:
                with open(ref_cache_path, 'r', encoding='utf-8') as f:
                    ref_cache = json.load(f)
                
                if "groups" not in ref_cache:
                    metadata_issues.append(ConformityIssue(
                        file_path=str(ref_cache_path),
                        issue_type="missing_cache_structure",
                        severity="major", 
                        description="Structure cache références incomplète",
                        expected="Champ 'groups' présent",
                        current="Structure manquante",
                        fix_suggestion="Ajouter structure complète cache"
                    ))
                else:
                    print(f"   ✅ references_cache.json - structure valide")
                    
            except json.JSONDecodeError:
                metadata_issues.append(ConformityIssue(
                    file_path=str(ref_cache_path),
                    issue_type="invalid_json",
                    severity="critical",
                    description="Cache références JSON invalide",
                    expected="JSON valide",
                    current="JSON corrompu", 
                    fix_suggestion="Corriger syntaxe JSON cache"
                ))
        else:
            metadata_issues.append(ConformityIssue(
                file_path=str(ref_cache_path),
                issue_type="missing_file",
                severity="major",
                description="Cache références manquant",
                expected="Fichier references_cache.json présent",
                current="Fichier absent",
                fix_suggestion="Créer cache références"
            ))
        
        return {
            "issues": metadata_issues,
            "files_checked": 2,
            "metadata_violations": len(metadata_issues)
        }
    
    def _check_nested_field(self, data: dict, field_path: str) -> bool:
        """Vérification champ imbriqué"""
        keys = field_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False
        
        return True
    
    def check_documentation_completeness(self) -> Dict:
        """Vérification complétude documentation"""
        print("\n📚 VÉRIFICATION DOCUMENTATION")
        
        doc_issues = []
        
        # Vérification README principal
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            doc_issues.append(ConformityIssue(
                file_path=str(readme_path),
                issue_type="missing_documentation",
                severity="major",
                description="README.md principal manquant",
                expected="README.md à la racine",
                current="Fichier absent",
                fix_suggestion="Créer README.md principal"
            ))
        else:
            print("   ✅ README.md principal présent")
        
        # Vérification règles copilotage
        rules_path = self.project_root / "data/references_cache/REGLES_COPILOTAGE_v0.0.1.md"
        if rules_path.exists():
            print("   ✅ Règles copilotage présentes")
        else:
            doc_issues.append(ConformityIssue(
                file_path=str(rules_path),
                issue_type="missing_rules",
                severity="major",
                description="Règles copilotage manquantes",
                expected="REGLES_COPILOTAGE_v0.0.1.md",
                current="Fichier absent",
                fix_suggestion="Créer règles copilotage"
            ))
        
        # Vérification docs/README.md
        docs_readme = self.project_root / "docs/README.md"
        if docs_readme.exists():
            print("   ✅ docs/README.md présent")
        else:
            doc_issues.append(ConformityIssue(
                file_path=str(docs_readme),
                issue_type="missing_docs_readme",
                severity="minor",
                description="Documentation docs/ incomplète",
                expected="docs/README.md",
                current="Fichier absent",
                fix_suggestion="Créer documentation docs/"
            ))
        
        return {
            "issues": doc_issues,
            "files_checked": 3,
            "documentation_violations": len(doc_issues)
        }
    
    def generate_conformity_report(self) -> str:
        """Génération rapport conformité complet"""
        print("\n📋 GÉNÉRATION RAPPORT CONFORMITÉ")
        
        # Exécution tous les audits
        structure_audit = self.check_directory_structure()
        naming_audit = self.check_file_naming_conventions()
        metadata_audit = self.check_metadata_completeness()
        doc_audit = self.check_documentation_completeness()
        
        # Consolidation issues
        all_issues = (structure_audit["issues"] + 
                     naming_audit["issues"] + 
                     metadata_audit["issues"] + 
                     doc_audit["issues"])
        
        # Classification par sévérité
        critical_issues = [i for i in all_issues if i.severity == "critical"]
        major_issues = [i for i in all_issues if i.severity == "major"]
        minor_issues = [i for i in all_issues if i.severity == "minor"]
        
        # Calcul score conformité
        total_checks = (structure_audit["directories_checked"] + 
                       naming_audit["files_checked"] + 
                       metadata_audit["files_checked"] + 
                       doc_audit["files_checked"])
        
        total_violations = len(all_issues)
        conformity_score = max(0, 100 - (total_violations * 5))  # -5 points par violation
        
        # Génération rapport
        report_path = self.project_root / "data/references_cache/AUDIT_CONFORMITE_v0.0.1.md"
        
        report_content = f"""# 🔍 AUDIT CONFORMITÉ PROJET v0.0.1

## 🎯 **Résultats Audit Conformité PaniniFS-Research**

### **📊 Score Global de Conformité: {conformity_score:.1f}/100**

- **Total vérifications**: {total_checks}
- **Violations identifiées**: {total_violations}
- **Issues critiques**: {len(critical_issues)}
- **Issues majeures**: {len(major_issues)}
- **Issues mineures**: {len(minor_issues)}

### **🏆 État Conformité par Catégorie**

#### **📁 Structure Répertoires**
- Répertoires vérifiés: {structure_audit["directories_checked"]}
- Répertoires manquants: {structure_audit["missing_directories"]}
- Statut: {"✅ CONFORME" if structure_audit["missing_directories"] == 0 else f"❌ {structure_audit['missing_directories']} manquants"}

#### **📝 Conventions Nommage**
- Fichiers vérifiés: {naming_audit["files_checked"]}
- Violations nommage: {naming_audit["naming_violations"]}
- Statut: {"✅ CONFORME" if naming_audit["naming_violations"] == 0 else f"⚠️ {naming_audit['naming_violations']} violations"}

#### **📊 Métadonnées**
- Fichiers vérifiés: {metadata_audit["files_checked"]}
- Violations métadonnées: {metadata_audit["metadata_violations"]}
- Statut: {"✅ CONFORME" if metadata_audit["metadata_violations"] == 0 else f"❌ {metadata_audit['metadata_violations']} violations"}

#### **📚 Documentation**
- Fichiers vérifiés: {doc_audit["files_checked"]}
- Violations documentation: {doc_audit["documentation_violations"]}
- Statut: {"✅ CONFORME" if doc_audit["documentation_violations"] == 0 else f"⚠️ {doc_audit['documentation_violations']} violations"}

## 🚨 **Issues Critiques à Corriger Immédiatement**

{chr(10).join(f'''
### **{i+1}. {issue.issue_type.replace('_', ' ').title()}**
- **Fichier**: `{issue.file_path}`
- **Description**: {issue.description}
- **Attendu**: {issue.expected}
- **Actuel**: {issue.current}
- **Solution**: {issue.fix_suggestion}
''' for i, issue in enumerate(critical_issues)) if critical_issues else "🎉 **Aucune issue critique identifiée !**"}

## ⚠️ **Issues Majeures à Traiter**

{chr(10).join(f'''
### **{i+1}. {issue.issue_type.replace('_', ' ').title()}**
- **Fichier**: `{issue.file_path}`
- **Description**: {issue.description}
- **Solution**: {issue.fix_suggestion}
''' for i, issue in enumerate(major_issues)) if major_issues else "✅ **Aucune issue majeure identifiée !**"}

## 💡 **Issues Mineures (Améliorations)**

{chr(10).join(f'''
### **{i+1}. {issue.issue_type.replace('_', ' ').title()}**
- **Fichier**: `{issue.file_path}`
- **Description**: {issue.description}
- **Solution**: {issue.fix_suggestion}
''' for i, issue in enumerate(minor_issues[:5])) if minor_issues else "🎯 **Aucune amélioration mineure identifiée !**"}

{f"... et {len(minor_issues) - 5} autres issues mineures" if len(minor_issues) > 5 else ""}

## 🔧 **Plan d'Action Recommandé**

### **🚨 Priorité 1 (Issues Critiques)**
{chr(10).join(f"1. {issue.fix_suggestion}" for issue in critical_issues[:3]) if critical_issues else "✅ Aucune action critique requise"}

### **⚠️ Priorité 2 (Issues Majeures)**
{chr(10).join(f"1. {issue.fix_suggestion}" for issue in major_issues[:3]) if major_issues else "✅ Aucune action majeure requise"}

### **💡 Priorité 3 (Améliorations)**
{chr(10).join(f"1. {issue.fix_suggestion}" for issue in minor_issues[:3]) if minor_issues else "✅ Aucune amélioration requise"}

## 📈 **Recommandations Maintien Conformité**

### **Routine Quotidienne**
- Vérifier nommage nouveaux fichiers
- Mettre à jour métadonnées après modifications
- Documenter nouvelles analyses

### **Routine Hebdomadaire**
- Audit conformité automatique
- Nettoyage fichiers obsolètes
- Consolidation cache références

### **Routine Mensuelle**
- Révision règles copilotage
- Audit complet structure projet
- Mise à jour documentation

## ✅ **Validation Audit**

**Audit réalisé le**: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
**Conformité aux règles**: REGLES_COPILOTAGE_v0.0.1.md
**Prochaine révision**: Recommandée dans 7 jours

### **Critères Validation**
- ✅ Structure répertoires vérifiée
- ✅ Conventions nommage auditées  
- ✅ Métadonnées validées
- ✅ Documentation évaluée
- ✅ Plan d'action établi

---

**Audit Conformité v0.0.1 TERMINÉ** ✓  
*Maintien qualité projet validé*

---
*Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)

def run_project_audit():
    """Exécution audit complet projet"""
    print("🔍 AUDIT CONFORMITÉ PROJET PANINIFIX-RESEARCH")
    print("=" * 60)
    
    auditor = ProjectConformityAuditor()
    
    # Génération rapport complet
    report_path = auditor.generate_conformity_report()
    
    print(f"\n📄 Rapport audit: {report_path}")
    print(f"\n🎯 Audit terminé - Consultez le rapport pour détails")
    
    print("\n✅ AUDIT CONFORMITÉ TERMINÉ!")

if __name__ == "__main__":
    run_project_audit()
