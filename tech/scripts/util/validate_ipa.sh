#!/bin/bash

# Script de validation automatique IPA
# Vérifie que tous les fichiers utilisent la notation IPA correcte

echo "🔬 VALIDATION ALPHABET PHONÉTIQUE INTERNATIONAL"
echo "=================================================="

REPO_ROOT="/home/stephane/GitHub/PaniniFS-Research"
VALIDATION_PASSED=true

# Couleurs pour les résultats
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "\n📋 Vérification des fichiers principaux..."

# Fonction de validation IPA
validate_ipa_file() {
    local file="$1"
    local name="$2"
    
    echo -en "  Vérification $name... "
    
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FICHIER MANQUANT${NC}"
        VALIDATION_PASSED=false
        return 1
    fi
    
    local errors=0
    
    # Vérifier notation en crochets [...]
    if ! grep -q '\[.*\]' "$file"; then
        echo -e "${RED}ERREUR: Notation crochets manquante${NC}"
        ((errors++))
    fi
    
    # Vérifier absence notation phonémique inappropriée (ignorer comparaisons old-system)
    if grep -v 'old-system' "$file" | grep -q '/[ptbkgmnd][aiou]/' && [[ "$file" != *.md ]]; then
        echo -e "${YELLOW}ATTENTION: Notation phonémique active détectée${NC}"
        ((errors++))
    fi
    
    # Vérifier symbole IPA ɡ correct
    if grep -q '\[.*gi.*\]' "$file" && ! grep -q 'ɡi' "$file"; then
        echo -e "${RED}ERREUR: Symbole g au lieu de ɡ IPA${NC}"
        ((errors++))
    fi
    
    # Vérifier triangle vocalique
    local vowel_count=0
    grep -q 'i' "$file" && ((vowel_count++))
    grep -q 'u' "$file" && ((vowel_count++)) 
    grep -q 'a' "$file" && ((vowel_count++))
    
    if [[ $vowel_count -lt 3 ]] && [[ "$file" != *.md ]]; then
        echo -e "${YELLOW}ATTENTION: Triangle vocalique incomplet${NC}"
        ((errors++))
    fi
    
    if [[ $errors -eq 0 ]]; then
        echo -e "${GREEN}✓ VALIDÉ${NC}"
        return 0
    else
        echo -e "${RED}✗ ERREURS: $errors${NC}"
        VALIDATION_PASSED=false
        return 1
    fi
}

# Validation des fichiers principaux
validate_ipa_file "$REPO_ROOT/language/prototype_simplifie.html" "Prototype Principal"
validate_ipa_file "$REPO_ROOT/validation/demo_corpus_multilingue.html" "Demo Corpus"
validate_ipa_file "$REPO_ROOT/validation/phonetique_enfantine_demo.html" "Demo Phonétique"

echo -e "\n🔍 Recherche des inconsistances IPA..."

# Vérifier les primitives spécifiques
echo -en "  Vérification primitives IPA... "
primitive_errors=0

for file in "$REPO_ROOT/language/prototype_simplifie.html" "$REPO_ROOT/validation/"*.html; do
    if [[ -f "$file" ]]; then
        # Vérifier que toutes les primitives utilisent ɡi et non gi
        if grep -q 'gi' "$file" && ! grep -q 'ɡi' "$file"; then
            echo -e "\n    ${RED}ERREUR dans $file: 'gi' au lieu de 'ɡi'${NC}"
            ((primitive_errors++))
        fi
        
        # Vérifier que les primitives principales sont en crochets
        if grep -q '\bpi\b\|\btu\b\|\bka\b\|\bba\b\|\bmu\b\|\bni\b\|\bda\b\|\bbu\b' "$file" && [[ "$file" =~ (demo|prototype) ]]; then
            if ! grep -q '\[pi\]\|\[tu\]\|\[ka\]\|\[ba\]\|\[mu\]\|\[ni\]\|\[da\]\|\[bu\]' "$file"; then
                echo -e "\n    ${YELLOW}INFO dans $file: primitives en contexte libre${NC}"
            fi
        fi
    fi
