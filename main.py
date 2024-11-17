import threading
import time
import random
import json
import pika
from colorama import Fore, Style, init

init(autoreset=True)


# Configuração do RabbitMQ
RABBITMQ_HOST = 'rabbitmq_service'  # Nome do serviço no Docker Compose

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        break  # Sai do loop se a conexão for bem-sucedida
    except pika.exceptions.AMQPConnectionError:
        print("Aguardando RabbitMQ iniciar...")
        time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()

# Estoque inicial
estoque = {
    'produtoA': 100, 
    'produtoB': 50,
    'produtoC': 200,
    'produtoD': 30,
    'produtoE': 100
}

# Locks individuais para evitar condições de corrida
locks_por_produto = {produto: threading.Lock() for produto in estoque.keys()}

# Declaração de filas
channel.queue_declare(queue='fila_de_pedidos')
channel.queue_declare(queue='fila_de_processados')

# Função do cliente (produtor)
def cliente(num_pedidos):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    try:
        for _ in range(num_pedidos):
            produto = random.choice(list(estoque.keys()))
            quantidade = random.randint(1, 10)
            pedido = {'produto': produto, 'quantidade': quantidade}
            pedido_json = json.dumps(pedido)
            
            print(f"{Fore.GREEN}Cliente gerou o pedido: {pedido_json}")
            channel.basic_publish(exchange='', routing_key='fila_de_pedidos', body=pedido_json)
            time.sleep(random.uniform(0.1, 0.5))
    except Exception as e:
        print(f"{Fore.RED}Erro no cliente: {e}")
    finally:
        connection.close()

# Função do processador de estoque (consumidor)
def processador_de_estoque():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        pedido = json.loads(body)
        produto = pedido['produto']
        quantidade = pedido['quantidade']
        
        # Seção crítica
        with locks_por_produto[produto]:
            if estoque[produto] >= quantidade:
                estoque[produto] -= quantidade
                print(f"{Fore.BLUE}Pedido processado: {pedido}. Estoque atualizado: {estoque[produto]} unidades restantes.")
                
                # Publica o pedido processado na fila de processados
                try:
                    channel.basic_publish(exchange='', routing_key='fila_de_processados', body=json.dumps(pedido))
                except Exception as e:
                    print(f"{Fore.RED}Erro ao publicar na fila de processados: {e}")
            else:
                print(f"{Fore.RED}Estoque insuficiente para {produto}. Pedido não processado.")
    
    try:
        # Configura o consumo da fila de pedidos
        channel.basic_consume(queue='fila_de_pedidos', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        print(f"{Fore.RED}Erro no processador de estoque: {e}")
    finally:
        connection.close()

# Configuração das threads dos clientes e processadores
num_clientes = 3
num_pedidos_por_cliente = 10

clientes = []
for _ in range(num_clientes):
    t = threading.Thread(target=cliente, args=(num_pedidos_por_cliente,))
    clientes.append(t)
    t.start()

processadores = []
for _ in range(num_clientes):
    t = threading.Thread(target=processador_de_estoque)
    processadores.append(t)
    t.start()

# Aguardar finalização das threads de clientes
for t in clientes:
    t.join()

# Aguardar finalização das threads de processadores
for t in processadores:
    t.join()

# Exibe o estoque final
print(f"{Fore.CYAN}{Style.BRIGHT}Estoque Final:")
for produto, quantidade in estoque.items():
    print(f"{Fore.CYAN}Produto: {produto} | {quantidade} unidades restantes")

print(f"{Fore.CYAN}Fim da execução.")