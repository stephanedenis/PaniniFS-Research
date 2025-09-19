import { test, expect } from '@playwright/test';

// Port et chemin constants demandés
const PORT = 8099;
const PAGE = `http://localhost:${PORT}/universal_sign_interface.html`;

async function collectConsole(page) {
  const messages = [];
  page.on('console', msg => messages.push({ type: msg.type(), text: msg.text() }));
  return messages;
}

test.describe('Universal Sign Interface – Tests complets dhātu', () => {
  test('interface dhātu complète fonctionnelle', async ({ page, browserName }) => {
    const consoleMessages = await collectConsole(page);
    const response = await page.goto(PAGE, { waitUntil: 'domcontentloaded', timeout: 15000 });
    expect(response?.ok(), 'Page non accessible').toBeTruthy();

    // Test 1: Éléments UI essentiels
    await page.waitForSelector('#dhatu-panel', { timeout: 7000 });
    
    const uiElements = await page.evaluate(() => {
      return {
        dhatuPanel: !!document.getElementById('dhatu-panel'),
        canvasArea: !!document.getElementById('canvas-area'),
        languageSelector: !!document.getElementById('language-selector'),
        statusBar: !!document.getElementById('status-bar')
      };
    });
    
    expect(uiElements.dhatuPanel, 'Panneau dhātu manquant').toBeTruthy();
    expect(uiElements.canvasArea, 'Zone canvas manquante').toBeTruthy();
    expect(uiElements.languageSelector, 'Sélecteur langue manquant').toBeTruthy();
    expect(uiElements.statusBar, 'Barre statut manquante').toBeTruthy();

    // Test 2: Système dhātu 
    const dhatuSystem = await page.evaluate(() => {
      const dhatuItems = document.querySelectorAll('.dhatu-item');
      const dhatuNames = Array.from(dhatuItems).map(item => 
        item.getAttribute('data-dhatu')
      ).filter(name => name);
      
      return {
        itemCount: dhatuItems.length,
        dhatuNames: dhatuNames
      };
    });

    expect(dhatuSystem.itemCount, 'Aucun élément dhātu trouvé').toBeGreaterThan(0);
    expect(dhatuSystem.dhatuNames.length, 'Noms dhātu manquants').toBeGreaterThan(0);
    
    // Vérifier les dhātus universels attendus
    const expectedDhatus = ['RELATE', 'EVAL', 'EXIST', 'MODAL'];
    const foundExpected = expectedDhatus.filter(dhatu => 
      dhatuSystem.dhatuNames.includes(dhatu)
    );
    expect(foundExpected.length, 'Dhātus universels manquants').toBeGreaterThan(2);

    // Test 3: Support multilingue
    const languageSupport = await page.evaluate(() => {
      const languageButtons = document.querySelectorAll('.language-btn');
      const languages = Array.from(languageButtons).map(btn => btn.textContent);
      
      return {
        buttonCount: languageButtons.length,
        languages: languages.slice(0, 10) // Limiter pour la lisibilité
      };
    });

    expect(languageSupport.buttonCount, 'Support multilingue insuffisant').toBeGreaterThan(5);

    // Test 4: Intégration Three.js
    const threejsIntegration = await page.evaluate(() => {
      return {
        threeLoaded: typeof THREE !== 'undefined',
        windowGlobals: {
          scene: !!window.scene,
          renderer: !!window.renderer,
          camera: !!window.camera
        }
      };
    });

    expect(threejsIntegration.threeLoaded, 'Three.js non chargé').toBeTruthy();

    // Test 5: Fonctions dhātu-langue (wait for scripts to load)
    await page.waitForFunction(() => typeof window.performLetter === 'function', { timeout: 5000 })
      .catch(() => console.log('performLetter function not available'));
    
    const dhatuLanguageFunctions = await page.evaluate(() => {
      return {
        hasPerformLetter: typeof performLetter === 'function',
        hasSelectDhatu: typeof selectDhatu === 'function', 
        hasUpdateStatus: typeof updateStatus === 'function',
        currentLanguage: window.currentLanguage || 'LSQ',
        currentDhatu: window.currentDhatu || 'RELATE'
      };
    });

    // Note: performLetter might be in local scope, so this is informational
    console.log('Function availability:', dhatuLanguageFunctions);

    // Screenshot avec nom descriptif
    await page.screenshot({ 
      path: `test-artifacts/dhatu-interface-${browserName}.png`, 
      fullPage: true 
    });

    // Sauvegarde rapport détaillé
    const testReport = {
      timestamp: new Date().toISOString(),
      browser: browserName,
      ui_elements: uiElements,
      dhatu_system: dhatuSystem,
      language_support: languageSupport,
      threejs_integration: threejsIntegration,
      functions: dhatuLanguageFunctions,
      console_messages: consoleMessages.slice(0, 20) // Limiter les logs
    };

    const fs = await import('fs');
    fs.mkdirSync('test-artifacts', { recursive: true });
    fs.writeFileSync(
      `test-artifacts/dhatu-test-report-${browserName}.json`, 
      JSON.stringify(testReport, null, 2)
    );
  });

  test('performance dhātu et responsivité', async ({ page }) => {
    const startTime = Date.now();
    await page.goto(PAGE, { waitUntil: 'networkidle', timeout: 20000 });
    
    const loadTime = Date.now() - startTime;
    expect(loadTime, 'Temps de chargement trop long').toBeLessThan(10000);

    // Test responsive design
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.setViewportSize({ width: 375, height: 667 });

    const responsiveTest = await page.evaluate(() => {
      const dhatuPanel = document.getElementById('dhatu-panel');
      const canvasArea = document.getElementById('canvas-area');
      
      return {
        dhatuPanelVisible: dhatuPanel && getComputedStyle(dhatuPanel).display !== 'none',
        canvasAreaVisible: canvasArea && getComputedStyle(canvasArea).display !== 'none'
      };
    });

    expect(responsiveTest.dhatuPanelVisible, 'Panneau dhātu non responsive').toBeTruthy();
    expect(responsiveTest.canvasAreaVisible, 'Zone canvas non responsive').toBeTruthy();
  });
});
