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
        self.board.show_portals()
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
        self.persons["player"] = [Person(self, False, [1, 1])]
        self.persons["enemy"] = [Person(self, True, [10, 10])]
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
        self.direction = [999, 999]  # [up/down,left/right]
        self.delete_orientation = False
        self.canshoot = True  # relate to the judgement of condition

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
        self.orientation = self.game.c.create_oval(
            0, 0, 0, 0, fill="yellow", edge=None
        )  # initialise orientation

    def update_rect(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x - 1, y - 1)

    def speed_set(self, k):
        if k in ("Up", "w", "W"):
            self.speed_i = 0
            self.speed_j = -1
            self.direction = [0, -1]
        elif k in ("Left", "a", "A"):
            self.speed_i = -1
            self.speed_j = 0
            self.direction = [-1, 0]
        elif k in ("Down", "s", "S"):
            self.speed_i = 0
            self.speed_j = 1
            self.direction = [0, 1]
        elif k in ("Right", "d", "D"):
            self.speed_i = 1
            self.speed_j = 0
            self.direction = [1, 0]

    def speed_cancel(self, k):
        if k in ("Up", "w", "W", "Down", "s", "S"):
            self.speed_j = 0
        elif k in ("Left", "a", "A", "Right", "d", "D"):
            self.speed_i = 0

    def update_orientation(self):
        r_size = self.game.r_size
        i_orientation_test = self.i + self.direction[0]
        j_orientation_test = self.j + self.direction[1]
        self.game.c.delete(self.orientation)
        if (
            self.game.board.check_movement(j_orientation_test, i_orientation_test)
            and self.delete_orientation == False
        ):
            self.i_orientation = i_orientation_test
            self.j_orientation = j_orientation_test
            x_orientation, y_orientation = self.i_orientation * r_size, self.j_orientation * r_size
            self.game.c.delete(self.orientation)
            self.orientation = self.game.c.create_oval(
                x_orientation + 0.42 * r_size,
                y_orientation + 0.42 * r_size,
                x_orientation + 0.58 * r_size,
                y_orientation + 0.58 * r_size,
                fill="orange",
                edge=None,
                width=0,
            )

    # def shoot(self,k):
    #     r_size = self.game.r_size
    #     if self.canshoot == True and k in ("j","J"):
    #         ori_x = self.i * (r_size + self.direction[0])
    #         ori_y= self.j * (r_size + self.direction[1])
    #         self.bullet = self.game.c.create_line((1,1),(20,20), fill='red', dash=(3,3,1))
    #         #ori_x-1.5,ori_y-1.5,ori_x+1.5,ori_y+1.5

    def move(self):
        i_test = self.i + self.speed_i
        j_test = self.j + self.speed_j
        # if the player is in a portal
        if self.game.board.check_movement(
            j_test, i_test
        ) and self.game.board.check_portal(j_test, i_test):
            print(j_test, i_test)
            j_test, i_test = self.game.board.get_portal(j_test, i_test)
            print(j_test, i_test)
            j_test += self.speed_j
            i_test += self.speed_i
        if self.game.board.check_movement(j_test, i_test):
            self.i = i_test
            self.j = j_test

        self.update_rect()
        self.update_orientation()
        self.game.root.after(int(1000 / self.speed), self.move_control)

    def move_control(self):
        if self.evil:
            self.delete_orientation = False  # reset the orientation
            self.pathfinding()
        self.move()

    def pathfinding(self):
        start_node = (self.j, self.i)
        end_node = (self.game.persons["player"][0].j, self.game.persons["player"][0].i)

        def h_score(node):
            """estimated distance to the player"""
            return abs(node[0] - end_node[0]) + abs(
                node[1] - end_node[1]
            )  # Manhattan distance

        g_score = {start_node: 0}  # actual cost from start_node to a node
        f_score = {start_node: h_score(start_node)}  # sum of g_score and h_score

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
                    print("i found you!")
                    self.delete_orientation = True  # When chased up : delete orientation
                    self.speed_j, self.speed_i = 0, 0
                    return 0
                next_node = path[-1]
                self.speed_j = next_node[0] - start_node[0]
                self.speed_i = next_node[1] - start_node[1]
                self.direction = [self.speed_i, self.speed_j]
                return 0

            for neighbor in self.game.board.get_adj_coords(*current):
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
        self.create_portals()

    def create_walls(self):
        # GENERATING RANDOM WALLS
        # density = 0.1  # density of  walls
        np.random.seed(2)
        # self.walls = np.random.choice(
        #     [True, False],
        #     size=(self.game.height, self.game.width),
        #     p=(density, 1 - density),
        # )

        # GENERATES WALLS FROM WALL_TYPES
        self.walls = np.zeros((self.game.height, self.game.width))
        self.wall_types = list(np.load("./gamedata/wall_types.npy"))
        for i in range(7):
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

    def get_adj_coords(self, j, i):
        return [
            (j + dj, i + di)
            for dj in (-1, 0, 1)
            for di in (-1, 0, 1)
            if self.check_movement(j + dj, i + di) and abs(dj) + abs(di) != 2
        ]

    def check_movement(self, j_test, i_test):
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.walls[j_test, i_test]
        )

    def create_portals(self):
        # create portals on random coords and connects them
        self.portals = np.zeros((self.game.height, self.game.width))
        self.portals_coords = []
        while len(self.portals_coords) < 2:
            j = np.random.randint(self.game.height)
            i = np.random.randint(self.game.width)
            if self.check_movement(j, i):
                self.portals[j, i] = 1
                self.portals_coords.append((j, i))

    def show_portals(self):
        # show portals on the board
        r_size = self.game.r_size
        for j, i in self.portals_coords:
            x, y = i * r_size, j * r_size
            self.board_rectangles[j, i] = self.game.c.create_rectangle(
                x,
                y,
                x + r_size,
                y + r_size,
                fill="green",
            )

    def check_portal(self, j, i):
        # checks if the player is on the portal
        return self.portals[j, i]

    def get_portal(self, j, i):
        # returns the coords of the portal
        return (
            self.portals_coords[0]
            if (j, i) != self.portals_coords[0]
            else self.portals_coords[1]
        )


def main():
    game = Game(17, 20)


if __name__ == "__main__":
    main()
