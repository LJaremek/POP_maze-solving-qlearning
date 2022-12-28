import numpy as np
import matplotlib.pyplot as plt
from time import time
from matplotlib.ticker import MaxNLocator
import random
from map import gen_map
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
    """
    Returns:
        List: time_map_gen, time_random_player, 
              time_qlearning_player, moves_random_player, 
              moves_qlearning_player
    """
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


def make_plots(qx1, qx2, rx1, rx2, y, parameter, file_name):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Zależności ilości kroków oraz czasu od parametru: "+ parameter)
    ax1.set_title("QLearning")
    ax1.set_xlabel("Parametr " + parameter)
    ax1.set_ylabel("Czas")
    ax1.plot(y, qx1, color="red", marker="o", label="Czas")
    ax11 = ax1.twinx()
    ax11.plot(y, qx2, color="blue", marker="o", label="Kroki")
    ax11.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.legend(loc="upper left")
    ax11.legend(loc="upper right")
    
    ax2.set_title("Random")
    ax2.set_xlabel("Parametr " + parameter)
    ax2.plot(y, rx1, color="red", marker="o", label="Czas")
    ax21 = ax2.twinx()
    ax21.set_ylabel("Kroki")
    ax21.plot(y, rx2, color="blue", marker="o", label="Kroki")
    ax2.legend(loc="upper left")
    ax21.legend(loc="upper right")
    
    fig.set_size_inches(12, 5)
    fig.tight_layout(pad=1.0)
    plt.show()
    fig.savefig("plots/"+file_name+".jpg")
    


def beta_tests():
    results = np.empty((0,5))
    betas = []
    for beta in range(2, 10, 1):
        beta = beta/10
        betas.append(beta)
        result = solver(12, 12, 1500, 0.9, beta, 0.2, 200)
        results = np.vstack((results, np.array(result)))
    make_plots(results[:, 2], results[:, 4], results[:, 1], results[:, 3], betas, "Beta", "beta_tests")

    
def gamma_tests():
    results = np.empty((0,5))
    gammas = []
    for gamma in range(2, 10, 1):
        gamma = gamma/10
        gammas.append(gamma)
        result = solver(12, 12, 1500, gamma, 0.9, 0.2, 200)
        results = np.vstack((results, np.array(result)))
    make_plots(results[:, 2], results[:, 4], results[:, 1], results[:, 3], gammas, "Gamma", "gamma_tests")

    
def size_tests():
    results = np.empty((0,5))
    sizes = []
    for size in range(5, 13, 1):
        sizes.append(size)
        result = solver(size, size, 1500, 0.9, 0.9, 0.2, 200)
        results = np.vstack((results, np.array(result)))
    make_plots(results[:, 2], results[:, 4], results[:, 1], results[:, 3], sizes, "Wielkość", "size_tests")


def hardest_tests():
    results = np.empty((0,5))
    hardests = []
    for hardest in range(1, 6, 1):
        hardest = hardest/10
        hardests.append(hardest)
        result = solver(12, 12, 1500, 0.9, 0.9, hardest, 200)
        results = np.vstack((results, np.array(result)))
    make_plots(results[:, 2], results[:, 4], results[:, 1], results[:, 3], hardests, "Trudność", "hardest_tests")


if __name__ == "__main__":
    beta_tests()
    gamma_tests()
    size_tests()
    hardest_tests()
    