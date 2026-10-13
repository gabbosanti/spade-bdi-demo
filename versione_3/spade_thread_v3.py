
import asyncio
from pathlib import Path

import spade
from spade_bdi.bdi import BDIAgent

from queue import Empty

def run_spade(perception_queue, action_queue, stop_event):
    
    async def main():
        asl_path = Path(__file__).with_name("goomba0.asl")

        agent = BDIAgent(
            "goomba@localhost",
            "goomba_password",
            str(asl_path)
        )

        print("[SPADE] Starting agent...")

        await agent.start()
        
        perception = perception_queue.get(timeout=0.2)
            
        print(f"[Agent] Perception received: {perception}")
        
        ## BDI PART - TODO
        # PERCEZIONE -> AGGIORNA BELIEF -> PIANO -> AZIONE
        ##
        
        
        action_queue.put(action)
        print("[Agent] Action sent")

        print("[SPADE] Agent started")

        try:
            while not stop_event.is_set():
                await asyncio.sleep(0.1)
        finally:
            print("[SPADE] Stopping agent...")
            await agent.stop()
            print("[SPADE] Agent stopped")

    spade.run(main(), embedded_xmpp_server=False)
