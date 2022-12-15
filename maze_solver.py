import argparse
from random import seed
from time import time

from q_learning import random_player, train_player, get_way
from map import simple_gen_map, print_map

parser = argparse.ArgumentParser(description="Solve maze and show statistics.")

parser.add_argument(
    "-s", "--size", type=str, required=True,
    help="Size of the maze. Available: small/big"
    )

parser.add_argument(
    "-d", "--difficulty", type=str, required=True,
    help="Difficulty level of the maze. Available: easy/hard"
    )

parser.add_argument(
    "-b", "--beta", type=float, required=True,
    help="Beta parameter for q-learning. Range 0.0 - 1.0"
    )

parser.add_argument(
    "-g", "--gamma", type=float, required=True,
    help="Gamma parameter for q-learning. Range 0.0 - 1.0"
    )

parser.add_argument(
    "-e", "--epochs", type=int, required=True,
    help="Epochs number for q-learning player."
    )

parser.add_argument(
    "-p", "--print", type=str, required=False,
    help="print generated maze. Available: True/False"
    )

parser.add_argument(
    "-i", "--seed", type=int, required=False,
    help="seed for random module"
    )

args = parser.parse_args()

map_dict = {
        "player": "@",
        "aim": "$",
        "free": " ",
        "wall": "#"
        }

fields_dict = {
    "#": -1000,
    " ": -1
    }

def maze_solve():
    map_size = args.size
    diff_lvl = args.difficulty
    epochs = args.epochs
    gamma = args.gamma
    beta = args.beta
    print_ = args.print
    seed_ = args.seed
    
    if seed_ is not None:
        seed(seed_)
    
    start = (1, 1)
    if map_size == "small":
        map_dict["width"] = 7
        map_dict["height"] = 7
        end = (5, 5)
    if map_size == "big":
        map_dict["width"] = 12
        map_dict["height"] = 12
        end = (10, 10)

    time_map_gen = time()
    the_map = simple_gen_map(map_size, diff_lvl)
    time_map_gen = time() - time_map_gen

    time_random_player = time()
    moves_random_player = random_player(
            start_coords=start,
            end_coords=end,
            map_dict=map_dict,
            the_map=the_map
            )
    time_random_player = time() - time_random_player

    time_qlearning_player = time()
    q_table, path = train_player(epochs=epochs,
                                 map_dict=map_dict,
                                 fields_dict=fields_dict,
                                 the_map=the_map,
                                 q_table=None,
                                 aim_coords=end,
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

    if print_ == "True":
        print_map(the_map, the_way, start, end, "x", "S", "$", "#")

        print(
            time_map_gen,
            time_random_player, time_qlearning_player,
            moves_random_player, moves_qlearning_player
            )
        
    return [time_map_gen, time_random_player, time_qlearning_player, moves_random_player, moves_qlearning_player]

if __name__ == "__main__":
    maze_solve()
