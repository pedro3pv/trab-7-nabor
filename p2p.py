import json
import sys
import random
from collections import deque, defaultdict
from typing import Dict, Set, List, Tuple, Optional


class Node:
    def __init__(self, node_id: str, resources: Set[str]):
        self.id = node_id
        self.resources = set(resources)
        self.neighbors: Set[str] = set()
        # cache[resource_id] = set(node_ids que possuem o recurso)
        self.cache: Dict[str, Set[str]] = defaultdict(set)

    def add_neighbor(self, neighbor_id: str):
        if neighbor_id == self.id:
            raise ValueError(f"Aresta de loop detectada em {self.id}")
        self.neighbors.add(neighbor_id)


class P2PNetwork:
    def __init__(self, config: dict):
        self.nodes: Dict[str, Node] = {}
        self.min_neighbors = config["min_neighbors"]
        self.max_neighbors = config["max_neighbors"]

        # Cria nós
        for node_id, res_list in config["resources"].items():
            if not res_list:
                raise ValueError(f"Nó {node_id} sem recursos")
            self.nodes[node_id] = Node(node_id, set(res_list))

        # Cria arestas
        for a, b in config["edges"]:
            if a not in self.nodes or b not in self.nodes:
                raise ValueError(f"Aresta inválida: {a}-{b}")
            if a == b:
                raise ValueError(f"Aresta de loop detectada em {a}")
            self.nodes[a].add_neighbor(b)
            self.nodes[b].add_neighbor(a)

        # Valida rede
        self._validate_degrees()
        self._validate_connected()

    def _validate_degrees(self):
        for node in self.nodes.values():
            deg = len(node.neighbors)
            if deg < self.min_neighbors or deg > self.max_neighbors:
                raise ValueError(
                    f"Nó {node.id} tem {deg} vizinhos, "
                    f"fora do intervalo [{self.min_neighbors}, {self.max_neighbors}]"
                )

    def _validate_connected(self):
        # BFS a partir de um nó qualquer
        start = next(iter(self.nodes))
        visited = set()
        queue = deque([start])
        while queue:
            u = queue.popleft()
            if u in visited:
                continue
            visited.add(u)
            for v in self.nodes[u].neighbors:
                if v not in visited:
                    queue.append(v)
        if len(visited) != len(self.nodes):
            raise ValueError("A rede está particionada (não é totalmente conectada)")

    # ---------- Utilidades comuns ----------

    def _update_cache_on_hit(self, path: List[str], resource_id: str, target_id: str):
        """
        Atualiza o cache de todos os nós no caminho com a informação
        de que 'target_id' possui 'resource_id'.
        """
        for node_id in path:
            self.nodes[node_id].cache[resource_id].add(target_id)

    # ---------- Algoritmos de busca ----------

    def search(
        self,
        node_id: str,
        resource_id: str,
        ttl: int,
        algo: str,
        seed: Optional[int] = None,
    ) -> Tuple[bool, int, int, List[str]]:
        """
        Retorna:
          found: bool
          msg_count: int (nº de mensagens trocadas)
          nodes_involved: int (nº distinto de nós que processaram a busca)
          path: caminho até o alvo (se encontrado)
        """
        if node_id not in self.nodes:
            raise ValueError(f"Nó de origem {node_id} não existe")

        if seed is not None:
            random.seed(seed)

        algo = algo.lower()
        if algo == "flooding":
            return self._search_flooding(node_id, resource_id, ttl, informed=False)
        elif algo == "informed_flooding":
            return self._search_flooding(node_id, resource_id, ttl, informed=True)
        elif algo == "random_walk":
            return self._search_random_walk(node_id, resource_id, ttl, informed=False)
        elif algo == "informed_random_walk":
            return self._search_random_walk(node_id, resource_id, ttl, informed=True)
        else:
            raise ValueError(f"Algoritmo desconhecido: {algo}")

    def _search_flooding(
        self,
        start_id: str,
        resource_id: str,
        ttl: int,
        informed: bool,
    ) -> Tuple[bool, int, int, List[str]]:
        msg_count = 0
        visited = set()
        nodes_involved = set()
        # fila: (node_id, ttl_restante, path)
        queue = deque([(start_id, ttl, [start_id])])

        while queue:
            node_id, ttl_left, path = queue.popleft()
            if ttl_left < 0:
                continue
            if node_id in visited:
                continue

            visited.add(node_id)
            nodes_involved.add(node_id)
            node = self.nodes[node_id]

            # Verifica se o próprio nó tem o recurso
            if resource_id in node.resources:
                # acerto
                self._update_cache_on_hit(path, resource_id, node_id)
                return True, msg_count, len(nodes_involved), path

            # Se for "informado" e o nó souber quem tem o recurso
            if informed and resource_id in node.cache and node.cache[resource_id]:
                # Considera que a mensagem segue diretamente para um nó conhecido
                target_id = next(iter(node.cache[resource_id]))
                msg_count += 1
                path2 = path + [target_id]
                self._update_cache_on_hit(path2, resource_id, target_id)
                nodes_involved.add(target_id)
                return True, msg_count, len(nodes_involved), path2

            if ttl_left == 0:
                continue

            # Envia para todos os vizinhos (flood)
            for neigh_id in node.neighbors:
                if neigh_id not in visited:
                    msg_count += 1
                    queue.append((neigh_id, ttl_left - 1, path + [neigh_id]))

        return False, msg_count, len(nodes_involved), []

    def _search_random_walk(
        self,
        start_id: str,
        resource_id: str,
        ttl: int,
        informed: bool,
    ) -> Tuple[bool, int, int, List[str]]:
        msg_count = 0
        nodes_involved = set()
        current_id = start_id
        path = [current_id]

        while ttl >= 0:
            node = self.nodes[current_id]
            nodes_involved.add(current_id)

            # Verifica recurso local
            if resource_id in node.resources:
                self._update_cache_on_hit(path, resource_id, current_id)
                return True, msg_count, len(nodes_involved), path

            # Se for informado e souber alguém que possua o recurso
            if informed and resource_id in node.cache and node.cache[resource_id]:
                target_id = next(iter(node.cache[resource_id]))
                msg_count += 1
                path.append(target_id)
                nodes_involved.add(target_id)
                self._update_cache_on_hit(path, resource_id, target_id)
                return True, msg_count, len(nodes_involved), path

            if ttl == 0:
                break

            if not node.neighbors:
                break

            # Escolhe vizinho aleatório
            next_id = random.choice(list(node.neighbors))
            msg_count += 1
            ttl -= 1
            current_id = next_id
            path.append(current_id)

        return False, msg_count, len(nodes_involved), []


