# SPADE-BDI e game loop sincrono

`mario_sync_game.py` mostra una possibile integrazione fra un game loop
sincrono e un agente Goomba SPADE-BDI:

1. il loop aggiorna lo stato fittizio del mondo e costruisce una
   `PerceptionDTO`;
2. serializza la percezione in JSON e la invia all'agente tramite un messaggio
   SPADE;
3. il comportamento dell'agente aggiorna le belief BDI;
4. i piani AgentSpeak in `mario_goomba.asl` scelgono un'azione;
5. l'azione torna al loop sincrono tramite una coda thread-safe e modifica il
   mondo.

Installare le dipendenze ed eseguire:

```bash
python -m pip install spade spade-bdi
python mario_sync_game.py
```

Parametri utili per la simulazione:

```bash
python mario_sync_game.py --ticks 30 --width 8 --interval 0.1
```

Il loop di gioco gira in un thread dedicato; il loop asyncio di SPADE resta
libero di ricevere le percezioni e pianificare. Il thread sincrono aspetta
l'azione dell'agente prima di passare al tick successivo.
