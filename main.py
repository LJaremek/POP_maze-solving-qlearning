from q_learning import random_player, train_player, get_way
from map import gen_map, open_map_from_file
from termcolor import colored

WIDTH = 10
HEIGHT = 10
FREE = " "
WALL = "#"
WAY = "x"
START = "S"
AIM = "$"
fields_dict = {
    WALL: -1000,
    FREE: -1
    }


def main(map_path: str = None) -> None:
    map_dict = {
        "player": "@",
        "aim": AIM,
        "free": FREE,
        "wall": WALL,
        "width": WIDTH,
        "height": HEIGHT
        }

    start = (1, 1)
    end = (HEIGHT-2, WIDTH-2)

    if map_path is None:
        the_map = gen_map(map_dict, WIDTH, HEIGHT)
    else:
        the_map = open_map_from_file(map_path)

    random_moves = random_player(start_coords=start,
                                 end_coords=end,
                                 map_dict=map_dict,
                                 the_map=the_map)
    print(f"Random Player passes the map in {random_moves} moves.")

    print("Start training ...")
    q_table, path = train_player(epochs=1_000,
                                 map_dict=map_dict,
                                 fields_dict=fields_dict,
                                 the_map=the_map,
                                 q_table=None,
                                 aim_coords=end,
                                 beta=0.9,
                                 gamma=0.9)
    print("... end training.")

    print("Start getting the way ...")
    the_way = get_way(
        q_table=q_table,
        start_coords=start,
        end_coords=end,
        map_dict=map_dict,
        the_map=the_map
        )
    print("... end getting the way.")
    print(f"QTable Player passes the map in {len(the_way)} moves.")

    for x, y in the_way:
        the_map[x][y] = WAY
    the_map[start[0]][start[1]] = START
    the_map[end[0]][end[1]] = AIM
    for row in the_map:
        colored_row = ""
        for point in row:
            if point == WALL:
                colored_row += colored(point, "red")
            elif point == WAY:
                colored_row += colored(point, "green")
            elif point == START:
                colored_row += colored(point, "blue")
            elif point == AIM:
                colored_row += colored(point, "yellow")
            else:
                colored_row += point
        print("".join(colored_row))


if __name__ == "__main__":
    main()
