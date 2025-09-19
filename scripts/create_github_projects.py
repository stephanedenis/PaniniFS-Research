#!/usr/bin/env python3
"""
Script pour créer automatiquement les projets GitHub dhātu
Nécessite un token GitHub avec permissions repository et project
"""

import requests
import json
import os
from datetime import datetime

# Configuration
REPO_OWNER = "stephanedenis"
REPO_NAME = "PaniniFS-Research"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

if not GITHUB_TOKEN:
    print("❌ GITHUB_TOKEN environnement variable requise")
    print("Créez un token sur: https://github.com/settings/tokens")
    print("Permissions requises: repo, write:org, project")
    exit(1)

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

# Définition des projets
PROJECTS = {
    'core': [
        {
            'name': 'dhatu-universal-compressor',
            'description': '🧠 Système compression sémantique universelle dhātu - 100% reconstruction garantie',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-corpus-manager', 
            'description': '📚 Gestionnaire corpus multilingue - Collection autonome Gutenberg/ArXiv/HAL',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-web-framework',
            'description': '🌐 Framework web dhātu-natif - Dashboard temps réel + APIs',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-gpu-accelerator',
            'description': '⚡ Accélération GPU optimisée - Performance dhātu hardware',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        }
    ],
    'tools': [
        {
            'name': 'dhatu-pattern-analyzer',
            'description': '🔍 Analyse patterns sémantiques émergents - Corrélations dhātu',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-creative-generator',
            'description': '🎨 Génération créative assistée - Innovation dhātu-guidée',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-space-visualizer',
            'description': '🌌 Visualisation espaces multidimensionnels - Géométrie dhātu',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-evolution-simulator',
            'description': '🧬 Simulation évolution linguistique - Dynamiques dhātu',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        }
    ],
    'interfaces': [
        {
            'name': 'dhatu-dashboard',
            'description': '📊 Interface monitoring temps réel - UX dhātu responsive',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-api-gateway',
            'description': '🚪 Passerelle API unifiée - Microservices dhātu',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        }
    ],
    'research': [
        {
            'name': 'dhatu-linguistics-engine',
            'description': '🔬 Moteur analyse linguistique computationnelle - Théorie dhātu',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        },
        {
            'name': 'dhatu-multimodal-learning',
            'description': '🎭 Apprentissage multimodal dhātu - Gestuel + vocal + cognitif',
            'columns': ['📋 Backlog', '🏗️ In Progress', '🧪 Testing', '✅ Done']
        }
    ]
}

def create_project(category, project_info):
    """Créer un projet GitHub avec colonnes"""
    
    # 1. Créer le projet
    project_data = {
        'name': f"[{category.upper()}] {project_info['name']}",
        'body': project_info['description'],
        'state': 'open'
    }
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/projects"
    
    print(f"🚀 Création projet: {project_info['name']}")
    
    response = requests.post(url, headers=headers, json=project_data)
    
    if response.status_code == 201:
        project = response.json()
        project_id = project['id']
        print(f"✅ Projet créé: {project['html_url']}")
        
        # 2. Créer les colonnes
        for column_name in project_info['columns']:
            column_data = {'name': column_name}
            column_url = f"https://api.github.com/projects/{project_id}/columns"
            
            col_response = requests.post(column_url, headers=headers, json=column_data)
            if col_response.status_code == 201:
                print(f"  📋 Colonne créée: {column_name}")
            else:
                print(f"  ❌ Erreur colonne {column_name}: {col_response.status_code}")
        
        return True
        
    else:
        print(f"❌ Erreur création projet: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Créer tous les projets GitHub dhātu"""
    
    print("🎯 Création projets GitHub dhātu")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    for category, projects in PROJECTS.items():
        print(f"\n🔥 Catégorie: {category.upper()}")
        print("-" * 30)
        
        for project_info in projects:
            total_count += 1
            if create_project(category, project_info):
                success_count += 1
            print()
    
    print("=" * 50)
    print(f"✅ Projets créés: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 Tous les projets GitHub dhātu ont été créés avec succès!")
        print(f"🔗 Voir: https://github.com/{REPO_OWNER}/{REPO_NAME}/projects")
    else:
        print("⚠️  Certains projets n'ont pas pu être créés")

if __name__ == "__main__":
    main()