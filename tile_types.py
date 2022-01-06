from typing import Tuple

import numpy as np

"""
The graphics structured data type compatible with Console.tiles_rgb.
Make one for "graphics" and one for "tiles"
"""
graphic_dt  = np.dtype(
    [
        ("ch", np.int32), # unicode codepoint
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool), # True if the tile may be walked over.
        ("transparent", np.bool), # True if the tile doesn't block field of view.
        ("dark", graphic_dt), # Graphic for when the tile is not in field of view.
    ]
)

def new_tile(
    *, # This enforces use of keywords
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """
    Helper function for defining individual tile types
    """
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100))
)