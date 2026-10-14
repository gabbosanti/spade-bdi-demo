import time
from threading import Thread, Event

from spade_thread_v2 import run_spade


def run_game_loop(stop_event):
    while not stop_event.is_set():
        print("[Game] Game loop running")
        time.sleep(1)


if __name__ == "__main__":
    stop_event = Event()

    spade_thread = Thread(
        target=run_spade,
        args=(stop_event,),
        name="SPADE-Thread"
    )

    spade_thread.start() # Parte
    
    try:
        run_game_loop(stop_event)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
    finally:
        stop_event.set()
        spade_thread.join(timeout=10)

        if spade_thread.is_alive():
            print("[Main] Warning: SPADE thread did not stop in time")
        else:
            print("[Main] Finished")