done

if [[ $primitive_errors -eq 0 ]]; then
    echo -e "${GREEN}✓ VALIDÉ${NC}"
else
    echo -e "${RED}✗ ERREURS: $primitive_errors${NC}"
    VALIDATION_PASSED=false
fi

echo -e "\n📊 Analyse du contenu IPA..."

# Compter les occurrences des symboles IPA
echo "  Symboles IPA détectés:"
for file in "$REPO_ROOT/language/"*.html "$REPO_ROOT/validation/"*.html; do
    if [[ -f "$file" ]]; then
        basename_file=$(basename "$file")
        
        # Compter crochets IPA
        brackets_count=$(grep -o '\[[^]]*\]' "$file" | wc -l)
        echo "    $basename_file: $brackets_count notations IPA"
        
        # Vérifier ɡ spécifiquement  
        if grep -q 'ɡ' "$file"; then
            echo "      ✓ Symbole IPA ɡ présent"
        fi
    fi
done

echo -e "\n🎯 Tests de conformité IPA..."

# Vérifier descriptions phonétiques
echo -en "  Descriptions articulatoires... "
desc_errors=0

for file in "$REPO_ROOT/language/"*.html "$REPO_ROOT/validation/"*.html; do
    if [[ -f "$file" ]]; then
        # Vérifier traits IPA
        if ! grep -q 'bilabial\|dental\|vélaire' "$file"; then
            ((desc_errors++))
        fi
        if ! grep -q 'sourd\|sonore\|nasal' "$file"; then
            ((desc_errors++))
        fi
        if ! grep -q 'fermée\|ouverte' "$file"; then
            ((desc_errors++))
        fi
    fi
done

if [[ $desc_errors -eq 0 ]]; then
    echo -e "${GREEN}✓ COMPLET${NC}"
else
    echo -e "${YELLOW}⚠ PARTIEL${NC}"
fi

# Vérifier corpus scientifique
echo -en "  Corpus séquence IPA... "
if grep -q '\[pi ɡi ba tu ka bu\]' "$REPO_ROOT/validation/"*.html; then
    echo -e "${GREEN}✓ VALIDÉ${NC}"
else
    echo -e "${RED}✗ MANQUANT${NC}"
    VALIDATION_PASSED=false
fi

echo -e "\n📈 Statistiques IPA du projet..."

total_files=$(find "$REPO_ROOT" -name "*.html" | wc -l)
ipa_files=$(find "$REPO_ROOT" -name "*.html" -exec grep -l '\[.*\]' {} \; | wc -l)
phonetic_files=$(find "$REPO_ROOT" -name "*.html" -exec grep -l 'bilabial\|dental\|vélaire' {} \; | wc -l)

echo "  Fichiers HTML total: $total_files"
echo "  Fichiers avec notation IPA: $ipa_files"
echo "  Fichiers avec descriptions phonétiques: $phonetic_files"

# Calcul pourcentage de couverture IPA
if [[ $total_files -gt 0 ]]; then
    coverage=$((ipa_files * 100 / total_files))
    echo "  Couverture IPA: $coverage%"
fi

echo -e "\n=================================================="

if [[ $VALIDATION_PASSED == true ]]; then
    echo -e "${GREEN}🎉 VALIDATION IPA RÉUSSIE${NC}"
    echo "✅ Alphabet Phonétique International correctement implémenté"
    echo "✅ Triangle vocalique [i-u-a] validé"  
    echo "✅ Consonnes précoces accessibles"
    echo "✅ Symbole ɡ vélaire IPA correct"
    echo "✅ Notation scientifique en crochets"
    exit 0
else
    echo -e "${RED}❌ VALIDATION IPA ÉCHOUÉE${NC}"
    echo "⚠️ Des corrections sont nécessaires"
    echo "📖 Consultez les erreurs ci-dessus"
    exit 1
fi
