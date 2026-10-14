import json
import time
from threading import Thread, Event
import datetime
from spade_thread_v3 import run_spade
from perceptions import GoombaPerceptionDTO
from queue import Queue, Empty

# --- Game Engine simulator ---

def run_game_loop(perception_queue, action_queue, stop_event):
    
    while not stop_event.is_set():
        
        time.sleep(2)
        
        #generata una percezione statica
        perceptionDTO = GoombaPerceptionDTO(
            obstacle_ahead=True, #ho un ostacolo davanti
            direction="right" #mi sto muovendo a destra
        )
        
        perceptionJSON = json.dumps(perceptionDTO.__dict__)

        perception_queue.put(perceptionJSON) #metto la percezione nella coda
        print("[Game] Perception sent")

        try:
            action = action_queue.get(timeout=1.0)
            timestamp = datetime.datetime.now()
            print(f"[Game] Action received: {action} at {timestamp}")
        except Empty:
            print("[Game] No action received yet")


if __name__ == "__main__":
    
    perception_queue = Queue()
    action_queue = Queue()
    stop_event = Event()

    spade_thread = Thread(
        target=run_spade,
        args=(perception_queue, action_queue, stop_event),
        name="SPADE-Thread"
    )

    spade_thread.start() # Parte
    
    try:
        run_game_loop(perception_queue, action_queue, stop_event)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
    finally:
        stop_event.set()
        spade_thread.join(timeout=10)

        if spade_thread.is_alive():
            print("[Main] Warning: SPADE thread did not stop in time")
        else:
            print("[Main] Finished")
