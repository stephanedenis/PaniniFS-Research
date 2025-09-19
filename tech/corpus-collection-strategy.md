# Multilingual Scientific Corpus Collection Strategy

## Target Corpus Characteristics

### 1. **Mathematical Content Requirements**
- Heavy use of mathematical notation (LaTeX, Unicode symbols)
- Cross-domain mathematical concepts (algebra, analysis, geometry, statistics)
- Multiple representation formats (symbolic, textual, visual descriptions)
- Proof structures and logical reasoning patterns

### 2. **Multilingual Coverage**
- **Primary**: English, French, German, Spanish, Italian, Russian
- **Secondary**: Chinese, Japanese, Arabic, Hindi
- **Mathematical dialects**: Different notation conventions by region

### 3. **Domain Distribution**
- Pure Mathematics: 30%
- Physics: 25% 
- Computer Science: 20%
- Chemistry: 15%
- Biology/Bioinformatics: 10%

---

## Corpus Sources (Accessible & Verifiable)

### A. **ArXiv.org - Open Access Scientific Papers**
```bash
# Mathematics categories
cs.AI, cs.CL, cs.LG, cs.CC    # Computer Science
math.AG, math.NT, math.LO     # Pure Mathematics  
physics.gen-ph, quant-ph      # Physics
q-bio.QM, q-bio.BM           # Quantitative Biology
```

**Collection Strategy:**
```python
import arxiv
import requests
from pathlib import Path

def collect_arxiv_papers(categories, max_per_category=100):
    papers = []
    for category in categories:
        search = arxiv.Search(
            query=f"cat:{category}",
            max_results=max_per_category,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        for paper in search.results():
            papers.append({
                'id': paper.get_short_id(),
                'title': paper.title,
                'abstract': paper.summary,
                'pdf_url': paper.pdf_url,
                'categories': paper.categories,
                'language': detect_language(paper.title + paper.summary)
            })
    return papers
```

### B. **HAL (Hyper Articles en Ligne) - French Academic Repository**
```python
def collect_hal_papers():
    # French scientific papers with mathematical content
    # API: https://api.archives-ouvertes.fr/search/
    hal_query = {
        'q': 'mathematics OR physique OR informatique',
        'fq': 'language_s:fr',
        'rows': 1000,
        'fl': 'title_s,abstract_s,uri_s,docType_s'
    }
```

### C. **DBLP - Computer Science Bibliography** 
```python
def collect_dblp_papers():
    # Multilingual computer science papers
    # Focus on theoretical CS with mathematical content
    venues = [
        'STOC', 'FOCS', 'ICALP', 'LICS',  # Theory
        'ICML', 'NeurIPS', 'ICLR',        # ML (heavy math)
        'CCC', 'ITCS'                     # Complexity
    ]
```

### D. **Semantic Scholar - Cross-disciplinary**
```python
def collect_semantic_scholar():
    # Multilingual scientific corpus
    # API with good metadata and citation graphs
    fields = [
        'Mathematics', 'Physics', 'Computer Science',
        'Chemistry', 'Biology'
    ]
```

### E. **Wikipedia Scientific Articles**
```python
def collect_wikipedia_scientific():
    # Mathematics articles in multiple languages
    # Good for terminology comparison across languages
    math_categories = [
        'Category:Mathematics',
        'Category:Mathematical_analysis', 
        'Category:Algebra',
        'Category:Mathematical_logic'
    ]
    languages = ['en', 'fr', 'de', 'es', 'it', 'ru', 'zh', 'ja']
```

---

## Specialized Mathematical Notation Sources

### A. **MathOverflow & Math Stack Exchange**
```python
def collect_math_forums():
    # Rich mathematical discourse with informal language
    # Heavy LaTeX usage and multiple explanation styles
    # Question-answer format with ambiguity resolution
    
    # Stack Exchange Data Dump: https://archive.org/details/stackexchange
    sites = [
        'math.stackexchange.com',
        'mathoverflow.net',
        'physics.stackexchange.com',
        'cs.stackexchange.com'
    ]
```

### B. **Mathematical Journals (Open Access)**
```python
def collect_math_journals():
    journals = [
        'PLOS ONE',           # Multidisciplinary 
        'eLife',              # Biology with math models
        'Nature Communications', # Cross-disciplinary
        'Journal of Statistical Software', # Statistics/computing
    ]
```

### C. **Mathematical Encyclopedia/Reference**
```python
def collect_math_references():
    sources = [
        'Encyclopedia of Mathematics (SpringerLink)',
        'PlanetMath.org',
        'MathWorld (Wolfram)',
        'nLab (Category Theory wiki)'
    ]
```

---

## Collection Implementation

