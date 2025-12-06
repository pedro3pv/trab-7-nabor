# Implementação de Algoritmos de Busca em Sistemas P2P

Este projeto implementa uma simulação de uma rede Peer-to-Peer (P2P) não estruturada, permitindo a execução e comparação de diferentes algoritmos de busca de recursos (Flooding e Random Walk), incluindo suas variantes informadas (com cache).

## 1. Identificação da Equipe
*Preencha com os nomes dos integrantes:*
*   Pedro Augusto De Oliveira Neto - 2224213
*   Francisco Dantas Da Silva Neto - 2223879
*   Natanael Freitas De Azevedo - 2224186

## 2. Principais Funcionalidades

O software foi desenvolvido em **Python** e opera através de linha de comando (CLI). Suas principais capacidades incluem:

*   **Carregamento de Topologia:** Leitura de arquivos de configuração (`.json`) que definem nós, vizinhos (arestas) e recursos disponíveis em cada nó.
*   **Validação da Rede:** Verificação automática de integridade, garantindo que o grafo seja conexo (sem partições), não contenha laços (self-loops) e respeite os limites mínimos e máximos de vizinhos.
*   **Algoritmos de Busca:**
    *   **Flooding (Inundação):** Propaga a busca para todos os vizinhos até encontrar o recurso ou esgotar o TTL. Garante encontrar o caminho, mas gera alto tráfego.
    *   **Random Walk (Passeio Aleatório):** Envia a busca para apenas um vizinho aleatório por vez. Reduz o tráfego, mas pode demorar mais para encontrar recursos distantes.
    *   **Variantes Informadas:** Ambos os algoritmos possuem versões "Informed" que utilizam um cache local para armazenar a localização de recursos previamente encontrados, acelerando buscas futuras.
*   **Métricas de Desempenho:** Para cada busca, o sistema relata se houve sucesso, o número total de mensagens trocadas e a quantidade de nós distintos envolvidos.

## 3. Resultados dos Testes Comparativos

Abaixo estão os resultados obtidos executando os algoritmos na topologia de teste definida em `config.json`.

### Tabela de Resultados

| Cenário | Algoritmo | Origem → Destino | Msgs Trocadas | Nós Envolvidos | Caminho Encontrado | Observação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Recurso Próximo** | Flooding | n1 → n2 | 2 | 2 | `n1 -> n2` | Eficiente para vizinhos diretos. [1] |
| **Recurso Distante** | Flooding | n1 → n6 | 8 | 6 | `n1 -> n2 -> n4 -> n6` | Inundou a rede inteira (6 nós) para achar o alvo. [2] |
| **Recurso Distante** | Random Walk | n1 → n6 | 5 | 4 | `n1->n2->n1->n2->n4->n6` | Menos nós envolvidos que o Flooding, mas caminho redundante. [3] |

### Análise dos Dados
*   **Flooding em Recurso Distante:** O algoritmo garantiu o menor caminho lógico (`n1->n2->n4->n6`), mas ao custo de envolver **100% da rede** (6 de 6 nós) e gerar o maior número de mensagens (8). Isso confirma a característica de alto tráfego do algoritmo.[2]
*   **Random Walk em Recurso Distante:** O algoritmo utilizou menos mensagens (5) e incomodou menos nós (4) do que a inundação. No entanto, o caminho foi errático, visitando o nó `n2` múltiplas vezes (`n1->n2->n1->n2...`) antes de avançar, demonstrando a aleatoriedade do processo.[3]

## Como Executar

### Pré-requisitos
*   Python 3.x instalado.

### Comandos de Exemplo

Para reproduzir os testes acima, utilize os seguintes comandos no terminal:

```bash
# 1. Flooding - Recurso Próximo
python p2p.py config.json n1 imagem_festa.jpg 5 flooding

# 2. Flooding - Recurso Distante
python p2p.py config.json n1 archive.zip 5 flooding

# 3. Random Walk - Recurso Distante
python p2p.py config.json n1 archive.zip 20 random_walk
```

Para automação completa dos testes e geração de logs:
```bash
# Em ambientes Unix/Linux/Git Bash
./testes.sh
```