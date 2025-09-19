#!/usr/bin/env python3
"""
Simple Scientific Corpus Collector - Fixed Version
"""

import asyncio
import aiohttp
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict
import hashlib
import re

class CorpusCollector:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.request_delay = 2.0
        
    def detect_language(self, text: str) -> str:
        text_lower = text.lower()
        english_words = ['the', 'and', 'of', 'to', 'a', 'in', 'that', 'is']
        french_words = ['le', 'de', 'et', 'des', 'les', 'dans', 'pour', 'une']
        
        english_score = sum(1 for word in english_words if word in text_lower)
        french_score = sum(1 for word in french_words if word in text_lower)
        
        return 'en' if english_score > french_score else 'fr'
    
    def analyze_math_content(self, text: str) -> Dict[str, int]:
        latex_commands = len(re.findall(r'\\[a-zA-Z]+', text))
        unicode_math = len(re.findall(r'[∀∃∈∉∧∨¬→↔∑∏∫∂∇±×÷≤≥≠≡∞]', text))
        equations = len(re.findall(r'\$[^$]+\$', text))
        
        word_count = len(text.split())
        total_math = latex_commands + unicode_math + equations
        
        return {
            'latex_commands': latex_commands,
            'unicode_math': unicode_math,
            'equations': equations,
            'math_density': total_math / max(word_count, 1)
        }
    
    async def collect_arxiv(self, category: str, max_papers: int = 10) -> List[Dict]:
        papers = []
        
        url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_papers,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        xml_content = await response.text()
                        papers = self.parse_xml(xml_content, category)
                        print(f"✅ Collected {len(papers)} papers from {category}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        await asyncio.sleep(self.request_delay)
        return papers
    
    def parse_xml(self, xml_content: str, category: str) -> List[Dict]:
        papers = []
        
        try:
            root = ET.fromstring(xml_content)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            print(f"  📄 Found {len(entries)} entries")
            
            for i, entry in enumerate(entries):
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                
                if title_elem is None or summary_elem is None or id_elem is None:
                    continue
                
                title = title_elem.text.strip() if title_elem.text else ""
                abstract = summary_elem.text.strip() if summary_elem.text else ""
                paper_id = id_elem.text if id_elem.text else ""
                
                if not title or not abstract:
                    continue
                
                arxiv_id = paper_id.split('/')[-1] if '/' in paper_id else paper_id
                full_text = title + " " + abstract
                
                # Get categories
                cat_elems = entry.findall('{http://arxiv.org/schemas/atom}category')
                categories = [cat.get('term') for cat in cat_elems if cat.get('term')]
                
                # Analyze content
                language = self.detect_language(full_text)
                math_analysis = self.analyze_math_content(full_text)
                
                paper = {
                    'id': arxiv_id,
                    'title': title,
                    'abstract': abstract,
                    'categories': categories,
                    'primary_category': category,
                    'language': language,
                    'mathematical_analysis': math_analysis,
                    'content_hash': hashlib.md5(full_text.encode()).hexdigest(),
                    'url': f"https://arxiv.org/abs/{arxiv_id}",
                    'content_length': len(full_text)
                }
                
                papers.append(paper)
                
                # Debug first paper
                if i == 0:
                    print(f"  📝 Sample: {title[:50]}...")
                    print(f"     Math density: {math_analysis['math_density']:.4f}")
        
        except Exception as e:
            print(f"❌ XML parsing error: {e}")
        
        return papers
    
    async def collect_corpus(self) -> List[Dict]:
        print("🔬 Starting corpus collection...")
        
        categories = ['math.LO', 'math.NT', 'cs.AI', 'cs.LG', 'quant-ph']
        all_papers = []
        
        for category in categories:
            print(f"📚 Collecting from {category}")
            papers = await self.collect_arxiv(category, max_papers=5)
            all_papers.extend(papers)
        
        # Remove duplicates
        unique_papers = {}
        for paper in all_papers:
            content_hash = paper['content_hash']
            if content_hash not in unique_papers:
                unique_papers[content_hash] = paper
        
        final_papers = list(unique_papers.values())
        
        # Save results
        self.save_corpus(final_papers)
        
        print(f"✅ Total collected: {len(final_papers)} unique papers")
        return final_papers
    
    def save_corpus(self, papers: List[Dict]):
        corpus_file = self.output_dir / 'corpus.json'
        
        with open(corpus_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {corpus_file}")
        
        # Save summary
        summary_file = self.output_dir / 'summary.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Corpus Collection Summary\n")
            f.write(f"========================\n\n")
            f.write(f"Total papers: {len(papers)}\n\n")
            
            for i, paper in enumerate(papers[:3]):
                f.write(f"{i+1}. {paper['title']}\n")
                f.write(f"   Category: {paper['primary_category']}\n")
                f.write(f"   Math density: {paper['mathematical_analysis']['math_density']:.3f}\n\n")

async def main():
    collector = CorpusCollector(Path('./corpus_simple'))
    corpus = await collector.collect_corpus()
    return corpus

if __name__ == "__main__":
    corpus = asyncio.run(main())