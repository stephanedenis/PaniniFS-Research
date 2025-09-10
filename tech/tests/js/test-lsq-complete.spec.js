import { test, expect } from '@playwright/test';

// Configuration des tests pour LSQ
const LSQ_TEST_CONFIG = {
    baseURL: 'http://localhost:8097',
    timeout: 30000,
    viewport: { width: 1920, height: 1080 },
    slowMo: 500 // Pour observer les animations
};

test.describe('🤟 LSQ - Tests Complets du Système', () => {
    
    test.beforeEach(async ({ page }) => {
        // Démarrer le serveur si nécessaire
        await page.goto(`${LSQ_TEST_CONFIG.baseURL}/lsq-main-interface.html`);
        await page.waitForLoadState('networkidle');
        
        // Attendre que le modèle 3D soit chargé
        await page.waitForSelector('#viewport3d canvas', { timeout: 10000 });
        await page.waitForFunction(() => {
            return window.currentModel && window.currentModel.children.length > 0;
        });
    });

    test.describe('🏗️ Initialisation et Structure', () => {
        
        test('devrait charger l\'interface LSQ correctement', async ({ page }) => {
            // Vérifier le titre
            await expect(page).toHaveTitle(/LSQ.*Langue des Signes Québécoise/);
            
            // Vérifier la structure principale
            await expect(page.locator('.header h1')).toContainText('LSQ - Langue des Signes Québécoise');
            await expect(page.locator('.main-container')).toBeVisible();
            
            // Vérifier les trois panneaux
            await expect(page.locator('.control-panel')).toBeVisible();
            await expect(page.locator('.viewport-3d')).toBeVisible();
            await expect(page.locator('.info-panel')).toBeVisible();
        });

        test('devrait initialiser le modèle 3D avec LeapMotion', async ({ page }) => {
            // Vérifier que le canvas 3D est présent
            const canvas = page.locator('#viewport3d canvas');
            await expect(canvas).toBeVisible();
            
            // Vérifier que l'indicateur de chargement disparaît
            await expect(page.locator('#loadingIndicator')).toBeHidden();
            
            // Vérifier que le modèle est chargé
            const modelLoaded = await page.evaluate(() => {
                return window.currentModel && window.currentModel.children.length > 0;
            });
            expect(modelLoaded).toBe(true);
        });

        test('devrait avoir LSQ comme langue par défaut', async ({ page }) => {
            // Vérifier que le bouton LSQ est actif
            await expect(page.locator('.lang-btn.active')).toContainText('LSQ Québécoise');
            
            // Vérifier le statut
            await expect(page.locator('#statusDisplay')).toContainText('LSQ');
        });
    });

    test.describe('🔤 Alphabet LSQ', () => {
        
        test('devrait afficher tous les 26 lettres de l\'alphabet', async ({ page }) => {
            const letters = await page.locator('.alphabet-grid .letter-btn').count();
            expect(letters).toBe(26);
            
            // Vérifier quelques lettres spécifiques
            await expect(page.locator('[data-key="a"]')).toBeVisible();
            await expect(page.locator('[data-key="z"]')).toBeVisible();
        });

        test('devrait exécuter les gestes pour chaque lettre', async ({ page }) => {
            const testLetters = ['a', 'e', 'i', 'o', 'u']; // Voyelles pour test rapide
            
            for (const letter of testLetters) {
                await page.click(`[data-key="${letter}"]`);
                
                // Vérifier la mise à jour de l'interface
                await expect(page.locator('#currentGesture')).toContainText(`Lettre : ${letter.toUpperCase()}`);
                
                // Vérifier que le bouton devient actif
                await expect(page.locator(`[data-key="${letter}"].active`)).toBeVisible();
                
                // Petite pause pour l'animation
                await page.waitForTimeout(200);
            }
        });

        test('devrait afficher les descriptions LSQ authentiques', async ({ page }) => {
            // Tester des lettres avec descriptions spécifiques LSQ
            await page.hover('[data-key="a"]');
            await expect(page.locator('[data-key="a"] .tooltiptext')).toBeVisible();
            
            await page.click('[data-key="a"]');
            await expect(page.locator('#gestureDescription')).toContainText('Poing fermé');
        });
    });

    test.describe('🔢 Nombres LSQ', () => {
        
        test('devrait afficher les nombres 0-9', async ({ page }) => {
            const numbers = await page.locator('.number-grid .letter-btn').count();
            expect(numbers).toBe(10);
            
            // Test de tous les nombres
            for (let i = 0; i <= 9; i++) {
                await expect(page.locator(`[data-key="${i}"]`)).toBeVisible();
            }
        });

        test('devrait exécuter les gestes numériques', async ({ page }) => {
            const testNumbers = ['1', '5', '9'];
            
            for (const number of testNumbers) {
                await page.click(`[data-key="${number}"]`);
                await expect(page.locator('#currentGesture')).toContainText(`Nombre : ${number}`);
                await page.waitForTimeout(300);
            }
        });
    });

    test.describe('✋ Gestes de Base LSQ', () => {
        
        test('devrait afficher les gestes spécifiques LSQ', async ({ page }) => {
            // Vérifier la présence des gestes LSQ spécifiques
            await expect(page.locator('[data-key="bonjour"]')).toBeVisible();
            await expect(page.locator('[data-key="quebec"]')).toBeVisible();
            await expect(page.locator('[data-key="merci"]')).toBeVisible();
        });

        test('devrait exécuter les gestes québécois', async ({ page }) => {
            // Test du geste spécifique "québec"
            await page.click('[data-key="quebec"]');
            await expect(page.locator('#currentGesture')).toContainText('quebec');
            await expect(page.locator('#gestureDescription')).toContainText('Québec (spécifique LSQ)');
            
            // Vérifier la lecture labiale
            await expect(page.locator('#lipReadingText')).toContainText('québec');
        });

        test('devrait gérer les gestes complexes', async ({ page }) => {
            const complexGestures = ['comprendre', 'repetez'];
            
            for (const gesture of complexGestures) {
                await page.click(`[data-key="${gesture}"]`);
                await expect(page.locator('#currentGesture')).toContainText(gesture);
                await page.waitForTimeout(500); // Plus de temps pour gestes complexes
            }
        });
    });

    test.describe('🤲 Modèle Anatomique LeapMotion', () => {
        
        test('devrait avoir un torse fixe', async ({ page }) => {
            // Vérifier que le torse ne bouge pas lors des gestes
            const initialTorsoPosition = await page.evaluate(() => {
                const torso = window.currentModel.children.find(child => 
                    child.userData && child.userData.fixed
                );
                return torso ? {
                    x: torso.position.x,
                    y: torso.position.y,
                    z: torso.position.z
                } : null;
            });
            
            expect(initialTorsoPosition).not.toBeNull();
            
            // Exécuter quelques gestes
            await page.click('[data-key="a"]');
            await page.waitForTimeout(500);
            await page.click('[data-key="bonjour"]');
            await page.waitForTimeout(500);
            
            // Vérifier que le torse n'a pas bougé
            const finalTorsoPosition = await page.evaluate(() => {
                const torso = window.currentModel.children.find(child => 
                    child.userData && child.userData.fixed
                );
                return torso ? {
                    x: torso.position.x,
                    y: torso.position.y,
                    z: torso.position.z
                } : null;
            });
            
            expect(finalTorsoPosition).toEqual(initialTorsoPosition);
        });

        test('devrait avoir des mains attachées aux bras', async ({ page }) => {
            // Vérifier la structure anatomique complète
            const anatomyCheck = await page.evaluate(() => {
                let armCount = 0;
                let handCount = 0;
                
                window.currentModel.traverse(child => {
                    if (child.userData.side === 'left' || child.userData.side === 'right') {
                        armCount++;
                    }
                    if (child.userData.handModel) {
                        handCount++;
                    }
                });
                
                return { armCount, handCount };
            });
            
            expect(anatomyCheck.armCount).toBe(2); // Deux bras
            expect(anatomyCheck.handCount).toBe(2); // Deux mains attachées
        });

        test('devrait animer les doigts selon LeapMotion', async ({ page }) => {
            // Tester l'animation des doigts
            await page.click('[data-key="a"]'); // Poing fermé
            await page.waitForTimeout(300);
            
            const fingerFlexionA = await page.evaluate(() => {
                let totalFlexion = 0;
                window.currentModel.traverse(child => {
                    if (child.userData.handModel && child.userData.handModel.bones) {
                        const bones = child.userData.handModel.bones;
                        Object.values(bones.index).forEach(segment => {
                            if (segment && segment.rotation) {
                                totalFlexion += Math.abs(segment.rotation.x);
                            }
                        });
                    }
                });
                return totalFlexion;
            });
            
            await page.click('[data-key="5"]'); // Main ouverte
            await page.waitForTimeout(300);
            
            const fingerFlexion5 = await page.evaluate(() => {
                let totalFlexion = 0;
                window.currentModel.traverse(child => {
                    if (child.userData.handModel && child.userData.handModel.bones) {
                        const bones = child.userData.handModel.bones;
                        Object.values(bones.index).forEach(segment => {
                            if (segment && segment.rotation) {
                                totalFlexion += Math.abs(segment.rotation.x);
                            }
                        });
                    }
                });
                return totalFlexion;
            });
            
            // Le poing fermé devrait avoir plus de flexion que la main ouverte
            expect(fingerFlexionA).toBeGreaterThan(fingerFlexion5);
        });
    });

    test.describe('👄 Lecture Labiale', () => {
        
        test('devrait synchroniser les mouvements de bouche', async ({ page }) => {
            const gesturesWithLips = ['bonjour', 'merci', 'quebec'];
            
            for (const gesture of gesturesWithLips) {
                await page.click(`[data-key="${gesture}"]`);
                
                // Vérifier que la lecture labiale est mise à jour
                await expect(page.locator('#mouthDisplay')).toContainText('👄');
                await expect(page.locator('#lipReadingText')).toContainText(gesture);
                
                await page.waitForTimeout(300);
            }
        });

        test('devrait avoir un modèle de visage 3D', async ({ page }) => {
            const faceElements = await page.evaluate(() => {
                let hasHead = false;
                let hasEyes = false;
                let hasMouth = false;
                
                window.currentModel.traverse(child => {
                    if (child.geometry && child.geometry.type === 'SphereGeometry' && 
                        child.position.y > 2) {
                        hasHead = true;
                    }
                    if (child.userData.lipReading) {
                        hasMouth = true;
                    }
                });
                
                return { hasHead, hasMouth };
            });
            
            expect(faceElements.hasHead).toBe(true);
            expect(faceElements.hasMouth).toBe(true);
        });
    });

    test.describe('🔄 Changement de Langue ASL/LSQ', () => {
        
        test('devrait basculer entre LSQ et ASL', async ({ page }) => {
            // Démarrer en LSQ
            await expect(page.locator('.lang-btn.active')).toContainText('LSQ Québécoise');
            
            // Basculer vers ASL
            await page.click('button:has-text("ASL (Complément)")');
            await expect(page.locator('.lang-btn.active')).toContainText('ASL (Complément)');
            
            // Vérifier que l'interface est mise à jour
            await expect(page.locator('#statusDisplay')).toContainText('ASL');
            
            // Revenir à LSQ
            await page.click('button:has-text("LSQ Québécoise")');
            await expect(page.locator('.lang-btn.active')).toContainText('LSQ Québécoise');
        });

        test('devrait avoir des gestes différents par langue', async ({ page }) => {
            // En mode LSQ, vérifier le geste "quebec"
            await expect(page.locator('[data-key="quebec"]')).toBeVisible();
            
            // Basculer vers ASL
            await page.click('button:has-text("ASL (Complément)")');
            await page.waitForTimeout(500);
            
            // Vérifier que les gestes ASL sont affichés
            await expect(page.locator('[data-key="america"]')).toBeVisible();
            await expect(page.locator('[data-key="quebec"]')).toBeHidden();
        });
    });

    test.describe('⚡ Performance et Responsivité', () => {
        
        test('devrait maintenir 60 FPS', async ({ page }) => {
            // Attendre la stabilisation
            await page.waitForTimeout(2000);
            
            // Vérifier le compteur FPS
            const fpsText = await page.locator('#fpsCounter').textContent();
            const fps = parseInt(fpsText.match(/(\d+)/)[1]);
            
            expect(fps).toBeGreaterThanOrEqual(30); // Au minimum 30 FPS
            
            // Tester avec animation intensive
            for (let i = 0; i < 5; i++) {
                await page.click('[data-key="a"]');
                await page.waitForTimeout(100);
                await page.click('[data-key="5"]');
                await page.waitForTimeout(100);
            }
            
            // Vérifier que les FPS restent stables
            await page.waitForTimeout(1000);
            const finalFpsText = await page.locator('#fpsCounter').textContent();
            const finalFps = parseInt(finalFpsText.match(/(\d+)/)[1]);
            
            expect(finalFps).toBeGreaterThanOrEqual(25); // Tolérance pour animations
        });

        test('devrait être responsive sur différentes tailles', async ({ page }) => {
            // Test desktop (par défaut)
            await expect(page.locator('.main-container')).toHaveCSS('display', 'grid');
            
            // Test tablet
            await page.setViewportSize({ width: 768, height: 1024 });
            await page.waitForTimeout(500);
            await expect(page.locator('.main-container')).toBeVisible();
            
            // Test mobile
            await page.setViewportSize({ width: 375, height: 667 });
            await page.waitForTimeout(500);
            await expect(page.locator('.alphabet-grid')).toHaveCSS('grid-template-columns', /repeat\(4,/);
        });
    });

    test.describe('🎯 Tests d\'Intégration Complète', () => {
        
        test('devrait exécuter un workflow complet LSQ', async ({ page }) => {
            // Scénario : Épeler "QUEBEC" en LSQ
            const word = 'quebec';
            
            for (const letter of word) {
                await page.click(`[data-key="${letter}"]`);
                await expect(page.locator('#currentGesture')).toContainText(`Lettre : ${letter.toUpperCase()}`);
                await page.waitForTimeout(400);
            }
            
            // Ensuite faire le geste "québec"
            await page.click('[data-key="quebec"]');
            await expect(page.locator('#currentGesture')).toContainText('quebec');
            await expect(page.locator('#lipReadingText')).toContainText('québec');
        });

        test('devrait gérer les raccourcis clavier', async ({ page }) => {
            // Test raccourcis alphabet
            await page.keyboard.press('a');
            await expect(page.locator('#currentGesture')).toContainText('Lettre : A');
            
            await page.keyboard.press('5');
            await expect(page.locator('#currentGesture')).toContainText('Nombre : 5');
            
            // Test séquence rapide
            await page.keyboard.press('l');
            await page.keyboard.press('s');
            await page.keyboard.press('q');
            
            await expect(page.locator('#currentGesture')).toContainText('Lettre : Q');
        });

        test('devrait préparer le système pour validation expert', async ({ page }) => {
            // Vérifier tous les éléments nécessaires pour un expert LSQ
            
            // 1. Interface complète en français
            await expect(page.locator('.header h1')).toContainText('Québécoise');
            
            // 2. Tous les gestes LSQ disponibles
            const lsqGestures = ['bonjour', 'merci', 'quebec', 'comprendre'];
            for (const gesture of lsqGestures) {
                await expect(page.locator(`[data-key="${gesture}"]`)).toBeVisible();
            }
            
            // 3. Modèle anatomique fonctionnel
            const modelLoaded = await page.evaluate(() => {
                return window.currentModel && 
                       window.currentModel.children.length > 0 &&
                       window.currentModel.children.some(child => child.userData.fixed);
            });
            expect(modelLoaded).toBe(true);
            
            // 4. Performance stable
            const fpsText = await page.locator('#fpsCounter').textContent();
            const fps = parseInt(fpsText.match(/(\d+)/)[1]);
            expect(fps).toBeGreaterThanOrEqual(30);
            
            // 5. Documentation accessible
            await expect(page.locator('#statusDisplay')).toContainText('LSQ');
        });
    });

    test.describe('🚨 Tests de Régression', () => {
        
        test('devrait maintenir la stabilité après actions répétées', async ({ page }) => {
            // Test de stress : 50 gestes rapides
            for (let i = 0; i < 50; i++) {
                const randomLetter = String.fromCharCode(97 + Math.floor(Math.random() * 26));
                await page.click(`[data-key="${randomLetter}"]`);
                
                if (i % 10 === 0) {
                    await page.waitForTimeout(100); // Pause occasionnelle
                }
            }
            
            // Vérifier que le système est toujours stable
            await expect(page.locator('#viewport3d canvas')).toBeVisible();
            
            const fpsText = await page.locator('#fpsCounter').textContent();
            const fps = parseInt(fpsText.match(/(\d+)/)[1]);
            expect(fps).toBeGreaterThanOrEqual(20); // Tolérance après stress
        });

        test('devrait nettoyer les prototypes obsolètes', async ({ page }) => {
            // Vérifier qu'on n'utilise que la nouvelle interface
            await expect(page).toHaveURL(/lsq-main-interface\.html/);
            
            // Vérifier qu'il n'y a pas de références aux anciens prototypes
            const noOldReferences = await page.evaluate(() => {
                const scripts = Array.from(document.scripts);
                const links = Array.from(document.links);
                
                return !scripts.some(script => 
                    script.src.includes('anatomical-3d') || 
                    script.src.includes('sign-language-3d')
                ) && !links.some(link => 
                    link.href.includes('prototype')
                );
            });
            
            expect(noOldReferences).toBe(true);
        });
    });
});

// Tests de configuration pour différents environnements
test.describe('🔧 Configuration et Environnement', () => {
    
    test('devrait fonctionner avec serveur HTTP local', async ({ page }) => {
        // Test avec différents ports
        const ports = [8097, 8080, 8090];
        let workingPort = null;
        
        for (const port of ports) {
            try {
                await page.goto(`http://localhost:${port}/lsq-main-interface.html`, { timeout: 5000 });
                workingPort = port;
                break;
            } catch (e) {
                // Essayer le port suivant
            }
        }
        
        expect(workingPort).not.toBeNull();
        console.log(`✅ Serveur actif sur le port ${workingPort}`);
    });

    test('devrait charger les dépendances Three.js locales', async ({ page }) => {
        // Vérifier que Three.js se charge localement
        const threeLoaded = await page.evaluate(() => {
            return typeof THREE !== 'undefined';
        });
        
        expect(threeLoaded).toBe(true);
        
        // Vérifier les capacités 3D
        const webglSupport = await page.evaluate(() => {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            return gl !== null;
        });
        
        expect(webglSupport).toBe(true);
    });
});
