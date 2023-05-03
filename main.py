import tkinter as tk
import numpy as np
import time, queue
from PIL import Image, ImageTk


class Game:
    def __init__(self, height, width):
        self.t = time.time()
        self.width = width
        self.height = height  # nbr de case
        self.case_size = 50  # pixel par case

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
        self.c_width = self.width * self.case_size
        self.c_height = self.height * self.case_size  # canvas size (in pixel)
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}")
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_entities(self):
        self.entities = {"player": [], "enemy": [], "portal": []}
        self.entities["player"].append(Player(self, [1, 1], 1))
        self.entities["player"].append(Player(self, [15, 16], 2))
        self.entities["enemy"].append(Enemy(self, [10, 10], 1))
        self.entities["enemy"].append(Enemy(self, [14, 7], 2))
        self.entities["portal"].append(Portal(self, [4, 14], 1))
        self.entities["portal"].append(Portal(self, [6, 19], 2))

    def check_entities(self, j_test, i_test):
        for entity_list in self.entities.values():
            for entity in entity_list:
                if entity.j == j_test and entity.i == i_test:
                    return entity
        return False

    def check_case(self, j_test, i_test):
        if self.board.check_walls(j_test, i_test):
            return "wall"
        else:
            return self.check_entities(j_test, i_test)


class Entity:
    def __init__(self, game, spawn_coord, numéro):
        self.game = game
        self.j, self.i = spawn_coord
        self.numéro = numéro
        self.speed_j, self.speed_i = 0, 0
        self.orientation_j, self.orientation_i = 1, 0
        self.caracter_init()
        self.delete_orientation = False
        self.create_sprites()
        self.update_sprites()
        self.move_control()

    def caracter_init(self):
        pass

    def create_sprites(self):
        self.num_ani_frames = 3
        sprite_pixel = 48
        self.spritesheet = Image.open(self.spritesheet_path)
        self.sprites = [  # 0:down, 1:left, 2:right, 3:up
            # *(sprite_pixel * np.array([i, j, i + 1, j + 1]))
            [
                ImageTk.PhotoImage(
                    self.spritesheet.crop(
                        sprite_pixel
                        * np.array(
                            [
                                self.sprite_pos_in_sheet_i * 3 + i,
                                self.sprite_pos_in_sheet_j * 4 + j,
                                self.sprite_pos_in_sheet_i * 3 + i + 1,
                                self.sprite_pos_in_sheet_j * 4 + j + 1,
                            ]
                        )
                    ).resize((self.game.case_size, self.game.case_size))
                )
                for i in range(self.num_ani_frames)
            ]
            for j in range(4)
        ]
        self.update_sprite_dir()
        self.sprite_index = 0

    def update_sprites(self, move_only=False):
        case_size = self.game.case_size
        if hasattr(self, "shape"):
            self.game.c.delete(self.shape)
        self.shape = self.game.c.create_image(
            *(case_size * (np.array([self.i, self.j]) + 0.5)),
            image=self.sprites[self.sprite_dir][self.sprite_index],
        )

        self.sprite_index = (self.sprite_index + 1) % self.num_ani_frames
        if not move_only:
            self.game.root.after(300, self.update_sprites)

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

        if not self.game.check_case(j_test, i_test):
            self.i = i_test
            self.j = j_test
            self.update_sprites(move_only=True)

        self.game.root.after(int(1000 / self.speed), self.move_control)

    def move_control(self):
        self.move()

    def update_sprite_dir(self):
        if (self.orientation_i, self.orientation_j) == (0, 1):
            self.sprite_dir = 0
        elif (self.orientation_i, self.orientation_j) == (-1, 0):
            self.sprite_dir = 1
        elif (self.orientation_i, self.orientation_j) == (1, 0):
            self.sprite_dir = 2
        elif (self.orientation_i, self.orientation_j) == (0, -1):
            self.sprite_dir = 3
        else:
            raise ValueError("orientation not recognized")

        if isinstance(self, Portal) and self.numéro == 2:
            self.sprite_dir = 3
        elif isinstance(self, Bullet):
            self.sprite_dir = 3


