main hook plan

- app/main.py deve aceitar dois modos:
  - envio de painéis iniciais
  - roteamento de callback_query
- próxima integração:
  - ler update json de arquivo/local ou stdin
  - chamar app.callbacks.router_stub.dispatch
