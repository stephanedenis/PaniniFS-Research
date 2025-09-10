const { chromium } = require('playwright');

async function testModels3D() {
    console.log('🧪 TEST COMPLET DES MODÈLES 3D...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 1000
    });
    
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Capture TOUS les logs console
    const consoleLogs = [];
    page.on('console', msg => {
        const log = `[${msg.type()}] ${msg.text()}`;
        console.log(`🟦 Console: ${log}`);
        consoleLogs.push(log);
    });
    
    // Capture les erreurs JavaScript
    const jsErrors = [];
    page.on('pageerror', error => {
        const errorMsg = `❌ JS Error: ${error.message}`;
        console.error(errorMsg);
        jsErrors.push(errorMsg);
    });
    
    // Capture les échecs de requêtes
    const failedRequests = [];
    page.on('requestfailed', request => {
        const failMsg = `❌ Request failed: ${request.url()} - ${request.failure().errorText}`;
        console.error(failMsg);
        failedRequests.push(failMsg);
    });
    
    try {
        console.log('📍 Navigation vers l\'interface...');
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        // Attendre le chargement de Three.js
        console.log('⏳ Attente du chargement de Three.js...');
        await page.waitForFunction(() => window.THREE !== undefined, { timeout: 10000 });
        console.log('✅ Three.js chargé');
        
        // Capture initiale
        console.log('📸 Capture initiale...');
        await page.screenshot({ path: 'test-01-initial.png', fullPage: true });
        
        // Vérifier la présence du canvas 3D
        console.log('🎨 Vérification canvas 3D...');
        const canvasCount = await page.locator('canvas').count();
        console.log(`Canvas détectés: ${canvasCount}`);
        
        if (canvasCount === 0) {
            console.error('❌ AUCUN CANVAS 3D DÉTECTÉ !');
        }
        
        // Test chargement modèle main droite
        console.log('🤲 Test chargement main droite...');
        await page.click('text=🫱 Main Droite');
        await page.waitForTimeout(3000);
        await page.screenshot({ path: 'test-02-main-droite.png', fullPage: true });
        
        // Vérifier les objets 3D dans la scène
        const sceneInfo = await page.evaluate(() => {
            if (window.scene) {
                return {
                    children: window.scene.children.length,
                    objects: window.scene.children.map(child => ({
                        type: child.type,
                        name: child.name,
                        visible: child.visible,
                        position: child.position
                    }))
                };
            }
            return { error: 'Scene not found' };
        });
        
        console.log('🎯 Informations scène 3D:', JSON.stringify(sceneInfo, null, 2));
        
        // Test chargement corps complet
        console.log('🧍 Test chargement corps complet...');
        await page.click('text=🧍 Corps Complet');
        await page.waitForTimeout(3000);
        await page.screenshot({ path: 'test-03-corps-complet.png', fullPage: true });
        
        // Test sélection dhātu
        console.log('🧬 Test sélection dhātu...');
        await page.click('[data-dhatu="RELATE"]');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test-04-dhatu-relate.png', fullPage: true });
        
        // Test phrase commune
        console.log('💬 Test phrase commune...');
        await page.click('text=Bonjour/Hello');
        await page.waitForTimeout(2000);
        await page.screenshot({ path: 'test-05-phrase-bonjour.png', fullPage: true });
        
        // Test alphabet
        console.log('🔤 Test alphabet...');
        await page.click('text=A');
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test-06-alphabet-a.png', fullPage: true });
        
        // Vérifier les erreurs
        console.log('\n📊 RAPPORT DE TEST:');
        console.log(`Canvas 3D: ${canvasCount > 0 ? '✅' : '❌'}`);
        console.log(`Erreurs JS: ${jsErrors.length}`);
        console.log(`Requêtes échouées: ${failedRequests.length}`);
        console.log(`Logs console: ${consoleLogs.length}`);
        
        if (jsErrors.length > 0) {
            console.log('\n❌ ERREURS JAVASCRIPT:');
            jsErrors.forEach(error => console.log(`  ${error}`));
        }
        
        if (failedRequests.length > 0) {
            console.log('\n❌ REQUÊTES ÉCHOUÉES:');
            failedRequests.forEach(req => console.log(`  ${req}`));
        }
        
        // Test final de la scène après tous les chargements
        const finalSceneInfo = await page.evaluate(() => {
            if (window.scene && window.currentHands) {
                return {
                    sceneChildren: window.scene.children.length,
                    currentHands: {
                        left: window.currentHands.left ? 'present' : 'null',
                        right: window.currentHands.right ? 'present' : 'null'
                    },
                    renderer: window.renderer ? 'present' : 'null',
                    camera: window.camera ? 'present' : 'null'
                };
            }
            return { error: 'Scene objects not found' };
        });
        
        console.log('\n🎯 ÉTAT FINAL SCÈNE 3D:');
        console.log(JSON.stringify(finalSceneInfo, null, 2));
        
        await page.waitForTimeout(5000);
        
    } catch (error) {
        console.error('❌ ERREUR DURANT LE TEST:', error.message);
        await page.screenshot({ path: 'test-error.png', fullPage: true });
    } finally {
        await browser.close();
        
        console.log('\n🎯 CAPTURES GÉNÉRÉES:');
        console.log('  - test-01-initial.png');
        console.log('  - test-02-main-droite.png');
        console.log('  - test-03-corps-complet.png');
        console.log('  - test-04-dhatu-relate.png');
        console.log('  - test-05-phrase-bonjour.png');
        console.log('  - test-06-alphabet-a.png');
    }
}

testModels3D().catch(console.error);
