#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid
Anjesh Shrestha                anjesh
Andrew Rosario                 rosario2
Areez Ladhani                  areez
Shawna Dawson	               sndawson
Yourui Dong                    ydong

#############################################
# Your answer to question 1-a:
2 gliders, going in opposite directions

. * *
* * .
. . *
. . .
. . .
* . .
. * *
* * .

the simulation will move diagonally during its lifetime
in 4 itteration to return to it original image

#############################################
# Your answer to question 1-b:
Gosper glider gun which fires gliders forever
no 2 glider interact with one another on an unbounded grid
and the number of cells alive will always increase
because new gliders are being created
Also a "dirty" puffer train that leaves being debris

this is another unbounded growth pattern
that leaves behind 
* * * . *
* . . . .
. . . * *
. * * . *
* . * . *

#############################################
# Your answer to question 2:
In life.py uses a string for it's data structure in row major order

life-np.py uses an 2 dimensional matrix created with numpy 

what happened to num_nbrs in life-np.py:
    it is a part of the next_state function
    because there is no need for guard cells

how an infinite grid is implemented in life.py:
    it is implemented by the addition of guard cells
    when an alive cell is next to a guard cell.
    more row/coloumn is added to the side by the function pad
    before every itteration, pad checks for cells alive
    near the edges/guard cells.
    for the first or last unguarded row, which is the easiest
    due to the data structure being in row-major order
    increace the rows by 1
    for frist and last unguarded columns, which is much harder
    add a dead cell to each column at the end 
    or the begening after the guard cell
    
how the use of a guarded board simplifies num_nbrs.
    having a guarded border simplifies num_nbrs
    because it will not break the search for neighbours
    by looking at the next row or previous row
    if there were no guard cells, there would have to be 
    different type of checks in place

#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:

Anjesh: 33
Andrew: 50
Areez: 08
Shawna: 74
Yourui: 27
Total = 192

After iterations 192
......***.....
..............
..............
.......*......
........*.....


