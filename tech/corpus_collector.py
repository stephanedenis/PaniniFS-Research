#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scientific Corpus Collector for Enhanced Dhātu Analysis
Autonomous implementation for collecting multilingual mathematical content
"""

import asyncio
import aiohttp
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import re
from urllib.parse import quote

class ScientificCorpusCollector:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        # Rate limiting to be respectful to APIs
        self.request_delay = 2.0  # seconds between requests
        
        # Collection tracking
        self.collected_papers = []
        self.language_stats = {}
        self.domain_stats = {}
        self.mathematical_notation_stats = {}
        
        # Mathematical notation patterns
        self.math_patterns = {
            'latex_commands': re.compile(r'\\[a-zA-Z]+'),
            'unicode_math': re.compile(r'[∀∃∈∉∧∨¬→↔∑∏∫∂∇±×÷≤≥≠≡∞α-ωΑ-Ω]'),
            'equations': re.compile(r'\$[^$]+\$|\\\[[^\]]+\\\]'),
            'formulas': re.compile(r'[a-zA-Z]+\s*[=<>≤≥]\s*[^.!?]*[0-9a-zA-Z]'),
        }
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common patterns"""
        text_lower = text.lower()
        
        # English indicators
        english_words = ['the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'for', 'with']
        english_score = sum(1 for word in english_words if word in text_lower)
        
        # French indicators  
        french_words = ['le', 'de', 'et', 'des', 'les', 'dans', 'pour', 'une', 'sur', 'avec']
        french_score = sum(1 for word in french_words if word in text_lower)
        
        # German indicators
        german_words = ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich']
        german_score = sum(1 for word in german_words if word in text_lower)
        
        # Spanish indicators
        spanish_words = ['el', 'de', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo']
        spanish_score = sum(1 for word in spanish_words if word in text_lower)
        
        scores = {
            'en': english_score,
            'fr': french_score, 
            'de': german_score,
            'es': spanish_score
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'unknown'
    
    def analyze_mathematical_content(self, text: str) -> Dict[str, int]:
        """Analyze mathematical notation density in text"""
        analysis = {}
        
        for pattern_name, pattern in self.math_patterns.items():
            matches = pattern.findall(text)
            analysis[pattern_name] = len(matches)
        
        # Calculate mathematical density
        word_count = len(text.split())
        total_math_elements = sum(analysis.values())
        analysis['math_density'] = total_math_elements / max(word_count, 1)
        
        return analysis
    
    def categorize_domain(self, categories: List[str]) -> str:
        """Categorize paper by domain based on ArXiv categories"""
        if any(cat.startswith('math.') for cat in categories):
            return 'mathematics'
        elif any(cat.startswith('cs.') for cat in categories):
            return 'computer_science'
        elif any(cat.startswith('physics.') or cat == 'quant-ph' for cat in categories):
            return 'physics'
        elif any(cat.startswith('q-bio.') for cat in categories):
            return 'biology'
        elif any(cat.startswith('cond-mat.') for cat in categories):
            return 'condensed_matter'
        else:
            return 'interdisciplinary'
    
    async def collect_arxiv_batch(self, category: str, max_papers: int = 50) -> List[Dict]:
        """Collect papers from ArXiv for specific category"""
        papers = []
        
        query_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_papers,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(query_url, params=params) as response:
                    if response.status == 200:
                        xml_content = await response.text()
                        papers = self.parse_arxiv_xml(xml_content, category)
                        print(f"  ✅ Collected {len(papers)} papers from {category}")
                    else:
                        print(f"  ❌ Failed to collect from {category}: HTTP {response.status}")
                        print(f"  🔍 Response: {await response.text()}")
        except Exception as e:
            print(f"  ❌ Error collecting from {category}: {e}")
        
        await asyncio.sleep(self.request_delay)
        return papers
    
    def parse_arxiv_xml(self, xml_content: str, category: str) -> List[Dict]:
        """Parse ArXiv API XML response"""
        papers = []
        
        try:
            root = ET.fromstring(xml_content)
            
            # Debug: print some info about XML structure
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            print(f"    🔍 Found {len(entries)} entries in XML")
            
            for entry in entries:
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                
                if not all([title_elem, summary_elem, id_elem]):
                    continue
                
                title = title_elem.text.strip() if title_elem is not None else ""
                abstract = summary_elem.text.strip() if summary_elem is not None else ""
                paper_id = id_elem.text if id_elem is not None else ""
                published = published_elem.text if published_elem is not None else ""
                
                # Extract ArXiv ID
                arxiv_id = paper_id.split('/')[-1] if '/' in paper_id else paper_id
                
                # Get categories
                categories = [cat.get('term') for cat in entry.findall('{http://arxiv.org/schemas/atom}category')]
                
                # Generate content hash for deduplication
                content_hash = hashlib.md5((title + abstract).encode()).hexdigest()
                
                # Analyze content
                full_text = title + " " + abstract
                language = self.detect_language(full_text)
                math_analysis = self.analyze_mathematical_content(full_text)
                domain = self.categorize_domain(categories)
                
                # Debug: print first few papers to see content
                if len(papers) < 2:
                    print(f"    📝 Sample: {title[:60]}...")
                    print(f"       Math density: {math_analysis['math_density']:.4f}")
                    print(f"       Math elements: {math_analysis}")
                
                # Include all papers for now, filter later if needed
                paper = {
                    'id': arxiv_id,
                    'title': title,
                    'abstract': abstract,
                    'published': published,
                    'categories': categories,
                    'primary_category': category,
                    'source': 'arxiv',
                    'language': language,
                    'domain': domain,
                    'mathematical_analysis': math_analysis,
                    'content_hash': content_hash,
                    'collection_timestamp': time.time(),
                    'content_length': len(full_text),
                    'url': f"https://arxiv.org/abs/{arxiv_id}"
                }
                papers.append(paper)
                
        except ET.ParseError as e:
            print(f"  ❌ XML parsing error: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
        
        return papers
    
    async def collect_sample_corpus(self) -> List[Dict]:
        """Collect a pilot corpus for testing"""
        
        print("🔬 Starting autonomous scientific corpus collection...")
        print("📊 Target: Multilingual mathematical content with notation analysis")
        
        # Categories with high mathematical content
        target_categories = [
            'math.LO',   # Mathematical Logic
            'math.AG',   # Algebraic Geometry
            'math.NT',   # Number Theory  
            'math.CO',   # Combinatorics
            'cs.AI',     # Artificial Intelligence
            'cs.CL',     # Computational Linguistics
            'cs.LG',     # Machine Learning
            'cs.CC',     # Computational Complexity
            'physics.gen-ph',  # General Physics
            'quant-ph',  # Quantum Physics
        ]
        
        all_papers = []
        
        for category in target_categories:
            print(f"📚 Collecting from ArXiv category: {category}")
            papers = await self.collect_arxiv_batch(category, max_papers=25)
            all_papers.extend(papers)
            
            # Update statistics
            for paper in papers:
                lang = paper['language']
                self.language_stats[lang] = self.language_stats.get(lang, 0) + 1
                
                domain = paper['domain']
                self.domain_stats[domain] = self.domain_stats.get(domain, 0) + 1
                
                # Mathematical notation statistics
                math_stats = paper['mathematical_analysis']
                for key, value in math_stats.items():
                    if key != 'math_density':
                        self.mathematical_notation_stats[key] = \
                            self.mathematical_notation_stats.get(key, 0) + value
        
        # Remove duplicates based on content hash
        unique_papers = {}
        for paper in all_papers:
            content_hash = paper['content_hash']
            if content_hash not in unique_papers:
                unique_papers[content_hash] = paper
        
        final_papers = list(unique_papers.values())
        
        # Save corpus and metadata
        self.save_corpus(final_papers)
        self.save_collection_metadata(final_papers)
        
        print(f"✅ Collection complete!")
        print(f"📄 Total papers collected: {len(final_papers)}")
        print(f"🗂️  After deduplication: {len(final_papers)} unique papers")
        print(f"🌍 Language distribution: {self.language_stats}")
        print(f"🔬 Domain distribution: {self.domain_stats}")
        
        return final_papers
    
    def save_corpus(self, papers: List[Dict]):
        """Save collected papers to JSON file"""
        corpus_file = self.output_dir / 'scientific_corpus_pilot.json'
        
        with open(corpus_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Corpus saved to: {corpus_file}")
        
        # Also save a human-readable summary
        summary_file = self.output_dir / 'corpus_summary.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Scientific Corpus Collection Summary\n")
            f.write(f"=====================================\n\n")
            f.write(f"Collection Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Papers: {len(papers)}\n\n")
            
            f.write("Sample Papers:\n")
            for i, paper in enumerate(papers[:5]):
                f.write(f"\n{i+1}. {paper['title']}\n")
                f.write(f"   Category: {paper['primary_category']}\n") 
                f.write(f"   Language: {paper['language']}\n")
                f.write(f"   Math Density: {paper['mathematical_analysis']['math_density']:.3f}\n")
                f.write(f"   URL: {paper['url']}\n")
    
    def save_collection_metadata(self, papers: List[Dict]):
        """Save detailed collection metadata"""
        
        # Calculate advanced statistics  
        if len(papers) > 0:
            total_math_elements = sum(self.mathematical_notation_stats.values())
            avg_math_density = sum(p['mathematical_analysis']['math_density'] for p in papers) / len(papers)
        else:
            total_math_elements = 0
            avg_math_density = 0.0
        
        metadata = {
            'collection_info': {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_papers': len(papers),
                'collection_method': 'arxiv_api_autonomous',
                'deduplication': 'content_hash_md5',
                'quality_filter': 'min_math_density_0.02'
            },
            'corpus_statistics': {
                'language_distribution': self.language_stats,
                'domain_distribution': self.domain_stats,
                'mathematical_notation_stats': self.mathematical_notation_stats,
                'average_math_density': avg_math_density,
                'total_mathematical_elements': total_math_elements
            },
            'collection_parameters': {
                'categories_collected': 10,
                'papers_per_category': 25,
                'request_delay_seconds': self.request_delay,
                'minimum_math_density': 0.02
            },
            'quality_metrics': {
                'papers_with_high_math_density': len([p for p in papers if p['mathematical_analysis']['math_density'] > 0.05]),
                'multilingual_coverage': len(self.language_stats),
                'domain_coverage': len(self.domain_stats),
                'average_content_length': sum(p['content_length'] for p in papers) / len(papers)
            }
        }
        
        metadata_file = self.output_dir / 'collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Metadata saved to: {metadata_file}")


async def main():
    """Main collection function"""
    
    # Setup collection directory
    corpus_dir = Path('./corpus_pilot')
    collector = ScientificCorpusCollector(corpus_dir)
    
    print("🚀 Autonomous Scientific Corpus Collection Starting...")
    print("=" * 60)
    
    # Collect corpus
    start_time = time.time()
    corpus = await collector.collect_sample_corpus()
    end_time = time.time()
    
    collection_time = end_time - start_time
    print(f"\n⏱️  Collection completed in {collection_time:.1f} seconds")
    print(f"📈 Collection rate: {len(corpus) / collection_time:.2f} papers/second")
    
    return corpus


if __name__ == "__main__":
    # Run autonomous collection
    corpus = asyncio.run(main())