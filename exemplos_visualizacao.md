# Exemplos de Uso - Visualização e Animação

## Instalação de Dependências

Antes de usar as funcionalidades de visualização, instale as dependências necessárias:

```bash
pip install networkx matplotlib pillow
```

## 1. Visualização Estática da Rede

### Exibir no terminal
```bash
python3 p2p.py config.json visualize
```

### Salvar em arquivo PNG
```bash
python3 p2p.py config.json visualize network_topology.png
```

**Descrição**: Gera um gráfico visual mostrando:
- Todos os nós da rede P2P
- Conexões (arestas) entre os nós
- Recursos disponíveis em cada nó
- Layout otimizado para fácil visualização

## 2. Busca com Animação em Tempo Real

### Exibir animação no terminal
```bash
python3 p2p.py config.json animate n1 musica_rock.mp3 5 flooding
```

### Salvar animação como GIF
```bash
python3 p2p.py config.json animate n1 musica_rock.mp3 5 flooding busca_flooding.gif
```

**Descrição**: Cria uma animação mostrando:
- Nó inicial em **laranja**
- Nós visitados em **amarelo**
- Nó que possui o recurso em **verde** (quando encontrado)
- Caminho percorrido em **vermelho**
- Contador de mensagens e nós envolvidos
- Passo a passo da busca

## 3. Busca Sem Animação (modo original)

```bash
python3 p2p.py config.json search n1 musica_rock.mp3 5 flooding
```

**Descrição**: Executa a busca e mostra apenas os resultados finais (sem visualização).

## Exemplos Práticos

### Comparar diferentes algoritmos visualmente

**Flooding:**
```bash
python3 p2p.py config.json animate n1 archive.zip 10 flooding flooding_demo.gif
```

**Informed Flooding:**
```bash
python3 p2p.py config.json animate n1 archive.zip 10 informed_flooding informed_flooding_demo.gif
```

**Random Walk:**
```bash
python3 p2p.py config.json animate n1 archive.zip 10 random_walk random_walk_demo.gif
```

**Informed Random Walk:**
```bash
python3 p2p.py config.json animate n1 archive.zip 10 informed_random_walk informed_random_walk_demo.gif
```

### Testar com diferentes TTLs

```bash
# TTL baixo (pode não encontrar)
python3 p2p.py config.json animate n1 archive.zip 2 flooding ttl_2.gif

# TTL médio
python3 p2p.py config.json animate n1 archive.zip 5 flooding ttl_5.gif

# TTL alto (maior chance de encontrar)
python3 p2p.py config.json animate n1 archive.zip 10 flooding ttl_10.gif
```

## Características da Visualização

### Visualização Estática
- Mostra toda a topologia da rede
- Identifica recursos em cada nó
- Layout spring (força-repulsão) para melhor organização visual
- Pode ser salva como imagem para apresentações

### Animação da Busca
- Frame-by-frame da execução do algoritmo
- Cores indicativas do estado de cada nó
- Exibe estatísticas em tempo real (mensagens, nós envolvidos)
- Mostra o caminho exato percorrido
- Indicador visual quando o recurso é encontrado
- Pode ser salva como GIF para demonstrações

## Parâmetros dos Comandos

### visualize
```
python3 p2p.py <config.json> visualize [output.png]
```
- `config.json`: arquivo de configuração da rede
- `output.png` (opcional): arquivo de saída da imagem

### animate
```
python3 p2p.py <config.json> animate <node_id> <resource_id> <ttl> <algo> [output.gif]
```
- `node_id`: nó que inicia a busca
- `resource_id`: recurso a ser buscado
- `ttl`: Time To Live (número máximo de saltos)
- `algo`: algoritmo de busca
  - `flooding`
  - `informed_flooding`
  - `random_walk`
  - `informed_random_walk`
- `output.gif` (opcional): arquivo de saída da animação

### search
```
python3 p2p.py <config.json> search <node_id> <resource_id> <ttl> <algo>
```
- Mesmos parâmetros do animate, mas sem visualização
- Mais rápido para testes em lote

## Cores da Animação

| Cor | Significado |
|-----|-------------|
| 🟠 Laranja | Nó inicial (origem da busca) |
| 🟡 Amarelo | Nós visitados durante a busca |
| 🟢 Verde | Nó que possui o recurso (encontrado) |
| ⬜ Cinza | Nós não visitados |
| 🔴 Vermelho | Arestas do caminho percorrido |

## Dicas de Uso

1. **Para apresentações**: Salve as animações como GIF para incluir em slides
2. **Para análise**: Use o modo `visualize` primeiro para entender a topologia
3. **Para comparações**: Execute o mesmo cenário com diferentes algoritmos e compare os GIFs
4. **Para testes**: Use o modo `search` quando precisar apenas dos números
5. **Performance**: Redes muito grandes podem demorar para renderizar - considere usar TTL menor
