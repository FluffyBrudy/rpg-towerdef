from collections import deque
from typing import Dict, List, Optional, Tuple
import numpy as np

import numpy as np
from constants import NUM_COLS, NUM_ROWS


Coor = Tuple[int, int]


class ScreenGrid:
    _grids = np.array([])
    _directions = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])
    _obstacle_ids: Optional[np.ndarray] = None

    @classmethod
    def init_grid(cls, data: Optional[np.ndarray] = None):
        if data and data.shape == (NUM_ROWS, NUM_COLS):
            cls._grids = np.array(data)
        else:
            cls._grids = np.zeros((NUM_ROWS, NUM_COLS))
        cls._obstacle_ids = np.array([])

    @classmethod
    def bfs(cls, start: Coor, target: Coor):
        visited = np.zeros((NUM_ROWS, NUM_COLS), dtype=bool)
        queue: deque[Coor] = deque([start])
        possible_paths: Dict[Coor, Coor] = {}
        tracked_path: List[Coor] = []

        while len(queue) > 0:
            curr_node = queue.popleft()

            if curr_node == target:
                node = target
                while node != start:
                    tracked_path.append(node)
                    node = possible_paths.get(node, None)
                    if node is None:
                        return None
                return np.array(tracked_path, dtype=np.int8)

            for dx, dy in cls._directions:
                node_x, node_y = curr_node[0] + dx, curr_node[1] + dy
                if cls.is_valid_move(node_x, node_y):
                    visited[node_x][node_y] = True
                    queue.append((node_x, node_y))
                    possible_paths[(node_x, node_y)] = curr_node

    @classmethod
    def is_valid_move(cls, x: int, y: int):
        xlimit = cls._grids.shape[0]
        ylimit = cls._grids.shape[1]
        if x < 0 or y < 0 or x >= xlimit or y >= ylimit:
            return False
        if cls._grids[x][y] in cls._obstacle_ids:
            return False
        return True


if __name__ == "__main__":
    ScreenGrid.init_grid()
    path = ScreenGrid.bfs((0, 0), (3, 3))