### Phase 1: Automated Collection Script
```python
#!/usr/bin/env python3
"""
Scientific Corpus Collector for Enhanced Dhātu Analysis
"""

import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import json
import time

class ScientificCorpusCollector:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        
        # Metadata tracking
        self.collected_papers = []
        self.language_stats = {}
        self.domain_stats = {}
        
    async def collect_arxiv_batch(self, category: str, max_papers: int = 100):
        """Collect papers from ArXiv for specific category"""
        papers = []
        
        # ArXiv API query
        query_url = f"http://export.arxiv.org/api/query"
        params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_papers,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(query_url, params=params) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    papers = self.parse_arxiv_xml(xml_content)
                    
        await asyncio.sleep(self.request_delay)
        return papers
    
    def parse_arxiv_xml(self, xml_content: str) -> List[Dict]:
        """Parse ArXiv API XML response"""
        import xml.etree.ElementTree as ET
        
        papers = []
        root = ET.fromstring(xml_content)
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper = {
                'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'abstract': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'categories': [cat.get('term') for cat in entry.findall('{http://arxiv.org/schemas/atom}category')],
                'source': 'arxiv'
            }
            papers.append(paper)
            
        return papers
    
    async def collect_all_sources(self):
        """Orchestrate collection from all sources"""
        
        print("🔬 Starting scientific corpus collection...")
        
        # ArXiv categories to collect
        arxiv_categories = [
            'math.LO',   # Mathematical Logic
            'math.AG',   # Algebraic Geometry  
            'math.NT',   # Number Theory
            'cs.AI',     # Artificial Intelligence
            'cs.CL',     # Computational Linguistics
            'cs.LG',     # Machine Learning
            'physics.gen-ph',  # General Physics
            'quant-ph',  # Quantum Physics
            'q-bio.QM'   # Quantitative Methods in Biology
        ]
        
        all_papers = []
        
        for category in arxiv_categories:
            print(f"📚 Collecting from ArXiv category: {category}")
            papers = await self.collect_arxiv_batch(category, max_papers=50)
            all_papers.extend(papers)
            
            # Update statistics
            for paper in papers:
                lang = self.detect_language(paper['title'] + ' ' + paper['abstract'])
                self.language_stats[lang] = self.language_stats.get(lang, 0) + 1
                
                domain = self.categorize_domain(paper['categories'])
                self.domain_stats[domain] = self.domain_stats.get(domain, 0) + 1
        
        # Save collected corpus
        self.save_corpus(all_papers)
        self.save_metadata()
        
        print(f"✅ Collection complete: {len(all_papers)} papers collected")
        return all_papers
    
    def detect_language(self, text: str) -> str:
        """Detect language of text content"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'unknown'
    
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
        else:
            return 'interdisciplinary'
    
    def save_corpus(self, papers: List[Dict]):
        """Save collected papers to JSON file"""
        corpus_file = self.output_dir / 'scientific_corpus.json'
        with open(corpus_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Corpus saved to: {corpus_file}")
    
    def save_metadata(self):
        """Save collection metadata and statistics"""
        metadata = {
            'collection_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_papers': len(self.collected_papers),
            'language_distribution': self.language_stats,
            'domain_distribution': self.domain_stats,
            'sources': ['arxiv'],
            'collection_parameters': {
                'max_papers_per_category': 50,
                'request_delay': self.request_delay
            }
        }
        
        metadata_file = self.output_dir / 'collection_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Metadata saved to: {metadata_file}")

# Usage
async def main():
    collector = ScientificCorpusCollector(Path('./corpus'))
    corpus = await collector.collect_all_sources()
    return corpus

# Run collection
if __name__ == "__main__":
    asyncio.run(main())
```

---

## Expected Corpus Statistics

### Size Estimates
```
Small pilot corpus: 500 papers
- ArXiv: 450 papers (9 categories × 50 papers)
- Other sources: 50 papers
- Total text: ~50MB
- Processing time: ~2 hours

Medium corpus: 5000 papers  
- ArXiv: 4000 papers (20 categories × 200 papers)
- HAL (French): 500 papers
- Wikipedia: 300 articles
- Math forums: 200 discussions
- Total text: ~500MB
- Processing time: ~20 hours

Large corpus: 50000 papers
- Full ArXiv mathematical corpus
- Multiple language sources
- Total text: ~5GB
- Processing time: ~200 hours
```

### Language Distribution (Expected)
```
English: 70%
French: 8%
German: 6%
Spanish: 4%
Italian: 3%
Russian: 3%
Chinese: 2%
Japanese: 2%
Other: 2%
```

### Mathematical Notation Density
```
LaTeX commands per paper: 50-500
Unicode math symbols per paper: 20-200
Equations per paper: 5-50
Theorem/Proof structures: 1-20
```

---

## Quality Assurance

### Validation Criteria
1. **Mathematical content**: Minimum 10 mathematical symbols/formulas per document
2. **Language detection**: Confidence > 0.8 for primary language
3. **Duplicate detection**: Cosine similarity < 0.9 between documents
4. **Length requirements**: 500-50000 characters per document
5. **Encoding validation**: Valid UTF-8 with mathematical Unicode

### Manual Review Sample
- Manually review 100 random papers (2% of pilot corpus)
- Validate mathematical notation parsing
- Check ambiguity detection accuracy
- Verify multilingual equivalence detection

This corpus collection strategy will provide a robust, verifiable dataset for testing the enhanced dhātu algorithm on real scientific content with mathematical notation and multilingual complexity.