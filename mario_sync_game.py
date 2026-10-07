"""Synchronous Mario-style game loop connected to a SPADE-BDI Goomba."""

import argparse
import asyncio
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from queue import Queue
from typing import Literal

import agentspeak as asp
import spade
from agentspeak.stdlib import actions as stdlib_actions
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from spade_bdi.bdi import BDIAgent


Direction = Literal["left", "right"]
ActionName = Literal["turn_around", "move_left", "move_right"]


@dataclass(frozen=True)
class PerceptionDTO:
    tick: int
    goomba_x: int
    direction: Direction
    obstacle_ahead: bool

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, payload: str) -> "PerceptionDTO":
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("A perception must be a JSON object.")

        tick = data.get("tick")
        goomba_x = data.get("goomba_x")
        direction = data.get("direction")
        obstacle_ahead = data.get("obstacle_ahead")
        if type(tick) is not int or type(goomba_x) is not int:
            raise ValueError("Perception tick and goomba_x must be integers.")
        if direction not in ("left", "right"):
            raise ValueError("Perception direction must be 'left' or 'right'.")
        if type(obstacle_ahead) is not bool:
            raise ValueError("Perception obstacle_ahead must be a boolean.")

        return cls(tick, goomba_x, direction, obstacle_ahead)


@dataclass(frozen=True)
class GameAction:
    tick: int
    name: ActionName


class GameWorld:
    def __init__(self, width: int) -> None:
        if width < 2:
            raise ValueError("The game world must be at least two positions wide.")
        self.width = width
        self.goomba_x = 0
        self.direction: Direction = "right"

    def perceive(self, tick: int) -> PerceptionDTO:
        obstacle_ahead = (
            self.goomba_x == self.width - 1
            if self.direction == "right"
            else self.goomba_x == 0
        )
        return PerceptionDTO(tick, self.goomba_x, self.direction, obstacle_ahead)

    def apply(self, action: GameAction, tick: int) -> None:
        if action.tick != tick:
            raise RuntimeError(
                f"Received action for tick {action.tick} while processing tick {tick}."
            )

        if action.name == "turn_around":
            self.direction = "left" if self.direction == "right" else "right"
        elif action.name == "move_left":
            self.direction = "left"
            self.goomba_x = max(0, self.goomba_x - 1)
        elif action.name == "move_right":
            self.direction = "right"
            self.goomba_x = min(self.width - 1, self.goomba_x + 1)

        print(
            f"  mondo: {action.name} -> "
            f"x={self.goomba_x}, direction={self.direction}"
        )


def build_bdi_actions(action_queue: Queue[GameAction]) -> asp.Actions:
    actions = asp.Actions(stdlib_actions)

    def enqueue(name: ActionName):
        def action(agent, term, intention):
            tick = asp.grounded(term.args[0], intention.scope)
            action_queue.put(GameAction(tick, name))
            yield

        return action

    actions.add(".turn_around", 1)(enqueue("turn_around"))
    actions.add(".move_left", 1)(enqueue("move_left"))
    actions.add(".move_right", 1)(enqueue("move_right"))
    return actions


class GoombaAgent(BDIAgent):
    def __init__(
        self,
        jid: str,
        password: str,
        asl_file: str,
        action_queue: Queue[GameAction],
    ) -> None:
        self.action_queue = action_queue
        super().__init__(
            jid,
            password,
            asl_file,
            actions=build_bdi_actions(action_queue),
        )

    class PerceptionBehaviour(CyclicBehaviour):
        async def run(self) -> None:
            message = await self.receive(timeout=0)
            if message is None:
                return

            perception = PerceptionDTO.from_json(message.body)
            bdi = self.agent.bdi
            bdi.set_belief("game_tick", perception.tick)
            bdi.set_belief("goomba_x", perception.goomba_x)
            bdi.set_belief("direction", perception.direction)
            if perception.obstacle_ahead:
                bdi.set_belief("obstacle_ahead")
            else:
                bdi.remove_belief("obstacle_ahead")
            bdi.set_belief("perception", perception.tick)
            print(f"  agente: belief aggiornate da tick {perception.tick}")

    async def setup(self) -> None:
        template = Template(metadata={"performative": "PERCEPTION"})
        self.add_behaviour(self.PerceptionBehaviour(), template)


def run_game_loop(
    agent: Agent,
    loop: asyncio.AbstractEventLoop,
    action_queue: Queue[GameAction],
    ticks: int,
    width: int,
    interval: float,
) -> None:
    world = GameWorld(width)
    for tick in range(ticks):
        perception = world.perceive(tick)
        print(f"tick {tick}: invio percezione {perception.to_json()}")

        message = Message(to=str(agent.jid), body=perception.to_json())
        message.set_metadata("performative", "PERCEPTION")
        asyncio.run_coroutine_threadsafe(agent.send(message), loop).result(timeout=5)

        moved = False
        while not moved:
            action = action_queue.get(timeout=5)
            world.apply(action, tick)
            moved = action.name in ("move_left", "move_right")

        time.sleep(interval)


async def main(ticks: int, width: int, interval: float) -> None:
    action_queue: Queue[GameAction] = Queue()
    asl_file = str(Path(__file__).with_name("mario_goomba.asl"))
    goomba = GoombaAgent(
        "goomba@localhost",
        "password",
        asl_file,
        action_queue,
    )
    await goomba.start()
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(
            None,
            run_game_loop,
            goomba,
            loop,
            action_queue,
            ticks,
            width,
            interval,
        )
    finally:
        await goomba.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collega un game loop sincrono a un agente Goomba SPADE-BDI."
    )
    parser.add_argument("--ticks", type=int, default=20)
    parser.add_argument("--width", type=int, default=6)
    parser.add_argument("--interval", type=float, default=0.2)
    args = parser.parse_args()
    if args.ticks < 1:
        parser.error("--ticks deve essere almeno 1")
    if args.interval < 0:
        parser.error("--interval non puo essere negativo")

    spade.run(main(args.ticks, args.width, args.interval), True)
