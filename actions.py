from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """
        Return the engine this action belongs to
        """
        return self.entity.game_map.engine

    def perform(self) -> None:
        """
        Peform this actio with the objects needed to determine its scope.

        `self.engine` is the scope thjis action is being performed in.
        `self.entity` is the object performing the action.

        This method must be overridden by an Action subclass.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class DirectionalAction(Action):
    """
    An action which first checks the tile being moved into, then performs an
    action based on the tile contents.
    """
    def __init__(self, entity: Entity, dx: int, dy: int) -> None:
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """
        Return the action's destination.
        """
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MovementAction(DirectionalAction):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds
            return
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is not walkable
            return
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            return

        self.entity.move(self.dx, self.dy)

class MeleeAttack(DirectionalAction):
    def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            # No entity to attack
            return

        print(f"You kick the {target.name}, much to its annoyance!")


class BumpAction(DirectionalAction):
    """
    Bump applies a movement or an attack, depending on which is appropriate to the
    tile being targeted.
    """
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAttack(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()