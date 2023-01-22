class IncorrectQTable(Exception):
    def __init__(self) -> None:
        msg = "Q-Table is not correct. There are infinite loop!\n"
        msg += "Probably Q-Learning didn't get enough epochs.\n"
        msg += "Lets try use function draw_arrows to see the Q-Table."
        super().__init__(msg)
