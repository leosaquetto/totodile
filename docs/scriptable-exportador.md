# Scriptable — exportador de agenda e aniversários

Arquivo:
- `ios_scriptable/exportar_agenda_aniversarios.js`

## Configurar token no Scriptable
No app Scriptable, execute uma vez:

```javascript
Keychain.set("totodile_github_token", "TOKEN_AQUI")
```

> Não commitar token real.

## Como rodar
1. Abra o script `exportar_agenda_aniversarios.js` no Scriptable.
2. Execute manualmente ou via widget/atalho.
3. Opcional: passe parâmetro JSON com branch:
   - `{"branch":"main"}`

## Arquivos atualizados no GitHub
- `data/agenda/eventos.json`
- `data/aniversarios/aniversarios.json`

## Formato exportado
O script salva envelope com metadados:
- `exportedAt`
- `source`
- `count`
- `timezone`
- `branch`
- `items`

## Logs esperados no console
- quantidade de aniversários exportados
- quantidade de eventos exportados
- branch destino
- arquivos atualizados
