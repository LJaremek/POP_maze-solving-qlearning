from random import randint, choice

from exceptions import IncorrectQTable
from map import way_exist

MOVES: tuple[str] = ("w", "s", "a", "d")

def random_coords(
        the_map: list,
        aim_coords: tuple,
        free: str = " ") -> tuple[int, int]:

    x = randint(1, len(the_map)-2)
    y = randint(1, len(the_map[0])-2)
    is_way = way_exist(the_map, (x, y), aim_coords, free)

    while the_map[x][y] != free or not is_way:
        x = randint(1, len(the_map)-2)
        y = randint(1, len(the_map[0])-2)
        is_way = way_exist(the_map, (x, y), aim_coords, free)

    return x, y


def the_best_move(q_table: list, x: int, y: int) -> str:
    index = q_table[x][y].index(max(q_table[x][y]))
    return MOVES[index]


def next_move(x: int, y: int, move: str) -> tuple[int, int]:
    moves = {
        "w": (x-1, y),
        "s": (x+1, y),
        "a": (x, y-1),
        "d": (x, y+1)
        }

    return moves[move]


def make_q_table(width: int, height: int) -> list[list[list[int]]]:
    return [[
            [0 for _ in range(len(MOVES))]
            for _ in range(width)]
            for _ in range(height)]


def draw_arrows(
        the_map: list,
        q_table: list,
        arrows: list[int] = None
        ) -> None:

    if arrows is None:
        arrows = ["⇧", "⇩", "⇦", "⇨"]

    for y_index, row in enumerate(the_map):
        for x_index, cell in enumerate(row):
            index = q_table[y_index][x_index].index(
                max(q_table[y_index][x_index])
                )
            print(arrows[index], end="")
        print()


def random_player(
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
        map_dict: dict[str, str],
        the_map: list) -> int:

    WALL = map_dict["wall"]

    x, y = start_coords
    move_counter: int = 0

    while (x, y) != end_coords:
        move = choice(MOVES)
        old_x, old_y = x, y
        x, y = next_move(old_x, old_y, move)
        move_counter += 1
        if the_map[x][y] == WALL:
            x, y = old_x, old_y

    return move_counter


def train_player(
        epochs: int,
        map_dict: dict[str, str],
        fields_dict: dict[str, int],
        the_map: list[list[str]],
        q_table: list[list[list[int]]] = None,
        aim_coords: tuple[int, int] = None,
        beta: float = 0.9,
        gamma: float = 0.9
        ) -> tuple[list[list[list[int]]], list[tuple[int, int]]]:

    FREE = map_dict["free"]
    WALL = map_dict["wall"]
    WIDTH = map_dict["width"]
    HEIGHT = map_dict["height"]

    if q_table is None:
        q_table = make_q_table(WIDTH, HEIGHT)

    collisions_with_walls: int = 0

    for i in range(epochs):
        if i == epochs-1:
            path: list[tuple[int, int]] = []
        x, y = random_coords(the_map, aim_coords, FREE)
        while (x, y) != aim_coords:
            if i == epochs-1:
                path.append((x, y))
            move = the_best_move(q_table, x, y)
            old_x, old_y = x, y
            x, y = next_move(old_x, old_y, move)

            field = the_map[x][y]
            if field == WALL:
                x, y = old_x, old_y
                q_table[x][y][MOVES.index(move)] -= 1000
                collisions_with_walls += 1
                continue

            reward = fields_dict[field]

            old_q = q_table[old_x][old_y][MOVES.index(move)]
            new_q = old_q + beta*(reward + gamma*max(q_table[x][y]) - old_q)
            q_table[old_x][old_y][MOVES.index(move)] = new_q

    return q_table, path


def get_way(
        q_table: list[list[list[int]]],
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
        map_dict: dict[str, str],
        the_map: list[list[str]]
        ) -> list[tuple[int, int]]:

    the_way = [start_coords]

    x, y = start_coords
    old_x, old_y = None, None
    while (x, y) != end_coords:
        move = the_best_move(q_table, x, y)
        old_old_x, old_old_y = old_x, old_y
        old_x, old_y = x, y
        x, y = next_move(old_x, old_y, move)

        if old_old_x == x and old_old_y == y:
            raise IncorrectQTable()

        field = the_map[x][y]
        if field == map_dict["wall"]:
            print(the_way, field, x, y)
            return False

        the_way.append((x, y))

    return the_way
