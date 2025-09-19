#!/usr/bin/env node

import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';

const PORT = 8099;
const PAGE_URL = `http://localhost:${PORT}/universal_sign_interface.html`;

async function testDhatuInterface() {
    console.log('🧪 Testing Universal Dhātu Sign Interface');
    console.log('='.repeat(50));

    let browser;
    try {
        // Launch browser in headless mode
        console.log('🚀 Launching browser...');
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();
        
        // Collect console messages
        const consoleMessages = [];
        page.on('console', msg => {
            consoleMessages.push({
                type: msg.type(),
                text: msg.text(),
                timestamp: new Date().toISOString()
            });
        });

        // Navigate to the page
        console.log('📄 Loading interface...');
        const response = await page.goto(PAGE_URL, { 
            waitUntil: 'domcontentloaded', 
            timeout: 15000 
        });

        if (!response.ok()) {
            throw new Error(`Failed to load page: ${response.status()}`);
        }

        console.log('✅ Page loaded successfully');

        // Test 1: Check essential elements
        console.log('🔍 Testing UI elements...');
        
        const elementsTest = await page.evaluate(() => {
            const elements = {
                dhatuPanel: document.getElementById('dhatu-panel'),
                canvasArea: document.getElementById('canvas-area'),
                languageSelector: document.getElementById('language-selector'),
                statusBar: document.getElementById('status-bar')
            };
            
            return {
                dhatuPanel: !!elements.dhatuPanel,
                canvasArea: !!elements.canvasArea,
                languageSelector: !!elements.languageSelector,
                statusBar: !!elements.statusBar,
                allPresent: Object.values(elements).every(el => !!el)
            };
        });

        if (elementsTest.allPresent) {
            console.log('✅ All essential UI elements present');
        } else {
            console.log('⚠️  Some UI elements missing:', elementsTest);
        }

        // Test 2: Check dhātu system
        console.log('🔤 Testing dhātu system...');
        
        const dhatuTest = await page.evaluate(() => {
            const dhatuItems = document.querySelectorAll('.dhatu-item');
            const dhatuNames = Array.from(dhatuItems).map(item => 
                item.getAttribute('data-dhatu')
            ).filter(name => name);
            
            return {
                itemCount: dhatuItems.length,
                dhatuNames: dhatuNames,
                hasSelectDhatu: typeof selectDhatu === 'function'
            };
        });

        console.log(`✅ Found ${dhatuTest.itemCount} dhātu items`);
        console.log(`✅ Dhātu names: ${dhatuTest.dhatuNames.join(', ')}`);

        // Test 3: Test dhātu selection
        console.log('👆 Testing dhātu interaction...');
        
        if (dhatuTest.itemCount > 0) {
            try {
                await page.click('[data-dhatu="RELATE"]');
                
                const selectionTest = await page.evaluate(() => {
                    return {
                        currentDhatu: window.currentDhatu,
                        statusText: document.getElementById('status-bar')?.textContent
                    };
                });
                
                if (selectionTest.currentDhatu === 'RELATE') {
                    console.log('✅ Dhātu selection working');
                } else {
                    console.log('⚠️  Dhātu selection may not be working properly');
                }
            } catch (error) {
                console.log('⚠️  Dhātu interaction test failed:', error.message);
            }
        }

        // Test 4: Test language switching
        console.log('🌍 Testing language switching...');
        
        const languageTest = await page.evaluate(() => {
            const languageButtons = document.querySelectorAll('.language-btn');
            const languages = Array.from(languageButtons).map(btn => btn.textContent);
            
            return {
                buttonCount: languageButtons.length,
                languages: languages,
                currentLanguage: window.currentLanguage
            };
        });

        console.log(`✅ Found ${languageTest.buttonCount} language options: ${languageTest.languages.join(', ')}`);

        // Test 5: Test alphabet/digit generation
        console.log('🔤 Testing alphabet generation...');
        
        const alphabetTest = await page.evaluate(() => {
            const alphaGrid = document.getElementById('alpha-grid');
            const digitGrid = document.getElementById('digit-grid');
            
            return {
                alphabetButtons: alphaGrid ? alphaGrid.children.length : 0,
                digitButtons: digitGrid ? digitGrid.children.length : 0,
                hasPerformLetter: typeof performLetter === 'function',
                hasPerformDigit: typeof performDigit === 'function'
            };
        });

        console.log(`✅ Alphabet buttons: ${alphabetTest.alphabetButtons}`);
        console.log(`✅ Digit buttons: ${alphabetTest.digitButtons}`);

        // Test 6: Test Three.js integration
        console.log('🎨 Testing 3D rendering...');
        
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for potential 3D initialization
        
        const threejsTest = await page.evaluate(() => {
            return {
                threeLoaded: typeof THREE !== 'undefined',
                canvasPresent: !!document.querySelector('#canvas-area canvas'),
                handIKAvailable: !!window.handIK,
                sceneInitialized: !!window.scene
            };
        });

        if (threejsTest.threeLoaded) {
            console.log('✅ Three.js loaded');
        } else {
            console.log('⚠️  Three.js not detected');
        }

        if (threejsTest.canvasPresent) {
            console.log('✅ 3D canvas present');
        } else {
            console.log('⚠️  3D canvas not found');
        }

        // Test 7: Test letter execution
        console.log('👋 Testing letter execution...');
        
        if (alphabetTest.alphabetButtons > 0) {
            try {
                await page.click('.alphabet-btn');
                
                const letterTest = await page.evaluate(() => {
                    return {
                        statusUpdated: document.getElementById('status-bar')?.textContent.includes('Lettre')
                    };
                });
                
                if (letterTest.statusUpdated) {
                    console.log('✅ Letter execution working');
                } else {
                    console.log('⚠️  Letter execution feedback unclear');
                }
            } catch (error) {
                console.log('⚠️  Letter execution test failed:', error.message);
            }
        }

        // Take a screenshot
        console.log('📸 Taking screenshot...');
        await page.screenshot({ 
            path: './test_screenshot.png', 
            fullPage: true 
        });

        // Generate comprehensive report
        const report = {
            timestamp: new Date().toISOString(),
            page_url: PAGE_URL,
            test_results: {
                ui_elements: elementsTest,
                dhatu_system: dhatuTest,
                language_support: languageTest,
                alphabet_generation: alphabetTest,
                threejs_integration: threejsTest
            },
            console_messages: consoleMessages,
            screenshot_saved: 'test_screenshot.png',
            overall_status: 'PASS' // Will be updated based on critical failures
        };

        // Determine overall status
        const criticalFailures = [
            !elementsTest.allPresent,
            dhatuTest.itemCount === 0,
            languageTest.buttonCount === 0,
            !threejsTest.threeLoaded
        ].filter(failure => failure).length;

        report.overall_status = criticalFailures === 0 ? 'PASS' : 
                               criticalFailures <= 1 ? 'WARN' : 'FAIL';

        // Save report
        await fs.writeFile(
            './comprehensive_test_report.json',
            JSON.stringify(report, null, 2)
        );

        console.log('\n📊 TEST SUMMARY');
        console.log('='.repeat(30));
        console.log(`Overall Status: ${report.overall_status}`);
        console.log(`UI Elements: ${elementsTest.allPresent ? 'PASS' : 'FAIL'}`);
        console.log(`Dhātu System: ${dhatuTest.itemCount > 0 ? 'PASS' : 'FAIL'}`);
        console.log(`Languages: ${languageTest.buttonCount > 0 ? 'PASS' : 'FAIL'}`);
        console.log(`3D Integration: ${threejsTest.threeLoaded ? 'PASS' : 'FAIL'}`);
        console.log(`Console Messages: ${consoleMessages.length}`);
        console.log('✅ Comprehensive test report saved');

        return report;

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        return { status: 'ERROR', error: error.message };
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Run the test
if (import.meta.url === `file://${process.argv[1]}`) {
    testDhatuInterface()
        .then(report => {
            console.log('\n🏁 Testing completed');
            process.exit(report.overall_status === 'PASS' ? 0 : 1);
        })
        .catch(error => {
            console.error('💥 Unexpected error:', error);
            process.exit(2);
        });
}

export { testDhatuInterface };