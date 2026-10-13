from queue import Empty
from actions import GoombaActionDTO

# --- SPADE simulator ---

def run_spade(perception_queue, action_queue, stop_event):
    """Simula un agente che riceve percezioni e restituisce azioni."""

    while not stop_event.is_set():
        try:
            perception = perception_queue.get(timeout=0.2)
        except Empty:
            continue

        print(f"[Agent] Perception received: {perception}")

        # Comportamento provvisorio, non ancora BDI
        if perception.obstacle_ahead:
            action = GoombaActionDTO("TURN")
        else:
            action = GoombaActionDTO("MOVE_FORWARD")

        action_queue.put(action)
        print("[Agent] Action sent")

    