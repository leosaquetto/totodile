# Comandos do bot

## BotFather

O menu **Edit Commands** do BotFather só cria o menu visual de comandos no Telegram. Ele não registra webhook, não liga callbacks e não faz o bot responder sozinho.

Lista para colar no BotFather:

```text
agenda - ver agenda de hoje
agenda_hoje - ver eventos de hoje
agenda_semana - ver eventos da semana
aniversarios - ver aniversários de hoje
aniversarios_hoje - ver aniversários de hoje
aniversarios_semana - ver aniversários da semana
rotina - abrir painel de rotina
ajuda - listar comandos disponíveis
status - ver status do bot
debug_agenda - diagnosticar agenda
debug_aniversarios - diagnosticar aniversários
health - checar saúde do bot
```

## Rotas dos comandos

- `/agenda` e `/agenda_hoje`: envia agenda de hoje no tópico `agenda`.
- `/agenda_semana`: envia agenda da semana no tópico `agenda`.
- `/aniversarios` e `/aniversarios_hoje`: envia aniversários de hoje no tópico `aniversarios`.
- `/aniversarios_semana`: envia aniversários da semana no tópico `aniversarios`.
- `/agenda_mes`: envia eventos do mês no tópico `agenda`.
- `/aniversarios_mes`: envia aniversários do mês no tópico `aniversarios`.
- `/rotina`: envia painel de rotina no tópico geral.
- `/ajuda`: lista comandos disponíveis no tópico geral.
- `/status`: mostra status resumido no tópico geral.
- `/debug_agenda`: mostra diagnóstico de agenda no tópico `agenda`.
- `/debug_aniversarios`: mostra diagnóstico de aniversários no tópico `aniversarios`.
- `/health`: endpoint de saúde do bot.

`THREADS["general"]` é `None`, então mensagens gerais não enviam `message_thread_id`.

## Botões

- `agenda_hoje` e `agenda_semana`: enviam agenda no tópico `agenda`.
- `aniversarios_hoje` e `aniversarios_semana`: enviam aniversários no tópico `aniversarios`.
- `agenda_lida`, `aniversarios_lidos` e `agenda_lembrar_depois`: atualizam estado e respondem o callback.
- `rotina_tarefas_painel`: abre tarefas no tópico `tarefas`.
- `rotina_remedios_painel`: abre remédios no tópico `remedios`.
- `rotina_academia_painel`: abre academia no tópico `academia`.

## Comportamento de entrada

- Comando desconhecido chama `/ajuda`.
- Mensagens sem comando são ignoradas com segurança.
- Botões inline usam `callback_data` roteado por prefixo: `agenda_`, `aniversarios_`, `rotina_`, `prep_`, `tarefa_` e `academia_`.
- Callbacks respondem com `answerCallbackQuery` quando há `callback_query.id`.
