
import asyncio
from pathlib import Path

import spade
from spade_bdi.bdi import BDIAgent


def run_spade(stop_event):
    
    async def main():
        #asl_path = Path(__file__).with_name("goomba0.asl")

        print("[SPADE] ciao")

        agent = BDIAgent(
            "goomba@localhost",
            "goomba_password",
            "goomba0.asl"
        )

        print("[SPADE] Starting agent...")

        await agent.start()

        print("[SPADE] Agent started")

        try:
            while not stop_event.is_set():
                await asyncio.sleep(0.1)
        finally:
            print("[SPADE] Stopping agent...")
            await agent.stop()
            print("[SPADE] Agent stopped")

    spade.run(main(), embedded_xmpp_server=False)
