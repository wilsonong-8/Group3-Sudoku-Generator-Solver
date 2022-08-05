import sudokugenerator_easy
import pickle

num_of_backtrack_1 = 0

def generateBoard_hard():

    def find_next_blank_1(blank):
        # finds the next row, col on the puzzle that's not filled
        # return row, col  if there is none

        for r in range(9):
            for c in range(9):
                if blank[r][c] == -1:
                    return r, c

        return None, None

    def is_valid_1(blank, guess, row, col):
        # finds out whether the guess at the row/col of the puzzle is a valid guess

        row_vals = blank[row]
        if guess in row_vals:
            return False

        col_vals = [blank[i][col] for i in range(9)]
        if guess in col_vals:
            return False

        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if blank[r][c] == guess:
                    return False

        return True

    def solve_puzzle_1(blank):
        global num_of_backtrack_1

        # step 1: choose a blank on the puzzle and make a guess
        row, col = find_next_blank_1(blank)

        # If there's no empty blank left, returns True
        if row is None:
            return True

            # step 2: If found blank, then make a guess between 1 and 9
        for guess in range(1, 10):
            # step 3: check if it is a valid guess
            if is_valid_1(blank, guess, row, col):
                # step 3.1: if this is a valid guess, then place number into the list
                blank[row][col] = guess

                # step 4: recursively calls the solver
                if solve_puzzle_1(blank):
                    # empty_squares += 1
                    return True

            # step 5: if not valid or not True, then backtrack and try a new number
            blank[row][col] = -1
            num_of_backtrack_1 += 1
        # step 6: if none of the numbers work, puzzle is unsolvable - returns False
        return False

    global num_of_backtrack_1

    while True:
        import sudokusolver_main
        infile = open('empties.txt', 'rb')
        empties = int(pickle.load(infile))
        infile.close

        def pattern(r,c): return (3*(r%3)+r//3+c)%9

        from random import sample
        def shuffle(s): return sample(s,len(s))
        rBase = range(3)
        rows  = [ g*3 + r for g in shuffle(rBase) for r in shuffle(rBase) ]
        cols  = [ g*3 + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,3*3+1))

        board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

        with open('puzzle.txt', 'w') as f:
            for line in board: f.write(f"{line}\n")

        new_board = []
        squares = 9*9
        empties = empties
        for p in sample(range(squares),empties):
            board[p // 9][p % 9] = 0

        numSize = len(str(9))
        for line in board:
            # print(*(f"{n or '.':{numSize}} " for n in line))
            for i in line:
                new_board.append(i)

        for i in range(len(new_board)):
            if new_board[i] == 0:
                new_board[i] = -1

        def divide_chunks_1(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        x = list(divide_chunks_1(new_board, 9))

        solve_puzzle_1(x)

        infile_1 = open('backtrack_num.txt', 'rb')
        backtrack_stat = int(pickle.load(infile_1))
        infile_1.close

        # print(f"Original difficulty: {backtrack_stat}")
        backtrack_stat_final = int(backtrack_stat*1.5)

        # print(f"Run = {num_of_backtrack_1}")
        if num_of_backtrack_1 < backtrack_stat_final:                   #I WANT MORE DIFFICULT FUNCTION
            num_of_backtrack_1 = 0
            continue
        else:
            break


    print("Sudoku Board with Answers:")
    print("----------------------------")
    with open('puzzle.txt') as f:
        new_puzzle = f.read()
        print(new_puzzle)
    print("----------------------------")

    print(f"Sudoku Board with {empties} Blanks:")
    print("---------------------------")
    numSize = len(str(9))
    for line in board:
        print(*(f"{n or '.':{numSize}} " for n in line))
        for i in line:
            new_board.append(i)

        for i in range(len(new_board)):
            if new_board[i] == 0:
                new_board[i] = -1

        def divide_chunks_1(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        x = list(divide_chunks_1(new_board, 9))

    print("---------------------------\n")
    print("=====================================================================")
    print("GENERATING A HARDER PUZZLE")
    print(f"Number of Blanks: {empties}")
    print(f"Original difficulty: {backtrack_stat}")
    print(f"New Difficulty: {num_of_backtrack_1}")
    print("=====================================================================\n")

    outfile_1 = open('backtrack_num.txt', 'wb')
    pickle.dump(int(num_of_backtrack_1), outfile_1)
    outfile_1.close()


    answer3 = str(input('Enter (a)Easier / (b)Harder to Generate a different set of Puzzle or any key to Pass: \n'))
    if answer3 == 'a':
        print("===================================================================")
        sudokugenerator_easy.generateBoard_easy()
    elif answer3 == 'b':
        print("===================================================================")
        generateBoard_hard()
    else:
        return x
