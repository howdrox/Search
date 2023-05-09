import tkinter as tk
import tkinter.filedialog
import numpy as np
import time, queue, os
from PIL import Image, ImageTk


class Game:
    """
    The main class of the game

    Initialize the the window, the canvas, the board and the entities. Contains the main loop of the game.

    Parameters:
        height: height of the maze (in square)
        width: width of the maze (in square)
        enemy_number: number of enemy in the maze
    """

    def __init__(self, height, width, enemy_number):
        self.width = width + (width % 2 == 0)
        self.height = height + (height % 2 == 0)  # nbr de case
        self.square_size = 30  # pixel par case
        self.enemy_number = enemy_number
        self.create_window()
        self.create_canvas()
        self.seed = int(time.time())
        np.random.seed(self.seed)
        self.start_game()
        self.timer_title()
        self.create_menu()
        self.root.mainloop()

    def start_game(self, load: bool = False):
        """Loads the maze and creates the entities"""
        self.t = time.time()
        if load:
            self.board.load_walls()
        else:
            self.board = Board(self)
        self.board.show_walls()
        self.create_entities()

    def clear(self):
        """Clear the canvas and destroy all entities"""
        for entity_dict in self.entities.values():
            for entity in list(entity_dict.values()):
                entity.destroy()
        self.c.delete("all")

    def restart(self, regenerate: bool = False, load: bool = False):
        """Restart the game and changes the seed if specified"""
        self.clear()
        if regenerate:
            self.seed += 1
            np.random.seed(self.seed)
        else:
            np.random.seed(self.seed)
        self.start_game(load=load)

    def timer_title(self):
        """Timer to update the window title to include the time played"""
        self.root.title(f"Search - Time Played: {int(time.time() - self.t)}s")
        self.root.after(1000, self.timer_title)

    def create_window(self):
        """Initializes the window"""
        self.c_width = self.width * self.square_size
        self.c_height = self.height * self.square_size  # canvas size (in pixel)
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}")
        self.root.title("Search")

    def create_canvas(self):
        """Initializes the canvas"""
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_entities(self):
        """Initializes the entities. Both players, the enemies and the portals"""
        self.entities = {"player": {}, "enemy": {}, "portal": {}, "bullet": {}}
        self.entities["player"][1] = Player(self, self.get_random_empty_square(), 1)
        self.entities["player"][2] = Player(self, self.get_random_empty_square(), 2)
        for i in range(1, self.enemy_number + 1):
            while True:
                cood = self.get_random_empty_square()
                d1 = self.board.manhattan(
                    cood, (self.entities["player"][1].j, self.entities["player"][1].i)
                )
                d2 = self.board.manhattan(
                    cood, (self.entities["player"][2].j, self.entities["player"][2].i)
                )
                if d1 > Enemy.capture_distance and d2 > Enemy.capture_distance:
                    break
            self.entities["enemy"][i] = Enemy(self, cood, i)
        self.entities["portal"][1] = Portal(self, self.get_random_empty_square(), 1)
        self.entities["portal"][2] = Portal(self, self.get_random_empty_square(), 2)

    def check_entities(self, j_test, i_test):
        """Checks if there is an entity at the given coordinates. Returns the entity if there is one, False otherwise"""
        for entity_dict in self.entities.values():
            for entity in entity_dict.values():
                if entity.j == j_test and entity.i == i_test:
                    return entity
        return False

    def check_square(self, j_test, i_test):
        """
        Checks if there is a wall or an entity at the given coordinates.
        Returns the entity if there is one, 'wall' if there is a wall, False otherwise
        """
        if self.board.check_walls(j_test, i_test):
            return "wall"
        else:
            return self.check_entities(j_test, i_test)

    def get_random_empty_square(self):
        """Returns random coordinates of an empty square"""
        while True:
            i_test = np.random.randint(0, self.width)
            j_test = np.random.randint(0, self.height)
            if not self.check_square(j_test, i_test):
                return j_test, i_test

    def create_menu(self):
        """Initializes the menu"""
        self.mainmenu = tk.Menu(self.root)

        self.gamemenu = tk.Menu(self.mainmenu, tearoff=0)
        self.gamemenu.add_command(label="Restart", command=self.restart)
        self.mainmenu.add_cascade(label="Game", menu=self.gamemenu)

        self.mazemenu = tk.Menu(self.mainmenu, tearoff=0)
        self.mazemenu.add_command(
            label="Regenerate", command=lambda: self.restart(regenerate=True)
        )
        self.mazemenu.add_command(label="Save Maze", command=self.board.save_walls)
        self.mazemenu.add_command(
            label="Load Maze", command=lambda: self.restart(load=True)
        )
        self.mainmenu.add_cascade(label="Maze", menu=self.mazemenu)

        self.root.config(menu=self.mainmenu)


