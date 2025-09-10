const puppeteer = require('puppeteer');

console.log('🔬 TEST SIMPLE DES MODÈLES 3D...');

(async () => {
    const browser = await puppeteer.launch({ 
        headless: false, // Mode visible pour debugging
        defaultViewport: null,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // Écouter les messages de console
    page.on('console', msg => {
        console.log(`📺 ${msg.type()}: ${msg.text()}`);
    });
    
    try {
        console.log('🌐 Chargement de l\'interface...');
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'load',
            timeout: 20000 
        });
        
        console.log('⏳ Attente de l\'initialisation...');
        await page.waitForTimeout(5000);
        
        // Capture écran initial
        await page.screenshot({ path: 'interface-loaded.png' });
        console.log('📸 Interface initiale capturée');
        
        // Vérifier l'état de la scène
        const sceneInfo = await page.evaluate(() => {
            return {
                threeLoaded: typeof THREE !== 'undefined',
                gltfLoaded: typeof THREE !== 'undefined' && typeof THREE.GLTFLoader !== 'undefined',
                sceneExists: window.scene !== null,
                objectsInScene: window.scene ? window.scene.children.length : 0
            };
        });
        
        console.log('🎯 État de la scène:', JSON.stringify(sceneInfo, null, 2));
        
        if (sceneInfo.gltfLoaded) {
            console.log('🧍 Test chargement CesiumMan...');
            
            // Cliquer sur le bouton CesiumMan
            await page.click('button[onclick="loadHandModel(\'cesium\')"]');
            
            // Attendre le chargement
            await page.waitForTimeout(8000);
            
            // Vérifier le résultat
            const modelLoaded = await page.evaluate(() => {
                const model = window.scene.getObjectByName('human_model_cesium');
                return {
                    found: !!model,
                    position: model ? [model.position.x, model.position.y, model.position.z] : null,
                    children: model ? model.children.length : 0
                };
            });
            
            console.log('🎯 CesiumMan chargé:', JSON.stringify(modelLoaded, null, 2));
            
            if (modelLoaded.found) {
                await page.screenshot({ path: 'cesium-man-success.png' });
                console.log('📸 CesiumMan screenshot prise');
            }
        }
        
        console.log('✅ Tests terminés');
        
    } catch (error) {
        console.error('❌ Erreur:', error.message);
        await page.screenshot({ path: 'error-debug.png' });
    }
    
    // Garder le navigateur ouvert pour inspection manuelle
    console.log('🔍 Navigateur restera ouvert pour inspection...');
    // await browser.close();
})();
