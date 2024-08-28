# Gerenciamento de Pedidos de Estoque com Python

Este projeto é uma simulação simples de um sistema de gerenciamento de pedidos de estoque usando programação paralela em Python. A aplicação utiliza threads para simular clientes que fazem pedidos e processadores de estoque que processam esses pedidos, garantindo a atualização correta do estoque e evitando condições de corrida.

## Descrição

Este projeto é uma prova de conceito (PoC) para um sistema de gerenciamento de pedidos de estoque. Ele demonstra como threads podem ser usadas para simular clientes (produtores) que fazem pedidos e processadores de estoque (consumidores) que processam esses pedidos. O sistema utiliza uma fila para gerenciar os pedidos e sincroniza as operações de processamento de estoque usando locks para evitar condições de corrida.

## Funcionalidades
- Simulação de múltiplos clientes fazendo pedidos simultâneos.
- Processamento de pedidos em tempo real por múltiplos processadores de estoque.
- Sincronização das operações de estoque para evitar problemas de concorrência.
- Saídas coloridas para facilitar a identificação de eventos no terminal.

Relatório: https://docs.google.com/document/d/1VBHwpndfBJ4gMynqht2UB7-fGcZI6NgZ6Cbc-MyQ8G4/edit?usp=sharing 