#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 GÉNÉRATEUR PDF DHĀTU - FONTS + PAYSAGE CORRIGÉS
=================================================
Version corrigée avec:
- Test fonts réel + fallbacks
- Mode paysage automatique pour tableaux larges
- Debug fonts pour identifier problèmes

Version: 1.1 - Fonts + Paysage
Date: 08/09/2025
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, PageTemplate, Frame
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import json
import sys

class DhatuFontsPaysageGenerator:
    """Générateur avec fonts testées + mode paysage"""
    
    def __init__(self):
        print("📄 GÉNÉRATEUR PDF DHĀTU - FONTS + PAYSAGE CORRIGÉS")
        print("   🔤 Test fonts + fallbacks")
        print("   📏 Mode paysage automatique")
        print("   🌍 Support Unicode amélioré")
        
        self._debug_fonts()
        self._setup_fonts()
        
        self.output_path = Path("/home/stephane/GitHub/PaniniFS-Research/DHATU_FONTS_PAYSAGE.pdf")
        self.corpus_path = Path("/home/stephane/GitHub/PaniniFS-Research/experiments/dhatu/prompts_child/")
        
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        self.story = []
        self.corpus_data = {}
        
    def _debug_fonts(self):
        """Debug fonts disponibles"""
        print("   🔍 Debug fonts système...")
        
        font_paths = [
            '/usr/share/fonts/truetype/NotoSans-Regular.ttf',
            '/usr/share/fonts/truetype/NotoSans-Bold.ttf', 
            '/usr/share/fonts/truetype/NotoSansArabic-Regular.ttf',
        ]
        
        for font_path in font_paths:
            if Path(font_path).exists():
                size = Path(font_path).stat().st_size / 1024
                print(f"     ✅ {Path(font_path).name} ({size:.1f}KB)")
            else:
                print(f"     ❌ {Path(font_path).name} - ABSENT")
                
    def _setup_fonts(self):
        """Configuration fonts avec tests robustes"""
        print("   🔤 Configuration fonts avec fallbacks...")
        
        self.available_fonts = {}
        
        # Test NotoSans Regular
        try:
            noto_regular = '/usr/share/fonts/truetype/NotoSans-Regular.ttf'
            if Path(noto_regular).exists():
                pdfmetrics.registerFont(TTFont('NotoSansTest', noto_regular))
                self.available_fonts['NotoSansTest'] = noto_regular
                print("     ✅ NotoSans Regular - OK")
            else:
                print("     ❌ NotoSans Regular - ABSENT")
        except Exception as e:
            print(f"     ❌ NotoSans Regular - ERREUR: {e}")
            
        # Test NotoSans Bold
        try:
            noto_bold = '/usr/share/fonts/truetype/NotoSans-Bold.ttf'
            if Path(noto_bold).exists():
                pdfmetrics.registerFont(TTFont('NotoSansBoldTest', noto_bold))
                self.available_fonts['NotoSansBoldTest'] = noto_bold
                print("     ✅ NotoSans Bold - OK")
            else:
                print("     ❌ NotoSans Bold - ABSENT")
        except Exception as e:
            print(f"     ❌ NotoSans Bold - ERREUR: {e}")
            
        # Test NotoSans Arabic
        try:
            noto_arabic = '/usr/share/fonts/truetype/NotoSansArabic-Regular.ttf'
            if Path(noto_arabic).exists():
                pdfmetrics.registerFont(TTFont('NotoSansArabicTest', noto_arabic))
                self.available_fonts['NotoSansArabicTest'] = noto_arabic
                print("     ✅ NotoSans Arabic - OK")
            else:
                print("     ❌ NotoSans Arabic - ABSENT")
        except Exception as e:
            print(f"     ❌ NotoSans Arabic - ERREUR: {e}")
        
        # Fonts par défaut selon disponibilité
        if 'NotoSansTest' in self.available_fonts:
            self.default_font = 'NotoSansTest'
            self.default_bold = 'NotoSansBoldTest' if 'NotoSansBoldTest' in self.available_fonts else 'NotoSansTest'
            print(f"   📝 Font sélectionnée: {self.default_font}")
        else:
            self.default_font = 'Helvetica'
            self.default_bold = 'Helvetica-Bold'
            print("   ⚠️  Fallback: Helvetica (pas de Unicode)")
            
    def _setup_styles(self):
        """Styles optimisés fonts"""
        
        self.styles.add(ParagraphStyle(
            name='TitlePaysage',
            fontSize=14,
            fontName=self.default_bold,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=16,
            spaceBefore=0
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionPaysage',
            fontSize=12,
            fontName=self.default_bold,
            textColor=colors.darkgreen,
            spaceBefore=16,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyPaysage',
            fontSize=9,
            fontName=self.default_font,
            alignment=TA_JUSTIFY,
            spaceBefore=3,
            spaceAfter=6,
            leftIndent=0.3*cm,
            rightIndent=0.3*cm
        ))
        
    def load_corpus_data(self):
        """Charge corpus"""
        print("   📂 Chargement corpus...")
        
        for lang_file in self.corpus_path.glob("*.json"):
            if lang_file.name == 'schema.json':
                continue
                
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.corpus_data[lang_code] = data
            except Exception:
                pass
        
        print(f"   📊 {len(self.corpus_data)} langues chargées")
        
    def generate_pdf(self):
        """Génération PDF avec mode paysage"""
        print("   🔄 Génération PDF mode portrait + paysage...")
        
        self.load_corpus_data()
        
        # Document avec templates portrait + paysage
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            title="Dhātu Fonts + Paysage"
        )
        
        # Templates
        portrait_frame = Frame(1.5*cm, 1.5*cm, A4[0]-3*cm, A4[1]-3*cm, id='portrait')
        landscape_frame = Frame(1.5*cm, 1.5*cm, landscape(A4)[0]-3*cm, landscape(A4)[1]-3*cm, id='landscape')
        
        portrait_template = PageTemplate(id='portrait', frames=[portrait_frame], pagesize=A4)
        landscape_template = PageTemplate(id='landscape', frames=[landscape_frame], pagesize=landscape(A4))
        
        doc.addPageTemplates([portrait_template, landscape_template])
        
        # Construction contenu
        self._build_content()
        
        # Build PDF
        doc.build(self.story)
        
        size_kb = self.output_path.stat().st_size / 1024
        print(f"   ✅ PDF généré: {self.output_path}")
        print(f"   📊 Taille: {size_kb:.1f} KB")
        
        return str(self.output_path)
        
    def _build_content(self):
        """Construction contenu avec modes portrait/paysage"""
        
        # Page titre (portrait)
        title = Paragraph(
            "🌍 PRIMITIVES DHĀTU - FONTS + PAYSAGE",
            self.styles['TitlePaysage']
        )
        self.story.append(title)
        
        intro_text = """
        <b>Corrections appliquées</b> :<br/>
        • Fonts Unicode testées et fallbacks<br/>
        • Mode paysage automatique pour tableaux larges<br/>
        • Support caractères multilingues amélioré<br/>
        • Tableaux avec largeur optimale
        """
        
        intro = Paragraph(intro_text, self.styles['BodyPaysage'])
        self.story.append(intro)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Test fonts
        self._test_unicode_display()
        
        # Phénomènes avec tableaux (mode paysage)
        phenomena = [
            ("🏃 AGENT-ACTION-PATIENT", "AAO"),
            ("📍 RELATIONS SPATIALES", "spatial"), 
            ("🔢 QUANTIFICATION", "quantification"),
            ("❌ NÉGATION", "negation"),
            ("🤔 MODALITÉ", "modality")
        ]
        
        for title, phenomenon in phenomena:
            self._build_phenomenon_landscape(title, phenomenon)
            
    def _test_unicode_display(self):
        """Test affichage Unicode"""
        
        test_title = Paragraph("🔤 TEST UNICODE", self.styles['SectionPaysage'])
        self.story.append(test_title)
        
        # Test différents scripts
        unicode_tests = [
            ("Latin", "Français: Le chat chasse la souris"),
            ("Arabe", "العربية: القطة تطارد الفأر"),
            ("Chinois", "中文: 猫追老鼠"),
            ("Japonais", "日本語: 猫がネズミを追いかける"),
            ("Émojis", "🐱 🏃 🐭 ✅ 📱 🌍")
        ]
        
        for script, text in unicode_tests:
            test_line = f"<b>{script}</b>: {text}"
            para = Paragraph(test_line, self.styles['BodyPaysage'])
            self.story.append(para)
            
        self.story.append(Spacer(1, 0.5*cm))
        
    def _build_phenomenon_landscape(self, title, phenomenon):
        """Section phénomène avec tableau paysage"""
        
        # Passage en mode paysage pour les tableaux
        self.story.append(NextPageTemplate('landscape'))
        self.story.append(PageBreak())
        
        # Titre section en paysage
        section_title = Paragraph(title, self.styles['SectionPaysage'])
        self.story.append(section_title)
        
        # Tableau large en mode paysage
        examples = self._get_examples_for_phenomenon(phenomenon)
        if examples:
            self._add_landscape_table(examples)
            
        # Retour mode portrait
        self.story.append(NextPageTemplate('portrait'))
        
    def _get_examples_for_phenomenon(self, phenomenon):
        """Récupère exemples pour phénomène"""
        
        examples = []
        
        # Paires de correspondances
        lang_pairs = [
            ('fr', 'en'),
            ('fr', 'arb'), 
            ('en', 'cmn'),
            ('en', 'jpn'),
            ('fr', 'deu')
        ]
        
        for source_lang, dest_lang in lang_pairs:
            if source_lang in self.corpus_data and dest_lang in self.corpus_data:
                
                source_example = None
                for item in self.corpus_data[source_lang].get('items', []):
                    if any(phenomenon in phen for phen in item.get('phenomena', [])):
                        source_example = item
                        break
                
                dest_example = None
                for item in self.corpus_data[dest_lang].get('items', []):
                    if any(phenomenon in phen for phen in item.get('phenomena', [])):
                        dest_example = item
                        break
                
                if source_example and dest_example:
                    examples.append({
                        'source_lang': source_lang,
                        'source_text': source_example['text'],
                        'dest_lang': dest_lang,
                        'dest_text': dest_example['text'],
                        'dhatu': self._generate_dhatu(phenomenon)
                    })
                    
                    if len(examples) >= 3:
                        break
        
        return examples
        
    def _generate_dhatu(self, phenomenon):
        """Génère dhātu pour phénomène"""
        
        patterns = {
            "AAO": "[AGT:agent] [ACT:action] [PAT:patient]",
            "spatial": "[ENT:entité] [LOC:relation] [LOC:lieu]", 
            "quantification": "[QUANT:nombre] [ENT:entité]",
            "negation": "[NEG] [ACT:action]",
            "modality": "[MODAL:mode] [ACT:action]"
        }
        
        return patterns.get(phenomenon, "[Structure dhātu universelle]")
        
    def _add_landscape_table(self, examples):
        """Tableau optimisé mode paysage"""
        
        if not examples:
            return
            
        # Header
        data = [["🌍 SOURCE (Langue A)", "🔧 DHĀTU (Universel)", "🎯 DESTINATION (Langue B)"]]
        
        # Drapeaux
        flags = {
            'fr': '🇫🇷', 'en': '🇬🇧', 'arb': '🇸🇦', 'cmn': '🇨🇳',
            'deu': '🇩🇪', 'jpn': '🇯🇵', 'kor': '🇰🇷'
        }
        
        for example in examples:
            source_flag = flags.get(example['source_lang'], '🌍')
            dest_flag = flags.get(example['dest_lang'], '🌍')
            
            data.append([
                f"{source_flag} {example['source_text']}",
                example['dhatu'], 
                f"{dest_flag} {example['dest_text']}"
            ])
        
        # Tableau paysage large : A4 paysage = 29.7cm utilisable
        # 3 colonnes : 8cm + 8cm + 8cm = 24cm < 29.7cm ✓
        table = Table(data, colWidths=[8*cm, 8*cm, 8*cm])
        
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), self.default_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Corps
            ('FONTNAME', (0, 1), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            
            # Bordures
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Padding généreux pour mode paysage
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))

def main():
    """Fonction principale"""
    try:
        generator = DhatuFontsPaysageGenerator()
        pdf_path = generator.generate_pdf()
        
        print(f"\n🎯 PDF FONTS + PAYSAGE GÉNÉRÉ:")
        print(f"   📄 {pdf_path}")
        print(f"   🔤 Fonts Unicode testées")
        print(f"   📏 Mode paysage pour tableaux larges")
        print(f"   🌍 Support multilingue amélioré")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
