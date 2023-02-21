import tkinter as tk

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.c_width = width * 50
        self.c_height = height * 50

        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}") 
        self.root.title("Search")
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height, bg="black")
        self.c.place(anchor=tk.CENTER)

        self.board = [[False for i in range(height)] for i in range(width)]
        self.fill_walls()
        self.root.mainloop()

    def fill_walls(self):
        """Modify slef.board to add in walls"""
        with open("./board.txt", "r") as f:
            self.board = f.readline()
    
    def show_walls(self):
        """Creates walls on canvas"""
        for i in range(self.width):
            for j in range(self.height):
                self.c.create_rectangle(i * 50 + 10, j * 50 + 10, 50, 50, fill="grey")
    
        

def main():
    game = Game(7, 7)

if __name__ == "__main__":
    main()