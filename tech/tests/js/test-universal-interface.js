const { chromium } = require('playwright');
const fs = require('fs');

async function testUniversalInterface() {
    console.log('🧪 Test de l\'interface universelle dhātu...');
    
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Capture des logs console
    page.on('console', msg => {
        console.log(`🟦 Console [${msg.type()}]:`, msg.text());
    });
    
    // Capture des erreurs
    page.on('pageerror', error => {
        console.error('🔴 Erreur page:', error.message);
    });
    
    try {
        console.log('📍 Navigation vers l\'interface...');
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        console.log('📸 Capture d\'écran initiale...');
        await page.screenshot({ path: 'test-universal-interface-initial.png', fullPage: true });
        
        // Vérifier la présence des dhātu
        console.log('🧬 Vérification des dhātu...');
        const dhatuCount = await page.locator('.dhatu-item').count();
        console.log(`✅ Dhātu détectés: ${dhatuCount}`);
        
        // Vérifier la présence des langues signées
        console.log('🌍 Vérification des langues signées...');
        const languageCount = await page.locator('.language-btn').count();
        console.log(`✅ Langues signées détectées: ${languageCount}`);
        
        // Vérifier la zone 3D
        console.log('🎨 Vérification zone 3D...');
        const canvasExists = await page.locator('canvas').count() > 0;
        console.log(`Canvas 3D présent: ${canvasExists}`);
        
        // Test interaction dhātu
        console.log('🔄 Test interaction dhātu...');
        await page.click('[data-dhatu="MODAL"]');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test-dhatu-modal-click.png', fullPage: true });
        
        // Test sélection langue
        console.log('🗣️ Test sélection langue...');
        await page.click('text=ASL (USA)');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test-language-asl-selection.png', fullPage: true });
        
        // Test alphabet
        console.log('🔤 Test alphabet...');
        await page.click('text=A');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test-alphabet-letter-a.png', fullPage: true });
        
        // Vérifier erreurs Three.js
        const errors = await page.evaluate(() => {
            return window.console._logs || [];
        });
        
        console.log('📊 Résumé du test:');
        console.log(`- Dhātu: ${dhatuCount}/9`);
        console.log(`- Langues: ${languageCount}`);
        console.log(`- Canvas 3D: ${canvasExists ? 'Oui' : 'Non'}`);
        
        await page.waitForTimeout(3000);
        
    } catch (error) {
        console.error('❌ Erreur durant le test:', error);
        await page.screenshot({ path: 'test-error-screenshot.png', fullPage: true });
    } finally {
        await browser.close();
    }
}

testUniversalInterface().catch(console.error);
