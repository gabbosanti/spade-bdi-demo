import spade
from spade_bdi.bdi import BDIAgent


class GoombaAgent(BDIAgent):

    def add_custom_actions(self, actions):

        @actions.add(".move_right", 0)
        def move_right(agent, term, intention):
            print("Goomba moves right!")
            yield


async def main():
    goomba = GoombaAgent(
        "Goomba@localhost",
        "password",
        "goomba0.asl"
    )

    await goomba.start()
if __name__ == "__main__":
    spade.run(main(), True)