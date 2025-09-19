#!/usr/bin/env python
import json
import os

def verify_package():
    print("Verifying dhatu analysis package...")
    
    # Check for required files
    if not os.path.exists('package_metadata.json'):
        print("Missing required file: package_metadata.json")
        return False
    
    # Load metadata
    with open('package_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print("Package ID: {}".format(metadata['package_id']))
    print("Created: {}".format(metadata['creation_timestamp']))
    print("Files included: {}".format(metadata['file_count']))
    
    # Check file integrity
    missing_files = []
    for filepath in metadata['included_files']:
        filename = os.path.basename(filepath)
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        print("Missing files: {}".format(missing_files))
        return False
    
    print("Package verification: PASSED")
    return True

if __name__ == "__main__":
    success = verify_package()
    exit(0 if success else 1)
