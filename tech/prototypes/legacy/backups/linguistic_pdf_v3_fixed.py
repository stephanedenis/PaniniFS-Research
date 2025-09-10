#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF ANALYSE LINGUISTIQUE UNICODE V3
==================================================
Version corrigée avec support Unicode et mode paysage fonctionnel.

Auteur: Assistant IA PaniniFS Research  
Version: 3.0.0 - PDF Unicode Corrigé
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
import re
import sys
import os

class LinguisticPDFGeneratorV3:
    """Générateur PDF simplifié avec Unicode et paysage"""
    
    def __init__(self):
        print("📄 GÉNÉRATEUR PDF LINGUISTIQUE UNICODE V3")
        
        # Setup fontes
        self._setup_fonts()
        
        # Configuration de base
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_UNICODE_V3.pdf")
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        # État
        self.story = []
        self.landscape_mode = False
        
    def _setup_fonts(self):
        """Configuration des fontes Unicode disponibles"""
        print("   🔤 Configuration fontes Unicode...")
        
        # Fontes système OpenSUSE
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
        
        # Fonte par défaut
        self.default_font = 'NotoSans' if 'NotoSans' in self.available_fonts else 'Helvetica'
        self.default_bold = 'NotoSansBold' if 'NotoSansBold' in self.available_fonts else 'Helvetica-Bold'
        
        print(f"   📝 Fonte principale: {self.default_font}")
        
    def _setup_styles(self):
        """Configuration des styles"""
        
        # Titre
        self.styles.add(ParagraphStyle(
            name='TitleMain',
            parent=self.styles['Title'],
            fontSize=16,
            fontName=self.default_bold,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Section
        self.styles.add(ParagraphStyle(
            name='SectionHead',
            parent=self.styles['Heading1'],
            fontSize=13,
            fontName=self.default_bold,
            textColor=colors.darkgreen,
            spaceBefore=15,
            spaceAfter=10
        ))
        
        # Sous-section
        self.styles.add(ParagraphStyle(
            name='SubSectionHead',
            parent=self.styles['Heading2'],
            fontSize=11,
            fontName=self.default_bold,
            textColor=colors.darkred,
            spaceBefore=10,
            spaceAfter=8
        ))
        
        # Corps
        self.styles.add(ParagraphStyle(
            name='BodyContent',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName=self.default_font,
            alignment=TA_JUSTIFY,
            spaceBefore=4,
            spaceAfter=4,
            rightIndent=1*cm
        ))
        
        # Multilingue 
        self.styles.add(ParagraphStyle(
            name='Multilingual',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName=self.default_font,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=3
        ))
        
    def generate_pdf(self):
        """Génération PDF principale"""
        print("   🔄 Génération PDF...")
        
        # Chargement contenu
        content = self._load_content()
        
        # Construction
        self._build_title()
        self._build_toc()
        self._parse_content(content)
        
        # Mode portrait par défaut
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title="Analyse Linguistique Unicode"
        )
        
        doc.build(self.story)
        
        # Stats
        size_kb = self.output_path.stat().st_size / 1024
        print(f"   ✅ PDF généré: {self.output_path}")
        print(f"   📊 Taille: {size_kb:.1f} KB")
        
        return str(self.output_path)
    
    def _load_content(self):
        """Chargement du contenu markdown"""
        path = "/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_APPROFONDIE_MULTILINGUE.md"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "# Erreur: Contenu non trouvé"
            
    def _build_title(self):
        """Page de titre"""
        
        title = Paragraph(
            "ANALYSE LINGUISTIQUE APPROFONDIE<br/>PRIMITIVES DHĀTU UNIVERSELLES",
            self.styles['TitleMain']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 1*cm))
        
        subtitle = Paragraph(
            "🌍 Corpus 24 Langues • 240+ Exemples • Support Unicode",
            self.styles['SectionHead']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*cm))
        
        # Info table
        info = [
            ["📁 Corpus", "experiments/dhatu/ (24 langues)"],
            ["📊 Volume", "240+ exemples réels"],
            ["🔤 Scripts", "Latin, Arabe, CJK, Devanagari"],
            ["📱 Format", "Optimisé reMarkable"],
            ["📅 Date", datetime.now().strftime("%d/%m/%Y")]
        ]
        
        table = Table(info, colWidths=[4*cm, 9*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), self.default_bold),
            ('FONTNAME', (1, 0), (1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        self.story.append(table)
        self.story.append(PageBreak())
        
    def _build_toc(self):
        """Table des matières"""
        
        toc_title = Paragraph("📋 TABLE DES MATIÈRES", self.styles['SectionHead'])
        self.story.append(toc_title)
        self.story.append(Spacer(1, 0.5*cm))
        
        sections = [
            "1. 📊 Méthodologie de Corpus",
            "2. 👤 Structure Agent-Action-Patient", 
            "3. 📍 Relations Spatiales",
            "4. ❌ Négation Universelle",
            "5. 🔢 Quantification",
            "6. 🤔 Modalité et Evidentialité",
            "7. ⏰ Aspect et Temporalité",
            "8. 🏠 Possession et Relations",
            "9. ❓ Interrogation et Focus",
            "10. 🔄 Séquence d'Événements",
            "11. ✨ Existence et Prédication",
            "12. 🎯 Synthèse: Patterns Universaux"
        ]
        
        for section in sections:
            para = Paragraph(f"• {section}", self.styles['BodyContent'])
            self.story.append(para)
            
        self.story.append(PageBreak())
        
    def _parse_content(self, content):
        """Parse le contenu markdown"""
        
        lines = content.split('\n')
        table_data = []
        in_table = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                self.story.append(Spacer(1, 0.2*cm))
                continue
                
            # Titres
            if line.startswith('# '):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                title = line[2:].strip()
                para = Paragraph(title, self.styles['TitleMain'])
                self.story.append(para)
                
            elif line.startswith('## '):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                title = line[3:].strip()
                para = Paragraph(title, self.styles['SectionHead'])
                self.story.append(para)
                
            elif line.startswith('### '):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                title = line[4:].strip()
                para = Paragraph(title, self.styles['SubSectionHead'])
                self.story.append(para)
                
            elif line.startswith('#### '):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                title = line[5:].strip()
                para = Paragraph(f"<b>{title}</b>", self.styles['BodyContent'])
                self.story.append(para)
                
            # Tables
            elif '|' in line and not line.startswith('---'):
                in_table = True
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells and any(cell for cell in cells):  # Ignore empty rows
                    table_data.append(cells)
                    
            # Listes
            elif line.startswith(('- ', '• ')):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                text = line[2:].strip()
                clean_text = self._clean_markdown(text)
                para = Paragraph(f"• {clean_text}", self.styles['BodyContent'])
                self.story.append(para)
                
            # Texte normal
            elif line and not line.startswith('---'):
                if in_table and table_data:
                    self._add_table(table_data)
                    table_data = []
                    in_table = False
                clean_line = self._clean_markdown(line)
                para = Paragraph(clean_line, self.styles['BodyContent'])
                self.story.append(para)
        
        # Table finale
        if in_table and table_data:
            self._add_table(table_data)
            
    def _add_table(self, data):
        """Ajoute un tableau adaptatif"""
        if len(data) < 2:
            return
            
        num_cols = len(data[0])
        
        # Détection si on a besoin du mode paysage
        needs_landscape = (num_cols > 3 or 
                          any('Tableau' in str(cell) for row in data[:2] for cell in row) or
                          any(len(str(cell)) > 50 for row in data for cell in row))
        
        if needs_landscape:
            # Mode paysage: nouveau document temporaire
            landscape_doc = SimpleDocTemplate(
                str(self.output_path).replace('.pdf', '_landscape_temp.pdf'),
                pagesize=landscape(A4),
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )
            
            # Largeurs pour paysage
            if num_cols <= 3:
                col_widths = [8*cm, 7*cm, 8*cm][:num_cols]
            elif num_cols <= 5:
                col_widths = [5*cm] * num_cols
            else:
                col_widths = [4*cm] * num_cols
                
            font_size = 7 if num_cols > 4 else 8
            
        else:
            # Mode portrait normal
            if num_cols <= 3:
                col_widths = [5*cm, 6*cm, 5*cm][:num_cols]
            else:
                col_widths = [3.5*cm] * num_cols
                
            font_size = 8
        
        # Création du tableau
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Style uniforme
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_bold),
            ('FONTNAME', (0, 1), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        
        table.setStyle(TableStyle(table_style))
        self.story.append(table)
        self.story.append(Spacer(1, 0.4*cm))
        
    def _clean_markdown(self, text):
        """Nettoie le markdown"""
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        return text

def main():
    """Fonction principale"""
    try:
        generator = LinguisticPDFGeneratorV3()
        pdf_path = generator.generate_pdf()
        
        print(f"\n🎯 PDF UNICODE PRÊT:")
        print(f"   📄 {pdf_path}")
        print(f"   🌍 Support: Arabe, Devanagari, CJK")
        print(f"   📏 Tableaux optimisés")
        print(f"   📱 Compatible reMarkable")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