#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
    A = np.zeros((r, c), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if B[j][k] == ACH:
                A[j, k] = ALIVE
    return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
    N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if A[j][k] == ALIVE:
                N[j+t, k+t] = ALIVE
    return N, r+2*t, c+2*t


def print_array(A, r, c):
    print('')
    for j in range(r):
        out = ''
        for k in range(c):
            out += ACH if A[j, k] == ALIVE else DCH
        print(out)


def show_array(A, r, c):
    for j in range(r):
        line = ''
        for k in range(c):
            line += str(A[j, k])
        print(line)
    print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = 0
            if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
                num += 1
            if j > 0 and A[j-1, k] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
                num += 1
            if k > 0 and A[j, k-1] == ALIVE:
                num += 1
            if k < c-1 and A[j, k+1] == ALIVE:
                num += 1
            if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
                num += 1
            if j < r-1 and A[j+1, k] == ALIVE:
                num += 1
            if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
                num += 1
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""
def next_state2(A, r, c):
  N = np.zeros((r,c), dtype=np.int8)
  changed = False
  for j in range(r):
    for k in range(c):
      num = num_nbrs2(A,j,k,r,c)
      if A[j,k] == ALIVE: 
        if num > 1 and num < 4: 
          N[j,k] = ALIVE
        else:
          N[j,k] = DEAD 
          changed = True
      else:               
        if num == 3:
          N[j,k] = ALIVE
          changed = True
        else:
          N[j,k] = DEAD
  return N, changed

#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""
"""
1 2 3 4
5 6 7 8
9 1 2 3
"""
def num_nbrs2(A,j,k,r,c):
  num = 0
  numtop = 0
  numbot = 0
  B = np.zeros((r,c), dtype=np.int8)
  B[j,k] = 2
  if j==0:
    
    if j==0 and k>0 and A[r-1, k-1] == ALIVE:
      B[r-1, k-1] = 1
      num += 1 #at top row, left
    if j==0 and A[r-1, k] == ALIVE:
      B[r-1, k] = 1
      num += 1 #at top row, middle
    if j==0 and k<c-1 and A[r-1, k+1] == ALIVE:
      B[r-1, k+1] = 1
      num += 1 #at top row, right
    
  if j==r-1:
    
    if j==r-1 and k>0 and A[0, k-1] == ALIVE:
      B[0, k-1] = 1
      num += 1 #at bottom row , left  
    if j==r-1 and A[0, k] == ALIVE:
      B[0, k] = 1
      num += 1 #at bottom row, middle
    if j==r-1 and k<c-1 and A[0, k+1] == ALIVE:
      B[0, k+1] = 1
      num += 1 #at bottom row , right
    
  
  if j>0   and k>0   and A[j-1, k-1] == ALIVE:
    B[j-1, k-1] = 1
    num += 1
  if j>0             and A[j-1, k  ] == ALIVE:
    B[j-1, k] = 1
    num += 1
  if j>0   and k<c-1 and A[j-1, k+1] == ALIVE:
    B[j-1, k+1] = 1
    num += 1
  if           k>0   and A[j  , k-1] == ALIVE:
    B[j  , k-1] = 1
    num += 1
  if           k<c-1 and A[j  , k+1] == ALIVE:
    B[j  , k+1] = 1
    num += 1
  if j<r-1 and k>0   and A[j+1, k-1] == ALIVE:
    B[j+1, k-1] = 1
    num += 1
  if j<r-1           and A[j+1, k  ] == ALIVE:
    B[j+1, k ] = 1
    num += 1
  if j<r-1 and k<c-1 and A[j+1, k+1] == ALIVE:
    B[j+1, k+1] = 1
    num += 1

  return num
#############################################


#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""
def next_state_torus(A, r, c):
  N = np.zeros((r,c), dtype=np.int8)
  changed = False
  for j in range(r):
    for k in range(c):
      num = num_nbrs_torus(A,j,k,r,c)
      if A[j,k] == ALIVE: 
        if num > 1 and num < 4: 
          N[j,k] = ALIVE
        else:
          N[j,k] = DEAD 
          changed = True
      else:               
        if num == 3:
          N[j,k] = ALIVE
          changed = True
        else:
          N[j,k] = DEAD
  return N, changed
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""
def num_nbrs_torus(A,j,k,r,c):
  num = 0
  numtop = 0
  numbot = 0
  B = np.zeros((r,c), dtype=np.int8)
  B[j,k] = 2
  
  if j==0:
    if j==0 and k>0 and A[r-1, k-1] == ALIVE:
      B[r-1, k-1] = 1
      num += 1 #at top row, left
    if j==0 and A[r-1, k] == ALIVE:
      B[r-1, k] = 1
      num += 1 #at top row, middle
    if j==0 and k<c-1 and A[r-1, k+1] == ALIVE:
      B[r-1, k+1] = 1
      num += 1 #at top row, right
    
  if j==r-1:
    if j==r-1 and k>0 and A[0, k-1] == ALIVE:
      B[0, k-1] = 1
      num += 1 #at bottom row , left  
    if j==r-1 and A[0, k] == ALIVE:
      B[0, k] = 1
      num += 1 #at bottom row, middle
    if j==r-1 and k<c-1 and A[0, k+1] == ALIVE:
      B[0, k+1] = 1
      num += 1 #at bottom row , right

  if k==0:
    if j>0 and k==0 and A[j-1, c-1] == ALIVE:
      B[j-1, c-1] = 1
      num += 1 #at left col, top
    if k==0 and A[j, c-1] == ALIVE:
      B[j, c-1] = 1
      num += 1 #at left col, middle
    if j<r-1 and k==0 and A[j+1, c-1] == ALIVE:
      B[j+1, c-1] = 1
      num += 1 #at left col, bottom
    
  if k==c-1:
    if j>0 and k==c-1 and A[j-1, 0] == ALIVE:
      B[j-1, 0] = 1
      num += 1 #at right col, top
    if k==c-1 and A[j, 0] == ALIVE:
      B[j, 0] = 1
      num += 1 #at right col, middle
    if j<r-1 and k==c-1 and A[j+1, 0] == ALIVE:
      B[j+1, 0] = 1
      num += 1 #at right col, bottom

  if j==0 and k==0 and A[r-1, c-1] == ALIVE:
      B[r-1, c-1] = 1
      num += 1 #at top left, opposite corner

  if j==0 and k==c-1 and A[r-1, 0] == ALIVE:
      B[r-1, 0] = 1
      num += 1 #at top right, opposite corner

  if j==r-1 and k==0 and A[0, c-1] == ALIVE:
      B[0, c-1] = 1
      num += 1 #at bottom left, opposite corner

  if j==r-1 and k==c-1 and A[0, 0] == ALIVE:
      B[0, 0] = 1
      num += 1 #at bottom right, opposite corner
  
    
  
  if j>0   and k>0   and A[j-1, k-1] == ALIVE:
    B[j-1, k-1] = 1
    num += 1
  if j>0             and A[j-1, k  ] == ALIVE:
    B[j-1, k] = 1
    num += 1
  if j>0   and k<c-1 and A[j-1, k+1] == ALIVE:
    B[j-1, k+1] = 1
    num += 1
  if           k>0   and A[j  , k-1] == ALIVE:
    B[j  , k-1] = 1
    num += 1
  if           k<c-1 and A[j  , k+1] == ALIVE:
    B[j  , k+1] = 1
    num += 1
  if j<r-1 and k>0   and A[j+1, k-1] == ALIVE:
    B[j+1, k-1] = 1
    num += 1
  if j<r-1           and A[j+1, k  ] == ALIVE:
    B[j+1, k ] = 1
    num += 1
  if j<r-1 and k<c-1 and A[j+1, k+1] == ALIVE:
    B[j+1, k+1] = 1
    num += 1

  return num
#############################################


"""
input, output
"""

pause = 0

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
  itn = 0
  B, r, c = get_board()
  print(B, r, c)
  X = convert_board(B,r,c)
  A,r,c = expand_grid(X,r,c,0)
  print_array(A,r,c)
  print("Before any itteration")
  while itn <= max_itn:
    sleep(pause)
    newA, delta = next_state_torus(A, r, c)
    if not delta:  break
    itn += 1
    A = newA
    print_array(A, r, c)
    print('\niterations', itn)


def main():
    interact(192)

if __name__ == '__main__':
    main()
