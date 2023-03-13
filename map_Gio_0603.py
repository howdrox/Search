import tkinter as tk
import random
class map():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.rows = 30
        self.cols = 30
        self.rect_width = 25
        self.rect_height = 25
        self.num_walls = 150
        self.canvas = tk.Canvas(self.window, width=self.cols*self.rect_width
                                 ,height=self.rows*self.rect_height)
        self.canvas.pack()
        self.rectangles = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.rasterize()
        self.create_walls()
    
    def rasterize(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.rect_width
                y1 = row * self.rect_height
                x2 = x1 + self.rect_width
                y2 = y1 + self.rect_height
                self.rectangles[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
    
    def create_walls(self):
        for i in range(self.num_walls):
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
            self.canvas.itemconfig(self.rectangles[row][col], fill="black") 
            # finalement le nombre des rectangles noirs < num_walls à cause de la répétition


if __name__ == "__main__":
    app = map()
    app.window.mainloop()