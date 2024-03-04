import tkinter as TK
import customtkinter as ctk
from tkinter import font
import random


class MineSweeper():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry('720x720')
        self.center = 'center'
        self.tiles = {}
        self.tile_size = 30
        self.game_state = 0
        self.difficulty = {'easy' : (8,8, 20), 'medium' : (14,14, 50), 'hard' : (20,20, 99)} # rows, cols, mine count
        difficulty_menu = ctk.CTkComboBox(self.root, values=['Hard', 'Medium', 'Easy'], width=100)
        difficulty_menu.grid(padx=10, pady=10)
        diff = difficulty_menu.get().lower()
        #difficulty_menu.bind("<<ComboboxSelected>>", lambda: self.fieldFrame.destroy())
        self.field_frame = ctk.CTkFrame(self.root, border_color='white')
        if diff == 'easy':
            self.root.geometry('420x420')
            self.tile_size = 40
        elif diff == 'medium':
            self.root.geometry('620x620')
            self.tile_size = 40
        else:
            pass
        self.createField(diff)
        self.field_frame.place(relx=0.5, rely=0.5, anchor=self.center)
        

    def createField(self, diff: str):
        k = 0
        rows = self.difficulty[diff][0]
        cols = self.difficulty[diff][1]
        # create the grid with the rows, cols and assigned mine positions
        for i in range(1, rows+1):
            for j in range(1, cols+1):
                # frame that holds the tile
                frame = ctk.CTkFrame(self.field_frame, width=self.tile_size, height=self.tile_size)
                # its iterative position on the grid
                frame.grid(row=i, column=j)
                if (j+i)%2==0:
                    color = '#aad750'
                elif (j+i)%2==1:
                    color = '#a0ce47'
                # the tile itself attaching ontop of the frame
                tile = ctk.CTkButton(frame, width=self.tile_size, height=self.tile_size, corner_radius=0 , text='', fg_color=color, hover_color='#a0de47', text_color='black')
                tile.configure(command=lambda i=i, j=j, t=tile: self.tileSelected(diff, i, j, self.game_state,t))
                
                # place the tile on the frame rendering it visible
                tile.place(relx=0.5, rely=0.5, anchor=self.center)
                # dictionary to hold the tile's info
                k += 1
                self.tiles[(i, j)] = [i,j,0,k]             
        
        
            
    def tileSelected(self, diff:str, i:int, j:int, game_state:int, t:ctk.CTkButton = None):
        k = 0
        rows = self.difficulty[diff][0]
        cols = self.difficulty[diff][1]
        tiles = self.field_frame.winfo_children()
        #tiles[5].winfo_children()[0].configure(fg_color="red")
        if game_state == 0:
            # create all possible tiles, then select random ones to become mines
            mines = random.sample([(i,j) for i in range(1, rows+1) for j in range(1, cols+1)], self.difficulty[diff][2])
            # check the grid index and see if it should be a mine, exclude the user's first selected space
            for (r,c) in self.tiles:
                if  (r,c) in mines and (r,c) != (i,j):
                    self.tiles[(r,c)][2] = 1

            del mines
            pass
        print((j+rows)-rows)
        #print(400)
        if self.tiles[(i, j)][2] == 1:
            print('Game Over')
            return -1
        # iterate through all 9 spaces including the selected tile and mark them as mines if valid
        empty_cells = []
        '''for m in range(3):
            for n in range(3):
                if ((i-1)+m, (j-1)+n) in self.tiles:
                    v = 1 if self.tiles[((i-1)+m, (j-1)+n)][2] == 1 else 0
                    if v == 0 and self.game_state == 0:
                        row = (i-1)+m
                        col = (j-1)+n
                        empty_cells.append(self.tiles[(row, col)][3])
                        tile_num = self.tiles[(row, col)][3]
                        self.removeTile(k, tiles[tile_num].winfo_children()[0])
                        #print(self.tiles[((i-1)+m, (j-1)+n)])
                        #print("open tiles here")
                    k += v'''
        k += self.mineCheck(i, j, rows, tiles)
        self.removeTile(k, t)
        self.game_state = 1
        # TODO - open up any empty space around the clicked one recursively until there are no more changes
        #print(f'mines near this cell: {k}')

    def mineCheck(self,  i:int, j:int, rows: int, tiles: list):
        k = 0
        cells = []
        for m in range(3):
            for n in range(3):
                mine = 1 if ((i-1)+m, (j-1)+n) in self.tiles and self.tiles[((i-1)+m, (j-1)+n)][2] == 1 else 0
                #index = self.tiles[((i-1)+m, (j-1)+n)][3]
                #print(index)
                #if mine == 0 and ((i-1)+m, (j-1)+n) in self.tiles:
                    #cells.append(index)
                k += mine
        if k < 1:
            print('vacant cell')
            print(cells)
        return k


    def removeTile(self, k:int = 0, t:ctk.CTkButton = None):
        colors = ('#ffffff', '#3bdb63', '#3bdbb3', '#3b5bdb', '#713bdb', '#b13bdb', '#db3bbe', '#db3b76', '#db3b3b')
        t.configure(False, fg_color='transparent', hover=False, text=f'{k}', text_color=colors[k], font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"))
        t.configure(command=None)

if __name__ == '__main__':
    # create root window
    main = MineSweeper().root
    main.resizable(False, False)
    main.mainloop()
