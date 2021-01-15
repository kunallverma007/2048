from tkinter import Frame, Label, CENTER
import random

import driver
import constants as cons


def gen():
    return random.randint(0, cons.GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {cons.KEY_UP: driver.up, cons.KEY_DOWN: driver.down,
                         cons.KEY_LEFT: driver.left, cons.KEY_RIGHT: driver.right,
                         cons.KEY_UP_ALT: driver.up, cons.KEY_DOWN_ALT: driver.down,
                         cons.KEY_LEFT_ALT: driver.left, cons.KEY_RIGHT_ALT: driver.right,
                         cons.KEY_H: driver.left, cons.KEY_L: driver.right,
                         cons.KEY_K: driver.up, cons.KEY_J: driver.down}

        self.grid_cells = []
        self.init_grid()
        self.matrix = driver.start_game(cons.GRID_LEN)
        self.matrix2 = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=cons.BACKGROUND_COLOR_GAME,
                           width=cons.SIZE, height=cons.SIZE)
        background.grid()

        for i in range(cons.GRID_LEN):
            grid_row = []
            for j in range(cons.GRID_LEN):
                cell = Frame(background, bg=cons.BACKGROUND_COLOR_CELL_EMPTY,
                             width=cons.SIZE / cons.GRID_LEN,
                             height=cons.SIZE / cons.GRID_LEN)
                cell.grid(row=i, column=j, padx=cons.GRID_PADDING,
                          pady=cons.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=cons.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=cons.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(cons.GRID_LEN):
            for j in range(cons.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=cons.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=cons.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=cons.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == cons.KEY_BACK and len(self.matrix2) > 1:
            self.matrix = self.matrix2.pop()
            self.update_grid_cells()

        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = driver.place_two(self.matrix)

                self.matrix2.append(self.matrix)
                self.update_grid_cells()
                if driver.curr(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=cons.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=cons.BACKGROUND_COLOR_CELL_EMPTY)
                if driver.curr(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=cons.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=cons.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


game_grid = GameGrid()
