#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: leoli
"""
from Cube import Cube

def get_moveset_rank(moveset, cube_rank = 1):
    """ Computes the rank of a given moveset.\n
    Def. Rank = The number of times a moveset has to be applied to return 
    to the original state of the cube.\n
    Def. Moveset = A moveset is a list of tuples of the form (move, amount)\n
    Example: [('X0', 1), ('Z2', 3)].\n
    :cube_rank: the rank of the cube, default 1 (3x3x3)
    """ 
    cube = Cube(cube_rank)
    cube.apply_moveset(moveset)
    moveset_rank = 1
    while not cube.is_solved():
        cube.apply_moveset(moveset)
        moveset_rank += 1
    return moveset_rank
