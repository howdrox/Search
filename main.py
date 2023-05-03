import tkinter as tk
import numpy as np
import time, queue
from PIL import Image, ImageTk


class Game:
    def __init__(self, height, width):
        self.t = time.time()
        self.width = width
        self.height = height  # nbr de case
        self.square_size = 45  # pixel par case

        self.create_window()
        self.timer_title()
        self.create_canvas()
        self.board = Board(self)
        self.board.show_walls()
        self.create_entities()
        self.root.mainloop()

    def timer_title(self):
        self.root.title(f"Search - Time Played: {int(time.time() - self.t)}s")
        self.root.after(1000, self.timer_title)

    def create_window(self):
        self.c_width = self.width * self.square_size
        self.c_height = self.height * self.square_size  # canvas size (in pixel)
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}")
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_entities(self):
        self.entities = {"player": {}, "enemy": {}, "portal": {}}
        self.entities["player"][1] = Player(self, self.get_random_empty_square(), 1)
        self.entities["player"][2] = Player(self, self.get_random_empty_square(), 2)
        self.entities["enemy"][1] = Enemy(self, self.get_random_empty_square(), 1)
        self.entities["enemy"][2] = Enemy(self, self.get_random_empty_square(), 2)
        self.entities["portal"][1] = Portal(self, self.get_random_empty_square(), 1)
        self.entities["portal"][2] = Portal(self, self.get_random_empty_square(), 2)

    def check_entities(self, j_test, i_test):
        for entity_dict in self.entities.values():
            for entity in entity_dict.values():
                if entity.j == j_test and entity.i == i_test:
                    return entity
        return False

    def check_square(self, j_test, i_test):
        if self.board.check_walls(j_test, i_test):
            return "wall"
        else:
            return self.check_entities(j_test, i_test)

    def get_random_empty_square(self):
        while True:
            i_test = np.random.randint(0, self.width)
            j_test = np.random.randint(0, self.height)
            if not self.check_square(j_test, i_test):
                return j_test, i_test


class Entity:
    def __init__(self, game, spawn_coord, id):
        self.game = game
        self.j, self.i = spawn_coord
        self.id = id
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
                        * (
                            np.array(
                                [
                                    self.sprite_pos_in_sheet_i * 3 + i,
                                    self.sprite_pos_in_sheet_j * 4 + j,
                                ]
                                * 2
                            )
                            + (0, 0, 1, 1)
                        )
                    ).resize((self.game.square_size,) * 2)
                )
                for i in range(self.num_ani_frames)
            ]
            for j in range(4)
        ]
        self.update_sprite_dir()
        self.sprite_index = 0

    def update_sprites(self, move_only=False):
        square_size = self.game.square_size
        if hasattr(self, "shape"):
            self.game.c.delete(self.shape)
        self.shape = self.game.c.create_image(
            *(square_size * (np.array([self.i, self.j]) + 0.5)),
            image=self.sprites[self.sprite_dir][self.sprite_index],
        )

        self.sprite_index = (self.sprite_index + 1) % self.num_ani_frames
        if not move_only:
            self.to_update_sprites = self.game.root.after(300, self.update_sprites)

    def destroy(self):
        self.game.c.delete(self.shape)
        if hasattr(self, "to_update_sprites"):
            self.game.root.after_cancel(self.to_update_sprites)
        if hasattr(self, "to_move_control"):
            self.game.root.after_cancel(self.to_move_control)
        if isinstance(self, Person):
            del self.game.entities[self.__class__.__name__.lower()][self.id]

    def get_portal(self, j_test, i_test):
        # returns the coords of the portal
        portal1, portal2 = self.game.entities["portal"].values()
        if (j_test, i_test) == (portal1.j, portal1.i):
            return portal2.j, portal2.i
        else:
            return portal1.j, portal1.i

    def move(self):
        i_test, j_test = self.i + self.speed_i, self.j + self.speed_j
        # if the player is in a portal
        if isinstance(self.game.check_square(j_test, i_test), Portal):
            j_test, i_test = self.get_portal(j_test, i_test)
            j_test += self.speed_j
            i_test += self.speed_i

        square_touched = self.game.check_square(j_test, i_test)

        if not square_touched:
            self.i = i_test
            self.j = j_test
            self.update_sprites(move_only=True)
        elif isinstance(self, Bullet):
            if square_touched == "wall":
                self.destroy()
                return "死了哈哈哈没了"
            if isinstance(square_touched, Enemy):
                square_touched.destroy()
                self.destroy()
                return "die"

        self.to_move_control = self.game.root.after(
            int(1000 / self.speed), self.move_control
        )

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

        if isinstance(self, Portal) and self.id == 2:
            self.sprite_dir = 3
        elif isinstance(self, Bullet):
            self.sprite_dir = 3


