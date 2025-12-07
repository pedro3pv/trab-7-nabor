#!/bin/bash

# Script de demonstração das funcionalidades de visualização
# Sistema P2P - Trabalho 7

echo "=============================================="
echo "Demo de Visualização - Sistema P2P"
echo "=============================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se as dependências estão instaladas
echo -e "${BLUE}Verificando dependências...${NC}"
python3 -c "import networkx, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Instalando dependências necessárias...${NC}"
    pip install networkx matplotlib pillow
fi

echo ""
echo -e "${GREEN}✓ Dependências instaladas${NC}"
echo ""

# 1. Visualização da topologia
echo -e "${BLUE}1. Gerando visualização da topologia da rede...${NC}"
python3 p2p.py config.json visualize network_topology.png
echo -e "${GREEN}   → Arquivo salvo: network_topology.png${NC}"
echo ""

# 2. Demonstração de cada algoritmo
echo -e "${BLUE}2. Gerando animações dos algoritmos de busca...${NC}"
echo ""

echo -e "${YELLOW}   a) Flooding${NC}"
python3 p2p.py config.json animate n1 archive.zip 10 flooding demo_flooding.gif
echo -e "${GREEN}      → Arquivo salvo: demo_flooding.gif${NC}"
echo ""

echo -e "${YELLOW}   b) Informed Flooding${NC}"
python3 p2p.py config.json animate n1 archive.zip 10 informed_flooding demo_informed_flooding.gif
echo -e "${GREEN}      → Arquivo salvo: demo_informed_flooding.gif${NC}"
echo ""

echo -e "${YELLOW}   c) Random Walk${NC}"
python3 p2p.py config.json animate n1 archive.zip 10 random_walk demo_random_walk.gif
echo -e "${GREEN}      → Arquivo salvo: demo_random_walk.gif${NC}"
echo ""

echo -e "${YELLOW}   d) Informed Random Walk${NC}"
python3 p2p.py config.json animate n1 archive.zip 10 informed_random_walk demo_informed_random_walk.gif
echo -e "${GREEN}      → Arquivo salvo: demo_informed_random_walk.gif${NC}"
echo ""

# 3. Comparação com diferentes TTLs
echo -e "${BLUE}3. Demonstrando efeito do TTL (usando Flooding)...${NC}"
echo ""

echo -e "${YELLOW}   TTL = 2 (limitado)${NC}"
python3 p2p.py config.json animate n1 archive.zip 2 flooding demo_ttl_2.gif
echo -e "${GREEN}      → Arquivo salvo: demo_ttl_2.gif${NC}"
echo ""

echo -e "${YELLOW}   TTL = 5 (médio)${NC}"
python3 p2p.py config.json animate n1 archive.zip 5 flooding demo_ttl_5.gif
echo -e "${GREEN}      → Arquivo salvo: demo_ttl_5.gif${NC}"
echo ""

echo -e "${YELLOW}   TTL = 10 (amplo)${NC}"
python3 p2p.py config.json animate n1 archive.zip 10 flooding demo_ttl_10.gif
echo -e "${GREEN}      → Arquivo salvo: demo_ttl_10.gif${NC}"
echo ""

# 4. Testes comparativos (modo texto)
echo -e "${BLUE}4. Executando testes comparativos (modo texto)...${NC}"
echo ""

echo -e "${YELLOW}Buscando 'musica_rock.mp3' a partir de n1:${NC}"
echo ""
for algo in flooding informed_flooding random_walk informed_random_walk; do
    echo -e "   ${algo}:"
    python3 p2p.py config.json search n1 musica_rock.mp3 10 $algo | grep -E "(Encontrado|Mensagens|Nós)" | sed 's/^/      /'
    echo ""
done

# Resumo final
echo "=============================================="
echo -e "${GREEN}✓ Demonstração concluída!${NC}"
echo "=============================================="
echo ""
echo "Arquivos gerados:"
echo "  • network_topology.png - Topologia da rede"
echo "  • demo_flooding.gif - Animação do Flooding"
echo "  • demo_informed_flooding.gif - Animação do Informed Flooding"
echo "  • demo_random_walk.gif - Animação do Random Walk"
echo "  • demo_informed_random_walk.gif - Animação do Informed Random Walk"
echo "  • demo_ttl_*.gif - Comparação de diferentes TTLs"
echo ""
echo "Consulte 'exemplos_visualizacao.md' para mais informações!"
echo ""
