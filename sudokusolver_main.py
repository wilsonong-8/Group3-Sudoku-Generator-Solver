from sudokugenerator import *
import sudokugenerator_easy
import sudokugenerator_hard
from pprint import pprint
import csv
import time
import pickle


empty_squares = 0
valid_num_placed = 0
num_of_backtrack = 0
num_of_guess = 0


def find_next_blank(blank):
    # finds the next row, col on the puzzle that's not filled
    # return row, col  if there is none

    for r in range(9):
        for c in range(9):
            if blank[r][c] == -1:
                return r, c

    return None, None


def is_valid(blank, guess, row, col):
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


def solve_puzzle(blank):
    global empty_squares
    global valid_num_placed, num_of_backtrack, num_of_guess

    # solve sudoku using backtracking technique

    # step 1: choose a blank on the puzzle and make a guess
    row, col = find_next_blank(blank)

    # If there's no empty blank left, returns True
    if row is None:
        return True

        # step 2: If found blank, then make a guess between 1 and 9
    for guess in range(1, 10):
        # step 3: check if it is a valid guess
        num_of_guess += 1

        if is_valid(blank, guess, row, col):
            # step 3.1: if this is a valid guess, then place number into the list
            blank[row][col] = guess
            valid_num_placed += 1

            # step 4: recursively calls the solver
            if solve_puzzle(blank):
                empty_squares += 1
                return True

        # step 5: if not valid or not True, then backtrack and try a new number
        blank[row][col] = -1
        num_of_backtrack += 1

    # step 6: if none of the numbers work, puzzle is unsolvable - returns False
    return False




if __name__ == '__main__':

    with open('introduction.txt') as f:
        contents = f.read()
        print(contents)
        print()
    while True:
        question_board = generateBoard()
        input("---Press Enter to run the Auto Solver---")
        print()
        print("===================================================================")
        print("Solution by Solver:")
        start = time.time()
        solve_puzzle(question_board)
        end = time.time()
        pprint(question_board)
        print()
        time_taken = round((end - start) * 10000000)
        print(f"Time taken: {time_taken} ns")
        print(f"Valid number placed in cell = {valid_num_placed}")
        print(f"Number of backtracks = {num_of_backtrack}")
        print(f"Number of guesses made = {num_of_guess}")
        print()
        print(f"For {empty_squares} empty Blanks in the puzzle")

        with open('statistics.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            with open('statistics.csv', 'a') as f:
                writer = csv.writer(f, delimiter=',')
                data = [[empty_squares], [time_taken], [valid_num_placed], [num_of_backtrack], [num_of_guess]]
                writer.writerow(data)

        if num_of_backtrack > 3000:
            print(f"The Difficulty Level of {num_of_backtrack} is very High. Suggest decreasing the difficulty. ")
        elif num_of_backtrack > 1500:
            print(f"The Difficulty Level of {num_of_backtrack} slightly High. Suggest decreasing the difficulty. ")
        elif num_of_backtrack > 300:
            print(f"The Difficulty Level of {num_of_backtrack} slightly Low. Suggest increasing the difficulty. ")
        else:
            print(f"The Difficulty Level of {num_of_backtrack} very Low. Suggest increasing the difficulty. ")
        print("===================================================================\n")

        answer2 = str(input('Enter (a)Easier / (b)Harder to Generate a different set of Puzzle or any key to Pass: \n'))
        if answer2 =='a':

            outfile = open('empties.txt', 'wb')
            pickle.dump(int(empty_squares), outfile)
            outfile.close()

            outfile_1 = open('backtrack_num.txt', 'wb')
            pickle.dump(int(num_of_backtrack), outfile_1)
            outfile_1.close()
            print("===================================================================")
            sudokugenerator_easy.generateBoard_easy()

        elif answer2 =='b':

            outfile = open('empties.txt', 'wb')
            pickle.dump(int(empty_squares), outfile)
            outfile.close()

            outfile_1 = open('backtrack_num.txt', 'wb')
            pickle.dump(int(num_of_backtrack), outfile_1)
            outfile_1.close()
            print("===================================================================")
            sudokugenerator_hard.generateBoard_hard()

        elif answer2 == 'c':
            break


        while True:
            print("=====================================================================")
            answer = str(input('Do you want to RERUN the entire PROGRAM again? (y/n): '))
            if answer in ('y', 'n'):
                break
            print("invalid input.")
        if answer == 'y':
            empty_squares = 0
            valid_num_placed = 0
            num_of_backtrack = 0
            num_of_guess = 0
            print("\n\n")
            continue
        else:
            print("\nThank you for using our Sudoku Program. Goodbye!")
            break


