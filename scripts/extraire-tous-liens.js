// Script JavaScript à exécuter dans la console du navigateur
// pour extraire TOUS les liens d'articles depuis toutes les pages

// Fonction pour extraire les liens d'une page
function extraireLiensPage() {
    const liens = [];
    document.querySelectorAll('a[href*="/fr/actualites/"]').forEach(a => {
        const href = a.href;
        if (href.match(/\/fr\/actualites\/\d+/) && 
            !href.includes('?start=') && 
            !href.includes('?page=') &&
            !href.endsWith('/fr/actualites')) {
            if (!liens.includes(href)) {
                liens.push(href);
            }
        }
    });
    return liens;
}

// Fonction pour naviguer vers une page et extraire les liens
async function extraireTousLiens() {
    const baseUrl = 'https://gfz-online.fr/fr/actualites';
    const tousLiens = new Set();
    
    // Page 1
    console.log('Page 1...');
    const liens1 = extraireLiensPage();
    liens1.forEach(l => tousLiens.add(l));
    console.log(`${liens1.length} liens trouvés (Total: ${tousLiens.size})`);
    
    // Pages 2 à 9 (incrément de 5)
    for (let page = 2; page <= 9; page++) {
        const start = (page - 1) * 5;
        const url = `${baseUrl}?start=${start}`;
        
        console.log(`\nPage ${page} (${url})...`);
        
        try {
            // Charger la page
            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extraire les liens
            const liensPage = [];
            doc.querySelectorAll('a[href*="/fr/actualites/"]').forEach(a => {
                const href = a.href || a.getAttribute('href');
                if (href && href.match(/\/fr\/actualites\/\d+/) && 
                    !href.includes('?start=') && 
                    !href.includes('?page=') &&
                    !href.endsWith('/fr/actualites')) {
                    const lienComplet = href.startsWith('http') ? href : `https://gfz-online.fr${href}`;
                    liensPage.push(lienComplet);
                }
            });
            
            liensPage.forEach(l => tousLiens.add(l));
            console.log(`${liensPage.length} nouveaux liens (Total: ${tousLiens.size})`);
            
            // Attendre un peu avant la prochaine requête
            await new Promise(resolve => setTimeout(resolve, 1000));
        } catch (error) {
            console.error(`Erreur page ${page}:`, error);
        }
    }
    
    const liensArray = Array.from(tousLiens).sort();
    console.log(`\n✅ Total: ${liensArray.length} liens uniques trouvés\n`);
    console.log(JSON.stringify(liensArray, null, 2));
    
    // Copier dans le presse-papiers
    if (navigator.clipboard) {
        navigator.clipboard.writeText(JSON.stringify(liensArray, null, 2));
        console.log('✅ Liens copiés dans le presse-papiers !');
    }
    
    return liensArray;
}

// Lancer l'extraction
extraireTousLiens();
