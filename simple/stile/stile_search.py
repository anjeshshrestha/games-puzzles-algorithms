# simple bfs program to solve sliding tile
from collections import deque
#from random import shuffle
from time import sleep, time
from sys import stdin
from copy import deepcopy
import itertools
import threading
lock = threading.RLock()
import concurrent.futures
from tqdm import tqdm
from multiprocess import Pool

def int2chr(t): # nonneg int to single in '0123456789ABCDEFGHIJ...'
  if t <= 9: return chr(t+ord('0'))
  else:      return chr(t-10 + ord('A'))

def chr2int(c): # chr in '0123456789ABCDEFGHIJ...' to int
  if c in '0123456789': return ord(c) - ord('0')
  else: return 10 + ord(c) - ord('A')

def list2str(L): # list nonneg ints to string monochars
  s = ''
  for x in L: s += int2chr(x)
  return s

def pretty(s,cols,monochar): # string to printable matrix
  # if monochar true: print elements as monochars 
  # else:             print elements as ints
  count, outstr, BLANK = 0, '', ' '
  for x in s:
    count += 1
    if monochar:  
      if x == '0': outstr += ' ' + BLANK
      else:        outstr += ' ' + x
    else:
      if   x == '0':          outstr += '  ' + BLANK     # blank
      elif x in ' 123456789': outstr += '  ' + x         # digit
      else:                   outstr += ' ' + str(chr2int(x))   # 2 digits
    if count%cols == 0: outstr += '\n'
  #sleep(.005)
  return outstr

def str_swap(s,lcn,shift): # swap chars at s[lcn], s[lcn+shift]
  a , b = min(lcn,lcn+shift), max(lcn,lcn+shift)
  return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

