#!/usr/bin/env python3
"""
Mathematical Notation Parser for Scientific Content
Specialized parser for LaTeX, Unicode math, and scientific notation
"""

import re
import json
from typing import Dict, List, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class NotationType(Enum):
    LATEX_COMMAND = "latex_command"
    UNICODE_SYMBOL = "unicode_symbol"
    ASCII_MATH = "ascii_math"
    EQUATION_BLOCK = "equation_block"
    INLINE_MATH = "inline_math"
    FORMULA_REFERENCE = "formula_reference"

class MathDomain(Enum):
    ALGEBRA = "algebra"
    ANALYSIS = "analysis"
    GEOMETRY = "geometry"
    LOGIC = "logic"
    STATISTICS = "statistics"
    PHYSICS = "physics"
    COMPUTER_SCIENCE = "computer_science"
    GENERAL = "general"

@dataclass
class MathNotation:
    notation: str
    type: NotationType
    domain: MathDomain
    dhatu_mapping: List[str]
    semantic_weight: float
    context_clues: List[str]

@dataclass
class ParsedMathContent:
    original_text: str
    notations: List[MathNotation]
    complexity_score: float
    domain_distribution: Dict[MathDomain, float]
    dhatu_mappings: Dict[str, float]

class MathNotationParser:
    def __init__(self):
        self.notation_database = self._build_notation_database()
        self.pattern_cache = self._compile_patterns()
        
    def _build_notation_database(self) -> Dict[str, MathNotation]:
        """Build comprehensive database of mathematical notations"""
        
        notations = {}
        
        # Logical operators and quantifiers - map to MODAL, EXIST, DECIDE
        logical_notations = [
            ("∀", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["EXIST", "MODAL"], 0.9, ["universal", "for all"]),
            ("∃", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["EXIST", "MODAL"], 0.9, ["existential", "there exists"]),
            ("∄", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["EXIST", "MODAL"], 0.8, ["does not exist"]),
            ("¬", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["MODAL", "DECIDE"], 0.8, ["negation", "not"]),
            ("∧", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["RELATE", "DECIDE"], 0.7, ["and", "conjunction"]),
            ("∨", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["RELATE", "DECIDE"], 0.7, ["or", "disjunction"]),
            ("→", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["CAUSE", "RELATE"], 0.8, ["implies", "if then"]),
            ("↔", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["RELATE", "MODAL"], 0.8, ["iff", "equivalence"]),
            ("⟹", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["CAUSE", "RELATE"], 0.8, ["implies"]),
            ("⟺", NotationType.UNICODE_SYMBOL, MathDomain.LOGIC, ["RELATE", "MODAL"], 0.8, ["if and only if"]),
        ]
        
        # Set theory and relations - map to RELATE, EXIST
        set_notations = [
            ("∈", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE", "EXIST"], 0.9, ["element of", "belongs to"]),
            ("∉", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE", "EXIST"], 0.8, ["not element of"]),
            ("⊂", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.8, ["subset", "contained in"]),
            ("⊃", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.8, ["superset", "contains"]),
            ("⊆", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.8, ["subset or equal"]),
            ("⊇", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.8, ["superset or equal"]),
            ("∪", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.7, ["union"]),
            ("∩", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["RELATE"], 0.7, ["intersection"]),
            ("∅", NotationType.UNICODE_SYMBOL, MathDomain.ALGEBRA, ["EXIST"], 0.7, ["empty set", "null"]),
        ]
        
        # Comparison and equality - map to EVAL, RELATE  
        comparison_notations = [
            ("=", NotationType.ASCII_MATH, MathDomain.GENERAL, ["EVAL", "RELATE"], 0.9, ["equals", "is"]),
            ("≠", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["EVAL", "RELATE"], 0.8, ["not equal"]),
            ("≈", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["EVAL", "RELATE"], 0.7, ["approximately equal"]),
            ("≡", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["RELATE"], 0.8, ["equivalent", "identical"]),
            ("≅", NotationType.UNICODE_SYMBOL, MathDomain.GEOMETRY, ["RELATE"], 0.8, ["congruent", "isomorphic"]),
            ("∼", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["RELATE"], 0.7, ["similar", "related"]),
            ("<", NotationType.ASCII_MATH, MathDomain.GENERAL, ["EVAL"], 0.8, ["less than"]),
            (">", NotationType.ASCII_MATH, MathDomain.GENERAL, ["EVAL"], 0.8, ["greater than"]),
            ("≤", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["EVAL"], 0.8, ["less than or equal"]),
            ("≥", NotationType.UNICODE_SYMBOL, MathDomain.GENERAL, ["EVAL"], 0.8, ["greater than or equal"]),
        ]
        
        # Calculus and analysis - map to ITER, CAUSE, EVAL
        calculus_notations = [
            ("∫", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["integral", "integration"]),
            ("∑", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["sum", "summation"]),
            ("∏", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["product"]),
            ("∂", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["CAUSE", "EVAL"], 0.8, ["partial derivative"]),
            ("∇", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["CAUSE", "EVAL"], 0.8, ["gradient", "del"]),
            ("∞", NotationType.UNICODE_SYMBOL, MathDomain.ANALYSIS, ["MODAL", "EXIST"], 0.7, ["infinity"]),
            ("lim", NotationType.ASCII_MATH, MathDomain.ANALYSIS, ["MODAL", "EVAL"], 0.8, ["limit"]),
        ]
        
        # Probability and statistics - map to MODAL, EVAL, FEEL
        stats_notations = [
            ("ℙ", NotationType.UNICODE_SYMBOL, MathDomain.STATISTICS, ["MODAL", "EVAL"], 0.8, ["probability"]),
            ("𝔼", NotationType.UNICODE_SYMBOL, MathDomain.STATISTICS, ["EVAL", "FEEL"], 0.8, ["expectation"]),
            ("Var", NotationType.ASCII_MATH, MathDomain.STATISTICS, ["EVAL", "FEEL"], 0.7, ["variance"]),
            ("σ", NotationType.UNICODE_SYMBOL, MathDomain.STATISTICS, ["EVAL"], 0.7, ["standard deviation"]),
            ("μ", NotationType.UNICODE_SYMBOL, MathDomain.STATISTICS, ["EVAL"], 0.7, ["mean"]),
            ("∝", NotationType.UNICODE_SYMBOL, MathDomain.STATISTICS, ["RELATE"], 0.7, ["proportional to"]),
        ]
        
        # Physics notations - map to CAUSE, EVAL, EXIST
        physics_notations = [
            ("ℏ", NotationType.UNICODE_SYMBOL, MathDomain.PHYSICS, ["EXIST"], 0.8, ["reduced Planck constant"]),
            ("∆", NotationType.UNICODE_SYMBOL, MathDomain.PHYSICS, ["CAUSE", "EVAL"], 0.8, ["change", "delta"]),
            ("ψ", NotationType.UNICODE_SYMBOL, MathDomain.PHYSICS, ["EXIST"], 0.7, ["wave function"]),
            ("φ", NotationType.UNICODE_SYMBOL, MathDomain.PHYSICS, ["EXIST"], 0.7, ["phase", "field"]),
        ]
        
        # LaTeX commands
        latex_notations = [
            (r"\\forall", NotationType.LATEX_COMMAND, MathDomain.LOGIC, ["EXIST", "MODAL"], 0.9, ["universal quantifier"]),
            (r"\\exists", NotationType.LATEX_COMMAND, MathDomain.LOGIC, ["EXIST", "MODAL"], 0.9, ["existential quantifier"]),
            (r"\\int", NotationType.LATEX_COMMAND, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["integral"]),
            (r"\\sum", NotationType.LATEX_COMMAND, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["summation"]),
            (r"\\prod", NotationType.LATEX_COMMAND, MathDomain.ANALYSIS, ["ITER", "EVAL"], 0.9, ["product"]),
            (r"\\lim", NotationType.LATEX_COMMAND, MathDomain.ANALYSIS, ["MODAL", "EVAL"], 0.8, ["limit"]),
            (r"\\partial", NotationType.LATEX_COMMAND, MathDomain.ANALYSIS, ["CAUSE", "EVAL"], 0.8, ["partial derivative"]),
        ]
        
        # Combine all notations
        all_notations = (logical_notations + set_notations + comparison_notations + 
                        calculus_notations + stats_notations + physics_notations + latex_notations)
        
        # Build database
        for notation, type_enum, domain, dhatus, weight, clues in all_notations:
            notations[notation] = MathNotation(
                notation=notation,
                type=type_enum,
                domain=domain,
                dhatu_mapping=dhatus,
                semantic_weight=weight,
                context_clues=clues
            )
        
        return notations
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for efficient matching"""
        
        patterns = {}
        
        # LaTeX patterns
        patterns['latex_command'] = re.compile(r'\\[a-zA-Z]+(?:\*)?')
        patterns['latex_environment'] = re.compile(r'\\begin\{([^}]+)\}.*?\\end\{\1\}', re.DOTALL)
        patterns['latex_inline'] = re.compile(r'\$([^$]+)\$')
        patterns['latex_display'] = re.compile(r'\$\$([^$]+)\$\$')
        patterns['latex_bracket'] = re.compile(r'\\\[([^\]]+)\\\]')
        
        # Unicode math symbols (comprehensive)
        unicode_symbols = ''.join(self.notation_database.keys())
        patterns['unicode_math'] = re.compile(f'[{re.escape(unicode_symbols)}]')
        
        # ASCII mathematical expressions
        patterns['ascii_formula'] = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*\s*[=<>≤≥≠]\s*[^.!?;]*[a-zA-Z0-9)]')
        patterns['ascii_function'] = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)')
        
        # Equation references
        patterns['equation_ref'] = re.compile(r'\(?\s*(?:eq|equation|formula)\s*\.?\s*\(?(\d+)\)?', re.IGNORECASE)
        
        return patterns
    
    def parse_mathematical_content(self, text: str) -> ParsedMathContent:
        """Parse mathematical content from text"""
        
        found_notations = []
        
        # Find LaTeX commands
        for match in self.pattern_cache['latex_command'].finditer(text):
            command = match.group(0)
            if command in self.notation_database:
                notation = self.notation_database[command]
                found_notations.append(notation)
        
        # Find Unicode math symbols
        for match in self.pattern_cache['unicode_math'].finditer(text):
            symbol = match.group(0)
            if symbol in self.notation_database:
                notation = self.notation_database[symbol]
                found_notations.append(notation)
        
        # Find ASCII math operators
        for symbol in ['=', '<', '>']:
            if symbol in text and symbol in self.notation_database:
                notation = self.notation_database[symbol]
                found_notations.append(notation)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity(found_notations, text)
        
        # Calculate domain distribution
        domain_distribution = self._calculate_domain_distribution(found_notations)
        
        # Calculate dhātu mappings
        dhatu_mappings = self._calculate_dhatu_mappings(found_notations)
        
        return ParsedMathContent(
            original_text=text,
            notations=found_notations,
            complexity_score=complexity_score,
            domain_distribution=domain_distribution,
            dhatu_mappings=dhatu_mappings
        )
    
    def _calculate_complexity(self, notations: List[MathNotation], text: str) -> float:
        """Calculate mathematical complexity score"""
        
        if not notations:
            return 0.0
        
        # Base complexity from notation count
        base_complexity = len(notations) / len(text.split()) if text.split() else 0
        
        # Weight by semantic importance
        weighted_complexity = sum(n.semantic_weight for n in notations) / len(notations)
        
        # Domain diversity bonus
        unique_domains = len(set(n.domain for n in notations))
        domain_bonus = min(unique_domains / 3, 1.0)  # Cap at 1.0
        
        total_complexity = (base_complexity + weighted_complexity + domain_bonus) / 3
        return min(total_complexity, 1.0)  # Cap at 1.0
    
    def _calculate_domain_distribution(self, notations: List[MathNotation]) -> Dict[MathDomain, float]:
        """Calculate distribution across mathematical domains"""
        
        if not notations:
            return {}
        
        domain_counts = {}
        total_weight = 0
        
        for notation in notations:
            domain = notation.domain
            weight = notation.semantic_weight
            domain_counts[domain] = domain_counts.get(domain, 0) + weight
            total_weight += weight
        
        # Normalize
        if total_weight > 0:
            return {domain: count / total_weight for domain, count in domain_counts.items()}
        else:
            return {}
    
    def _calculate_dhatu_mappings(self, notations: List[MathNotation]) -> Dict[str, float]:
        """Calculate dhātu activation weights from mathematical notations"""
        
        dhatu_weights = {}
        
        for notation in notations:
            for dhatu in notation.dhatu_mapping:
                weight = notation.semantic_weight / len(notation.dhatu_mapping)  # Split weight among dhātus
                dhatu_weights[dhatu] = dhatu_weights.get(dhatu, 0) + weight
        
        return dhatu_weights
    
    def analyze_scientific_corpus(self, corpus_file: Path) -> Dict[str, Any]:
        """Analyze mathematical notation in scientific corpus"""
        
        print("🔢 Analyzing mathematical notation in corpus...")
        
        with open(corpus_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        corpus_analysis = {
            'corpus_info': {
                'total_papers': len(papers),
                'papers_with_math': 0,
                'total_notations': 0
            },
            'notation_statistics': {},
            'domain_analysis': {},
            'dhatu_mathematical_mapping': {},
            'paper_analyses': {}
        }
        
        all_notations = []
        all_domains = []
        all_dhatu_weights = {}
        
        for i, paper in enumerate(papers):
            print(f"🔍 Analyzing paper {i+1}/{len(papers)}: {paper['title'][:40]}...")
            
            text = paper['title'] + " " + paper['abstract']
            parsed = self.parse_mathematical_content(text)
            
            if parsed.notations:
                corpus_analysis['corpus_info']['papers_with_math'] += 1
                all_notations.extend(parsed.notations)
                
                # Aggregate domains
                for domain, weight in parsed.domain_distribution.items():
                    if domain not in all_domains:
                        all_domains.append(domain)
                
                # Aggregate dhātu weights
                for dhatu, weight in parsed.dhatu_mappings.items():
                    all_dhatu_weights[dhatu] = all_dhatu_weights.get(dhatu, 0) + weight
            
            # Store individual paper analysis
            corpus_analysis['paper_analyses'][paper['id']] = {
                'math_complexity': parsed.complexity_score,
                'notation_count': len(parsed.notations),
                'domain_distribution': {d.name: w for d, w in parsed.domain_distribution.items()},
                'dhatu_mappings': parsed.dhatu_mappings,
                'found_notations': [n.notation for n in parsed.notations]
            }
        
        corpus_analysis['corpus_info']['total_notations'] = len(all_notations)
        
        # Aggregate statistics
        if all_notations:
            # Notation frequency
            notation_freq = {}
            for notation in all_notations:
                notation_freq[notation.notation] = notation_freq.get(notation.notation, 0) + 1
            
            corpus_analysis['notation_statistics'] = {
                'most_common': sorted(notation_freq.items(), key=lambda x: x[1], reverse=True)[:10],
                'total_unique': len(notation_freq),
                'average_per_paper': len(all_notations) / max(corpus_analysis['corpus_info']['papers_with_math'], 1)
            }
            
            # Domain analysis
            domain_totals = {}
            for domain in all_domains:
                domain_totals[domain.name] = sum(1 for n in all_notations if n.domain == domain)
            
            corpus_analysis['domain_analysis'] = domain_totals
            
            # Mathematical dhātu mapping
            total_dhatu_weight = sum(all_dhatu_weights.values())
            if total_dhatu_weight > 0:
                corpus_analysis['dhatu_mathematical_mapping'] = {
                    dhatu: weight / total_dhatu_weight 
                    for dhatu, weight in all_dhatu_weights.items()
                }
        
        return corpus_analysis
    
    def generate_math_report(self, corpus_file: Path) -> Dict[str, Any]:
        """Generate comprehensive mathematical notation report"""
        
        analysis = self.analyze_scientific_corpus(corpus_file)
        
        # Add insights and recommendations
        insights = []
        
        if analysis['corpus_info']['papers_with_math'] > 0:
            math_coverage = analysis['corpus_info']['papers_with_math'] / analysis['corpus_info']['total_papers']
            insights.append(f"📊 {math_coverage:.1%} of papers contain mathematical notation")
            
            if 'most_common' in analysis['notation_statistics']:
                top_notation = analysis['notation_statistics']['most_common'][0]
                insights.append(f"🔢 Most common notation: '{top_notation[0]}' ({top_notation[1]} occurrences)")
            
            if analysis['dhatu_mathematical_mapping']:
                top_math_dhatu = max(analysis['dhatu_mathematical_mapping'].items(), key=lambda x: x[1])
                insights.append(f"🎯 Mathematical content most strongly activates: {top_math_dhatu[0]} ({top_math_dhatu[1]:.2f})")
        
        analysis['insights'] = insights
        
        return analysis


def main():
    """Main mathematical notation analysis"""
    
    print("🔢 Mathematical Notation Parser for Scientific Content")
    print("=" * 60)
    
    # Check corpus
    corpus_file = Path('./corpus_simple/corpus.json')
    if not corpus_file.exists():
        print("❌ Corpus file not found. Please run corpus collection first.")
        return
    
    # Run analysis
    parser = MathNotationParser()
    report = parser.generate_math_report(corpus_file)
    
    # Save report
    output_file = Path('./corpus_simple/mathematical_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Analysis saved to: {output_file}")
    
    # Print summary
    info = report['corpus_info']
    print(f"\n📊 Mathematical Content Analysis:")
    print(f"   Papers with math: {info['papers_with_math']}/{info['total_papers']}")
    print(f"   Total notations: {info['total_notations']}")
    
    if 'notation_statistics' in report:
        stats = report['notation_statistics']
        print(f"   Unique notations: {stats['total_unique']}")
        print(f"   Avg per paper: {stats['average_per_paper']:.1f}")
    
    print(f"\n💡 Key Insights:")
    for insight in report.get('insights', []):
        print(f"   {insight}")


if __name__ == "__main__":
    main()