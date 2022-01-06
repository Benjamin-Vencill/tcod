from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity:Entity) -> None:
        """
        Peform this actio with the objects needed to determine its scope.

        `engine` is the scope thjis action is being performed in.
        `entity` is the object performing the action.

        This method must be overridden by an Action subclass.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class DirectionalAction(Action):
    """
    An action which first checks the tile being moved into, then performs an
    action based on the tile contents.
    """
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MovementAction(DirectionalAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds
            return
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is not walkable
            return
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            return
        
        entity.move(self.dx, self.dy)

class MeleeAttack(DirectionalAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            # No entity to attack
            return
        
        print(f"You kick the {target.name}, much to its annoyance!")


class BumpAction(DirectionalAction):
    """
    Bump applies a movement or an attack, depending on which is appropriate to the 
    tile being targeted.
    """
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAttack(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)