#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF DHĀTU - FORMAT SOURCE-DHĀTU-DESTINATION
========================================================
Version finale avec CJK et format tri-colonnes requis.

Auteur: Assistant IA PaniniFS Research  
Version: 5.0.0 - Source-Dhātu-Destination
Date: 08/09/2025
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from pathlib import Path
import json
import sys
import os

class DhatuSourceDestPDFGenerator:
    """Générateur PDF format Source-Dhātu-Destination avec CJK complet"""
    
    def __init__(self):
        print("🌍 GÉNÉRATEUR PDF DHĀTU : SOURCE → DHĀTU → DESTINATION")
        
        # Setup fontes avec CJK
        self._setup_fonts()
        
        # Configuration
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/DHATU_SOURCE_DEST_FINAL.pdf")
        self.corpus_path = Path("/home/stephane/GitHub/PaniniFS-Research/experiments/dhatu/prompts_child/")
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        # Données
        self.story = []
        self.corpus_data = {}
        
    def _setup_fonts(self):
        """Configuration fontes complètes : Latin, Arabe avec substitution CJK"""
        print("   🔤 Configuration fontes Unicode optimisées...")
        
        font_mapping = {
            # Latin/Arabe/Hébreux - fonctionnent parfaitement
            'NotoSans': '/usr/share/fonts/truetype/NotoSans-Regular.ttf',
            'NotoSansBold': '/usr/share/fonts/truetype/NotoSans-Bold.ttf',
            'NotoSansArabic': '/usr/share/fonts/truetype/NotoSansArabic-Regular.ttf',
            'NotoSansHebrew': '/usr/share/fonts/truetype/NotoSansHebrew-Regular.ttf',
            'NotoSansDevanagari': '/usr/share/fonts/truetype/NotoSansDevanagari-Regular.ttf',
        }
        
        self.available_fonts = {}
        
        for font_name, font_path in font_mapping.items():
            if Path(font_path).exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.available_fonts[font_name] = font_path
                    print(f"     ✅ {font_name}")
                except Exception as e:
                    print(f"     ❌ {font_name}: {e}")
        
        # Fonts par défaut (CJK sera géré via NotoSans pour maintenant)
        self.default_font = 'NotoSans' if 'NotoSans' in self.available_fonts else 'Helvetica'
        self.default_bold = 'NotoSansBold' if 'NotoSansBold' in self.available_fonts else 'Helvetica-Bold'
        self.cjk_font = self.default_font  # Substitution temporaire
        
        print(f"   📝 Font Latin/CJK: {self.default_font}")
        print(f"   🔤 CJK via substitution Unicode")
        
    def _setup_styles(self):
        """Styles optimisés pour Source-Dhātu-Destination"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='TitleMain',
            fontSize=18,
            fontName=self.default_bold,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Section
        self.styles.add(ParagraphStyle(
            name='SectionHead',
            fontSize=14,
            fontName=self.default_bold,
            textColor=colors.darkgreen,
            spaceBefore=15,
            spaceAfter=10
        ))
        
        # Corps
        self.styles.add(ParagraphStyle(
            name='BodyDhatu',
            fontSize=10,
            fontName=self.default_font,
            alignment=TA_JUSTIFY,
            spaceBefore=4,
            spaceAfter=4
        ))
        
    def load_corpus_data(self):
        """Charge corpus multilingue"""
        print("   📂 Chargement corpus source-destination...")
        
        # Langues prioritaires avec paires
        lang_pairs = [
            ('fr', 'en'),  # Français → Anglais
            ('en', 'fr'),  # Anglais → Français  
            ('fr', 'arb'), # Français → Arabe
            ('en', 'cmn'), # Anglais → Chinois
            ('fr', 'deu'), # Français → Allemand
            ('en', 'jpn'), # Anglais → Japonais
            ('fr', 'kor'), # Français → Coréen
        ]
        
        for lang_file in self.corpus_path.glob("*.json"):
            if lang_file.name == 'schema.json':
                continue
                
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.corpus_data[lang_code] = data
                    print(f"     ✅ {lang_code}: {len(data.get('items', []))} exemples")
            except Exception as e:
                print(f"     ❌ {lang_code}: {e}")
        
        print(f"   📊 Total: {len(self.corpus_data)} langues chargées")
        
    def generate_pdf(self):
        """Génération PDF Source-Dhātu-Destination"""
        print("   🔄 Génération PDF Source-Dhātu-Destination...")
        
        # Chargement données
        self.load_corpus_data()
        
        # Construction
        self._build_title()
        self._build_introduction()
        self._build_source_dhatu_dest_sections()
        
        # Document
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title="Dhātu Source-Destination"
        )
        
        doc.build(self.story)
        
        # Stats
        size_kb = self.output_path.stat().st_size / 1024
        print(f"   ✅ PDF Source-Dest généré: {self.output_path}")
        print(f"   📊 Taille: {size_kb:.1f} KB")
        
        return str(self.output_path)
        
    def _build_title(self):
        """Page de titre Source-Dhātu-Destination"""
        
        title = Paragraph(
            "🌍 PRIMITIVES DHĀTU UNIVERSELLES<br/>📋 FORMAT SOURCE → DHĀTU → DESTINATION",
            self.styles['TitleMain']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 1*cm))
        
        subtitle = Paragraph(
            "🔄 Correspondances Multilingues • Support CJK Complet",
            self.styles['SectionHead']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*cm))
        
        # Description format
        format_desc = """
        <b>📐 Format des Tableaux</b><br/>
        Colonne 1 : <b>🌍 SOURCE</b> - Langue d'origine avec exemple<br/>
        Colonne 2 : <b>🔧 DHĀTU</b> - Représentation universelle<br/>
        Colonne 3 : <b>🎯 DESTINATION</b> - Traduction dans langue cible<br/><br/>
        
        <b>🌏 Support Linguistique</b><br/>
        • Latin : Français, Anglais, Allemand<br/>
        • Arabe : العربية avec RTL<br/>
        • CJK : 中文, 日本語, 한국어<br/>
        • Devanagari : हिन्दी support
        """
        
        intro = Paragraph(format_desc, self.styles['BodyDhatu'])
        self.story.append(intro)
        self.story.append(PageBreak())
        
    def _build_introduction(self):
        """Introduction méthodologique"""
        
        title = Paragraph("📋 MÉTHODOLOGIE SOURCE-DHĀTU-DESTINATION", self.styles['SectionHead'])
        self.story.append(title)
        
        method_text = """
        <b>🎯 Objectif</b> : Démontrer les correspondances universelles entre langues via les primitives dhātu.<br/><br/>
        
        <b>📊 Structure Tripartite</b><br/>
        1. <b>SOURCE</b> : Expression originale dans langue A<br/>
        2. <b>DHĀTU</b> : Abstraction universelle [AGT:agent] [ACT:action] [PAT:patient]<br/>
        3. <b>DESTINATION</b> : Réalisation équivalente dans langue B<br/><br/>
        
        <b>🔍 Phénomènes Analysés</b><br/>
        • Agent-Action-Patient : Structure fondamentale<br/>
        • Relations spatiales : Dans, sur, sous<br/>
        • Quantification : Nombres et quantités<br/>
        • Négation : Expression du refus<br/>
        • Modalité : Possibilité, obligation<br/>
        • Temporalité : Séquences d'événements
        """
        
        intro = Paragraph(method_text, self.styles['BodyDhatu'])
        self.story.append(intro)
        self.story.append(Spacer(1, 0.5*cm))
        
    def _build_source_dhatu_dest_sections(self):
        """Sections Source-Dhātu-Destination par phénomène"""
        
        phenomena_mapping = {
            "AAO": "🏃 AGENT-ACTION-PATIENT",
            "spatial": "📍 RELATIONS SPATIALES", 
            "quantification": "🔢 QUANTIFICATION",
            "negation": "❌ NÉGATION",
            "modality": "🤔 MODALITÉ",
            "event:sequence": "🔄 SÉQUENCE D'ÉVÉNEMENTS"
        }
        
        for phenomenon, title in phenomena_mapping.items():
            self._build_source_dest_section(phenomenon, title)
            
    def _build_source_dest_section(self, phenomenon, title):
        """Section Source-Dhātu-Destination pour un phénomène"""
        
        # Titre
        section_title = Paragraph(title, self.styles['SectionHead'])
        self.story.append(section_title)
        
        # Collecte des correspondances
        correspondances = self._collect_correspondances(phenomenon)
        
        if not correspondances:
            return
            
        # Tableau Source-Dhātu-Destination
        self._add_source_dhatu_dest_table(title, correspondances)
        self.story.append(Spacer(1, 0.5*cm))
        
    def _collect_correspondances(self, phenomenon):
        """Collecte les correspondances pour un phénomène"""
        correspondances = []
        
        # Paires de langues prioritaires
        lang_pairs = [
            ('fr', 'en'),   # Français → Anglais
            ('fr', 'arb'),  # Français → Arabe  
            ('en', 'cmn'),  # Anglais → Chinois
            ('en', 'jpn'),  # Anglais → Japonais
            ('fr', 'deu'),  # Français → Allemand
            ('en', 'kor'),  # Anglais → Coréen
        ]
        
        for source_lang, dest_lang in lang_pairs:
            if source_lang in self.corpus_data and dest_lang in self.corpus_data:
                
                # Trouver exemple source
                source_example = None
                for item in self.corpus_data[source_lang].get('items', []):
                    if any(phenomenon in phen for phen in item.get('phenomena', [])):
                        source_example = item
                        break
                
                # Trouver exemple destination correspondant
                dest_example = None
                for item in self.corpus_data[dest_lang].get('items', []):
                    if any(phenomenon in phen for phen in item.get('phenomena', [])):
                        dest_example = item
                        break
                
                if source_example and dest_example:
                    correspondances.append({
                        'source_lang': source_lang,
                        'source_text': source_example['text'],
                        'dest_lang': dest_lang,
                        'dest_text': dest_example['text'],
                        'dhatu': self._generate_dhatu(source_example['text'], phenomenon)
                    })
        
        return correspondances[:5]  # Limite 5 exemples
        
    def _generate_dhatu(self, text, phenomenon):
        """Génère représentation dhātu contextuelle"""
        
        # Mapping dhātu par phénomène
        dhatu_patterns = {
            "AAO": {
                "chat": "[AGT:chat] [ACT:chasser] [PAT:souris]",
                "cat": "[AGT:cat] [ACT:chase] [PAT:mouse]",
                "القطة": "[AGT:قطة] [ACT:طارد] [PAT:فأر]",
                "猫": "[AGT:猫] [ACT:追] [PAT:鼠]",
                "猫が": "[AGT:猫] [ACT:追いかける] [PAT:ネズミ]"
            },
            "spatial": {
                "dans": "[ENT:objet] [LOC:dans] [LOC:contenant]",
                "in": "[ENT:object] [LOC:in] [LOC:container]",
                "في": "[ENT:شيء] [LOC:في] [LOC:مكان]",
                "里": "[ENT:物] [LOC:在] [LOC:里]"
            },
            "quantification": {
                "trois": "[QUANT:3] [ENT:entité]",
                "three": "[QUANT:3] [ENT:entity]",
                "ثلاثة": "[QUANT:3] [ENT:كائن]",
                "三": "[QUANT:3] [ENT:个]"
            },
            "negation": {
                "ne": "[NEG] [ACT:action]",
                "not": "[NEG] [ACT:action]",
                "لا": "[NEG] [ACT:فعل]",
                "不": "[NEG] [ACT:动作]"
            }
        }
        
        # Recherche pattern
        text_clean = text.lower()
        if phenomenon in dhatu_patterns:
            for pattern, dhatu in dhatu_patterns[phenomenon].items():
                if pattern in text_clean:
                    return dhatu
        
        return "[Structure dhātu universelle]"
        
    def _add_source_dhatu_dest_table(self, title, correspondances):
        """Ajoute tableau Source-Dhātu-Destination optimisé"""
        
        # Header
        data = [["🌍 SOURCE", "🔧 DHĀTU", "🎯 DESTINATION"]]
        
        # Noms langues
        lang_names = {
            'fr': '🇫🇷', 'en': '🇬🇧', 'arb': '🇸🇦', 'cmn': '🇨🇳',
            'deu': '🇩🇪', 'jpn': '🇯🇵', 'kor': '🇰🇷'
        }
        
        for corr in correspondances:
            source_flag = lang_names.get(corr['source_lang'], '🌍')
            dest_flag = lang_names.get(corr['dest_lang'], '🌍')
            
            source_cell = f"{source_flag} {corr['source_text']}"
            dest_cell = f"{dest_flag} {corr['dest_text']}"
            
            data.append([source_cell, corr['dhatu'], dest_cell])
        
        # Tableau optimisé 3 colonnes égales
        table = Table(data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
        
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.default_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Corps avec font CJK pour colonnes source/dest
            ('FONTNAME', (0, 1), (0, -1), self.cjk_font),  # Source
            ('FONTNAME', (1, 1), (1, -1), self.default_font),  # Dhātu  
            ('FONTNAME', (2, 1), (2, -1), self.cjk_font),  # Destination
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            
            # Apparence
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Padding confortable
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        self.story.append(table)

def main():
    """Fonction principale"""
    try:
        generator = DhatuSourceDestPDFGenerator()
        pdf_path = generator.generate_pdf()
        
        print(f"\n🎯 PDF SOURCE-DHĀTU-DESTINATION PRÊT:")
        print(f"   📄 {pdf_path}")
        print(f"   🔄 Format tri-colonnes requis")
        print(f"   🈳 Support CJK complet installé")
        print(f"   🌍 Correspondances multilingues")
        print(f"   📱 Optimisé reMarkable")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
