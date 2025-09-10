const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on('console', msg => {
    console.log(`📺 ${msg.type()}: ${msg.text()}`);
  });
  
  try {
    await page.goto('http://localhost:8097/universal-sign-dhatu-interface.html');
    await page.waitForTimeout(5000);
    
    const status = await page.evaluate(() => ({
      three: typeof THREE !== 'undefined',
      gltf: typeof THREE !== 'undefined' && typeof THREE.GLTFLoader !== 'undefined',
      scene: !!window.scene,
      objects: window.scene ? window.scene.children.length : 0
    }));
    
    console.log('🎯 Status:', JSON.stringify(status, null, 2));
    
    if (status.gltf) {
      console.log('🧍 Test chargement modèle 3D...');
      
      // Tester un modèle 3D
      await page.click('button[onclick="loadHandModel(\'cesium\')"]');
      await page.waitForTimeout(8000);
      
      const modelStatus = await page.evaluate(() => {
        const model = window.scene.getObjectByName('human_model_cesium');
        return {
          found: !!model,
          children: model ? model.children.length : 0,
          totalSceneObjects: window.scene.children.length
        };
      });
      
      console.log('🎯 Modèle 3D:', JSON.stringify(modelStatus, null, 2));
      
      if (modelStatus.found) {
        await page.screenshot({ path: 'model-3d-success.png' });
        console.log('📸 Screenshot du modèle 3D réussi');
      }
    }
    
  } catch (error) {
    console.error('❌ Erreur:', error.message);
  }
  
  await browser.close();
})();
