import random
import string

def generate_random_grid(size):
    """Generates a random NxN grid of uppercase letters."""
    return [[random.choice(string.ascii_uppercase) for _ in range(size)] for _ in range(size)]

# --- YOUR CODE BELOW ---
class Boggle:
    def __init__(self, grid, dictionary):
        self.grid =[]
        self.dictionary = dictionary
        self.solutions = []

        self.setGrid(grid)
        self.setDictionary(dictionary)

    def setDictionary(self, dictionary):
        if not dictionary or not isinstance(dictionary, list):
            self.dictionary = []
            return
        for w in dictionary:
            if not isinstance(w, str):
                self.dictionary = []
                return
        self.dictionary = dictionary
      
    def setGrid(self, grid):
        if not grid or not isinstance(grid,list):
          self.grid = []
          return 

        for row in grid:
          if not isinstance(row, list) or len(row)!= len(grid):
            self.grid = []
            return 
          
          for cell in row:
            if not isinstance(cell, str):
              self.grid = []
              return 
        self.grid = grid
        size = len(self.grid)
        for r in range(size):
            for c in range(size):
                self.grid[r][c] = self.grid[r][c].upper()
    
    def getSolution(self):
        self.solutions = []
        if not self.grid or not self.dictionary:
          return []
        rows = len(self.grid)
        cols = len(self.grid[0])

        for word in self.dictionary:
          word = word.upper()
          if len(word)<3:
            continue
          
          visited  = [[False]* cols for _ in range(rows)]

          if self._exists(word, visited):
            self.solutions.append(word)
        
        return self.solutions
    
    def _exists(self, word, visited):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                fresh_visited = [row[:] for row in visited]
                if self._dfs(r, c, word, 0, fresh_visited):
                    return True
        return False
    
    def _dfs(self, r,c, word, index, visited):
      if index ==len(word):
        return True
      if r<0 or r>=len(self.grid) or c<0 or c>= len(self.grid[0]) or visited[r][c]:
        return False
      cell = self.grid[r][c]
      if not word.startswith(cell, index):
        return False

      visited[r][c] = True
      next_index = index+ len(cell)

      for dr in [-1, 0, 1]:
        for dc in [-1,0, 1]:
          if dr!=0 or dc!= 0:
            if self._dfs(r + dr, c + dc, word, next_index, visited):
              visited[r][c]= False
              return True

      visited[r][c]= False
      return False