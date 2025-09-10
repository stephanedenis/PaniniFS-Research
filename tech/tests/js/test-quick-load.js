const puppeteer = require('puppeteer');

console.log('🧪 TEST RAPIDE DE CHARGEMENT...');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // Écouter les erreurs
    page.on('console', msg => {
        if (msg.type() === 'error') {
            console.log(`🔴 ERREUR JS: ${msg.text()}`);
        }
    });
    
    page.on('error', err => {
        console.log(`🔴 ERREUR PAGE: ${err.message}`);
    });
    
    page.on('pageerror', err => {
        console.log(`🔴 ERREUR SCRIPT: ${err.message}`);
    });
    
    try {
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'domcontentloaded',
            timeout: 10000 
        });
        console.log('✅ Page chargée');
        
        // Vérifier Three.js
        const threeStatus = await page.evaluate(() => {
            return typeof THREE !== 'undefined' ? THREE.REVISION : 'NON_TROUVE';
        });
        console.log(`🎮 Three.js: ${threeStatus}`);
        
        // Vérifier GLTFLoader
        const gltfStatus = await page.evaluate(() => {
            return typeof THREE !== 'undefined' && typeof THREE.GLTFLoader !== 'undefined' ? 'DISPONIBLE' : 'MANQUANT';
        });
        console.log(`📦 GLTFLoader: ${gltfStatus}`);
        
    } catch (error) {
        console.error('❌ Erreur:', error.message);
    }
    
    await browser.close();
})();
