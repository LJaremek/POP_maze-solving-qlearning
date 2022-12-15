import numpy as np
import matplotlib.pyplot as plt
from time import time
import random
from map import gen_map, print_map
from q_learning import random_player, train_player, get_way

FREE = " "
WALL = "#"
WAY = "x"
START = "S"
AIM = "$"
fields_dict = {
    WALL: -1000,
    FREE: -1
}

def solver(width, height, epochs, gamma, beta, blocks_percentage = None, seed = None):
    map_dict = {
        "player": "@",
        "aim": AIM,
        "free": FREE,
        "wall": WALL,
        "width": width,
        "height": height
        }
    
    if seed is not None:
        random.seed(seed)
    if blocks_percentage is not None:
        blocks = width * height * blocks_percentage
    else:
        blocks = None
    
    start = (1, 1)
    end = (height-2, width-2)
    time_map_gen = time()
    the_map = gen_map(map_dict, width, height, used_blocks=blocks)
    time_map_gen = time() - time_map_gen

    time_random_player = time()
    moves_random_player = random_player(
            start_coords= start,
            end_coords= end,
            map_dict=map_dict,
            the_map=the_map
            )
    time_random_player = time() - time_random_player

    time_qlearning_player = time()
    q_table, _ = train_player(epochs=epochs,
                              map_dict=map_dict,
                              fields_dict=fields_dict,
                              the_map=the_map,
                              q_table=None,
                              aim_coords=(height-2, width-2),
                              beta=beta,
                              gamma=gamma)
    time_qlearning_player = time() - time_qlearning_player

    the_way = get_way(
        q_table=q_table,
        start_coords=start,
        end_coords=end,
        map_dict=map_dict,
        the_map=the_map
        )

    moves_qlearning_player = len(the_way)
    # print_map(the_map, the_way, start, end, WAY, START, AIM, WALL)
    return [time_map_gen, time_random_player, time_qlearning_player, moves_random_player, moves_qlearning_player]


def beta_tests():
    results = solver(12, 12, 1000, 0.9, 0.9, 0.2, 200)

    
def gamma_tests():
    results = solver(12, 12, 1000, 0.9, 0.9, 0.2, 200)

    
def size_tests():
    results = solver(12, 12, 1000, 0.9, 0.9, 0.2, 200)


def hardest_tests():
    results = solver(12, 12, 1000, 0.9, 0.9, 0.2, 200)


if __name__ == "__main__":
    beta_tests()
    