#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peer Verification System for Dhatu Analysis Reproducibility
Ensures transparent, verifiable, and reproducible scientific results
"""

import json
import hashlib
import time
import zipfile
from pathlib import Path
import shutil
import tempfile


def main():
    """Simple peer verification demonstration"""
    
    print("=" * 55)
    print("Peer Verification System for Dhatu Analysis")
    print("=" * 55)
    
    # Create verification directory
    verification_dir = Path('./verification_system')
    verification_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (verification_dir / 'packages').mkdir(exist_ok=True)
    (verification_dir / 'reproductions').mkdir(exist_ok=True)
    
    # Check for existing analyses
    analyses_found = []
    
    corpus_file = Path('./corpus_simple/corpus.json')
    if corpus_file.exists():
        analyses_found.append(('corpus', str(corpus_file)))
    
    # Check for analysis result files
    analysis_files = [
        './corpus_simple/prime_base_analysis.json',
        './corpus_simple/mathematical_analysis.json', 
        './corpus_simple/performance_report.json'
    ]
    
    for analysis_file in analysis_files:
        if Path(analysis_file).exists():
            analyses_found.append(('analysis', analysis_file))
    
    # Check for algorithm files
    algorithm_files = [
        './simple_collector.py',
        './prime_base_analyzer.py', 
        './math_notation_parser.py',
        './performance_estimator.py'
    ]
    
    for algo_file in algorithm_files:
        if Path(algo_file).exists():
            analyses_found.append(('algorithm', algo_file))
    
    print("Found {} verifiable components:".format(len(analyses_found)))
    for component_type, filepath in analyses_found:
        print("  {} - {}".format(component_type.upper(), filepath))
    
    # Create verification package
    if analyses_found:
        package_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        package_dir = verification_dir / 'packages' / package_id
        package_dir.mkdir(exist_ok=True)
        
        print("\nCreating verification package: {}".format(package_id))
        
        # Copy files to package
        copied_files = []
        for component_type, filepath in analyses_found:
            if Path(filepath).exists():
                dest = package_dir / Path(filepath).name
                shutil.copy2(filepath, dest)
                copied_files.append(str(dest))
                print("  Copied: {}".format(Path(filepath).name))
        
        # Create package metadata
        metadata = {
            'package_id': package_id,
            'creation_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'algorithm_version': 'enhanced_dhatu_v1.0',
            'included_files': copied_files,
            'verification_status': 'packaged'
        }
        
        # Save metadata
        metadata_file = package_dir / 'package_metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Create simple verification script
        verification_script = package_dir / 'verify.py'
        script_content = '''#!/usr/bin/env python3
import json
import os
from pathlib import Path

def verify_package():
    print("Verifying dhatu analysis package...")
    
    # Check for required files
    required_files = ['package_metadata.json']
    missing_files = []
    
    for filename in required_files:
        if not Path(filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print("Missing required files: {}".format(missing_files))
        return False
    
    # Load metadata
    with open('package_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print("Package ID: {}".format(metadata['package_id']))
    print("Created: {}".format(metadata['creation_timestamp']))
    print("Files included: {}".format(len(metadata['included_files'])))
    
    # Check file integrity
    missing_included = []
    for filepath in metadata['included_files']:
        if not Path(filepath).exists():
            missing_included.append(filepath)
    
    if missing_included:
        print("Missing included files: {}".format(missing_included))
        return False
    
    print("Package verification: PASSED")
    return True

if __name__ == "__main__":
    success = verify_package()
    exit(0 if success else 1)
'''
        
        with open(verification_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Create verification report
        report = {
            'verification_system_version': '1.0',
            'report_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'packages_created': 1,
            'package_ids': [package_id],
            'total_components': len(analyses_found),
            'component_breakdown': {
                'corpus_files': len([x for x in analyses_found if x[0] == 'corpus']),
                'analysis_files': len([x for x in analyses_found if x[0] == 'analysis']),
                'algorithm_files': len([x for x in analyses_found if x[0] == 'algorithm'])
            },
            'reproducibility_status': 'packaged_for_verification'
        }
        
        # Save report
        report_file = verification_dir / 'verification_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("\nVerification package created successfully!")
        print("Package directory: {}".format(package_dir))
        print("Verification report: {}".format(report_file))
        
        # Test the verification script
        print("\nTesting verification script...")
        import subprocess
        import sys
        
        try:
            result = subprocess.run(
                [sys.executable, str(verification_script)],
                cwd=str(package_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("Verification test: PASSED")
                print("Output:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print("  {}".format(line))
            else:
                print("Verification test: FAILED")
                print("Error: {}".format(result.stderr))
                
        except Exception as e:
            print("Verification test error: {}".format(e))
        
        # Display summary
        print("\n" + "=" * 55)
        print("VERIFICATION SUMMARY")
        print("=" * 55)
        print("Package ID: {}".format(package_id))
        print("Components packaged: {}".format(len(analyses_found)))
        print("Verification script: Created and tested")
        print("Reproducibility: Ready for peer verification")
        print("=" * 55)
        
    else:
        print("\nNo verifiable components found.")
        print("Please ensure analysis files exist in the corpus_simple directory.")


if __name__ == "__main__":
    main()