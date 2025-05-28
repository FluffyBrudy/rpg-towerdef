from enum import Enum
from typing import Optional
from random import choice
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
from pygame.transform import flip

from constants import GRAPHICS_PATH
from typedefs.globaltype import Coor
from utils.imgutils import load_frames


class WarriorStatus(Enum):
    ATTACK = "attack"
    IDLE = "idle"
    RUN = "run"


class WarriorDirection(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    NODIR = ""


class Warrior(Sprite):
    directionless_states = [WarriorStatus.IDLE, WarriorStatus.RUN]

    def __init__(self, pos: Coor, zindex: int, /, *groups: Group) -> None:
        super().__init__(*groups)

        self.zindex = zindex

        troop_color = "blue"
        warrior = (
            GRAPHICS_PATH / "Factions" / "Knights" / "Troops" / "Warrior" / troop_color
        )
        warrior_attack = warrior / WarriorStatus.ATTACK.value

        self._original_pos = pos

        self.state_frames = {
            WarriorStatus.IDLE: {
                WarriorDirection.NODIR: load_frames(warrior / WarriorStatus.IDLE.value)
            },
            WarriorStatus.RUN: {
                WarriorDirection.NODIR: load_frames(warrior / WarriorStatus.RUN.value),
            },
            WarriorStatus.ATTACK: {
                WarriorDirection.TOP: load_frames(
                    warrior_attack / WarriorDirection.TOP.value
                ),
                WarriorDirection.BOTTOM: load_frames(
                    warrior_attack / WarriorDirection.BOTTOM.value
                ),
                WarriorDirection.RIGHT: load_frames(
                    warrior_attack / WarriorDirection.RIGHT.value
                ),
            },
        }
        self.image: Surface = self.state_frames[WarriorStatus.IDLE][
            WarriorDirection.NODIR
        ][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.frame_index = 0
        self.animation_speed = choice([0.2])

        self.state = WarriorStatus.ATTACK
        self.direction = WarriorDirection.BOTTOM

        self.attack_radius = self.rect.width
        self.enemy_rect: Optional[Rect] = None
        self.movement_path = []

    def animate(self):
        self.frame_index += self.animation_speed
        current_frames = self._get_current_frames()
        if self.frame_index >= len(current_frames):
            self.frame_index = 0
        self.image = current_frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)  # type: ignore

    def _get_current_frames(self):
        state = self.state_frames[self.state]  # type: ignore
        if self.state in Warrior.directionless_states:
            return state[WarriorDirection.NODIR]
        return state[self.direction]

    def update(self, *args, **kwargs):
        self.animate()
        enemy_rect: Optional[Rect] = kwargs.get("enemy", None)
