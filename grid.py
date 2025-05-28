from collections import deque
from typing import Dict, List, Optional, Tuple
import numpy as np
from numpy._typing import NDArray, _8Bit

Coor = Tuple[int, int]


class ScreenGrid:
    _grids: NDArray[np.signedinteger[_8Bit]] = np.array([])
    _directions = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]], dtype=np.int8)
    _obstacle_ids: Optional[np.ndarray] = None
    cell_size: Optional[int] = None
    grid_count: Optional[Coor] = None

    @classmethod
    def init_grid(
        cls, cell_size: int, grid_count: Coor, data: Optional[np.ndarray] = None
    ):
        cls.cell_size = cell_size
        cls.grid_count = grid_count

        if data and data.shape == (cls.grid_count[0], cls.grid_count[1]):
            cls._grids = np.array(data)
        else:
            cls._grids = np.zeros((cls.grid_count[0], cls.grid_count[1]), dtype=np.int8)
        cls._obstacle_ids = np.array([], dtype=np.int8)

    @classmethod
    def bfs(cls, start: Coor, target: Coor):
        if cls.grid_count is None:
            raise ValueError("grid not initialized")
        visited = np.zeros((cls.grid_count[0], cls.grid_count[1]), dtype=bool)
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

    @classmethod
    def add_obstacle_at(cls, x: int, y: int, obstacle_id: int):
        cls._obstacle_ids = obstacle_id  # type:ignore
        cls._grids[x, y] = obstacle_id


if __name__ == "__main__":
    pass
