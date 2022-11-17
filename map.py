from random import randint


def open_map_from_file(path: str) -> list[list[str]]:
    the_map = []

    with open(path, "r", -1, "utf-8") as file:
        for row in file:
            the_map.append(list(row.strip()))

    return the_map


def get_map(map_path: str) -> list[list[str]]:
    return open_map_from_file(map_path)


def save_map(
        the_map: list[list[str]],
        file_name: str = "my_map.txt"
        ) -> None:

    with open(file_name, "w", -1, "utf-8") as file:
        for row in the_map:
            print(row, file=file)


def way_exist(
        the_map: list[list[str]],
        start: tuple[int, int],
        stop: tuple[int, int],
        free: str = " "
        ) -> bool:

    the_map = copy_map(the_map)
    to_check = [start]

    while len(to_check) != 0:
        x, y = to_check.pop(0)
        if (x, y) == stop:
            return True

        the_map[x][y] = "x"

        fields = [(x+1, y),
                  (x-1, y),
                  (x, y+1),
                  (x, y-1)]

        for x, y in fields:
            if the_map[x][y] == free:
                to_check.append((x, y))

    return False


def copy_map(the_map: list[list[str]]) -> list[list[str]]:
    return [row[:] for row in the_map]


def gen_map(
        map_dict: dict[str, str],
        width: int = 10,
        height: int = 10,
        start: tuple[int, int] = (0, 1),
        end: tuple[int, int] = None
        ) -> list[list[str]]:
    """
    12x12 is good number formap size ;)
    """
    MAX_WALL_TO_CHECK = 5

    if end is None:
        end = (height-2, width-2)

    wall = map_dict["wall"]
    free = map_dict["free"]

    the_map = [list(wall*width),
               list(wall*width)]

    for _ in range(height-2):
        the_map.insert(1, list(wall + free*(width-2) + wall))

    used = width*height*10/100
    tries = 0
    walls_to_check = MAX_WALL_TO_CHECK
    map_check_point = copy_map(the_map)
    while used > 0:
        x = randint(1, height-1)
        y = randint(1, width-1)
        if the_map[x][y] != wall:
            the_map[x][y] = wall

            if walls_to_check == 0:
                if way_exist(the_map, start, end, free):
                    used -= MAX_WALL_TO_CHECK
                    walls_to_check = MAX_WALL_TO_CHECK
                    map_check_point = copy_map(the_map)
                else:
                    tries += 5
                    the_map = copy_map(map_check_point)
            else:
                walls_to_check -= 1

            if tries > 20:
                tries = 0
                used -= MAX_WALL_TO_CHECK

    return the_map


if __name__ == "__main__":
    map_dict = {"wall": "#", "free": " "}
    the_map = gen_map(map_dict, 13, 13)
    for row in the_map:
        print("".join(row))

    with open("testing_map.txt", "w") as file:
        [print("".join(row), file=file) for row in the_map]
