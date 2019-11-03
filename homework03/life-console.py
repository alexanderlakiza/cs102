import curses
import time
import pathlib
import msvcrt
import threading


from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)


    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addstr(0, 0, '+')
        screen.addstr(self.life.rows + 1, 0, '+')
        screen.addstr(0, self.life.cols + 1, '+')
        screen.addstr(self.life.rows + 1, self.life.cols + 1, '+')

        for i in range(1, self.life.cols + 1):
            screen.addstr(0, i, '-')
            screen.addstr(self.life.rows + 1, i, '-')
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')


    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')


    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        sleep_time = 0.6
        curses.noecho()
        pause = False
        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
            if msvcrt.kbhit() and chr(screen.getch()) == 'q':
                running = False
            if msvcrt.kbhit() and chr(screen.getch()) == 'p':
                pause = not pause
            if pause == True:
                continue
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(sleep_time)
            self.life.step()
            
        time.sleep(1)
        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=10)
    ui = Console(life)
    ui.run()