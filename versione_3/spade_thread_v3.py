import asyncio
import spade
import json

from pathlib import Path
from goomba_agent import GoombaAgent
from perceptions import GoombaPerceptionDTO
from queue import Empty

def run_spade(perception_queue, action_queue, stop_event):
    
    async def main():
        asl_path = Path(__file__).with_name("goomba.asl")

        goombaAgent = GoombaAgent(
            "goomba@localhost",
            "goomba_password",
            str(asl_path)
        )

        print("[SPADE] Starting agent...")

        await goombaAgent.start()
        
        print("Wait until user interrupts with ctrl+C")
        await spade.wait_until_finished(goombaAgent)
        
        #ricevo la percezione in formato json string
        perceptionJSON = perception_queue.get(timeout=0.2)
        print(f"[Agent] Perception received: {perceptionJSON}")

        perceptionDICT = json.loads(perceptionJSON)
        perceptionDTO = GoombaPerceptionDTO(**perceptionDICT)
        
        #aggiorno la belief
        if (perceptionDTO.obstacle_ahead) :    
            goombaAgent.bdi.set_belief("obstacle_ahead")
        
        #asl ragiona ed elabora un piano....
        
        action = goombaAgent.bdi.get_belief("direction")

        action_queue.put(action)
        print("[Agent] Action sent")

        print("[SPADE] Agent started")

        try:
            while not stop_event.is_set():
                await asyncio.sleep(0.1)
        finally:
            print("[SPADE] Stopping agent...")
            await goombaAgent.stop()
            print("[SPADE] Agent stopped")

    spade.run(main(), embedded_xmpp_server=False)
