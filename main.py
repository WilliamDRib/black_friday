import threading
import queue
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

# Estoque
estoque = {'produtoA': 100, 
           'produtoB': 50,
           'produtoC': 200,
           'produtoD': 30,
           'produtoE': 100}

# Fila de pedidos
fila_de_pedidos = queue.Queue()

def cliente(num_pedidos):
    for i in range(num_pedidos):
        produto = random.choice(list(estoque.keys()))
        quantidade = random.randint(1, 10)
        pedido = {'produto': produto, 'quantidade': quantidade}
        print(f"{Fore.GREEN}Cliente gerou o pedido: {pedido}")
        fila_de_pedidos.put(pedido)
        time.sleep(random.uniform(0.1, 0.5))

def processador_de_estoque():
    while True:
        try:
            pedido = fila_de_pedidos.get(timeout=2)
            produto = pedido['produto']
            quantidade = pedido['quantidade']

            # Checa o estoque e processa o pedido
            with threading.Lock():  # Sincronização para evitar corrida
                if estoque[produto] >= quantidade:
                    estoque[produto] -= quantidade
                    print(f"{Fore.BLUE}Pedido processado: {pedido}.\nEstoque atualizado: {estoque[produto]} unidades restantes.")
                else:
                    print(f"{Fore.RED}Estoque insuficiente para {produto}. Pedido não processado.")

            fila_de_pedidos.task_done()
            
        except queue.Empty:
            print(f"{Fore.YELLOW}Nenhum pedido na fila")
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

print(f"{Fore.CYAN}End")