class Entity:
    """
    Entity class. Parent of all entities i.e. players, enemies, portals and bullets.

    For all entities, `i` and `j` represent the coordinates of the entity on the board.
    With the origin at the top left corner, `i` is the vertical coordinate and `j` the horizontal one.

    Parameters:
        game: Game object
        spawn_coord: Coordinates of the spawn
        id: Id of the entity
    """

    def __init__(self, game, spawn_coord, id):
        """
        Initializes variable common to all entities.
        """
        self.game = game
        self.j, self.i = spawn_coord
        self.id = id
        self.speed_j, self.speed_i = 0, 0
        self.orientation_j, self.orientation_i = 1, 0
        self.caracter_init()
        self.create_sprites()
        self.update_sprites()
        self.move_control()

    def caracter_init(self):
        """
        Placeholder for the caracter initialization. To be implemented in the children classes.
        Manages the varying sprites of an entity, used for the `Player` class.
        """
        pass

    def create_sprites(self):
        """
        Creates a list of sprites for each orientation of the entity.
        """
        self.num_ani_frames = 3
        sprite_pixel = 48  # size of a sprite in the spritesheet
        self.spritesheet = Image.open(self.spritesheet_path)
        # 0:down, 1:left, 2:right, 3:up
        self.sprites = [
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
        """
        Changes the sprite of the entity to animate it and move it. Takes into account the orientation and the speed of the entity.
        """
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
        """
        Destroys the entity. Mainly used for the `Bullet` class once it hits a wall or a `Person`.
        """
        self.game.c.delete(self.shape)
        if hasattr(self, "to_update_sprites"):
            self.game.root.after_cancel(self.to_update_sprites)
        if hasattr(self, "to_move_control"):
            self.game.root.after_cancel(self.to_move_control)
        if not isinstance(self, Bullet):
            del self.game.entities[self.__class__.__name__.lower()][self.id]
        else:
            try:
                del self.game.entities[self.__class__.__name__.lower()][self.id]
            except KeyError:
                pass

    def get_portal(self, j_test, i_test):
        """Returns the coords of the other portal"""
        portal1, portal2 = self.game.entities["portal"].values()
        if (j_test, i_test) == (portal1.j, portal1.i):
            return portal2.j, portal2.i
        else:
            return portal1.j, portal1.i

    def move(self):
        """
        Changes the entities coordinates. Takes into account the speed of the entity and the collisions with the walls.

        Calls the function `move_control` as part of a timer.
        """
        i_test, j_test = self.i + self.speed_i, self.j + self.speed_j
        # if the player is in a portal
        if isinstance(self.game.check_square(j_test, i_test), Portal):
            j_test, i_test = self.get_portal(j_test, i_test)
            j_test += self.speed_j
            i_test += self.speed_i

        square_touched = self.game.check_square(j_test, i_test)

        if not square_touched or isinstance(square_touched, Bullet):
            self.i = i_test
            self.j = j_test
            self.update_sprites(move_only=True)
        elif isinstance(self, Bullet):
            if square_touched == "wall" or isinstance(square_touched, Bullet):
                self.destroy()
                return "子弹撞墙没了"  # bullet hits a wall and disappears
            if isinstance(square_touched, Person):
                square_touched.hp -= 1
                if square_touched.hp <= 0:
                    square_touched.destroy()
                self.destroy()
                return "子弹打人没了"  # bullet hits a person and disappears
        elif isinstance(self, Enemy):
            if isinstance(square_touched, Player):
                square_touched.hp -= 1
                if square_touched.hp <= 0:
                    square_touched.destroy()

        self.to_move_control = self.game.root.after(
            int(1000 / self.speed), self.move_control
        )

    def move_control(self):
        """
        Controls what functions are called after the movement timer is over.
        """
        self.move()

    def update_sprite_dir(self):
        """
        Updates the sprite direction to use a different sprite depending on the orientation of the entity.
        0: down, 1: left, 2: right, 3: up
        """
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
    """
    Parent class for the `Player` and `Enemy` classes. Inherits from `Entity`.
    """

    hp = 10


class Player(Person):
    """
    Class for the player. Inherits from `Person`.
    """

    speed = 15

    def caracter_init(self):
        """
        Specifies the player's sprite image and binds the keys to the player's movement.
        AZERTY keyboard compatible only (for the teacher marking this code).
        """
        if self.id == 1:
            self.spritesheet_path = "./img/characters/Actor3.png"
            self.sprite_pos_in_sheet_i = 2
            self.sprite_pos_in_sheet_j = 1
        else:
            self.spritesheet_path = "./img/characters/Actor3.png"
            self.sprite_pos_in_sheet_i = 3
            self.sprite_pos_in_sheet_j = 0

        move_keys = (
            ["z", "s", "q", "d"] if self.id == 1 else ["Up", "Down", "Left", "Right"]
        )
        for key in move_keys:
            self.game.root.bind(
                f"<KeyPress-{key}>", lambda e: self.key_speed_set(e.keysym)
            )
            self.game.root.bind(
                f"<KeyRelease-{key}>", lambda e: self.key_speed_cancel(e.keysym)
            )
        attack_key = "a" if self.id == 1 else "!"
        self.game.root.bind(f"<KeyPress-{attack_key}>", lambda e: self.shoot(e.keysym))

    def key_speed_set(self, k):
        """
        Updates the speed of the player if a key is pressed.
        """
        if k in ("Up", "z", "Z"):
            self.speed_i = 0
            self.speed_j = -1
        elif k in ("Left", "q", "Q"):
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
        """
        Cancels the speed of the player if a key is released.
        """
        if k in ("Up", "z", "Z", "Down", "s", "S"):
            self.speed_j = 0
        elif k in ("Left", "q", "Q", "Right", "d", "D"):
            self.speed_i = 0

    def shoot(self, k):
        """
        Creates a bullet if the player presses the attack key.
        """
        bullet_j = self.j + self.orientation_j
        bullet_i = self.i + self.orientation_i
        if not self.game.board.check_walls(bullet_j, bullet_i):
            bullet_id = (self.id, time.time())
            bullet = Bullet(self.game, (bullet_j, bullet_i), bullet_id)
            self.game.entities["bullet"][bullet_id] = bullet
            bullet.speed_i = self.orientation_i
            bullet.speed_j = self.orientation_j
            bullet.shootby = self.id


class Enemy(Person):
    """
    Class for the enemies. Inherits from `Person`.
    """

    capture_distance = 10
    speed = 5
    angry_duration = 1  # seconds
    spritesheet_path = "./img/characters/Monster.png"
    sprite_pos_in_sheet_i = 0
    sprite_pos_in_sheet_j = 0

    def move_control(self):
        """
        Controls what functions are called after the movement timer is over.
        """
        self.pathfinding()
        self.move()

    def pathfinding(self):
        """
        Finds the shortest path to the player and moves the enemy accordingly.
        Uses the A* algorithm.
        """
        start_node = (self.j, self.i)
        players = list(self.game.entities["player"].values())

        if len(players) == 0:
            self.speed_j, self.speed_i = 0, 0
            return 0
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
                    self.speed_j, self.speed_i = 0, 0
                    return 0
                elif len(path) <= self.capture_distance:
                    self.angry_start = time.time()
                elif (
                    not hasattr(self, "angry_start")
                    or time.time() - self.angry_start > self.angry_duration
                ):
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

        # If there is no path to the end_node
        self.speed_j, self.speed_i = 0, 0


class Portal(Entity):
    """
    Class for the portals. Inherits from `Entity`.
    """

    speed = 0.1
    spritesheet_path = "./img/characters/!Door2.png"
    sprite_pos_in_sheet_i = 0
    sprite_pos_in_sheet_j = 0

    def move_control(self):
        """
        Controls what functions are called after the movement timer is over.
        """
        self.refresh()
        self.move()

    def refresh(self):
        """
        Refreshes the portal's position.
        """
        self.j, self.i = self.game.get_random_empty_square()


class Bullet(Entity):
    """
    Class for the bullets. Inherits from `Entity`.
    """

    speed = 20
    spritesheet_path = "./img/characters/!Flame.png"
    sprite_pos_in_sheet_i = 2
    sprite_pos_in_sheet_j = 1
    shootby = None


class Board:
    """
    Class for the board. Contains the board's data and methods.

    Parameters:
        game (Game): Game object.
    """

    def __init__(self, game):
        self.game = game
        self.create_walls()
        self.create_sprites()

    def create_walls(self):
        """
        Creates a labyrinth of walls.
        """

        def allow_visit(j, i):
            """
            Checks if a square can be visited.
            """
            return (
                j not in [0, self.game.height - 1]
                and i not in [0, self.game.width - 1]
                and (j, i)
                not in [to_visit_cood for to_visit_cood, parent_cood in to_visit]
                and (j, i) not in visited_path
            )

        def mark_to_visit(j, i):
            """
            Marks a square to be visited.
            """
            for adj_coord in [(j + 1, i), (j - 1, i), (j, i + 1), (j, i - 1)]:
                if allow_visit(*adj_coord):
                    to_visit.append((adj_coord, (j, i)))

        X, Y = np.meshgrid(np.arange(self.game.width), np.arange(self.game.height))
        self.walls = (X % 2 == 0) | (Y % 2 == 0)

        while True:
            begin_j, begin_i = np.random.randint(
                0, self.game.height
            ), np.random.randint(0, self.game.width)
            if begin_j % 2 and begin_i % 2:
                break
        visited_island = {(begin_j, begin_i)}
        visited_path = set()
        to_visit = []
        mark_to_visit(begin_j, begin_i)
        while to_visit:
            (visiting_cood, parent_cood) = to_visit.pop(
                np.random.randint(len(to_visit))
            )
            visiting_j, visiting_i = visiting_cood
            detect_j, detect_i = np.array(visiting_cood) * 2 - np.array(parent_cood)
            visited_path.add(visiting_cood)
            if (detect_j, detect_i) not in visited_island:
                self.walls[detect_j, detect_i] = 0
                self.walls[visiting_j, visiting_i] = 0
            visited_island.add((detect_j, detect_i))
            mark_to_visit(detect_j, detect_i)

    def load_walls(self):
        """
        Loads the walls from a file.
        """
        path = tk.filedialog.askopenfilename(
            initialfile="wall.npy",
            initialdir=os.path.join(os.path.dirname(__file__), "walls"),
            filetypes=[("Numpy array", "*.npy")],
        )
        self.walls = np.load(path)

    def save_walls(self):
        """
        Saves the walls to a file.
        """
        path = tk.filedialog.asksaveasfilename(
            initialfile="wall.npy",
            initialdir=os.path.join(os.path.dirname(__file__), "walls"),
            filetypes=[("Numpy array", "*.npy")],
        )
        np.save(path, self.walls)

    def create_sprites(self):
        """
        Creates the sprites for the walls and the floor.
        """
        sprite_pixel = 48
        self.floor_spritesheet_path = "img/tilesets/Outside_A5.png"
        self.floor_sprite = ImageTk.PhotoImage(
            Image.open(self.floor_spritesheet_path)
            .crop(sprite_pixel * (np.array([7, 2] * 2) + (0, 0, 1, 1)))
            .resize((self.game.square_size,) * 2)
        )
        self.wall_spritesheet_path = "img/tilesets/Outside_B.png"
        self.wall_sprite = ImageTk.PhotoImage(
            Image.open(self.wall_spritesheet_path)
            .crop(sprite_pixel * (np.array([8, 4] * 2) + (0, 0, 1, 1)))
            .resize((self.game.square_size,) * 2)
        )

    def show_walls(self):
        """
        Shows the walls on the canvas.
        """
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
        """
        Returns the adjacent coordinates of a square on the board.
        """
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
        """Returns the manhattan distance between two nodes."""
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def check_walls(self, j_test, i_test):
        """
        Returns True if the square is a wall or out of bounds.
        """
        return (
            not 0 <= j_test < self.game.height
            or not 0 <= i_test < self.game.width
            or self.walls[j_test, i_test]
        )


def main():
    game = Game(18, 32, enemy_number=2)


if __name__ == "__main__":
    main()
