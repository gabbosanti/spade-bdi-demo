Prove per testare la comunicazione tra game loop (sincrono) e spade_bdi (asincrono)

# Prima versione - DONE

Testata la comunicazione tra due thread senza SPADE, simulando il comportamento dell'agente.

`game_loop_thread.py` contiene il game loop sincrono che invia costantemente percezioni a un altro thread che risponde con azioni statiche (non BDI)

# Seconda versione - DONE
Testata la comunicazione tra il thread con il game loop principale e un altro thread che contiene SPADE ed esegue un piano agent-speak
avviare `spade run` in un altro terminale per far partire il server xmpp

# Terza versione - TODO

