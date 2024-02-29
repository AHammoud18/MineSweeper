import tkinter as TK
import customtkinter as ctk
import random


class MineSweeper():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry('720x720')
        self.center = 'center'
        self.tiles = {}
        self.tile_size = 30
        self.difficulty = {'easy' : (8,8, 20), 'medium' : (14,14, 50), 'hard' : (20,20, 99)} # rows, cols, mine count
        difficulty_menu = ctk.CTkComboBox(self.root, values=['Hard', 'Medium', 'Easy'], width=100)
        difficulty_menu.grid(padx=10, pady=10)
        diff = difficulty_menu.get().lower()
        #difficulty_menu.bind("<<ComboboxSelected>>", lambda: self.fieldFrame.destroy())
        self.fieldFrame = ctk.CTkFrame(self.root, border_color='white')
        if diff == 'easy':
            self.root.geometry('420x420')
            self.tile_size = 40
        elif diff == 'medium':
            self.root.geometry('620x620')
            self.tile_size = 40
        else:
            pass
        self.createField(diff)
        self.fieldFrame.place(relx=0.5, rely=0.5, anchor=self.center)

        
    

    def createField(self, diff: str):
        rows = self.difficulty[diff][0]
        cols = self.difficulty[diff][1]
        # create all possible tiles, then select random ones to become mines
        mines = random.sample([(i,j) for i in range(rows) for j in range(cols)], self.difficulty[diff][2]) 
        # create the grid with the rows, cols and assigned mine positions
        for i in range(rows):
            for j in range(cols):
                # frame that holds the tile
                frame = ctk.CTkFrame(self.fieldFrame, width=self.tile_size, height=self.tile_size)
                # its iterative position on the grid
                frame.grid(row=i, column=j)
                mine = 0
                if (j+i)%2==0:
                    color = '#aad750'
                elif (j+i)%2==1:
                    color = '#a0ce47'
                # the tile itself attaching ontop of the frame
                tile = ctk.CTkButton(frame, width=self.tile_size, height=self.tile_size, corner_radius=0 , text='', command=lambda i=i, j=j: self.tileSelected(i, j, rows, cols), fg_color=color)
                # check the grid index and see if it should be a mine
                if  (i,j) in mines:
                    tile.configure(False, fg_color='red')
                    mine = 1
                # place the tile on the frame rendering it visible
                tile.place(relx=0.5, rely=0.5, anchor=self.center)
                # dictionary to hold the tile's info
                self.tiles[(i, j)] = (i,j,mine)
                        
        del mines

    def columnCheck(self, i, j):
        k = 0
        for n in range(3):
            if (i, (j-1)+n) in self.tiles:
                k += 1 if self.tiles[(i, (j-1)+n)][2] == 1 else 0
        return k
            

    def tileSelected(self, i: int, j:int, rows: int, cols: int):
        # same row
        if self.tiles[(i, j)][2] == 1:
            print('Game Over')
            return -1
        mines = 0
        mines += self.columnCheck(i, j)
        # top row
        if (i-1) >= 0:
            mines += self.columnCheck(i-1, j)
        # bottom row
        if  (i+1) < rows:
            mines += self.columnCheck(i+1, j)
        else:
            pass
        print(mines)
        


if __name__ == '__main__':
    # create root window
    main = MineSweeper().root
    main.resizable(False, False)
    main.mainloop()
