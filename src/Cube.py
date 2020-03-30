#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leoli
"""
from termcolor import colored

COLORS = ['R', 'G', 'B', 'Y', 'W', 'M']
COLORS_DICT = {'R' : 'red', 'G' : 'green', 'B' : 'cyan', 'Y' : 'yellow', 'W' : 'white', 'M' : 'magenta'}
AXES = ["X", "Y", "Z"]

class Cube:
    
    def __init__(self, size = 3):
        if size < 1:
            raise ValueError("The size of the cube must be greater than one.")
        self.rank = size - 2
        self.size = size
        self.faces_names = ["Front", "Back", "Up", "Down", "Left", "Right"]
        self.state = { face : [[COLORS[i]] * (self.size) for _ in range(self.size)] for i, face in enumerate(self.faces_names)}
        self.move_names = [axis + "{}".format(i) for axis in AXES for i in range(self.size)]

    def move(self, move_type, amount = 1):
        amount = amount % 4
        
        if move_type[0] == 'X':
            for _ in range(amount): 
                col_index = int(move_type[1])
                for row_index in range(self.size):
                    #Up <- Front
                    up_temp = self.state['Up'][row_index][col_index]
                    self.state['Up'][row_index][col_index] = self.state['Front'][row_index][col_index]
                    #Front <- Down
                    self.state['Front'][row_index][col_index] = self.state['Down'][row_index][col_index]
                    #Down <- Back
                    self.state['Down'][row_index][col_index] = self.state['Back'][self.size - 1 - row_index][self.size - 1 - col_index]
                    #Back <- Up
                    self.state['Back'][self.size - 1 - row_index][self.size - 1 - col_index] = up_temp
                
                #if it is the first or last row rotate the left or right face
                if col_index == 0:
                    self._rotate_face(self.state['Left'], False)
                elif col_index == self.size - 1:
                    self._rotate_face(self.state['Right'])
                    
        elif move_type[0] == 'Y':
            for _ in range(amount): 
                row_index = self.size - 1 - int(move_type[1])
                for col_index in range(self.size):
                    #Front <- Right
                    front_temp = self.state['Front'][row_index][col_index]
                    self.state['Front'][row_index][col_index] = self.state['Right'][row_index][col_index]
                    #Right <- Back
                    self.state['Right'][row_index][col_index] = self.state['Back'][row_index][col_index]
                    #Back <- Left
                    self.state['Back'][row_index][col_index] = self.state['Left'][row_index][col_index]
                    #Left <- Front
                    self.state['Left'][row_index][col_index] = front_temp
                
                if row_index == self.size - 1:
                    self._rotate_face(self.state['Down'], False)
                elif row_index == 0:
                    self._rotate_face(self.state['Up'])
                    
        elif move_type[0] == 'Z':
            for _ in range(amount): 
                row_index = self.size - 1 - int(move_type[1])
                for col_index in range(self.size):
                    #Up <- Right
                    up_temp = self.state['Up'][row_index][col_index]
                    self.state['Up'][row_index][col_index] = self.state['Right'][col_index][self.size - 1 - row_index]
                    #Right <- Down
                    self.state['Right'][col_index][self.size - 1 - row_index] = self.state['Down'][self.size - 1 - row_index][self.size - 1 - col_index]
                    #Down <- Left
                    self.state['Down'][self.size - 1 - row_index][self.size - 1 - col_index] = self.state['Left'][self.size - 1 - col_index][row_index]
                    #Left <- Up
                    self.state['Left'][self.size - 1 - col_index][row_index] = up_temp
                
                if row_index == self.size - 1:
                    self._rotate_face(self.state['Front'], False)
                elif row_index == 0:
                    self._rotate_face(self.state['Back'])
                    
        else :
            raise ValueError("Inavlid move identifier: see move_names\n")
    
    def _rotate_face(self, face, clockwise = True):
        #In an N*N matrix the i-indexed column becomes the (N-1)-i indexed row.
        #In place matrix rotation algorithm
        N = len(face)
        def rotate_4_elements(i, j):
            tmp = face[i][j]
            if clockwise:
                face[i][j] = face[N-j-1][i]
                face[N-j-1][i] = face[N-i-1][N-j-1]
                face[N-i-1][N-j-1] = face[j][N-i-1]
                face[j][N-i-1] = tmp
            else :
                face[i][j] = face[j][N-i-1]
                face[j][N-i-1] = face[N-i-1][N-j-1]
                face[N-i-1][N-j-1] = face[N-j-1][i]
                face[N-j-1][i] = tmp
            
        for circle in range(N // 2):
            for row_index in range(circle, N - circle - 1):
                rotate_4_elements(row_index, circle)
                
    def apply_moveset(self, moveset):
        for move, amount in moveset:
            self.move(move, amount)
                
    def is_solved(self):
        for face_name in self.faces_names:
            color = self.state[face_name][0][0]
            for i in range(self.size):
                for j in range(self.size):
                    if self.state[face_name][i][j] != color:
                        return False
        return True
                    

    def __str__(self):
        string = ""
        for row in self.state['Up']:
            string += " " * len(row) * 2
            for quad in row:
                string += colored(quad, COLORS_DICT[quad]) + " "
            string += "\n"
        
        for row_index in range(self.size):
            for quad in self.state["Left"][row_index]:
                string += colored(quad, COLORS_DICT[quad]) + " "
            for quad in self.state["Front"][row_index]:
                string += colored(quad, COLORS_DICT[quad]) + " "
            for quad in self.state["Right"][row_index]:
                string += colored(quad, COLORS_DICT[quad]) + " "
            for quad in self.state["Back"][row_index]:
                string += colored(quad, COLORS_DICT[quad]) + " "
            
            string += "\n"
        
        for row in self.state["Down"]:
            string += " " * len(row) * 2
            for quad in row:
                string += colored(quad, COLORS_DICT[quad]) + " "
            string += "\n"
            
        return string

if __name__ == '__main__':
    cube = Cube()
    print(cube)
    print("Cube is solved : {}".format(cube.is_solved()))
    cube.move('X0')
    print(cube)
    print("Cube is solved : {}".format(cube.is_solved()))
    cube.move('Y0')
    print(cube)
    cube.move('Z0')
    print(cube)
    print(cube.move_names)