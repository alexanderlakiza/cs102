import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.noecho()

        sleep_time = 0.5
        while self.life.is_changing and not self.life.is_max_generations_exceed:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(sleep_time)
            self.life.step()

        time.sleep(sleep_time)
        screen.clear()
        time.sleep(1)
        
        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()