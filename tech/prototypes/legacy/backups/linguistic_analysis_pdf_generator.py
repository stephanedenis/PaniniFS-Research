#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF ANALYSE LINGUISTIQUE APPROFONDIE
=====================================================
Générateur PDF spécialisé pour l'analyse linguistique multilingue
avec corpus réels et tableaux comparatifs pour annotation reMarkable.

Auteur: Assistant IA PaniniFS Research  
Version: 1.0.0 - PDF Analyse Linguistique
Date: 08/09/2025
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, PageTemplate
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
import urllib.request

class LinguisticAnalysisPDFGenerator:
    """Générateur PDF pour analyse linguistique approfondie"""
    
    def __init__(self):
        print("📄 GÉNÉRATEUR PDF ANALYSE LINGUISTIQUE MULTILINGUE")
        
        # Setup Unicode fonts
        self._setup_unicode_fonts()
        
        # Configuration PDF optimisée pour reMarkable
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_MULTILINGUE_REMARKABLE.pdf")
        
        # Create document with multiple page templates
        self._setup_document_templates()
        
        # Setup styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Story pour contenu
        self.story = []
        
    def _setup_unicode_fonts(self):
        """Configuration des fontes Unicode pour tous les scripts"""
        print("   🔤 Configuration fontes Unicode...")
        
        # Search for Noto fonts on the system
        font_paths = [
            "/usr/share/fonts/truetype/noto/",
            "/usr/share/fonts/noto/",
            "/usr/share/fonts/google-noto/",
            "/usr/share/fonts/TTF/",
            "/System/Library/Fonts/",
            "/home/stephane/.fonts/"
        ]
        
        # Dictionary of required fonts
        self.unicode_fonts = {
            'NotoSans': 'NotoSans-Regular.ttf',
            'NotoSansBold': 'NotoSans-Bold.ttf', 
            'NotoSansArabic': 'NotoSansArabic-Regular.ttf',
            'NotoSansCJK': 'NotoSansCJK-Regular.ttc',
            'NotoSansDevanagari': 'NotoSansDevanagari-Regular.ttf',
            'NotoSansHebrew': 'NotoSansHebrew-Regular.ttf',
            'NotoSansThai': 'NotoSansThai-Regular.ttf',
            'NotoSerif': 'NotoSerif-Regular.ttf'
        }
        
        # Try to register fonts
        for font_name, font_file in self.unicode_fonts.items():
            font_registered = False
            for path in font_paths:
                font_path = Path(path) / font_file
                if font_path.exists():
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                        print(f"     ✅ {font_name} trouvée : {font_path}")
                        font_registered = True
                        break
                    except Exception as e:
                        continue
            
            if not font_registered:
                print(f"     ⚠️  {font_name} non trouvée, utilisation Helvetica")
                
    def _setup_document_templates(self):
        """Setup document avec templates portrait et paysage"""
        
        # Template portrait normal
        portrait_frame = Frame(
            2*cm, 2*cm, A4[0]-4*cm, A4[1]-4*cm,
            leftPadding=0, bottomPadding=0, rightPadding=1*cm, topPadding=0
        )
        portrait_template = PageTemplate(
            id='portrait',
            frames=[portrait_frame],
            pagesize=A4
        )
        
        # Template paysage pour les tableaux
        landscape_frame = Frame(
            1.5*cm, 1.5*cm, landscape(A4)[0]-3*cm, landscape(A4)[1]-3*cm,
            leftPadding=0, bottomPadding=0, rightPadding=0.5*cm, topPadding=0
        )
        landscape_template = PageTemplate(
            id='landscape', 
            frames=[landscape_frame],
            pagesize=landscape(A4)
        )
        
        # Document avec templates multiples
        self.doc = SimpleDocTemplate(
            str(self.output_path),
            pageTemplates=[portrait_template, landscape_template],
            title="Analyse Linguistique Multilingue",
            author="PaniniFS Research"
        )
        
    def _setup_unicode_fonts(self):
        """Configuration des fontes Unicode pour toutes les langues"""
        print("   🌍 Configuration fontes Unicode...")
        
        try:
            # Try to use system fonts
            fonts_to_try = [
                ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans'),
                ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'LiberationSans'),
                ('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', 'NotoSans'),
                ('/System/Library/Fonts/Arial Unicode MS.ttf', 'ArialUnicode'),  # macOS
            ]
            
            self.unicode_font = 'Helvetica'  # Fallback
            
            for font_path, font_name in fonts_to_try:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        self.unicode_font = font_name
                        print(f"   ✅ Fonte Unicode: {font_name}")
                        break
                    except:
                        continue
            
            if self.unicode_font == 'Helvetica':
                print("   ⚠️  Utilisation Helvetica (support Unicode limité)")
                
        except Exception as e:
            print(f"   ⚠️  Erreur configuration fontes: {e}")
            self.unicode_font = 'Helvetica'
        
    def _setup_custom_styles(self):
        """Configuration des styles personnalisés pour reMarkable"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Sous-titre de section  
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.darkgreen,
            spaceBefore=15,
            spaceAfter=10
        ))
        
        # Sous-section
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading2'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.darkred,
            spaceBefore=10,
            spaceAfter=8
        ))
        
        # Corps de texte optimisé pour annotation
        self.styles.add(ParagraphStyle(
            name='BodyAnnotation',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName=self.unicode_font,
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leftIndent=0.2*cm,
            rightIndent=1*cm  # Espace pour annotations
        ))
        
        # Style tableaux
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=colors.white,
            alignment=TA_CENTER
        ))
        
        # Style exemples linguistiques avec Unicode
        self.styles.add(ParagraphStyle(
            name='LinguisticExample',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName=self.unicode_font,
            textColor=colors.darkblue,
            leftIndent=0.5*cm,
            spaceBefore=3,
            spaceAfter=3
        ))
        
        # Style pour cellules tableaux avec Unicode
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName=self.unicode_font,
            alignment=TA_LEFT,
            wordWrap='CJK'  # Meilleur wrapping pour langues asiatiques
        ))
        
    def generate_pdf(self):
        """Génération du PDF principal"""
        print("   🔄 Génération PDF en cours...")
        
        # Chargement du contenu markdown
        content = self._load_linguistic_analysis()
        
        # Page de titre
        self._add_title_page()
        
        # Table des matières
        self._add_table_of_contents()
        
        # Contenu principal parsé
        self._parse_and_add_content(content)
        
        # Construction PDF
        self.doc.build(self.story)
        
        file_size = self.output_path.stat().st_size / 1024  # KB
        print(f"   ✅ PDF généré : {self.output_path}")
        print(f"   📊 Taille : {file_size:.1f} KB")
        print(f"   📱 Optimisé pour reMarkable")
        
        return str(self.output_path)
    
    def _load_linguistic_analysis(self):
        """Chargement de l'analyse linguistique"""
        analysis_path = "/home/stephane/GitHub/PaniniFS-Research/ANALYSE_LINGUISTIQUE_APPROFONDIE_MULTILINGUE.md"
        
        try:
            with open(analysis_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "# Erreur : Analyse linguistique non trouvée"
    
    def _add_title_page(self):
        """Page de titre optimisée reMarkable"""
        
        # Titre principal
        title = Paragraph(
            "ANALYSE LINGUISTIQUE APPROFONDIE<br/>PRIMITIVES DHĀTU UNIVERSELLES",
            self.styles['MainTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 1*cm))
        
        # Sous-titre
        subtitle = Paragraph(
            "Corpus Multilingue • 24 Langues • 240+ Exemples<br/>Enjeux Sémantiques et Pragmatiques",
            self.styles['SectionTitle']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 1.5*cm))
        
        # Informations de base
        info_data = [
            ["Corpus Principal", "PaniniFS-Research/experiments/dhatu/"],
            ["Langues Analysées", "24 familles typologiques"],
            ["Volume Exemples", "240+ phrases authentiques"],
            ["Primitives Dhātu", "22 éléments consolidés"],
            ["Universalité", "76-98% selon phénomènes"],
            ["Date Génération", datetime.now().strftime("%d/%m/%Y")]
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 8*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.story.append(info_table)
        self.story.append(PageBreak())
        
    def _add_table_of_contents(self):
        """Table des matières"""
        
        toc_title = Paragraph("TABLE DES MATIÈRES", self.styles['SectionTitle'])
        self.story.append(toc_title)
        self.story.append(Spacer(1, 0.5*cm))
        
        toc_items = [
            "1. MÉTHODOLOGIE DE CORPUS",
            "2. STRUCTURE AGENT-ACTION-PATIENT (AAO)",
            "3. RELATIONS SPATIALES",
            "4. NÉGATION UNIVERSELLE", 
            "5. QUANTIFICATION UNIVERSELLE",
            "6. MODALITÉ ET EVIDENTIALITÉ",
            "7. ASPECTUALITÉ ET TEMPORALITÉ",
            "8. POSSESSION ET RELATIONS",
            "9. INTERROGATION ET FOCUS",
            "10. SÉQUENCE D'ÉVÉNEMENTS", 
            "11. EXISTENCE ET PRÉDICATION",
            "12. SYNTHÈSE : PATTERNS UNIVERSAUX",
            "13. SOURCES ET RÉFÉRENCES"
        ]
        
        for item in toc_items:
            toc_para = Paragraph(f"• {item}", self.styles['BodyAnnotation'])
            self.story.append(toc_para)
        
        self.story.append(PageBreak())
        
    def _parse_and_add_content(self, content):
        """Parse le markdown et ajoute au PDF"""
        
        lines = content.split('\n')
        current_table_data = []
        in_table = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                self.story.append(Spacer(1, 0.3*cm))
                continue
                
            # Titres niveau 1 (# )
            if line.startswith('# '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                title_text = line[2:].strip()
                para = Paragraph(title_text, self.styles['MainTitle'])
                self.story.append(para)
                self.story.append(Spacer(1, 0.5*cm))
                
            # Titres niveau 2 (## )
            elif line.startswith('## '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                title_text = line[3:].strip()
                para = Paragraph(title_text, self.styles['SectionTitle'])
                self.story.append(para)
                
            # Titres niveau 3 (### )
            elif line.startswith('### '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                title_text = line[4:].strip()
                para = Paragraph(title_text, self.styles['SubSection'])
                self.story.append(para)
                
            # Titres niveau 4 (#### )
            elif line.startswith('#### '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                title_text = line[5:].strip()
                para = Paragraph(f"<b>{title_text}</b>", self.styles['BodyAnnotation'])
                self.story.append(para)
                
            # Tableaux markdown
            elif '|' in line and not line.startswith('---'):
                in_table = True
                # Parse table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells:  # Ignore empty rows
                    current_table_data.append(cells)
                    
            # Listes à puces
            elif line.startswith('- ') or line.startswith('• '):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                bullet_text = line[2:].strip()
                para = Paragraph(f"• {bullet_text}", self.styles['BodyAnnotation'])
                self.story.append(para)
                
            # Texte normal
            elif line and not line.startswith('---'):
                if in_table and current_table_data:
                    self._add_table_to_story(current_table_data)
                    current_table_data = []
                    in_table = False
                # Clean up markdown formatting
                clean_line = self._clean_markdown(line)
                para = Paragraph(clean_line, self.styles['BodyAnnotation'])
                self.story.append(para)
        
        # Final table if exists
        if in_table and current_table_data:
            self._add_table_to_story(current_table_data)
    
    def _add_table_to_story(self, table_data):
        """Ajoute un tableau au story avec gestion paysage pour les grandes tables"""
        if len(table_data) < 2:  # Need at least header + 1 row
            return
            
        num_cols = len(table_data[0])
        
        # Déterminer si on a besoin du mode paysage
        needs_landscape = num_cols > 3 or any(len(str(cell)) > 30 for row in table_data for cell in row)
        
        if needs_landscape:
            # Passer en mode paysage pour ce tableau
            self.story.append(NextPageTemplate('landscape_template'))
            self.story.append(PageBreak())
            
            # Colonnes optimisées pour paysage
            if num_cols <= 3:
                col_widths = [8*cm, 9*cm, 8*cm][:num_cols]
            elif num_cols <= 5:
                col_widths = [5*cm] * num_cols
            else:
                col_widths = [4*cm] * num_cols
        else:
            # Mode portrait - limiter à 3 colonnes max
            if num_cols > 3:
                # Diviser en plusieurs tableaux
                self._split_and_add_tables(table_data)
                return
            col_widths = [5*cm, 6*cm, 5*cm][:num_cols]
        
        # Wrapper les cellules pour éviter le débordement
        wrapped_data = []
        for row in table_data:
            wrapped_row = []
            for cell in row:
                if len(str(cell)) > 40:  # Cellule trop longue
                    # Diviser en plusieurs lignes
                    wrapped_cell = self._wrap_cell_content(str(cell))
                    wrapped_row.append(Paragraph(wrapped_cell, self.styles['TableCell']))
                else:
                    wrapped_row.append(Paragraph(str(cell), self.styles['TableCell']))
            wrapped_data.append(wrapped_row)
        
        table = Table(wrapped_data, colWidths=col_widths, repeatRows=1)
        
        # Style tableau amélioré
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), self.unicode_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
        
        table.setStyle(TableStyle(table_style))
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        if needs_landscape:
            # Revenir en mode portrait après le tableau
            self.story.append(NextPageTemplate('portrait_template'))
            self.story.append(PageBreak())
    
    def _split_and_add_tables(self, table_data):
        """Divise les gros tableaux en plusieurs tables de 3 colonnes max"""
        if not table_data or len(table_data[0]) <= 3:
            return
            
        header = table_data[0]
        rows = table_data[1:]
        
        # Diviser par groupes de 3 colonnes
        col_groups = []
        for i in range(0, len(header), 3):
            group_header = header[i:i+3]
            group_data = [group_header]
            
            for row in rows:
                group_row = row[i:i+3]
                # Compléter avec des cellules vides si nécessaire
                while len(group_row) < len(group_header):
                    group_row.append("")
                group_data.append(group_row)
            
            col_groups.append(group_data)
        
        # Ajouter chaque groupe comme tableau séparé
        for i, group in enumerate(col_groups):
            if i > 0:
                self.story.append(Spacer(1, 0.3*cm))
            self._add_table_to_story(group)
    
    def _wrap_cell_content(self, content):
        """Wrap le contenu des cellules trop longues"""
        max_line_length = 30
        words = content.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_line_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '<br/>'.join(lines)
    
    def _clean_markdown(self, text):
        """Nettoie le formatage markdown pour PDF"""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic  
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Code inline
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        # Remove markdown links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        return text

def main():
    """Fonction principale"""
    try:
        generator = LinguisticAnalysisPDFGenerator()
        pdf_path = generator.generate_pdf()
        print(f"\n🎯 PDF PRÊT POUR REMARKABLE:")
        print(f"   📄 {pdf_path}")
        print(f"   📱 Format optimisé pour annotation")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur génération PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
