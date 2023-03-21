import tkinter as tk
import json
import numpy as np
import random
from threading import Timer


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
        for p in self.persons:
            p.show()

        self.root.bind("<KeyPress>", lambda e: self.persons[0].move(e.keysym))
        self.root.bind("<KeyRelease>", lambda e: self.persons[0].stop(e.keysym))
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
        self.persons = []
        self.persons.append(Person(self, False, [1, 4]))
        self.persons.append(Person(self, True, [6, 6]))


class Person:
    def __init__(self, game, evil, spawn_coord):
        self.game = game
        self.evil = evil
        self.j, self.i = spawn_coord
        self.dt = 500
        self.directions = [False, False, False, False]
        self.mvt_timer = [
            tmr(self.dt, lambda: self.mvt("w")),
            tmr(self.dt, lambda: self.mvt("a")),
            tmr(self.dt, lambda: self.mvt("s")),
            tmr(self.dt, lambda: self.mvt("d")),
        ]

    def show(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.shape = self.game.c.create_rectangle(
            x, y, x + r_size, y + r_size, fill="red" if self.evil else "blue"
        )

    def update(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x, y)

    def move(self, k):
        if k in ("Up", "w") and not k[0]:
            k[0] = True
            self.mvt_timer[0].start()
        elif k in ("Left", "a") and not k[1]:
            k[1] = True
            self.mvt_timer[1].start()
        elif k in ("Down", "s") and not k[2]:
            k[2] = True
            self.mvt_timer[2].start()
        elif k in ("Right", "d") and not k[3]:
            k[3] = True
            self.mvt_timer[3].start()

    def mvt(self, k):
        print(k)
        # coord où on veut aller
        j_test, i_test = self.j, self.i
        if k in ("Up", "w"):
            j_test = self.j - 1
        elif k in ("Left", "a"):
            i_test = self.i - 1
        elif k in ("Down", "s"):
            j_test = self.j + 1
        elif k in ("Right", "d"):
            i_test = self.i + 1

        if self.check_movement(j_test, i_test):
            self.j, self.i = j_test, i_test

        self.update()

        # self.mvt_timer.start()
        # if not self.allow_movement:
        #     self.mvt_timer.cancel()

    def check_movement(self, j_test, i_test):
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.game.board.walls[j_test, i_test]
        )

    def stop(self, k):
        if k in ("Up", "w"):
            self.mvt_timer[0].cancel()
        elif k in ("Left", "a"):
            self.mvt_timer[1].cancel()
        elif k in ("Down", "s"):
            self.mvt_timer[2].cancel()
        elif k in ("Right", "d"):
            self.mvt_timer[3].cancel()

        # if k == self.allow_movement:
        #     self.allow_movement = None
        #     self.game.root.after_cancel(self.timer)


class Board:
    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.board_rectangles = np.zeros((self.game.height, self.game.width))
        self.create_walls()

    def create_walls(self):
        self.walls = np.load("gamedata/walls.npy")

    # CODE POUR GENERER ALEATOIREMENT LA CARTE, NE PAS SUPPRIMER

    # def create_walls(self):
    #     self.walls = np.zeros((self.height, self.width))
    #     for i in range(56):
    #         x = random.randint(0, self.width-1)
    #         y = random.randint(0, self.height-1)
    #         self.walls[y, x] = True
    #     data = {"walls": self.walls.tolist()}
    #     with open("/mnt/insa/lkusno/Home_INSA/Informatique/Algo/A2/Search/data.json", "w") as f:
    #         json.dump(data, f)

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


# Définition de la classe MonTimer
class tmr:
    # Le cosntructeur avec comme arguments délai (la période de répétition) et fonction (la méthode à répéter)
    def __init__(self, delai, fonction):
        self.delai = delai
        self.fonction = fonction
        self.timer = Timer(delai, self.run)  # Création du timer

    # La méthode au démarage qui lance le Timer
    def start(self):
        self.timer.start()

    # Lors de son exécution, un nouveau Timer est créé pour de nouveau lancer la méthode à répéter
    def run(self):
        self.timer = Timer(self.delai, self.run)
        self.timer.start()
        self.fonction()

    # Lors de l'arrêt de cette tâche, le Timer s'arrête et s'annule
    def cancel(self):
        self.timer.cancel()


def main():
    game = Game(19, 23)


if __name__ == "__main__":
    main()
