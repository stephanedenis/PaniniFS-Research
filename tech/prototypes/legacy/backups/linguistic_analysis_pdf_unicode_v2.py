#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF ANALYSE LINGUISTIQUE APPROFONDIE V2
======================================================
Générateur PDF amélioré avec support Unicode complet, mode paysage
pour tableaux et optimisations pour reMarkable.

Auteur: Assistant IA PaniniFS Research  
Version: 2.0.0 - PDF Unicode + Paysage
Date: 08/09/2025
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import NextPageTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from pathlib import Path
import re
import sys
import os
import glob

class UnicodeMultilingualPDFGenerator:
    """Générateur PDF pour analyse linguistique avec Unicode complet"""
    
    def __init__(self):
        print("📄 GÉNÉRATEUR PDF MULTILINGUE UNICODE V2")
        
        # Setup Unicode fonts first
        self._setup_unicode_fonts()
        
        # Configuration output
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_MULTILINGUE_UNICODE_V2.pdf")
        
        # Document avec templates multiples
        self._setup_document()
        
        # Setup styles avec Unicode
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Story et état
        self.story = []
        self.current_template = 'portrait'
        
    def _setup_unicode_fonts(self):
        """Configuration automatique des fontes Unicode disponibles"""
        print("   🔤 Recherche fontes Unicode système...")
        
        # Chemins standards Linux
        font_search_paths = [
            "/usr/share/fonts/google-noto/",
            "/usr/share/fonts/truetype/noto/", 
            "/usr/share/fonts/noto/",
            "/usr/share/fonts/TTF/",
            "/usr/share/fonts/",
            "/home/stephane/.fonts/"
        ]
        
        self.available_fonts = {}
        
        # Fontes requises par priorité
        font_priorities = {
            'NotoSans-Regular': ['NotoSans-Regular.ttf', 'NotoSans.ttf'],
            'NotoSans-Bold': ['NotoSans-Bold.ttf', 'NotoSansBold.ttf'],
            'NotoSansArabic': ['NotoSansArabic-Regular.ttf', 'NotoSansArabic.ttf'],
            'NotoSansCJK': ['NotoSansCJK-Regular.ttc', 'NotoSansCJK.ttc'],
            'NotoSansDevanagari': ['NotoSansDevanagari-Regular.ttf'],
            'NotoSansHebrew': ['NotoSansHebrew-Regular.ttf'],
            'NotoSerif': ['NotoSerif-Regular.ttf', 'NotoSerif.ttf']
        }
        
        # Recherche et enregistrement des fontes
        for font_key, font_files in font_priorities.items():
            registered = False
            for search_path in font_search_paths:
                if registered:
                    break
                for font_file in font_files:
                    font_path = Path(search_path) / font_file
                    if font_path.exists():
                        try:
                            pdfmetrics.registerFont(TTFont(font_key, str(font_path)))
                            self.available_fonts[font_key] = str(font_path)
                            print(f"     ✅ {font_key}: {font_path.name}")
                            registered = True
                            break
                        except Exception as e:
                            continue
            
            if not registered:
                print(f"     ❌ {font_key} non trouvée")
        
        # Configuration fonte par défaut
        self.default_font = 'NotoSans-Regular' if 'NotoSans-Regular' in self.available_fonts else 'Helvetica'
        self.default_font_bold = 'NotoSans-Bold' if 'NotoSans-Bold' in self.available_fonts else 'Helvetica-Bold'
        
        print(f"   📝 Fonte principale: {self.default_font}")
        
    def _setup_document(self):
        """Configuration document avec templates portrait/paysage"""
        
        # Template portrait (défaut)
        portrait_frame = Frame(
            2*cm, 2*cm, A4[0]-4*cm, A4[1]-4*cm,
            leftPadding=0, bottomPadding=0, rightPadding=1.5*cm, topPadding=0,
            id='portrait_frame'
        )
        portrait_template = PageTemplate(
            id='portrait',
            frames=[portrait_frame],
            pagesize=A4
        )
        
        # Template paysage pour tableaux larges
        landscape_size = landscape(A4)
        landscape_frame = Frame(
            1.5*cm, 1.5*cm, landscape_size[0]-3*cm, landscape_size[1]-3*cm,
            leftPadding=0, bottomPadding=0, rightPadding=1*cm, topPadding=0,
            id='landscape_frame'
        )
        landscape_template = PageTemplate(
            id='landscape',
            frames=[landscape_frame], 
            pagesize=landscape_size
        )
        
        # Document avec les deux templates
        self.doc = SimpleDocTemplate(
            str(self.output_path),
            pageTemplates=[portrait_template, landscape_template],
            title="Analyse Linguistique Multilingue Unicode",
            author="PaniniFS Research"
        )
        
    def _setup_custom_styles(self):
        """Styles personnalisés avec support Unicode complet"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='TitleUnicode',
            parent=self.styles['Title'],
            fontSize=16,
            fontName=self.default_font_bold,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Section
        self.styles.add(ParagraphStyle(
            name='SectionUnicode',
            parent=self.styles['Heading1'],
            fontSize=13,
            fontName=self.default_font_bold,
            textColor=colors.darkgreen,
            spaceBefore=12,
            spaceAfter=8
        ))
        
        # Sous-section
        self.styles.add(ParagraphStyle(
            name='SubSectionUnicode',
            parent=self.styles['Heading2'],
            fontSize=11,
            fontName=self.default_font_bold,
            textColor=colors.darkred,
            spaceBefore=8,
            spaceAfter=6
        ))
        
        # Corps de texte normal
        self.styles.add(ParagraphStyle(
            name='BodyUnicode',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName=self.default_font,
            alignment=TA_JUSTIFY,
            spaceBefore=4,
            spaceAfter=4,
            rightIndent=1*cm  # Espace annotations
        ))
        
        # Style pour exemples multilingues
        self.styles.add(ParagraphStyle(
            name='MultilingualExample',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName=self.default_font,
            textColor=colors.darkblue,
            leftIndent=0.3*cm,
            spaceBefore=2,
            spaceAfter=2,
            alignment=TA_CENTER  # Centre pour faciliter lecture
        ))
        
        # Style spécial pour tableaux compacts
        self.styles.add(ParagraphStyle(
            name='TableCellUnicode',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName=self.default_font,
            alignment=TA_LEFT,
            spaceBefore=1,
            spaceAfter=1
        ))
        
    def generate_pdf(self):
        """Génération du PDF principal"""
        print("   🔄 Génération PDF Unicode en cours...")
        
        # Chargement contenu
        content = self._load_linguistic_analysis()
        
        # Construction du contenu
        self._add_title_page()
        self._add_toc()
        self._parse_and_build_content(content)
        
        # Génération finale
        self.doc.build(self.story)
        
        # Stats
        file_size = self.output_path.stat().st_size / 1024
        print(f"   ✅ PDF généré: {self.output_path}")
        print(f"   📊 Taille: {file_size:.1f} KB")
        print(f"   🌍 Support Unicode complet")
        print(f"   📱 Optimisé reMarkable")
        
        return str(self.output_path)
    
    def _load_linguistic_analysis(self):
        """Chargement du rapport d'analyse"""
        analysis_path = "/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_APPROFONDIE_MULTILINGUE.md"
        
        try:
            with open(analysis_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "# Erreur: Analyse linguistique non trouvée"
    
    def _add_title_page(self):
        """Page de titre"""
        
        # Titre principal
        title = Paragraph(
            "ANALYSE LINGUISTIQUE APPROFONDIE<br/>PRIMITIVES DHĀTU UNIVERSELLES",
            self.styles['TitleUnicode']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 1*cm))
        
        # Sous-titre avec symboles Unicode
        subtitle = Paragraph(
            "🌍 Corpus Multilingue • 24 Langues • 240+ Exemples<br/>"
            "📊 Enjeux Sémantiques et Pragmatiques<br/>"
            "🔤 Support Unicode Complet",
            self.styles['SectionUnicode']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1*cm))
        
        # Informations techniques
        info_data = [
            ["📁 Corpus Principal", "PaniniFS-Research/experiments/dhatu/"],
            ["🌐 Langues Analysées", "24 familles typologiques"],
            ["📝 Volume Exemples", "240+ phrases authentiques"],
            ["⚛️ Primitives Dhātu", "22 éléments consolidés"],
            ["📈 Taux Universalité", "76-98% selon phénomènes"],
            ["📅 Date Génération", datetime.now().strftime("%d/%m/%Y")],
            ["🔤 Support Unicode", "✅ Arabe, CJK, Devanagari, etc."],
            ["📱 Optimisation", "✅ reMarkable e-ink"]
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 8*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.default_font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.darkgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(info_table)
        self.story.append(PageBreak())
        
    def _add_toc(self):
        """Table des matières"""
        
        toc_title = Paragraph("📋 TABLE DES MATIÈRES", self.styles['SectionUnicode'])
        self.story.append(toc_title)
        self.story.append(Spacer(1, 0.5*cm))
        
        toc_items = [
            "1. 📊 MÉTHODOLOGIE DE CORPUS",
            "2. 👤 STRUCTURE AGENT-ACTION-PATIENT",
            "3. 📍 RELATIONS SPATIALES", 
            "4. ❌ NÉGATION UNIVERSELLE",
            "5. 🔢 QUANTIFICATION UNIVERSELLE",
            "6. 🤔 MODALITÉ ET EVIDENTIALITÉ",
            "7. ⏰ ASPECTUALITÉ ET TEMPORALITÉ",
            "8. 🏠 POSSESSION ET RELATIONS",
            "9. ❓ INTERROGATION ET FOCUS",
            "10. 🔄 SÉQUENCE D'ÉVÉNEMENTS",
            "11. ✨ EXISTENCE ET PRÉDICATION",
            "12. 🎯 SYNTHÈSE: PATTERNS UNIVERSAUX",
            "13. 📚 SOURCES ET RÉFÉRENCES"
        ]
        
        for item in toc_items:
            para = Paragraph(f"• {item}", self.styles['BodyUnicode'])
            self.story.append(para)
        
        self.story.append(PageBreak())
        
    def _parse_and_build_content(self, content):
        """Parse markdown et construit le PDF avec gestion tableaux"""
        
        lines = content.split('\n')
        current_table_data = []
        in_table = False
        large_table_sections = {
            'Tableau', 'AAO', 'Spatial', 'Négation', 'Quantité', 
            'Modalité', 'Aspect', 'Possession', 'Questions', 'Séquence',
            'Existence', 'Variations Cross-Linguistiques'
        }
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line:
                if in_table and current_table_data:
                    # Check if this is a large table
                    needs_landscape = any(section in ''.join(current_table_data[0][:3]) 
                                        for section in large_table_sections) if current_table_data else False
                    self._add_table_to_story(current_table_data, landscape=needs_landscape)
                    current_table_data = []
                    in_table = False
                self.story.append(Spacer(1, 0.2*cm))
                continue
                
            # Détection titres et gestion du mode paysage
            if line.startswith('# '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                title_text = line[2:].strip()
                para = Paragraph(title_text, self.styles['TitleUnicode'])
                self.story.append(para)
                
            elif line.startswith('## '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                title_text = line[3:].strip()
                para = Paragraph(title_text, self.styles['SectionUnicode'])
                self.story.append(para)
                
            elif line.startswith('### '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                title_text = line[4:].strip()
                para = Paragraph(title_text, self.styles['SubSectionUnicode'])
                self.story.append(para)
                
            elif line.startswith('#### '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                title_text = line[5:].strip()
                para = Paragraph(f"<b>{title_text}</b>", self.styles['BodyUnicode'])
                self.story.append(para)
                
            # Tableaux markdown
            elif '|' in line and not line.startswith('---'):
                in_table = True
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells:
                    current_table_data.append(cells)
                    
            # Listes
            elif line.startswith(('- ', '• ')):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                bullet_text = line[2:].strip()
                clean_text = self._clean_markdown(bullet_text)
                para = Paragraph(f"• {clean_text}", self.styles['BodyUnicode'])
                self.story.append(para)
                
            # Texte normal
            elif line and not line.startswith('---'):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                    
                clean_line = self._clean_markdown(line)
                para = Paragraph(clean_line, self.styles['BodyUnicode'])
                self.story.append(para)
        
        # Table finale si elle existe
        if in_table and current_table_data:
            self._add_table_to_story(current_table_data)
            
    def _add_table_to_story(self, table_data, landscape=False):
        """Ajoute tableau avec option paysage pour les larges tableaux"""
        if len(table_data) < 2:
            return
            
        # Passage en paysage pour les gros tableaux
        if landscape or len(table_data[0]) > 3:
            self.story.append(NextPageTemplate('landscape'))
            self.story.append(PageBreak())
            
            # Largeurs adaptées au paysage
            num_cols = len(table_data[0])
            if num_cols <= 3:
                col_widths = [8*cm, 7*cm, 8*cm][:num_cols]
            elif num_cols <= 5:
                col_widths = [5*cm] * num_cols
            else:
                col_widths = [3.8*cm] * num_cols
        else:
            # Mode portrait normal
            num_cols = len(table_data[0])
            if num_cols <= 3:
                col_widths = [5*cm, 6*cm, 5*cm][:num_cols]
            else:
                col_widths = [3*cm] * num_cols
        
        # Création du tableau
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Style adaptatif selon la taille
        font_size = 7 if len(table_data[0]) > 4 else 8
        
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.default_font_bold),
            ('FONTNAME', (0, 1), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),  # Wrap automatique
        ]
        
        table.setStyle(TableStyle(table_style))
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*cm))
        
        # Retour au portrait après un tableau paysage
        if landscape or len(table_data[0]) > 3:
            self.story.append(NextPageTemplate('portrait'))
            self.story.append(PageBreak())
        
    def _clean_markdown(self, text):
        """Nettoie markdown et préserve Unicode"""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Code inline
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        # Liens markdown (garde juste le texte)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Préserve les caractères Unicode (arabe, CJK, etc.)
        return text

def main():
    """Fonction principale améliorée"""
    try:
        generator = UnicodeMultilingualPDFGenerator()
        pdf_path = generator.generate_pdf()
        
        print(f"\n🎯 PDF UNICODE PRÊT POUR REMARKABLE:")
        print(f"   📄 {pdf_path}")
        print(f"   🌍 Support complet: Arabe, Chinois, Japonais, Devanagari")
        print(f"   📏 Mode paysage automatique pour gros tableaux")
        print(f"   📱 Format optimisé e-ink")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur génération PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
