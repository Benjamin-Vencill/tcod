from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class GameMap:
    def __init__(
        self,
        engine: Engine,
        width: int,
        height: int,
        entities: Iterable[Entity] = ()
    ) -> None:
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Return True if x and y are inside the map boundary
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        """
        If there is a blocking entity at the location, return it.
        Otherwise, return None.
        """
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        return None

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the visible array, draw it with light colors.
        If a tile is not in the visible array, but has been explored, draw it with dark
            colors.
        Otherwise, draw it with shroud colors.
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.shroud,
        )

        for entity in self.entities:
            # Only print visible entities
            if self.visible[entity.x, entity.y]:
                console.print(
                    entity.x,
                    entity.y,
                    entity.char,
                    fg=entity.color,
                )