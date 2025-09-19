import { test, expect } from '@playwright/test';

const PORT = 8099;
const PAGE = `http://localhost:${PORT}/universal_sign_interface.html`;

test.describe('Universal Dhātu Interface - Core Functionality', () => {
  test('dhātu interface loads and displays core elements', async ({ page }) => {
    // Navigate to the interface
    const response = await page.goto(PAGE, { waitUntil: 'domcontentloaded', timeout: 15000 });
    expect(response?.ok()).toBeTruthy();

    // Test core UI elements
    await page.waitForSelector('#dhatu-panel', { timeout: 7000 });
    
    const coreElements = await page.evaluate(() => {
      return {
        dhatuPanel: !!document.getElementById('dhatu-panel'),
        canvasArea: !!document.getElementById('canvas-area'),
        languageSelector: !!document.getElementById('language-selector'),
        statusBar: !!document.getElementById('status-bar')
      };
    });

    expect(coreElements.dhatuPanel).toBeTruthy();
    expect(coreElements.canvasArea).toBeTruthy();
    expect(coreElements.languageSelector).toBeTruthy();
    expect(coreElements.statusBar).toBeTruthy();

    // Test dhātu system presence
    const dhatuElements = await page.evaluate(() => {
      const items = document.querySelectorAll('.dhatu-item');
      return {
        count: items.length,
        names: Array.from(items).map(item => item.getAttribute('data-dhatu')).filter(Boolean)
      };
    });

    expect(dhatuElements.count).toBeGreaterThan(5);
    expect(dhatuElements.names).toContain('RELATE');
    expect(dhatuElements.names).toContain('EVAL');

    // Test language support
    const languageElements = await page.evaluate(() => {
      const buttons = document.querySelectorAll('.language-btn');
      return {
        count: buttons.length,
        hasLSQ: Array.from(buttons).some(btn => btn.textContent.includes('LSQ')),
        hasASL: Array.from(buttons).some(btn => btn.textContent.includes('ASL'))
      };
    });

    expect(languageElements.count).toBeGreaterThan(10);
    expect(languageElements.hasLSQ).toBeTruthy();
    expect(languageElements.hasASL).toBeTruthy();

    // Test Three.js presence
    const threejsStatus = await page.evaluate(() => {
      return {
        loaded: typeof THREE !== 'undefined',
        hasScene: !!window.scene,
        hasRenderer: !!window.renderer
      };
    });

    expect(threejsStatus.loaded).toBeTruthy();

    console.log('✅ All core interface tests passed');
  });

  test('dhātu semantic integration functional', async ({ page }) => {
    await page.goto(PAGE, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForSelector('#dhatu-panel', { timeout: 7000 });

    // Test dhātu semantic concepts
    const semanticTest = await page.evaluate(() => {
      const dhatuItems = document.querySelectorAll('.dhatu-item');
      const semanticConcepts = [];
      
      dhatuItems.forEach(item => {
        const dhatu = item.getAttribute('data-dhatu');
        const concept = item.querySelector('.dhatu-concept')?.textContent;
        if (dhatu && concept) {
          semanticConcepts.push({ dhatu, concept });
        }
      });

      return {
        concepts: semanticConcepts,
        hasSemanticMapping: semanticConcepts.length > 0
      };
    });

    expect(semanticTest.hasSemanticMapping).toBeTruthy();
    expect(semanticTest.concepts.length).toBeGreaterThan(5);

    // Check for key dhātu concepts
    const conceptTexts = semanticTest.concepts.map(c => c.concept.toLowerCase());
    const hasRelationConcept = conceptTexts.some(c => c.includes('relation') || c.includes('spatial'));
    const hasModalConcept = conceptTexts.some(c => c.includes('modal') || c.includes('négation'));
    
    expect(hasRelationConcept || hasModalConcept).toBeTruthy();

    console.log('✅ Dhātu semantic integration verified');
  });

  test('multilingual sign language support', async ({ page }) => {
    await page.goto(PAGE, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForSelector('#language-selector', { timeout: 7000 });

    // Test multilingual capabilities
    const multilingualTest = await page.evaluate(() => {
      const languageButtons = document.querySelectorAll('.language-btn');
      const languages = Array.from(languageButtons).map(btn => btn.textContent);
      
      const signLanguages = languages.filter(lang => 
        lang.includes('LSQ') || lang.includes('ASL') || lang.includes('LSF') || 
        lang.includes('BSL') || lang.includes('DGS') || lang.includes('JSL')
      );

      return {
        totalLanguages: languages.length,
        signLanguages: signLanguages.length,
        supportedRegions: signLanguages.map(lang => {
          if (lang.includes('LSQ')) return 'Quebec';
          if (lang.includes('ASL')) return 'USA';
          if (lang.includes('LSF')) return 'France';
          if (lang.includes('BSL')) return 'UK';
          if (lang.includes('DGS')) return 'Germany';
          if (lang.includes('JSL')) return 'Japan';
          return 'Other';
        }).filter((v, i, a) => a.indexOf(v) === i)
      };
    });

    expect(multilingualTest.signLanguages).toBeGreaterThan(5);
    expect(multilingualTest.supportedRegions.length).toBeGreaterThan(3);

    console.log('✅ Multilingual sign language support verified');
    console.log(`Supported regions: ${multilingualTest.supportedRegions.join(', ')}`);
  });
});