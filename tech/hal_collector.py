#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HAL (Hyper Articles en Ligne) Collector for French Scientific Papers
Collecteur de corpus scientifique français avec analyse mathématique
"""

import asyncio
import aiohttp
import json
import time
import hashlib
import re
import os
from typing import List, Dict
from urllib.parse import quote


class HALCorpusCollector:
    """Collecteur de corpus HAL pour articles scientifiques français"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Rate limiting pour respecter l'API HAL
        self.request_delay = 1.5  # secondes entre requêtes
        
        # Statistiques de collection
        self.collected_papers = []
        self.language_stats = {}
        self.mathematical_notation_stats = {}
        
    def detect_language(self, text: str) -> str:
        """Détection simple de langue basée sur patterns courants"""
        text_lower = text.lower()
        
        # Indicateurs français
        french_words = ['le', 'de', 'et', 'des', 'les', 'dans', 'pour', 'une', 'sur', 'avec', 'nous', 'cette', 'sont']
        french_score = sum(1 for word in french_words if word in text_lower)
        
        # Indicateurs anglais
        english_words = ['the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'for', 'with', 'we', 'this', 'are']
        english_score = sum(1 for word in english_words if word in text_lower)
        
        return 'fr' if french_score > english_score else 'en'
    
    def analyze_mathematical_content(self, text: str) -> Dict[str, int]:
        """Analyse du contenu mathématique dans le texte"""
        math_patterns = {
            'latex_commands': re.compile(r'\\[a-zA-Z]+'),
            'unicode_math': re.compile(r'[∀∃∫∑∇∂→⟺≤≥≠±×÷∈∉⊂⊃∩∪∧∨¬]'),
            'equations': re.compile(r'[a-zA-Z]\s*[=<>≤≥]\s*[^.!?]*[0-9a-zA-Z]'),
        }
        
        results = {}
        for key, pattern in math_patterns.items():
            matches = pattern.findall(text)
            results[key] = len(matches)
        
        # Densité mathématique
        total_math = sum(results.values())
        results['math_density'] = total_math / len(text) if len(text) > 0 else 0
        
        return results
    
    async def collect_hal_batch(self, query: str, max_papers: int = 50) -> List[Dict]:
        """Collecte par batch depuis l'API HAL"""
        papers = []
        
        # Construction requête HAL API
        hal_api_url = "https://api.archives-ouvertes.fr/search/"
        params = {
            'q': query,
            'fq': 'language_s:fr',  # Filtrer français
            'rows': max_papers,
            'fl': 'title_s,abstract_s,uri_s,docType_s,submittedDate_s,classification_s',
            'wt': 'json'
        }
        
        print(f"    Collecte HAL: {query} (max {max_papers})")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(hal_api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        docs = data.get('response', {}).get('docs', [])
                        
                        for doc in docs:
                            title = doc.get('title_s', [''])[0] if doc.get('title_s') else ''
                            abstract = doc.get('abstract_s', [''])[0] if doc.get('abstract_s') else ''
                            uri = doc.get('uri_s', [''])[0] if doc.get('uri_s') else ''
                            submitted = doc.get('submittedDate_s', [''])[0] if doc.get('submittedDate_s') else ''
                            
                            if title and abstract:
                                full_text = title + " " + abstract
                                content_hash = hashlib.md5(full_text.encode()).hexdigest()
                                
                                # Analyse contenu
                                language = self.detect_language(full_text)
                                math_analysis = self.analyze_mathematical_content(full_text)
                                
                                paper = {
                                    'id': content_hash[:12],  # ID unique basé sur contenu
                                    'title': title,
                                    'abstract': abstract,
                                    'source': 'hal',
                                    'language': language,
                                    'mathematical_analysis': math_analysis,
                                    'content_hash': content_hash,
                                    'url': uri,
                                    'submitted_date': submitted,
                                    'collection_timestamp': time.time(),
                                    'content_length': len(full_text)
                                }
                                
                                papers.append(paper)
                    else:
                        print(f"    Erreur HAL API: {response.status}")
        
        except Exception as e:
            print(f"    Erreur lors de la collecte HAL: {e}")
        
        await asyncio.sleep(self.request_delay)
        return papers
    
    async def collect_scientific_corpus(self) -> List[Dict]:
        """Collecte corpus scientifique français depuis HAL"""
        
        print("Collecte corpus scientifique français (HAL)")
        print("=" * 50)
        
        # Domaines mathématiques et scientifiques en français
        queries = [
            'mathématiques OR "analyse mathématique"',
            'informatique OR "intelligence artificielle"',
            'physique OR "mécanique quantique"',
            'chimie OR "chimie quantique"',
            'biologie OR "bioinformatique"',
            '"théorie des nombres" OR "algèbre"',
            '"géométrie" OR "topologie"',
            '"logique mathématique" OR "théorie des ensembles"'
        ]
        
        all_papers = []
        
        for query in queries:
            print(f"\nRequête: {query}")
            papers = await self.collect_hal_batch(query, max_papers=25)
            all_papers.extend(papers)
            
            # Mise à jour statistiques
            for paper in papers:
                lang = paper['language']
                self.language_stats[lang] = self.language_stats.get(lang, 0) + 1
        
        # Déduplication basée sur hash contenu
        unique_papers = {}
        for paper in all_papers:
            content_hash = paper['content_hash']
            if content_hash not in unique_papers:
                unique_papers[content_hash] = paper
        
        final_papers = list(unique_papers.values())
        
        print(f"\nCollecte terminée:")
        print(f"  Total brut: {len(all_papers)}")
        print(f"  Après déduplication: {len(final_papers)}")
        print(f"  Langues détectées: {self.language_stats}")
        
        return final_papers
    
    def save_corpus(self, papers: List[Dict]):
        """Sauvegarde du corpus collecté"""
        # Sauvegarde principale
        output_file = os.path.join(self.output_dir, 'corpus_hal_french.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        # Résumé
        summary_file = os.path.join(self.output_dir, 'corpus_hal_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("Corpus HAL Collection Summary\\n")
            f.write("================================\\n\\n")
            f.write(f"Collection Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"Total Papers: {len(papers)}\\n\\n")
            
            f.write("Sample Papers:\\n\\n")
            for i, paper in enumerate(papers[:5]):
                f.write(f"{i+1}. {paper['title']}\\n")
                f.write(f"   Language: {paper['language']}\\n")
                f.write(f"   Math density: {paper['mathematical_analysis']['math_density']:.3f}\\n\\n")
        
        print(f"Corpus sauvegardé: {output_file}")
        print(f"Résumé: {summary_file}")


async def main():
    """Fonction principale de collecte HAL"""
    
    # Configuration
    output_dir = './corpus_hal'
    
    # Création collecteur
    collector = HALCorpusCollector(output_dir)
    
    # Collecte corpus
    papers = await collector.collect_scientific_corpus()
    
    # Sauvegarde
    collector.save_corpus(papers)
    
    print(f"\nMission HAL terminée: {len(papers)} articles français collectés")
    return papers


if __name__ == "__main__":
    # Lancement collection HAL
    corpus = asyncio.run(main())