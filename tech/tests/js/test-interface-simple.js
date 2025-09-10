// Test simple pour vérifier l'interface sans Playwright
const http = require('http');

function testInterface() {
    console.log('🧪 Test simple de l\'interface...');
    
    const options = {
        hostname: 'localhost',
        port: 8097,
        path: '/universal-sign-dhatu-interface.html',
        method: 'GET'
    };
    
    const req = http.request(options, (res) => {
        console.log(`✅ Interface accessible - Status: ${res.statusCode}`);
        
        let data = '';
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        res.on('end', () => {
            console.log(`📏 Taille de l'interface: ${data.length} caractères`);
            
            // Vérifier la présence de Three.js
            if (data.includes('three.min.js')) {
                console.log('✅ Three.js référencé dans l\'interface');
            } else {
                console.log('❌ Three.js non référencé');
            }
            
            // Vérifier la présence des dhātu
            if (data.includes('data-dhatu=')) {
                const dhatuMatches = data.match(/data-dhatu="/g);
                console.log(`✅ Dhātu détectés: ${dhatuMatches ? dhatuMatches.length : 0}`);
            } else {
                console.log('❌ Aucun dhātu détecté');
            }
            
            // Vérifier les fonctions 3D
            if (data.includes('loadHandModel')) {
                console.log('✅ Fonction loadHandModel présente');
            } else {
                console.log('❌ Fonction loadHandModel manquante');
            }
            
            if (data.includes('initThreeJS')) {
                console.log('✅ Fonction initThreeJS présente');
            } else {
                console.log('❌ Fonction initThreeJS manquante');
            }
            
            if (data.includes('debugLog')) {
                console.log('✅ Logs de debug activés');
            } else {
                console.log('❌ Logs de debug non activés');
            }
            
            console.log('\n🎯 Test terminé - Interface semble OK pour test manuel');
        });
    });
    
    req.on('error', (e) => {
        console.error(`❌ Erreur: ${e.message}`);
    });
    
    req.end();
}

// Test de Three.js
function testThreeJS() {
    console.log('\n🧪 Test de Three.js...');
    
    const options = {
        hostname: 'localhost',
        port: 8097,
        path: '/three.min.js',
        method: 'HEAD'
    };
    
    const req = http.request(options, (res) => {
        console.log(`✅ Three.js accessible - Status: ${res.statusCode}`);
        console.log(`📏 Taille: ${res.headers['content-length']} bytes`);
    });
    
    req.on('error', (e) => {
        console.error(`❌ Three.js non accessible: ${e.message}`);
    });
    
    req.end();
}

setTimeout(() => {
    testInterface();
    setTimeout(() => {
        testThreeJS();
    }, 1000);
}, 500);
