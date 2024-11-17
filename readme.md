# Gerenciamento de Pedidos de Estoque com Python

Este projeto é uma simulação simples de um sistema de gerenciamento de pedidos de estoque usando programação paralela em Python. A aplicação utiliza threads para simular clientes que fazem pedidos e processadores de estoque que processam esses pedidos, garantindo a atualização correta do estoque e evitando condições de corrida.

## Descrição

Este projeto é uma prova de conceito (PoC) que demonstra como threads podem ser usadas para simular clientes (produtores) que fazem pedidos e processadores de estoque (consumidores) que processam esses pedidos. Agora, os pedidos são gerenciados e transportados em formato JSON, e há uma fila tanto para pedidos quanto para pedidos processados. O sistema utiliza locks para cada produto, evitando condições de corrida ao acessar o estoque.

## Funcionalidades
- Simulação de múltiplos clientes fazendo pedidos simultâneos.
- Processamento de pedidos em tempo real por múltiplos processadores de estoque.
- Sincronização das operações de estoque para evitar problemas de concorrência.
- Uso de locks específicos para cada produto para garantir a consistência do estoque.
- Fila para gerenciar a entrada de pedidos e a saída de pedidos processados.
- Saídas coloridas para facilitar a identificação de eventos no terminal.
- Conversão dos pedidos para o formato JSON para facilitar o processamento e integração.

## Ordem de execução

- Clientes fazem pedidos e adicionam à fila de pedidos.
- Processadores de estoque pegam os pedidos da fila, verificam a disponibilidade no estoque, e atualizam o estoque se possível.
- Pedidos processados são colocados em uma segunda fila, que armazena todos os pedidos que foram concluídos com sucesso.
- Ao final, o estoque restante é exibido, assim como os pedidos processados.

Relatório: https://docs.google.com/document/d/1VBHwpndfBJ4gMynqht2UB7-fGcZI6NgZ6Cbc-MyQ8G4/edit?usp=sharing 

## Comandos

- docker-compose up --build
- acessar o rabbitMQ : http://localhost:15672/
user: guest
pass: guest

- docker logs app_service
- docker logs rabbitmq_service