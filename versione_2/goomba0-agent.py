import asyncio
import spade
from spade_bdi.bdi import BDIAgent

class GoombaAgent(BDIAgent):

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
            print("Goomba turns around!")
            self.bdi.set_belief("direction", "left")
            yield

