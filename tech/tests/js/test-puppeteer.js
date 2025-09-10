const puppeteer = require('puppeteer');

async function testModelsQuick() {
    console.log('🧪 TEST RAPIDE DES MODÈLES 3D...');
    
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: false,
            defaultViewport: { width: 1920, height: 1080 },
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const page = await browser.newPage();
        
        // Capture des logs console
        page.on('console', msg => {
            console.log(`🟦 Console [${msg.type()}]:`, msg.text());
        });
        
        // Capture des erreurs
        page.on('pageerror', error => {
            console.error('🔴 Erreur JS:', error.message);
        });
        
        console.log('📍 Navigation vers l\'interface...');
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'networkidle0',
            timeout: 10000 
        });
        
        // Attendre que Three.js soit chargé
        await page.waitForFunction(() => window.THREE !== undefined, { timeout: 5000 });
        console.log('✅ Three.js chargé');
        
        // Attendre que l'init soit terminé
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Capture avant interaction
        await page.screenshot({ path: 'debug-01-initial.png', fullPage: true });
        console.log('📸 Capture initiale prise');
        
        // Vérifier la présence du canvas
        const canvasExists = await page.$('canvas');
        console.log(`Canvas 3D présent: ${canvasExists ? 'OUI' : 'NON'}`);
        
        if (canvasExists) {
            const canvasInfo = await page.evaluate(() => {
                const canvas = document.querySelector('canvas');
                return {
                    width: canvas.width,
                    height: canvas.height,
                    style: canvas.style.cssText
                };
            });
            console.log('🎨 Info canvas:', canvasInfo);
        }
        
        // Vérifier les objets dans la scène
        const sceneInfo = await page.evaluate(() => {
            if (window.scene) {
                return {
                    children: window.scene.children.length,
                    objects: window.scene.children.map(child => ({
                        type: child.type,
                        name: child.name,
                        visible: child.visible
                    }))
                };
            }
            return null;
        });
        
        console.log('🎯 Scène 3D:', JSON.stringify(sceneInfo, null, 2));
        
        // Test clic sur modèle main droite
        console.log('🤲 Test clic main droite...');
        await page.click('text=🫱 Main Droite');
        await new Promise(resolve => setTimeout(resolve, 2000));
        await page.screenshot({ path: 'debug-02-main-droite.png', fullPage: true });
        
        // Vérifier à nouveau la scène après clic
        const sceneAfter = await page.evaluate(() => {
            if (window.scene && window.currentHands) {
                return {
                    sceneChildren: window.scene.children.length,
                    handsLoaded: {
                        left: window.currentHands.left ? 'YES' : 'NO',
                        right: window.currentHands.right ? 'YES' : 'NO'
                    }
                };
            }
            return null;
        });
        
        console.log('🎯 Scène après clic:', JSON.stringify(sceneAfter, null, 2));
        
        console.log('✅ Test terminé');
        
    } catch (error) {
        console.error('❌ Erreur test:', error.message);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Installer puppeteer si nécessaire
try {
    require('puppeteer');
    testModelsQuick();
} catch (e) {
    console.log('📦 Installation de puppeteer...');
    const { exec } = require('child_process');
    exec('npm install puppeteer', (error, stdout, stderr) => {
        if (error) {
            console.error('❌ Erreur installation puppeteer:', error);
            return;
        }
        console.log('✅ Puppeteer installé');
        testModelsQuick();
    });
}
