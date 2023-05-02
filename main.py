import tkinter as tk
import numpy as np
import time
import queue


class Game:
    def __init__(self, height, width):
        self.t = time.time()
        self.width = width
        self.height = height  # nbr de case
        self.r_size = 32  # pixel par case

        self.create_window()
        self.timer()
        self.create_canvas()
        self.board = Board(self)
        self.board.show_walls()
        self.create_entities()
        self.root.mainloop()

    def timer(self):
        self.root.title(f"Search Play time: {int(time.time() - self.t)}s")
        self.root.after(1000, self.timer)

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
        self.entities = {"player": [], "enemy": [], "portal": []}
        self.entities["player"].append(Player(self, [1, 1], 1))
        self.entities["enemy"].append(Enemy(self, [10, 10], 1))
        self.entities["enemy"].append(Enemy(self, [14, 7], 2))
        self.entities["portal"].append(Portal(self, [4, 14], 1))
        self.entities["portal"].append(Portal(self, [6, 19], 2))
        self.root.bind(
            "<KeyPress>", lambda e: self.entities["player"][0].speed_set(e.keysym)
        )
        self.root.bind(
            "<KeyRelease>", lambda e: self.entities["player"][0].speed_cancel(e.keysym)
        )


class Entity:
    def __init__(self, game, spawn_coord, numéro):
        self.game = game
        self.j, self.i = spawn_coord
        self.numéro = numéro
        self.caracter_init()
        self.direction = [999, 999]  # [up/down,left/right]
        self.delete_orientation = False
        self.canshoot = True  # relate to the judgement of condition
        self.num_sprites = 3
        self.sprites = [
            [
                self.subimage(32 * i, 0, 32 * (i + 1), 32)
                for i in range(self.num_sprites)
            ],
            [
                self.subimage(32 * i, 32, 32 * (i + 1), 64)
                for i in range(self.num_sprites)
            ],
            [
                self.subimage(32 * i, 64, 32 * (i + 1), 96)
                for i in range(self.num_sprites)
            ],
            [
                self.subimage(32 * i, 96, 32 * (i + 1), 128)
                for i in range(self.num_sprites)
            ],
        ]
        self.sprite_dir = 0  # 0:down, 1:left, 2:right, 3:up
        self.sprite_index = 0
        self.shape = self.game.c.create_image(
            0, 0, image=self.sprites[self.sprite_dir][self.sprite_index]
        )

        # initialise orientation
        self.orientation = self.game.c.create_oval(0, 0, 0, 0, fill="yellow", edge=None)
        self.speed_j, self.speed_i = 0, 0
        self.show()
        self.move_control()

    def show(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size + 32
        self.game.c.delete(self.shape)
        self.shape = self.game.c.create_image(
            x + r_size / 2,
            y - r_size / 2,
            image=self.sprites[self.sprite_dir][self.sprite_index],
        )

        self.sprite_index = (self.sprite_index + 1) % self.num_sprites
        # sprite loop
        self.game.root.after(400, self.show)

    def update_rect(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x, y)

    def update_orientation(self):
        r_size = self.game.r_size
        i_orientation_test = self.i + self.direction[0]
        j_orientation_test = self.j + self.direction[1]
        if (
            self.game.board.check_movement(j_orientation_test, i_orientation_test)
            and self.delete_orientation == False
        ):
            self.i_orientation = i_orientation_test
            self.j_orientation = j_orientation_test
            x_orientation, y_orientation = (
                self.i_orientation * r_size,
                self.j_orientation * r_size,
            )
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
        else:
            self.game.c.delete(self.orientation)

    def check_portal(self, j_test, i_test):
        # checks if the player is on the portal
        return (j_test, i_test) in [
            (portal.j, portal.i) for portal in self.game.entities["portal"]
        ]

    def get_portal(self, j_test, i_test):
        # returns the coords of the portal
        portal1, portal2 = self.game.entities["portal"]
        if (j_test, i_test) == (portal1.j, portal1.i):
            return portal2.j, portal2.i
        else:
            return portal1.j, portal1.i

    def move(self):
        i_test, j_test = self.i + self.speed_i, self.j + self.speed_j
        # if the player is in a portal
        if self.check_portal(j_test, i_test):
            j_test, i_test = self.get_portal(j_test, i_test)
            j_test += self.speed_j
            i_test += self.speed_i

        if self.game.board.check_movement(j_test, i_test):
            self.i = i_test
            self.j = j_test

        self.update_rect()
        self.update_orientation()
        self.game.root.after(int(1000 / self.speed), self.move_control)

    def move_control(self):
        pass

    def subimage(self, l, t, r, b):
        dst = tk.PhotoImage()
        dst.tk.call(dst, "copy", self.spritesheet, "-from", l, t, r, b, "-to", 0, 0)
        return dst

    def determine_sprite_dir(self, dir):
        # done by copilot
        if dir == [0, 1]:
            return 0
        elif dir == [-1, 0]:
            return 1
        elif dir == [1, 0]:
            return 2
        elif dir == [0, -1]:
            return 3


class Player(Entity):
    def caracter_init(self):
        self.speed = 15
        self.spritesheet = tk.PhotoImage(file="./img/spritesheet1.png")

    def move_control(self):
        self.move()

    def speed_set(self, k):
        if k in ("Up", "w", "W"):
            self.speed_i = 0
            self.speed_j = -1
            self.direction = [0, -1]
            self.sprite_dir = 3
        elif k in ("Left", "a", "A"):
            self.speed_i = -1
            self.speed_j = 0
            self.direction = [-1, 0]
            self.sprite_dir = 1
        elif k in ("Down", "s", "S"):
            self.speed_i = 0
            self.speed_j = 1
            self.direction = [0, 1]
            self.sprite_dir = 0
        elif k in ("Right", "d", "D"):
            self.speed_i = 1
            self.speed_j = 0
            self.direction = [1, 0]
            self.sprite_dir = 2

    def speed_cancel(self, k):
        if k in ("Up", "w", "W", "Down", "s", "S"):
            self.speed_j = 0
        elif k in ("Left", "a", "A", "Right", "d", "D"):
            self.speed_i = 0


class Enemy(Entity):
    def caracter_init(self):
        self.speed = 5
        self.spritesheet = tk.PhotoImage(file="./img/spritesheet2.png")

    def move_control(self):
        self.pathfinding()
        self.move()

    def pathfinding(self):
        start_node = (self.j, self.i)
        end_node = (
            self.game.entities["player"][0].j,
            self.game.entities["player"][0].i,
        )

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
                    self.game.root.title("Game Over")
                    # When found player : delete orientation
                    self.delete_orientation = True
                    self.speed_j, self.speed_i = 0, 0
                    return 0
                next_node = path[-1]
                self.speed_j = next_node[0] - start_node[0]
                self.speed_i = next_node[1] - start_node[1]
                self.direction = [self.speed_i, self.speed_j]
                self.sprite_dir = self.determine_sprite_dir(self.direction)
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


class Portal(Entity):
    def caracter_init(self):
        self.speed = 0
        self.spritesheet = tk.PhotoImage(file="./img/spritesheet1.png")


class Board:
    """
    les attributs de cette classe sont :
        self.game
        self.walls
        self.wall_rectangles
    """

    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.create_walls()

    def create_walls(self):
        # GENERATING RANDOM WALLS
        # density = 0.1  # density of  walls
        np.random.seed(2)

        # GENERATES WALLS FROM WALL_TYPES
        self.walls = np.zeros((self.game.height, self.game.width))
        wall_types = list(np.load("./gamedata/wall_types.npy"))
        for i in range(7):
            # Gets the wall type
            rnd = np.random.randint(len(wall_types))
            wall = wall_types[rnd]
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
        self.wall_rectangles = np.zeros((self.game.height, self.game.width))
        for j in range(self.game.height):
            for i in range(self.game.width):
                self.wall_rectangles[j, i] = self.game.c.create_rectangle(
                    i * r_size,
                    j * r_size,
                    (i + 1) * r_size,
                    (j + 1) * r_size,
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


def main():
    game = Game(17, 20)


if __name__ == "__main__":
    main()
