#!/usr/bin/env node

import fetch from 'node-fetch';
import { promises as fs } from 'fs';
import path from 'path';

const PORT = 8099;
const BASE_URL = `http://localhost:${PORT}`;

async function validateInterface() {
    console.log('🧪 Validating Universal Sign Interface...');
    console.log('='.repeat(50));

    try {
        // Test 1: Check if server is responding
        console.log('📡 Testing server availability...');
        const response = await fetch(`${BASE_URL}/universal_sign_interface.html`);
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        
        console.log('✅ Server is responding correctly');
        
        // Test 2: Check HTML content
        console.log('📄 Analyzing HTML content...');
        const htmlContent = await response.text();
        
        // Check for essential elements
        const essentialElements = [
            'dhatu-panel',
            'canvas-area', 
            'language-selector',
            'status-bar'
        ];
        
        const missingElements = essentialElements.filter(id => 
            !htmlContent.includes(`id="${id}"`)
        );
        
        if (missingElements.length > 0) {
            console.log(`⚠️  Missing elements: ${missingElements.join(', ')}`);
        } else {
            console.log('✅ All essential UI elements found');
        }
        
        // Test 3: Check for Three.js dependencies
        console.log('🔧 Checking Three.js dependencies...');
        const hasThreeJS = htmlContent.includes('three.min.js') || htmlContent.includes('three.js');
        const hasOrbitControls = htmlContent.includes('OrbitControls');
        
        if (hasThreeJS) {
            console.log('✅ Three.js library detected');
        } else {
            console.log('⚠️  Three.js library not found');
        }
        
        if (hasOrbitControls) {
            console.log('✅ OrbitControls detected');
        } else {
            console.log('⚠️  OrbitControls not found');
        }
        
        // Test 4: Check for dhātu system integration
        console.log('🔤 Checking dhātu system integration...');
        const dhatuKeywords = ['dhatu', 'DHATU', 'dhātu'];
        const foundDhatus = dhatuKeywords.filter(keyword => 
            htmlContent.includes(keyword)
        );
        
        if (foundDhatus.length > 0) {
            console.log('✅ Dhātu system integration found');
        } else {
            console.log('⚠️  Dhātu system integration not detected');
        }
        
        // Test 5: Check language support
        console.log('🌍 Checking language support...');
        const languageKeywords = ['LSQ', 'ASL', 'langue', 'sign'];
        const foundLanguages = languageKeywords.filter(keyword => 
            htmlContent.toLowerCase().includes(keyword.toLowerCase())
        );
        
        if (foundLanguages.length > 0) {
            console.log(`✅ Language support detected: ${foundLanguages.join(', ')}`);
        } else {
            console.log('⚠️  Language support not clearly detected');
        }
        
        // Generate report
        console.log('\n📊 VALIDATION REPORT');
        console.log('='.repeat(30));
        
        const report = {
            timestamp: new Date().toISOString(),
            server_status: 'OK',
            html_size: htmlContent.length,
            essential_elements: {
                total: essentialElements.length,
                missing: missingElements.length,
                missing_list: missingElements
            },
            dependencies: {
                threejs: hasThreeJS,
                orbit_controls: hasOrbitControls
            },
            dhatu_integration: foundDhatus.length > 0,
            language_support: foundLanguages,
            overall_status: missingElements.length === 0 ? 'GOOD' : 'NEEDS_ATTENTION'
        };
        
        // Save report
        await fs.writeFile(
            './interface_validation_report.json', 
            JSON.stringify(report, null, 2)
        );
        
        console.log(`Status: ${report.overall_status}`);
        console.log(`HTML Size: ${report.html_size} bytes`);
        console.log(`Missing Elements: ${report.essential_elements.missing}`);
        console.log('✅ Validation report saved to interface_validation_report.json');
        
        return report;
        
    } catch (error) {
        console.error('❌ Validation failed:', error.message);
        return { status: 'FAILED', error: error.message };
    }
}

// Run validation if this is the main module
if (import.meta.url === `file://${process.argv[1]}`) {
    validateInterface()
        .then(report => {
            console.log('\n🏁 Validation completed');
            process.exit(report.overall_status === 'GOOD' ? 0 : 1);
        })
        .catch(error => {
            console.error('💥 Unexpected error:', error);
            process.exit(2);
        });
}

export { validateInterface };