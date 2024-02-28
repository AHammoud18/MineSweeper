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
        diff = 'hard'
        self.fieldFrame = ctk.CTkFrame(self.root)
        self.border_frame = ctk.CTkFrame(self.root, width=self.fieldFrame.winfo_width(), height=self.fieldFrame.winfo_height(), border_color='white', border_width=8)
        self.border_frame.place(relx=0.5, rely=0.5, anchor=self.center)
        self.fieldFrame.place(relx=0.5, rely=0.5, anchor=self.center)
        if diff == 'easy':
            self.root.geometry('420x420')
            self.tile_size = 40
        elif diff == 'medium':
            self.root.geometry('620x620')
            self.tile_size = 40
        else:
            pass
        
        self.createField(diff)
        bar = ctk.CTkComboBox(self.root)
        bar['values'] = ('Easy', 'Medium', 'Hard')
        bar.grid(padx=10, pady=10)
        
    

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
                tile = ctk.CTkButton(frame, width=self.tile_size, height=self.tile_size, corner_radius=0 , text='', command=lambda i=i, j=j: self.tileSelected(i, j), fg_color=color)
                # check the grid index and see if it should be a mine
                if  (i,j) in mines:
                    tile.configure(False, fg_color='red')
                    mine = 1
                # place the tile on the frame rendering it visible
                tile.place(relx=0.5, rely=0.5, anchor=self.center)
                # dictionary to hold the tile's info
                self.tiles[(i, j)] = f'{i,j}, mine: {mine}'
                        
        del mines, rows, cols

    def tileSelected(self, i: int, j:int):
        print(self.tiles[(i,j)])

if __name__ == '__main__':
    # create root window
    main = MineSweeper().root
    main.resizable(False, False)
    main.mainloop()
