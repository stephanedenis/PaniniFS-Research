#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 GÉNÉRATEUR HTML RAPPORT RECHERCHE UNICODE
====================================================================
Conversion du rapport markdown vers HTML avec support Unicode
complet et présentation optimisée pour révision linguistique.

Auteur: Assistant IA PaniniFS Research
Version: 0.0.1 - HTML Unicode Generator
Date: 08/09/2025
"""

import markdown
from pathlib import Path
import re

def generate_html_report():
    """Génération rapport HTML avec Unicode"""
    print("🌐 GÉNÉRATION RAPPORT HTML UNICODE")
    
    # Lecture fichier markdown
    md_path = Path("/home/stephane/GitHub/PaniniFS-Research/RAPPORT_RECHERCHE_UNICODE_COMPLET.md")
    html_path = Path("/home/stephane/GitHub/PaniniFS-Research/RAPPORT_RECHERCHE_UNICODE_COMPLET.html")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Conversion markdown vers HTML
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'fenced_code', 'toc'],
        extension_configs={
            'toc': {'title': 'Table des Matières'}
        }
    )
    
    # Template HTML avec support Unicode
    html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Recherche Panini-Dhatu - Unicode Complet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&family=Noto+Serif:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&display=swap');
        
        body {{
            font-family: 'Noto Serif', serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #fafafa;
            color: #333;
        }}
        
        h1, h2, h3 {{
            font-family: 'Noto Sans', sans-serif;
            color: #2c3e50;
        }}
        
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        h2 {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }}
        
        .dhatu {{
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-weight: bold;
            color: #27ae60;
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        .ipa {{
            font-family: 'Noto Sans', monospace;
            color: #e74c3c;
            background: #fdf2f2;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        .trinaire {{
            font-family: 'Noto Sans', sans-serif;
            font-weight: bold;
            color: #8e44ad;
            background: #f8f4fd;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 8px;
            text-align: center;
            vertical-align: middle;
        }}
        
        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        .emoji {{
            font-size: 1.2em;
        }}
        
        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #27ae60;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        @media print {{
            body {{ 
                background: white;
                font-size: 12pt;
            }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    {html_content}
    
    <script>
        // Amélioration des tableaux
        document.querySelectorAll('table').forEach(table => {{
            table.style.fontSize = '0.9em';
        }});
        
        // Coloration syntaxique spéciale
        document.querySelectorAll('code').forEach(code => {{
            const text = code.textContent;
            if (text.match(/^[A-Z]{{1,5}}$/)) {{
                code.className = 'dhatu';
            }} else if (text.match(/^\/.*\/$/)) {{
                code.className = 'ipa';
            }} else if (text.match(/[AEI]$/)) {{
                code.className = 'trinaire';
            }}
        }});
        
        // Statistiques visuelles
        const statsHTML = `
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">22.7%</div>
                <div>Compression Trinaire</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">20</div>
                <div>Primitives Dhatu</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">87.5%</div>
                <div>Couverture Préscolaire</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">7</div>
                <div>Systèmes Panksepp</div>
            </div>
        </div>
        `;
        
        const firstH2 = document.querySelector('h2');
        if (firstH2) {{
            firstH2.insertAdjacentHTML('afterend', statsHTML);
        }}
    </script>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    file_size = html_path.stat().st_size / 1024  # KB
    
    print(f"✅ HTML généré: {html_path.name}")
    print(f"📊 Taille: {file_size:.1f} KB")
    print(f"🌐 Support Unicode complet activé")
    
    return str(html_path)

if __name__ == "__main__":
    try:
        html_path = generate_html_report()
        print(f"\n🎯 RAPPORT HTML PRÊT!")
        print(f"📂 Ouvrir: file://{html_path}")
    except ImportError:
        print("❌ Module markdown manquant")
        print("💡 Installation: pip install markdown")
    except Exception as e:
        print(f"❌ Erreur: {e}")
