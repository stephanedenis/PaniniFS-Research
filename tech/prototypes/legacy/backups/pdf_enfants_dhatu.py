#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF ENFANTS - PRIMITIVES DHĀTU
===========================================
Version spécialisée : corpus enfants, tableaux 3 colonnes max.

Auteur: Assistant IA PaniniFS Research  
Version: 4.0.0 - Édition Enfants
Date: 08/09/2025
"""

from reportlab.lib.pagesizes import A4, landscape
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

class ChildFriendlyPDFGenerator:
    """Générateur PDF spécialisé pour contenu enfants avec tableaux optimisés"""
    
    def __init__(self):
        print("👶 GÉNÉRATEUR PDF PRIMITIVES DHĀTU - ÉDITION ENFANTS")
        
        # Setup fontes
        self._setup_fonts()
        
        # Configuration
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/PRIMITIVES_DHATU_ENFANTS.pdf")
        self.corpus_path = Path("/home/stephane/GitHub/PaniniFS-Research/experiments/dhatu/prompts_child/")
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        # Données
        self.story = []
        self.corpus_data = {}
        
    def _setup_fonts(self):
        """Configuration fontes Unicode enfants"""
        print("   🔤 Configuration fontes Unicode...")
        
        font_mapping = {
            'NotoSansArabic': '/usr/share/fonts/truetype/NotoSansArabic-Regular.ttf',
            'NotoSansArabicBold': '/usr/share/fonts/truetype/NotoSansArabic-Bold.ttf',
            'NotoSansDevanagari': '/usr/share/fonts/truetype/NotoSansDevanagari-Regular.ttf',
            'NotoSansHebrew': '/usr/share/fonts/truetype/NotoSansHebrew-Regular.ttf',
            'NotoSans': '/usr/share/fonts/truetype/NotoSans-Regular.ttf',
            'NotoSansBold': '/usr/share/fonts/truetype/NotoSans-Bold.ttf'
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
        
        self.default_font = 'NotoSans' if 'NotoSans' in self.available_fonts else 'Helvetica'
        self.default_bold = 'NotoSansBold' if 'NotoSansBold' in self.available_fonts else 'Helvetica-Bold'
        
    def _setup_styles(self):
        """Styles adaptés enfants"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='TitleMain',
            parent=self.styles['Title'],
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
        
        # Sous-section
        self.styles.add(ParagraphStyle(
            name='SubSectionHead',
            fontSize=12,
            fontName=self.default_bold,
            textColor=colors.darkred,
            spaceBefore=10,
            spaceAfter=8
        ))
        
        # Corps
        self.styles.add(ParagraphStyle(
            name='BodyEnfant',
            fontSize=10,
            fontName=self.default_font,
            alignment=TA_JUSTIFY,
            spaceBefore=4,
            spaceAfter=4,
            leftIndent=0.5*cm,
            rightIndent=0.5*cm
        ))
        
        # Description phénomène
        self.styles.add(ParagraphStyle(
            name='PhenomeneDesc',
            fontSize=9,
            fontName=self.default_font,
            textColor=colors.darkblue,
            alignment=TA_JUSTIFY,
            spaceBefore=3,
            spaceAfter=8,
            leftIndent=1*cm
        ))
        
    def load_corpus_data(self):
        """Charge le corpus enfants depuis JSON"""
        print("   📂 Chargement corpus enfants...")
        
        # Langues prioritaires pour enfants
        target_langs = ['fr', 'en', 'arb', 'cmn', 'deu', 'kor', 'jpn']
        
        for lang_file in self.corpus_path.glob("*.json"):
            if lang_file.name == 'schema.json':
                continue
                
            lang_code = lang_file.stem
            if lang_code in target_langs:
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.corpus_data[lang_code] = data
                        print(f"     ✅ {lang_code}: {len(data.get('items', []))} exemples")
                except Exception as e:
                    print(f"     ❌ {lang_code}: {e}")
        
        print(f"   📊 Total: {len(self.corpus_data)} langues chargées")
        
    def generate_pdf(self):
        """Génération PDF enfants"""
        print("   🔄 Génération PDF enfants...")
        
        # Chargement données
        self.load_corpus_data()
        
        # Construction
        self._build_title()
        self._build_introduction()
        self._build_phenomena_sections()
        
        # Document
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title="Primitives Dhātu - Édition Enfants"
        )
        
        doc.build(self.story)
        
        # Stats
        size_kb = self.output_path.stat().st_size / 1024
        print(f"   ✅ PDF enfants généré: {self.output_path}")
        print(f"   📊 Taille: {size_kb:.1f} KB")
        
        return str(self.output_path)
        
    def _build_title(self):
        """Page de titre enfants"""
        
        title = Paragraph(
            "🌍 PRIMITIVES DHĀTU UNIVERSELLES<br/>👶 ÉDITION ENFANTS",
            self.styles['TitleMain']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 1*cm))
        
        subtitle = Paragraph(
            "🎯 Langage Enfantin • 7 Langues • Tableaux Optimisés",
            self.styles['SectionHead']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*cm))
        
        # Info rapide
        intro_text = """
        <b>🎯 Objectif</b> : Comprendre comment les enfants apprennent le langage dans différentes cultures.<br/><br/>
        <b>📚 Contenu</b> : Exemples simples du quotidien (chat, souris, jouer, manger...)<br/><br/>
        <b>🌍 Langues</b> : Français, Anglais, Arabe, Chinois, Allemand, Coréen, Japonais<br/><br/>
        <b>📏 Format</b> : Tableaux 3 colonnes maximum pour lisibilité optimale
        """
        
        intro = Paragraph(intro_text, self.styles['BodyEnfant'])
        self.story.append(intro)
        self.story.append(PageBreak())
        
    def _build_introduction(self):
        """Introduction méthodologique"""
        
        title = Paragraph("📋 MÉTHODOLOGIE CORPUS ENFANTS", self.styles['SectionHead'])
        self.story.append(title)
        
        method_text = """
        <b>Principe</b> : Analyser comment les enfants de 3-8 ans construisent des phrases universelles.<br/><br/>
        
        <b>Exemples typiques</b> :<br/>
        • 🐱 "Le chat chasse la souris" (action simple)<br/>
        • 🏠 "La balle est dans la boîte" (localisation)<br/>
        • 🔢 "Trois enfants courent" (quantité)<br/>
        • ❌ "Il ne mange pas" (négation)<br/>
        • 🎮 "Tu peux jouer maintenant" (permission)<br/><br/>
        
        <b>Structures dhātu</b> : Représentation universelle sous forme [AGT:agent] [ACT:action] [PAT:patient]
        """
        
        intro = Paragraph(method_text, self.styles['BodyEnfant'])
        self.story.append(intro)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Table langues (2 colonnes seulement)
        lang_info = [
            ["🇫🇷 Français", "Le chat chasse la souris"],
            ["🇬🇧 Anglais", "The cat chases the mouse"],
            ["🇸🇦 Arabe", "القطة تطارد الفأر"],
            ["🇨🇳 Chinois", "猫追老鼠"],
            ["🇩🇪 Allemand", "Die Katze jagt die Maus"],
            ["🇰🇷 Coréen", "고양이가 쥐를 쫓는다"],
            ["🇯🇵 Japonais", "猫がネズミを追いかける"]
        ]
        
        table = Table(lang_info, colWidths=[5*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('FONTNAME', (0, 0), (0, -1), self.default_bold),
            ('FONTNAME', (1, 0), (1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        self.story.append(table)
        self.story.append(PageBreak())
        
    def _build_phenomena_sections(self):
        """Sections par phénomène avec tableaux 3 colonnes max"""
        
        phenomena_mapping = {
            "AAO": ("🏃 AGENT-ACTION-PATIENT", "Qui fait quoi à qui/quoi"),
            "spatial": ("📍 RELATIONS SPATIALES", "Où sont les choses"),
            "quantification": ("🔢 COMPTER", "Combien il y en a"),
            "negation": ("❌ DIRE NON", "Comment dire que quelque chose n'est pas vrai"),
            "modality": ("🤔 POSSIBILITÉ", "Ce qu'on peut ou doit faire"),
            "evidential": ("👂 ON DIT QUE", "Comment on sait quelque chose"),
            "event:sequence": ("🔄 SUITE D'ACTIONS", "Faire plusieurs choses dans l'ordre"),
            "comparison": ("⚖️ COMPARER", "Plus grand, plus petit"),
            "existence": ("✨ IL Y A", "Dire que quelque chose existe"),
            "possession": ("🏠 APPARTENIR", "À qui c'est")
        }
        
        for phenomenon, (title, description) in phenomena_mapping.items():
            self._build_phenomenon_section(phenomenon, title, description)
            
    def _build_phenomenon_section(self, phenomenon, title, description):
        """Section pour un phénomène spécifique"""
        
        # Titre
        section_title = Paragraph(title, self.styles['SectionHead'])
        self.story.append(section_title)
        
        # Description
        desc = Paragraph(f"<i>{description}</i>", self.styles['PhenomeneDesc'])
        self.story.append(desc)
        
        # Collecte exemples
        examples = []
        for lang_code, lang_data in self.corpus_data.items():
            for item in lang_data.get('items', []):
                if any(phenomenon in phen for phen in item.get('phenomena', [])):
                    examples.append({
                        'lang': lang_code,
                        'text': item['text'],
                        'dhatu': self._extract_dhatu(item['text']),
                        'id': item['id']
                    })
        
        if not examples:
            return
            
        # Limite pour lisibilité
        examples = examples[:6]  # Maximum 6 exemples
        
        # Tableaux 3 colonnes : Langue | Texte | Dhātu
        self._add_3col_table(f"Exemples {title}", examples)
        
        self.story.append(Spacer(1, 0.5*cm))
        
    def _extract_dhatu(self, text):
        """Génère représentation dhātu simplifiée"""
        # Mapping simple pour exemples courants
        dhatu_mapping = {
            # Chat/souris
            "chat chasse souris": "[AGT:chat] [ACT:chasser] [PAT:souris]",
            "cat chases mouse": "[AGT:cat] [ACT:chase] [PAT:mouse]",
            "القطة تطارد الفأر": "[AGT:قطة] [ACT:طارد] [PAT:فأر]",
            
            # Spatial
            "balle dans boîte": "[ENT:balle] [LOC:dans] [LOC:boîte]",
            "ball in box": "[ENT:ball] [LOC:in] [LOC:box]",
            "الكرة في الصندوق": "[ENT:كرة] [LOC:في] [LOC:صندوق]",
            
            # Quantité
            "trois enfants": "[QUANT:3] [ENT:enfants]",
            "three children": "[QUANT:3] [ENT:children]",
            "ثلاثة أطفال": "[QUANT:3] [ENT:أطفال]",
            
            # Négation
            "ne mange pas": "[NEG] [ACT:manger]",
            "does not eat": "[NEG] [ACT:eat]",
            "لا يأكل": "[NEG] [ACT:أكل]",
            
            # Modalité
            "peux jouer": "[MODAL:pouvoir] [ACT:jouer]",
            "can play": "[MODAL:can] [ACT:play]",
            "يمكن اللعب": "[MODAL:يمكن] [ACT:لعب]",
        }
        
        # Recherche approximative
        text_clean = text.lower().replace('.', '').replace('،', '')
        
        for pattern, dhatu in dhatu_mapping.items():
            if all(word in text_clean for word in pattern.split()[:2]):  # 2 premiers mots
                return dhatu
                
        # Fallback générique
        return "[Structure dhātu...]"
        
    def _add_3col_table(self, title, examples):
        """Ajoute tableau 3 colonnes optimisé"""
        
        # Header
        header_title = Paragraph(f"<b>{title}</b>", self.styles['SubSectionHead'])
        self.story.append(header_title)
        
        # Données tableau
        data = [["🌍 Langue", "💬 Exemple", "🔧 Structure Dhātu"]]
        
        lang_names = {
            'fr': '🇫🇷 Français',
            'en': '🇬🇧 Anglais', 
            'arb': '🇸🇦 Arabe',
            'cmn': '🇨🇳 Chinois',
            'deu': '🇩🇪 Allemand',
            'kor': '🇰🇷 Coréen',
            'jpn': '🇯🇵 Japonais'
        }
        
        for example in examples:
            lang_name = lang_names.get(example['lang'], example['lang'])
            data.append([
                lang_name,
                example['text'],
                example['dhatu']
            ])
        
        # Tableau optimisé 3 colonnes
        table = Table(data, colWidths=[3.5*cm, 6*cm, 6.5*cm])
        
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.default_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            
            # Corps
            ('FONTNAME', (0, 1), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            
            # Bordures
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Padding pour lisibilité
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*cm))

def main():
    """Fonction principale"""
    try:
        generator = ChildFriendlyPDFGenerator()
        pdf_path = generator.generate_pdf()
        
        print(f"\n🎯 PDF ENFANTS PRÊT:")
        print(f"   📄 {pdf_path}")
        print(f"   👶 Contenu adapté enfants 3-8 ans")
        print(f"   📏 Tableaux 3 colonnes maximum")
        print(f"   🌍 Support Unicode multilingue")
        print(f"   📱 Format reMarkable optimisé")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