class Tile:
  """a sliding tile class with simple search"""

  def __init__(self, state, row, col):
    # state will be the starting state of any computer search
    # initialized from stdin, 0 is blank, 
    # format: r c then tile entries, row by row, e.g.:
    # 2 3
    # 2 0 5
    # 4 1 3
    self.state = state
    self.rows, self.cols = row, col
    self.moves = 0
    
    #for line in stdin:
    #  for elem in line.split():
    #    self.state.append(int(elem))
        
    # rows, cols are 1st 2 elements of list, so pop them
    #self.rows, self.cols = self.state.pop(0), self.state.pop(0)
    # state now holds contents of tile in row-major order
    
    # assert 
    #   - at least 2 rows, at least 2 cols, 
    #   - all entries in [0 .. r*c-1], and
    #   - some entry 0
    assert(self.rows>=2 and self.cols>=2)
    for s in self.state: assert(s>=0 and s < self.rows*self.cols)
    ndx_min = self.state.index(min(self.state))
    assert(self.state[ndx_min] == 0)

    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.cols, self.cols
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down

  def legal_shifts(self,psn): # list of legal shifts
    S = []
    c,r = psn % self.cols, psn // self.cols # column number, row number
    if c > 0:           S.append(self.LF)
    if c < self.cols-1: S.append(self.RT)
    if r > 0:           S.append(self.UP)
    if r < self.rows-1: S.append(self.DN)
    return S
  
  def inversions(self):
    count, L, n = 0, self.state, len(self.state)
    for x in range(n-1):
      for y in range(x+1,n):
        if L[x] != 0 and L[y] != 0 and L[x] > L[y] : count += 1
    return count
  
  def slide(self,shift):
    # slide a tile   shift is from blank's perspective
    b_dx = self.state.index(0) # index of blank
    o_dx = b_dx + shift        # index of other tile
    self.state[b_dx], self.state[o_dx] = self.state[o_dx], self.state[b_dx]
  
  def bfs(self):
    def report(i, d, L, s):
      print(i,'iterations',s,'seconds',i/s,'itn/s')
      print(len(d), 'states')
      print('nodes by level')
      for j in range(len(L)):  print(j, L[j])
      print('')
      
    def targetlist(n): # return target state, as list
      L = []
      for j in range(1,n): L.append(j)
      L.append(0)
      return L
    
    start  = list2str(self.state)
    target = list2str(targetlist(self.rows*self.cols))
    # use a parent dictionary to
    #   - track seen states (all are in dictionary)
    #   - record parents, to recover solution transition sequence
    Parent = { start : start} 
    Fringe = deque() # the sliding tile states, as strings, we encounter
    Fringe.append(start)
    iteration, nodes_this_level, Levels = 0, 1, [1]
    start_time = time()
    while len(Fringe) > 0:
      iteration +=1
      stst = Fringe.popleft() # popleft() and append() give FIFO
      #print(pretty(stst, self.cols, True))
      ndx0 = stst.index('0')
      for shift in self.legal_shifts(ndx0):
        nbr = str_swap(stst,ndx0,shift)
        if nbr == target: 
          print('found target')
          countxx= 0
          while True:  # show the sequence, backwards
            #sleep(.5)
            print(pretty(stst, self.cols, True))
            p = Parent[stst]
            countxx += 1
            if p == stst:
              print("count = ", countxx)
              end_time = time()
              report(iteration, Parent, Levels, end_time-start_time)
              return
            stst = p
        elif nbr not in Parent: #only add from:to state that have not been explored yet, to avoid duplicate from states, in order to prevent a cycle, example going up, down, up ...
        #else:
          Parent[nbr] = stst
          Fringe.append(nbr)
          #print(Parent)
      nodes_this_level -= 1
      if nodes_this_level == 0:
        nodes_this_level = len(Fringe)
        Levels.append(nodes_this_level)
        print(' ',iteration,'iterations, level',len(Levels),'has',nodes_this_level,'nodes')
        #sleep(10)
    print('\nno solution found')
    end_time = time()
    #report(iteration, Parent, Levels, end_time-start_time)
  def bfs_allcheck(self):
    start  = list2str(self.state)
    target = '123456780'
    if start == target:
      return
    # use a parent dictionary to
    #   - track seen states (all are in dictionary)
    #   - record parents, to recover solution transition sequence
    Parent = { start : start} 
    Fringe = deque() # the sliding tile states, as strings, we encounter
    Fringe.append(start)
    iteration, nodes_this_level, Levels = 0, 1, [1]
    start_time = time()
    while len(Fringe) > 0:
      iteration +=1
      stst = Fringe.popleft() # popleft() and append() give FIFO
      #print(pretty(stst, self.cols, True))
      ndx0 = stst.index('0')
      for shift in self.legal_shifts(ndx0):
        nbr = str_swap(stst,ndx0,shift)
        if nbr == target: 
          countxx = 0
          while True:  # show the sequence, backwards
            #sleep(.5)
            p = Parent[stst]
            countxx += 1
            if p == stst:
              self.moves = countxx
              return
            stst = p
        elif nbr not in Parent: #only add from:to state that have not been explored yet, to avoid duplicate from states, in order to prevent a cycle, example going up, down, up ...
          Parent[nbr] = stst
          Fringe.append(nbr)
      nodes_this_level -= 1
      if nodes_this_level == 0:
        nodes_this_level = len(Fringe)
        Levels.append(nodes_this_level)
        #print(' ',iteration,'iterations, level',len(Levels),'has',nodes_this_level,'nodes')
        #sleep(10)
    self.moves = -1
    return
  def is_solvable(self):
    grid_odd = self.cols % 2 != 0
    inversions_even = self.inversions() % 2 == 0
    return (grid_odd and inversions_even)

def checker(random_list):
  temp = Tile(random_list,3,3)
  if temp.is_solvable():
    temp.bfs_allcheck()
    return temp.moves
  return -1


state = [3,2,6,4,7,5,8,1,0]
t = Tile(state,3,3)
print(t.inversions())
def main():
  state = [0,1,2,3,4,5,6,7,8]
  moves = 0
  count_solve = 0
  count = 0
  list_of_works = list(itertools.permutations(state)) #permuations of all possible board postions
  print(len(list_of_works)) #number of combinations
  print("working")
  starttime1 = time()
  everytime_reset = starttime1

  with Pool(processes=12) as pool: #run in multi process to speedup work
    for i in pool.imap_unordered(checker,list_of_works): #call checker for each board combination
      count += 1 #counter 
      if count % 1000 == 0:
        new_time = time()
        subsettime = new_time-everytime_reset
        totalTime = new_time-starttime1
        everytime_reset = new_time
        print(count, "Took this long for 1000:", subsettime, "TotalTime so far", totalTime) #to check progress
      if i >= 0: #if there is a solution will return number of moves, else return -1
        count_solve += 1 #count solvable moves
        moves += i #count the number of moves
  subsettime = new_time-everytime_reset
  totalTime = new_time-starttime1
  everytime_reset = new_time
  print(count, "Took this long for 1000:", subsettime, "TotalTime so far", totalTime)
  print("done")
  print("Total Perms", count) 
  print("Total Solvable", count_solve)
  print("Average moves", moves/count_solve) #print averages
  input()