def load_config(path: str) -> dict:
    """
    Espera um JSON no formato:
    {
      "num_nodes": 4,
      "min_neighbors": 1,
      "max_neighbors": 3,
      "resources": {
        "n1": ["r1", "r2"],
        "n2": ["r3"],
        "n3": ["r4"],
        "n4": ["r5"]
      },
      "edges": [
        ["n1", "n2"],
        ["n2", "n3"],
        ["n3", "n4"]
      ]
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # Checagem simples de consistência
    if cfg["num_nodes"] != len(cfg["resources"]):
        raise ValueError("num_nodes diferente da quantidade de nós em resources")

    return cfg


def main():
    if len(sys.argv) < 6:
        print(
            "Uso: python p2p.py <config.json> <node_id> <resource_id> <ttl> "
            "<algo: flooding|informed_flooding|random_walk|informed_random_walk>"
        )
        sys.exit(1)

    config_path = sys.argv[1]
    node_id = sys.argv[2]
    resource_id = sys.argv[3]
    ttl = int(sys.argv[4])
    algo = sys.argv[5]

    config = load_config(config_path)
    net = P2PNetwork(config)

    found, msg_count, nodes_involved, path = net.search(
        node_id=node_id,
        resource_id=resource_id,
        ttl=ttl,
        algo=algo,
    )

    print(f"Encontrado: {found}")
    print(f"Mensagens trocadas: {msg_count}")
    print(f"Nós envolvidos: {nodes_involved}")
    if found:
        print(f"Caminho: {' -> '.join(path)}")


if __name__ == "__main__":
    main()
