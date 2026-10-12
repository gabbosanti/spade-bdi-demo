
import time
import datetime 
from dataclasses import dataclass
from queue import Queue, Empty
from threading import Thread, Event

from spade_thread import run_spade

from perceptions import GoombaPerceptionDTO

# --- Game Engine simulator ---

def run_game_loop(perception_queue, action_queue, stop_event):
    while not stop_event.is_set():
        perception = GoombaPerceptionDTO(
            obstacle_ahead=True,
            direction="right"
        )

        perception_queue.put(perception)
        print("[Game] Perception sent")

        try:
            action = action_queue.get(timeout=1.0)
            timestamp = datetime.datetime.now()
            print(f"[Game] Action received: {action} at {timestamp}")
        except Empty:
            print("[Game] No action received yet")

        time.sleep(1)


if __name__ == "__main__":
    
    perception_queue = Queue()
    action_queue = Queue()
    stop_event = Event()

    spade_thread = Thread(
        target=run_spade,
        args=(perception_queue, action_queue, stop_event)
    )
    
    spade_thread.start()

    try:
        run_game_loop(
            perception_queue,
            action_queue,
            stop_event
        )
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
    finally:
        stop_event.set()
        spade_thread.join(timeout=2)
        print("[Main] Finished")
