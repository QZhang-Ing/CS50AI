import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation, handles the game plays
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else: 
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            


class MinesweeperAI():
    """
    Minesweeper game player, handles the logic and choose actions
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell) 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell) 

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # step1
        self.moves_made.add(cell)
        # step2
        self.mark_safe(cell)

        # step3
        # loop over 8 cells around cell to set up a set (sentence)
        i, j = cell
        new_sentence = set()
        for row in range(max(0, i - 1), min(i + 2, self.height)):
            for col in range(max(0, j - 1), min(j + 2, self.width)):
                if (row, col) != (i, j):
                    new_sentence.add((row, col))
        self.knowledge.append(Sentence(new_sentence, count))

        # step4
        self.check_upgrade()

        # step5
        # Loop over knowledge to check if:
        #    set1 = count1 and set2 = count2 where one is the subset of 
        #    the other. then a new sentence can be added to knowledge
        new_knowledge = []
        empty_knowledge = []
        # Loop over to find all new sentences and find all empty sentences
        for s1 in self.knowledge:
            if len(s1.cells) == 0:
                empty_knowledge.append(s1)
                continue
            for s2 in self.knowledge:
                if len(s2.cells) == 0:
                    empty_knowledge.append(s2)
                    continue
                if s1 == s2:
                    continue
                elif s1.cells.issubset(s2.cells):
                    cells = s2.cells - s1.cells
                    new_s = Sentence(cells, s2.count - s1.count)
                    if not new_s in self.knowledge:
                        new_knowledge.append(new_s)   
        # remove sublist(empty_knowledge) from self.knowledge
        self.knowledge = [x for x in self.knowledge if x not in empty_knowledge]
        # add new_knowledge to self.knowledge
        if len(new_knowledge) != 0:
            for sentence in new_knowledge:
                self.knowledge.append(sentence)
        '''
        Check and upgrade
        '''
        self.check_upgrade()



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
        else:
            for cell in self.safes:
                if (not cell in self.moves_made) and (not cell in self.mines):
                    return cell
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        '''
        Recursion approach
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width - 1)
        random_move = (i,j)
        if (not random_move in self.moves_made) and (not random_move in self.mines):
            return random_move
        else:
            self.make_random_move()
        '''
        # Generate random list for indexing
        random_row = list(range(self.height))
        random_col = list(range(self.width))
        random.shuffle(random_row)
        random.shuffle(random_col)
        
        for i in random_row:
            for j in random_col:
                random_move = (i, j)
                if (not random_move in self.moves_made) and (not random_move in self.mines):
                    return random_move
        return None

    def check_upgrade(self):
        for sentence in self.knowledge:
            mines = sentence.known_mines()
            safes = sentence.known_safes()
            # if known_mines returns non empty set()
            if len(mines) != 0:
                copie_mines = copy.deepcopy(mines)
                for cell in copie_mines:
                    self.mark_mine(cell)
            # if known_safes returns non empty set()
            if len(safes) != 0:
                copie_safes = copy.deepcopy(safes)
                for cell in copie_safes:
                    self.mark_safe(cell)
        
        copie_marksafe = copy.deepcopy(self.safes)
        for cell in copie_marksafe:
            self.mark_safe(cell)
        copie_markmines = copy.deepcopy(self.mines)
        for cell in copie_markmines:
            self.mark_mine(cell)