class Person(Entity):
    pass


class Player(Person):
    def caracter_init(self):
        self.speed = 15
        if self.id == 1:
            self.spritesheet_path = "./img/characters/Actor3.png"
            self.sprite_pos_in_sheet_i = 2
            self.sprite_pos_in_sheet_j = 1
        else:
            self.spritesheet_path = "./img/characters/Actor3.png"
            self.sprite_pos_in_sheet_i = 3
            self.sprite_pos_in_sheet_j = 0

        move_keys = (
            ["w", "s", "a", "d"] if self.id == 1 else ["Up", "Down", "Left", "Right"]
        )
        for key in move_keys:
            self.game.root.bind(
                f"<KeyPress-{key}>", lambda e: self.key_speed_set(e.keysym)
            )
            self.game.root.bind(
                f"<KeyRelease-{key}>", lambda e: self.key_speed_cancel(e.keysym)
            )
        attack_key = "q" if self.id == 1 else "/"
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
            bullet = Bullet(self.game, (bullet_j, bullet_i), self.id)
            bullet.speed_i = self.orientation_i
            bullet.speed_j = self.orientation_j


class Enemy(Person):
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
        players = list(self.game.entities["player"].values())
        end_node = (
            players[0].j,
            players[0].i,
        )
        if len(players) == 2:
            player2_node = (
                players[1].j,
                players[1].i,
            )
            if self.game.board.manhattan(
                start_node, player2_node
            ) < self.game.board.manhattan(start_node, end_node):
                end_node = player2_node

        g_score = {start_node: 0}  # actual cost from start_node to a node
        f_score = {
            start_node: self.game.board.manhattan(start_node, end_node)
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
                    f_score[neighbor] = tentative_g_score + self.game.board.manhattan(
                        neighbor, end_node
                    )
                    frontier.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current
                # If the neighbor is in the frontier and the tentative g_score is lower,
                # update its g_score, f_score, and parent
                elif tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.game.board.manhattan(
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
        self.j, self.i = self.game.get_random_empty_square()


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
        self.create_walls()
        self.create_sprites()

    def create_walls(self):
        # GENERATING RANDOM WALLS
        np.random.seed(10)

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

    def create_sprites(self):
        sprite_pixel = 48
        self.floor_spritesheet_path = "img/tilesets/Outside_A2.png"
        self.floor_sprite = ImageTk.PhotoImage(
            Image.open(self.floor_spritesheet_path)
            .crop(sprite_pixel * (np.array([0, 0] * 2) + (0, 0, 1, 1)))
            .resize((self.game.square_size,) * 2)
        )
        self.wall_spritesheet_path = "img/tilesets/World_A2.png"
        self.wall_sprite = ImageTk.PhotoImage(
            Image.open(self.wall_spritesheet_path)
            .crop(sprite_pixel * (np.array([14, 6] * 2) + (0, 0, 1, 1)))
            .resize((self.game.square_size,) * 2)
        )

    def show_walls(self):
        square_size = self.game.square_size
        floor_shapes = np.array(
            [
                [
                    self.game.c.create_image(
                        *(square_size * (np.array([i, j]) + 0.5)),
                        image=self.floor_sprite,
                    )
                    for i in range(self.game.width)
                ]
                for j in range(self.game.height)
            ]
        )

        wall_shapes = np.array(
            [
                [
                    self.game.c.create_image(
                        *(square_size * (np.array([i, j]) + 0.5)),
                        image=self.wall_sprite,
                    )
                    if self.walls[j, i]
                    else 0
                    for i in range(self.game.width)
                ]
                for j in range(self.game.height)
            ]
        )

    def get_adj_coords(self, j, i):
        res = []
        for coords_adj in [(j + 1, i), (j - 1, i), (j, i + 1), (j, i - 1)]:
            case_adj = self.game.check_square(*coords_adj)
            if (
                case_adj != "wall"
                and not isinstance(case_adj, Portal)
                and not isinstance(case_adj, Enemy)
            ):
                res.append(coords_adj)
        return res

    def manhattan(self, node1, node2):
        """manhattan distance"""
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def check_walls(self, j_test, i_test):
        return (
            not 0 <= j_test < self.game.height
            or not 0 <= i_test < self.game.width
            or self.walls[j_test, i_test]
        )


def main():
    game = Game(15, 20)


if __name__ == "__main__":
    main()
