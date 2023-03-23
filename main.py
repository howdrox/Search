import tkinter as tk
import numpy as np
import time
import queue


class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height  # nbr de case
        self.r_size = 40  # pixel par case

        self.create_window()
        self.create_canvas()
        self.board = Board(self)
        self.board.show_walls()
        self.create_entities()
        self.root.mainloop()

    def create_window(self):
        self.c_width = self.width * self.r_size
        self.c_height = self.height * self.r_size  # canvas size (in pixel)
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}")
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_entities(self):
        self.persons = {}
        self.persons['player'] = [Person(self, False, [1, 1])]
        self.persons['enemy'] = [Person(self, True, [10, 10])]
        self.root.bind(
            "<KeyPress>", lambda e: self.persons["player"][0].speed_set(e.keysym)
        )
        self.root.bind(
            "<KeyRelease>", lambda e: self.persons["player"][0].speed_cancel(e.keysym)
        )


class Person:
    def __init__(self, game, evil, spawn_coord):
        self.game = game
        self.evil = evil
        self.j, self.i = spawn_coord
        if self.evil:
            self.speed = 5  # cases per second
        else:
            self.speed = 15
        self.speed_j = 0
        self.speed_i = 0
        self.show()
        self.move_control()

    def show(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.shape = self.game.c.create_rectangle(
            x, y, x + r_size, y + r_size, fill="red" if self.evil else "blue"
        )

    def update(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x - 1, y - 1)

    def speed_set(self, k):
        if k in ("Up", "w"):
            self.speed_i = 0
            self.speed_j = -1
        elif k in ("Left", "a"):
            self.speed_j = 0
            self.speed_i = -1
        elif k in ("Down", "s"):
            self.speed_i = 0
            self.speed_j = 1
        elif k in ("Right", "d"):
            self.speed_j = 0
            self.speed_i = 1

    def speed_cancel(self, k):
        if k in ("Up", "w", "Down", "s"):
            self.speed_j = 0
        elif k in ("Left", "a", "Right", "d"):
            self.speed_i = 0

    def move(self):
        i_test = self.i + self.speed_i
        j_test = self.j + self.speed_j
        if self.game.board.check_movement(j_test, i_test):
            self.i += self.speed_i
            self.j += self.speed_j
        self.update()

        self.game.root.after(int(1000/self.speed), self.move_control)

    def move_control(self):
        if self.evil:
            self.pathfinding()
        self.move()

    def pathfinding(self):
        start_node = (self.j, self.i)
        end_node = (self.game.persons['player']
                    [0].j, self.game.persons['player'][0].i)

        def h_score(node):
            '''estimated distance to the player'''
            return abs(node[0] - end_node[0]) + abs(node[1] - end_node[1])  # Manhattan distance

        g_score = {start_node: 0}  # actual cost from start_node to a node        
        f_score = {start_node: h_score(start_node)}# sum of g_score and h_score

        frontier = queue.PriorityQueue()
        frontier.put((f_score[start_node], start_node))
        came_from = {}
        while not frontier.empty():
            _, current = frontier.get()
            
            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                if len(path) == 0:
                    print('i found you!')
                    self.speed_j,self.speed_i=0,0
                    return 0
                next_node = path[-1]
                self.speed_j = next_node[0]-start_node[0]
                self.speed_i = next_node[1]-start_node[1]
                return 0

            for neighbor in self.game.board.get_abut_place(*current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h_score(neighbor)
                    frontier.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current
                # If the neighbor is in the frontier and the tentative g_score is lower,
                # update its g_score, f_score, and parent
                elif tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h_score(neighbor)
                    frontier.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current


class Board:
    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.board_rectangles = np.zeros((self.game.height, self.game.width))
        self.create_walls()

    def create_walls(self):
        # GENERATING RANDOM WALLS
        # density = 0.1  # density of  walls
        np.random.seed(233)
        # self.walls = np.random.choice(
        #     [True, False],
        #     size=(self.game.height, self.game.width),
        #     p=(density, 1 - density),
        # )

        # GENERATES WALLS FROM WALL_TYPES
        self.walls = np.zeros((self.game.height, self.game.width))
        self.wall_types = list(np.load("./gamedata/wall_types.npy"))
        for i in range(32):
            # Gets the wall type
            rnd = np.random.randint(len(self.wall_types))
            wall = self.wall_types[rnd]
            # Rotates it randomly
            rot = np.random.randint(4)
            np.rot90(wall, rot)
            # Generates the position
            i = np.random.randint(self.game.width - 2)
            j = np.random.randint(self.game.height - 2)
            self.walls[j : j + wall.shape[0], i : i + wall.shape[1]] = wall

        np.save("./gamedata/walls", self.walls)
        # # self.walls = np.load("gamedata/walls.npy")

    def show_walls(self):
        r_size = self.game.r_size
        for j in range(self.game.height):
            for i in range(self.game.width):
                x, y = i * r_size, j * r_size
                self.board_rectangles[j, i] = self.game.c.create_rectangle(
                    x,
                    y,
                    x + r_size,
                    y + r_size,
                    fill="grey" if self.walls[j, i] else "white",
                )

    def get_abut_place(self, j, i):
        return [
            (j+dj, i+di) for dj in (-1, 0, 1) for di in (-1, 0, 1) if self.check_movement(j+dj, i+di) and abs(dj)+abs(di) != 2
        ]

    def check_movement(self, j_test, i_test):
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.game.board.walls[j_test, i_test]
        )


def main():
    game = Game(17, 35)


if __name__ == "__main__":
    main()
