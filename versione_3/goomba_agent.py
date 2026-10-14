import asyncio
import spade
from spade_bdi.bdi import BDIAgent
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
class GoombaAgent(BDIAgent):
    class PatrolBehaviour(CyclicBehaviour): # inner class
        async def on_start(self):
            print("Starting patrol behaviour . . .")

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        await asyncio.sleep(1)
        b = self.PatrolBehaviour()
        self.add_behaviour(b)
    
    def add_custom_actions(self, actions):

        @actions.add(".move_right", 0)
        def move_right(agent, term, intention):
            print("Goomba moves right!")
            yield

        @actions.add(".move_left", 0)
        def move_left(agent, term, intention):
            print("Goomba moves left!")
            yield

        @actions.add(".turn_around", 0)
        def turn_around(agent, term, intention):
            
            self.bdi.remove_belief("obstacle_ahead")
            
            if(self.bdi.get_belief("direction") == "right"):
                self.bdi.set_belief("direction", "left")
                print("Goomba turns left!")

            else :
                self.bdi.set_belief("direction", "right")
                print("Goomba turns right!")

            yield

