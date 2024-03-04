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
        self.mines = []
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
        k = 1
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
                tile.configure(command=lambda k=k, t=tile: self.tileSelected(diff, k, self.game_state,t))
                # place the tile on the frame rendering it visible
                tile.place(relx=0.5, rely=0.5, anchor=self.center)
                # dictionary to hold the tile's info
                self.tiles[k] = [0, 0]
                k += 1
        # create all possible tiles, then select random ones to become mines
        self.mines = random.sample([i for i in range(len(self.tiles))], self.difficulty[diff][2])
        for key in self.tiles:
            if key in self.mines:
                self.tiles[key][0] = 1
    
        
        
            
    def tileSelected(self, diff:str, k:int, game_state:int):
        mine_count = 0
        rows = self.difficulty[diff][0]
        tiles = self.field_frame.winfo_children() # list of buttons within the field frame

        if game_state == 0:
            
            # check the grid index and see if it should be a mine, exclude the user's first selected space
            self.tiles[k][0] = 0 if self.tiles[k][0] == 1 else None
                
            for key in self.tiles:
                mine_count = self.mineCheck(key, rows, self.mines)
                self.tiles[key][1] = mine_count
                
            self.game_state = 1
            pass

        if self.tiles[k][0] == 1:
            print('Game Over')
            return -1
        # iterate through all 9 spaces including the selected tile and mark them as mines if valid
        empty_cells = []
        self.removeTile(self.tiles[k][1], tiles[k-1].winfo_children()[0])
        self.tiles.pop(k)
        
        # TODO - open up any empty space around the clicked one recursively until there are no more changes
        #print(f'mines near this cell: {k}')

    def mineCheck(self,  k:int, rows: int, mines: list[int], tiles: list = None):
        mine_count = 0
        cells = []
        for v in range(3):
            i_0 = (k-1)+v
            i_1 = ((k-20)-1)+v
            i_2 = ((k+20)-1)+v
            mine_count += 1 if i_0 in mines else 0
            mine_count += 1 if i_1 in mines else 0
            mine_count += 1 if i_2 in mines else 0

        if mine_count < 1:
            #print('')
            pass
            #print(cells)
        return mine_count


    def removeTile(self, mine_count: int, t:ctk.CTkButton = None):
        colors = ('#ffffff', '#3bdb63', '#3bdbb3', '#3b5bdb', '#713bdb', '#b13bdb', '#db3bbe', '#db3b76', '#db3b3b')
        t.configure(False, fg_color='transparent', hover=False, text=f'{mine_count}' if mine_count > 0 else '', text_color=colors[mine_count], font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"))
        t.configure(command=None)

if __name__ == '__main__':
    # create root window
    main = MineSweeper().root
    main.resizable(False, False)
    main.mainloop()
