import threading
import queue
import time
import random
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Estoque
estoque = {
    'produtoA': 100, 
    'produtoB': 50,
    'produtoC': 200,
    'produtoD': 30,
    'produtoE': 100
}

# Criação de locks individuais para cada produto
locks_por_produto = {produto: threading.Lock() for produto in estoque.keys()}

# Fila de pedidos e fila de pedidos processados
fila_de_pedidos = queue.Queue()
fila_de_processados = queue.Queue()

def cliente(num_pedidos):
    for i in range(num_pedidos):
        produto = random.choice(list(estoque.keys()))
        quantidade = random.randint(1, 10)
        pedido = {'produto': produto, 'quantidade': quantidade}
        
        # Converte o pedido para JSON
        pedido_json = json.dumps(pedido)
        
        print(f"{Fore.GREEN}Cliente gerou o pedido: {pedido_json}")
        fila_de_pedidos.put(pedido_json)  # Adiciona o pedido à fila
        time.sleep(random.uniform(0.1, 0.5))

def processador_de_estoque():
    while True:
        try:
            # Pega o pedido da fila (formato JSON) e converte de volta para dicionário
            pedido_json = fila_de_pedidos.get(timeout=2)
            pedido = json.loads(pedido_json)
            produto = pedido['produto']
            quantidade = pedido['quantidade']

            # Seção crítica específica para o produto
            with locks_por_produto[produto]:
                if estoque[produto] >= quantidade:
                    estoque[produto] -= quantidade
                    print(f"{Fore.BLUE}Pedido processado: {pedido}. Estoque atualizado: {estoque[produto]} unidades restantes.")
                    
                    # Adiciona o pedido processado na fila de saída
                    fila_de_processados.put(json.dumps(pedido))
                else:
                    print(f"{Fore.RED}Estoque insuficiente para {produto}. Pedido não processado.")
            
            fila_de_pedidos.task_done()
            
        except queue.Empty:
            print(f"{Fore.YELLOW}Nenhum pedido na fila.")
            break

# Configuração das threads dos clientes e processadores de estoque
num_clientes = 3
num_pedidos_por_cliente = 10

clientes = []
for i in range(num_clientes):
    t = threading.Thread(target=cliente, args=(num_pedidos_por_cliente,))
    clientes.append(t)
    t.start()

processadores_de_estoque = []
for i in range(num_clientes):  # Igualando número de processadores de estoque ao de clientes
    t = threading.Thread(target=processador_de_estoque)
    processadores_de_estoque.append(t)
    t.start()

# Aguardar que todas as threads (clientes) finalizarem
for t in clientes:
    t.join()

# Aguardar que todas as threads (processadores_de_estoque) finalizarem
for t in processadores_de_estoque:
    t.join()

# Mostra os pedidos processados
print(f"{Fore.MAGENTA}{Style.BRIGHT}Pedidos Processados:")
while not fila_de_processados.empty():
    pedido_processado_json = fila_de_processados.get()
    print(f"{Fore.MAGENTA}{Style.BRIGHT} {pedido_processado_json}")

# Mostra o estoque final
print(f"{Fore.CYAN}{Style.BRIGHT}Estoque Final:")
for produto, quantidade in estoque.items():
    print(f"{Fore.CYAN}{Style.BRIGHT} Produto: {produto} | {quantidade} unidades restantes")

print(f"{Fore.CYAN}End")