class Player(Entity):
    def caracter_init(self):
        self.speed = 15
        self.spritesheet_path = "./img/characters/Actor3.png"
        self.sprite_pos_in_sheet_i = 2
        self.sprite_pos_in_sheet_j = 1

        move_keys = (
            ["w", "s", "a", "d"]
            if self.numéro == 1
            else ["Up", "Down", "Left", "Right"]
        )
        for key in move_keys:
            self.game.root.bind(
                f"<KeyPress-{key}>", lambda e: self.key_speed_set(e.keysym)
            )
            self.game.root.bind(
                f"<KeyRelease-{key}>", lambda e: self.key_speed_cancel(e.keysym)
            )
        attack_key = "q" if self.numéro == 1 else "/"
        self.game.root.bind(f"<KeyPress-{attack_key}>", lambda e: self.shoot(e.keysym))

    def key_speed_set(self, k):
        if k in ("Up", "w", "W"):
            self.speed_i = 0
            self.speed_j = -1
        elif k in ("Left", "a", "A"):
            self.speed_i = -1
            self.speed_j = 0
        elif k in ("Down", "s", "S"):
            self.speed_i = 0
            self.speed_j = 1
        elif k in ("Right", "d", "D"):
            self.speed_i = 1
            self.speed_j = 0
        self.orientation_i, self.orientation_j = self.speed_i, self.speed_j
        self.update_sprite_dir()

    def key_speed_cancel(self, k):
        if k in ("Up", "w", "W", "Down", "s", "S"):
            self.speed_j = 0
        elif k in ("Left", "a", "A", "Right", "d", "D"):
            self.speed_i = 0

    def shoot(self, k):
        bullet_j = self.j + self.speed_j
        bullet_i = self.i + self.speed_i
        if not self.game.board.check_walls(bullet_j, bullet_i):
            bullet = Bullet(self.game, (bullet_j, bullet_i), self.numéro)
            bullet.speed_i = self.orientation_i
            bullet.speed_j = self.orientation_j


class Enemy(Entity):
    def caracter_init(self):
        self.speed = 5
        self.spritesheet_path = "./img/characters/Monster.png"
        self.sprite_pos_in_sheet_i = 0
        self.sprite_pos_in_sheet_j = 0

    def move_control(self):
        self.pathfinding()
        self.move()

    def pathfinding(self):
        start_node = (self.j, self.i)
        players = self.game.entities["player"]
        end_node = (
            players[0].j,
            players[0].i,
        )
        if len(players) == 2:
            player2_node = (
                players[1].j,
                players[1].i,
            )
            if self.game.board.Manhattan(
                start_node, player2_node
            ) < self.game.board.Manhattan(start_node, end_node):
                end_node = player2_node

        g_score = {start_node: 0}  # actual cost from start_node to a node
        f_score = {
            start_node: self.game.board.Manhattan(start_node, end_node)
        }  # sum of g_score and h_score

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
                self.orientation_j, self.orientation_i = self.speed_j, self.speed_i
                self.update_sprite_dir()
                return 0

            for neighbor in self.game.board.get_adj_coords(*current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.game.board.Manhattan(
                        neighbor, end_node
                    )
                    frontier.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current
                # If the neighbor is in the frontier and the tentative g_score is lower,
                # update its g_score, f_score, and parent
                elif tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.game.board.Manhattan(
                        neighbor, end_node
                    )
                    frontier.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current


class Portal(Entity):
    def caracter_init(self):
        self.speed = 0.1
        self.spritesheet_path = "./img/characters/!Door2.png"
        self.sprite_pos_in_sheet_i = 0
        self.sprite_pos_in_sheet_j = 0

    def move_control(self):
        self.refresh()
        self.move()

    def refresh(self):
        while True:
            i_test = np.random.randint(0, self.game.width)
            j_test = np.random.randint(0, self.game.height)
            if not self.game.check_case(j_test, i_test):
                self.i = i_test
                self.j = j_test
                break


class Bullet(Entity):
    def caracter_init(self):
        self.speed = 20
        self.spritesheet_path = "./img/characters/!Flame.png"
        self.sprite_pos_in_sheet_i = 2
        self.sprite_pos_in_sheet_j = 1


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
        case_size = self.game.case_size
        self.wall_rectangles = np.zeros((self.game.height, self.game.width))
        for j in range(self.game.height):
            for i in range(self.game.width):
                self.wall_rectangles[j, i] = self.game.c.create_rectangle(
                    i * case_size,
                    j * case_size,
                    (i + 1) * case_size,
                    (j + 1) * case_size,
                    fill="grey" if self.walls[j, i] else "white",
                )

    def get_adj_coords(self, j, i):
        return [
            (j + dj, i + di)
            for dj in (-1, 0, 1)
            for di in (-1, 0, 1)
            if not self.check_walls(j + dj, i + di) and abs(dj) + abs(di) != 2
        ]

    def Manhattan(self, node1, node2):
        """Manhattan distance"""
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def check_walls(self, j_test, i_test):
        return (
            not 0 <= j_test < self.game.height
            or not 0 <= i_test < self.game.width
            or self.walls[j_test, i_test]
        )


def main():
    game = Game(17, 20)


if __name__ == "__main__":
    main()
