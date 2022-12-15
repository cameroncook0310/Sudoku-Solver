import tkinter as tk

# Helper function to check if the users starting puzzle input is a legal puzzle
def legal_puzzle(start_matrix):
    row_map = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    col_map = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    subgrid_map = {(0,0):[], (0,1):[], (0,2):[], (1,0):[], (1,1):[], (1,2):[], (2,0):[], (2,1):[], (2,2):[]}
    for row_index in range(9):
        for col_index in range(9):
            subgrid = (((row_index) - (row_index) % 3) / 3, ((col_index) - (col_index) % 3) / 3)
            if start_matrix[row_index][col_index] not in range(10):
                return False
            elif start_matrix[row_index][col_index] not in row_map[row_index] and start_matrix[row_index][col_index] not in col_map[col_index] and start_matrix[row_index][col_index] not in subgrid_map[subgrid]:
                if start_matrix[row_index][col_index]:
                    row_map[row_index].append(start_matrix[row_index][col_index])
                    col_map[col_index].append(start_matrix[row_index][col_index])
                    subgrid_map[((row_index - row_index % 3) / 3, (col_index - col_index % 3) / 3)].append(start_matrix[row_index][col_index])
            else:
                return False
    return True

# Class for creating the gui
class SudokuGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sudoku Solver')
        self.root.resizable(width = False, height='False')
        self.num_entry_frame = tk.Frame(self.root)
        self.num_entry_frame.pack()
        self.entries_list = []
        for i in range(9):
            for j in range(9):
                self.numEntry = tk.Entry(self.num_entry_frame, width=5, justify='center')
                if (j+1) % 3 == 0 and j != 8:
                    self.numEntry.grid(row=i, column=j, ipady=10, padx=(0,6))
                if (i+1) % 3 == 0 and i != 8:
                    self.numEntry.grid(row=i, column=j, ipady=10, pady=(0,6))
                else:       
                    self.numEntry.grid(row=i, column=j, ipady=10)
                self.entries_list.append(self.numEntry)
        self.start_button = tk.Button(self.root, text='Solve!', command=self.run_solver)
        self.text_lable = tk.Label(self.root, text='Enter starting numbers for puzzle')
        self.start_button.pack()
        self.text_lable.pack()
    
    # Takes the starting numbers of the puzzle from the gui and solves the puzzle
    def run_solver(self):
        starting_board = [[] for i in range(9)]
        iCount = 0
        for i in range(9):
            for j in range(9):
                if self.entries_list[iCount].get():
                    starting_board[i].append(int(self.entries_list[iCount].get()))
                else:
                    starting_board[i].append(0)
                iCount += 1 
        if legal_puzzle(starting_board):
            sudoku = Sudoku(starting_board)
            sudoku.solve_sudoku()
            for i in range(9):
                for j in range(9):
                    self.numEntry = tk.Entry(self.num_entry_frame, width=2, justify='center')
                    self.numEntry.insert(0, str(starting_board[i][j]))
                    self.numEntry.grid(row=i, column=j)
            self.text_lable.config(text= 'Solved!')
        else:
            self.text_lable.config(text = 'Invalid puzzle')

    # Starts the gui
    def run_gui(self):
        self.root.mainloop()


# Class takes starting numbers for puzzle and solves the puzzle
class Sudoku:
    def __init__(self, sudoku_matrix):
        self.__sudoku_matrix = sudoku_matrix
        self.__row_map = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
        self.__col_map = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
        self.__subgrid_map = {(0,0):[], (0,1):[], (0,2):[], (1,0):[], (1,1):[], (1,2):[], (2,0):[], (2,1):[], (2,2):[]}
        self.setup_maps()


    def get_sudoku_matrix(self):
        return self.__sudoku_matrix

    # Not done yet
    def set_sudoku_matrix(self, new_matrix):
        self.__sudoku_matrix = new_matrix

    # Sets up the hashmaps to keep track of what spaces are already taken with what numbers 
    def setup_maps(self):
        for row_index in range(9):
            for col_index in range(9):
                if self.__sudoku_matrix[row_index][col_index] != 0:
                    self.__row_map[row_index].append(self.__sudoku_matrix[row_index][col_index])
                    self.__col_map[col_index].append(self.__sudoku_matrix[row_index][col_index])
                    self.__subgrid_map[((row_index - row_index % 3) / 3, (col_index - col_index % 3) / 3)].append(self.__sudoku_matrix[row_index][col_index])
   
    # Looks for next empty space in the game matrix
    def next_space(self, curr_row, curr_col):   
        for row in range(9):
            for col in range(9):
                if self.__sudoku_matrix[row][col] == 0:
                    # Returns next empty space if there is one
                    return (row, col)
        # Returns false is there are no more empty spaces
        return False 

    # Checks row column and subgrid hash maps at the given row and column to see if the current number can legaly be placed there 
    def check_legality(self, row, col, curr_num):
        subgrid = ((row - row % 3) / 3, (col - col % 3) / 3)
        if curr_num not in self.__row_map[row] and curr_num not in self.__col_map[col] and curr_num not in self.__subgrid_map[subgrid]:
            self.__row_map[row].append(curr_num)
            self.__col_map[col].append(curr_num)
            self.__subgrid_map[subgrid].append(curr_num)
            return True
        return False

    # Uses backtracking to solve any legal sudoku matrix
    def solve_sudoku(self, start_row = 0, start_col = 0):
        # If there are no more spaces to fill, then the solution has been found and the solved matrix is returned
        if not self.next_space(start_row, start_col):
            return True 
        # Sets the current row and column to be the next empty space 
        r, c = self.next_space(start_row, start_col)
        for num in range(1, 10):
            # If the number is legal at that space, it temporarily is put in the space and sees if the matrix can be solved
            if self.check_legality(r, c, num):
                self.__sudoku_matrix[r][c] = num
                if not self.next_space(r, c):
                    return True
                next_r, next_c = self.next_space(r, c)
                # Continues to try and solve the matrix given how it is currently filled
                if self.solve_sudoku(next_r, next_c):
                    return True
                # Resets space and hash maps if path fails 
                self.__row_map[r].remove(num)
                self.__col_map[c].remove(num)
                self.__subgrid_map[((r - r % 3) / 3, (c - c % 3) / 3)].remove(num)
                self.__sudoku_matrix[r][c] = 0
        
        # Backtracks to last recursion instance where num has not yet gone past 9
        return False
        
        
# Driver run the program
def main():
    gui = SudokuGui()
    gui.run_gui()

main()





