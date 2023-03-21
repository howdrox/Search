import tkinter as tk
import random


class Maze(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_maze()
        self.master.bind("<Key>", self.move_player)

    def create_maze(self):
        self.cells = []
        self.player_pos = None
        self.exit_pos = None
        for i in range(19):
            row = []
            for j in range(19):
                if i == 0 or i == 18 or j == 0 or j == 18:
                    row.append(1)  # add walls around the border
                else:
                    row.append(2)  # add empty space
            self.cells.append(row)

        self.player_pos = (1, 1)
        self.cells[self.player_pos[0]][
            self.player_pos[1]
        ] = 0  # player represented by 0
        self.exit_pos = (17, 17)
        self.cells[self.exit_pos[0]][self.exit_pos[1]] = 3  # exit represented by 3

        # set player position and exit position
        self.player_pos = (1, 1)
        self.cells[self.player_pos[0]][
            self.player_pos[1]
        ] = 2  # player represented by 2
        self.exit_pos = (8, 8)
        self.cells[self.exit_pos[0]][self.exit_pos[1]] = 3  # exit represented by 3

        # generate maze using recursive backtracking algorithm
        self.generate_maze((1, 1))

        # create GUI for maze
        for i in range(19):
            for j in range(19):
                color = "black" if self.cells[i][j] == 1 else "white"
                if self.cells[i][j] == 2:
                    color = "grey"
                elif self.cells[i][j] == 0:
                    color = "green"
                elif self.cells[i][j] == 3:
                    color = "red"
                tk.Label(self, text="  ", bg=color).grid(row=i, column=j)

    def move_player(self, event):
        print(event)
        if event.keysym == "Up":
            new_pos = (self.player_pos[0] - 1, self.player_pos[1])
        elif event.keysym == "Down":
            new_pos = (self.player_pos[0] + 1, self.player_pos[1])
        elif event.keysym == "Left":
            new_pos = (self.player_pos[0], self.player_pos[1] - 1)
        elif event.keysym == "Right":
            new_pos = (self.player_pos[0], self.player_pos[1] + 1)
        else:
            return

        if self.cells[new_pos[0]][new_pos[1]] == 0:
            # move player to new position
            self.cells[self.player_pos[0]][self.player_pos[1]] = 0
            self.cells[new_pos[0]][new_pos[1]] = 2
            self.player_pos = new_pos

            # update GUI for maze
            for i in range(10):
                for j in range(10):
                    color = "white" if self.cells[i][j] == 0 else "black"
                    if self.cells[i][j] == 2:
                        color = "green"
                    elif self.cells[i][j] == 3:
                        color = "red"
                    tk.Label(self, text="  ", bg=color).grid(row=i, column=j)

            # check if player has reached the exit
            if self.player_pos == self.exit_pos:
                tk.messagebox.showinfo(
                    "You win!", "Congratulations, you found the exit!"
                )

    def generate_maze(self, pos):
        self.cells[pos[0]][pos[1]] = 0  # mark current cell as visited

        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for d in directions:
            neighbor_pos = (pos[0] + d[0], pos[1] + d[1])
            if (
                neighbor_pos[0] >= 0
                and neighbor_pos[0] < 19
                and neighbor_pos[1] >= 0
                and neighbor_pos[1] < 19
                and self.cells[neighbor_pos[0]][neighbor_pos[1]] == 2
            ):
                self.cells[pos[0] + d[0] // 2][
                    pos[1] + d[1] // 2
                ] = 0  # mark wall between current cell and neighbor as removed
                self.generate_maze(neighbor_pos)


root = tk.Tk()
maze = Maze(root)
maze.pack()
root.mainloop()
