const puppeteer = require('puppeteer');

console.log('🧪 TEST DES MODÈLES 3D COMPLETS AVEC RIGGING...');

(async () => {
    const browser = await puppeteer.launch({ 
        headless: false,
        defaultViewport: { width: 1580, height: 1080 }
    });
    
    const page = await browser.newPage();
    
    // Écouter les logs de console
    page.on('console', msg => {
        const type = msg.type();
        const text = msg.text();
        
        if (type === 'log') {
            console.log(`🟦 Console [${type}]: ${text}`);
        } else if (type === 'error') {
            console.log(`🔴 Console [${type}]: ${text}`);
        } else if (type === 'warn') {
            console.log(`🟨 Console [${type}]: ${text}`);
        }
    });
    
    try {
        console.log('📍 Navigation vers l\'interface...');
        await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html', { 
            waitUntil: 'networkidle0',
            timeout: 15000 
        });
        
        // Attendre que Three.js soit chargé
        await page.waitForFunction(() => typeof THREE !== 'undefined');
        console.log('✅ Three.js chargé');
        
        // Vérifier que GLTFLoader est disponible
        const gltfLoaderAvailable = await page.evaluate(() => {
            return typeof THREE.GLTFLoader !== 'undefined';
        });
        console.log(`📦 GLTFLoader disponible: ${gltfLoaderAvailable ? 'OUI' : 'NON'}`);
        
        // Attendre un peu pour l'initialisation
        await page.waitForTimeout(3000);
        
        // Capture initiale
        await page.screenshot({ path: 'interface-before-models.png' });
        console.log('📸 Capture avant chargement modèles');
        
        // Test 1: Charger CesiumMan
        console.log('🧍 Test chargement CesiumMan...');
        await page.click('button[onclick="loadHandModel(\'cesium\')"]');
        
        // Attendre le chargement
        await page.waitForTimeout(5000);
        
        // Vérifier le chargement
        const cesiumLoaded = await page.evaluate(() => {
            const model = window.scene.getObjectByName('human_model_cesium');
            return model ? {
                loaded: true,
                children: model.children.length,
                position: { x: model.position.x, y: model.position.y, z: model.position.z },
                scale: { x: model.scale.x, y: model.scale.y, z: model.scale.z }
            } : { loaded: false };
        });
        
        console.log(`🎯 CesiumMan: ${JSON.stringify(cesiumLoaded, null, 2)}`);
        
        if (cesiumLoaded.loaded) {
            await page.screenshot({ path: 'cesium-man-loaded.png' });
            console.log('📸 Screenshot CesiumMan prise');
        }
        
        // Test 2: Charger RiggedFigure
        console.log('👤 Test chargement RiggedFigure...');
        await page.click('button[onclick="loadHandModel(\'figure\')"]');
        
        await page.waitForTimeout(5000);
        
        const figureLoaded = await page.evaluate(() => {
            const model = window.scene.getObjectByName('human_model_figure');
            return model ? {
                loaded: true,
                children: model.children.length,
                position: { x: model.position.x, y: model.position.y, z: model.position.z }
            } : { loaded: false };
        });
        
        console.log(`🎯 RiggedFigure: ${JSON.stringify(figureLoaded, null, 2)}`);
        
        if (figureLoaded.loaded) {
            await page.screenshot({ path: 'rigged-figure-loaded.png' });
            console.log('📸 Screenshot RiggedFigure prise');
        }
        
        // Test 3: Vérifier l'état final de la scène
        const sceneState = await page.evaluate(() => {
            return {
                totalObjects: window.scene.children.length,
                models: window.scene.children
                    .filter(child => child.name.includes('human_model'))
                    .map(child => ({
                        name: child.name,
                        type: child.type,
                        children: child.children.length,
                        visible: child.visible
                    }))
            };
        });
        
        console.log('🎯 État final de la scène:');
        console.log(JSON.stringify(sceneState, null, 2));
        
        // Capture finale
        await page.screenshot({ path: 'interface-with-real-models.png', fullPage: false });
        console.log('📸 Capture finale prise');
        
        console.log('✅ Test des modèles 3D complets terminé');
        
    } catch (error) {
        console.error('❌ Erreur pendant le test:', error);
        await page.screenshot({ path: 'error-screenshot.png' });
    }
    
    await browser.close();
})();
