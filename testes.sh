#!/bin/bash
echo "--- TESTE 1: Recurso Próximo (Flooding) ---" >> resultados.txt
python p2p.py config.json n1 imagem_festa.jpg 5 flooding >> resultados.txt

echo "\n--- TESTE 2: Recurso Distante (Flooding) ---" >> resultados2.txt
python p2p.py config.json n1 archive.zip 5 flooding >> resultados2.txt

echo "\n--- TESTE 3: Recurso Distante (Random Walk) ---" >> resultados3.txt
python p2p.py config.json n1 archive.zip 20 random_walk >> resultados3.txt

echo "Testes concluídos. Verifique o arquivo resultados.txt"