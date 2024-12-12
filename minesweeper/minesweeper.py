import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
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

        if len(self.cells) < self.count:
            return "Error"

        if len(self.cells) == self.count and self.count != 0:
            print('Mine Identified')
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
        try:
            self.cells.remove(cell)
            self.count -= 1
        except:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        except:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
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

        # List of all cells
        self.cells = []
        for i in range(height):
            for j in range(width):
                self.cells.append((i,j))

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
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        neighbors = set()
        for i in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2)):
                if (i, j) == cell:
                    continue
                elif (i, j) in self.mines:
                    count -= 1
                elif (i, j) not in self.safes and (i, j) not in self.mines:
                    neighbors.add((i, j))
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        self.update_subsets()
        # 4)
        self.update_knowledge_base()
        # 5)
        self.update_subsets()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        cell = None
        for safe in self.safes:
            if safe not in self.moves_made:
                cell = safe
                break
        return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for cell in self.cells:
            if cell not in self.mines and cell not in self.moves_made:
                return cell

    def update_knowledge_base(self):
        original_knowledge = list(self.knowledge)
        for sentence in original_knowledge:
            if sentence.count == 0:
                for cell in list(sentence.cells):
                    self.mark_safe(cell)
            if len(sentence.cells) == sentence.count:
                for cell in list(sentence.cells):
                    self.mark_mine(cell)
        # Optionally, clean up redundant or empty sentences
        self.knowledge = [s for s in self.knowledge if s.cells and s.count >= 0]

    def update_subsets(self):
        original_knowledge = list(self.knowledge)
        n = len(original_knowledge)
        for i in range(n):
            for j in range(i + 1, n):
                if original_knowledge[i].cells.issubset(original_knowledge[j].cells):
                    difference_cells = original_knowledge[j].cells - original_knowledge[i].cells
                    difference_count = original_knowledge[j].count - original_knowledge[i].count
                    if difference_cells:
                        inferred_sentence = Sentence(difference_cells, difference_count)
                        self.knowledge.append(inferred_sentence)
                elif original_knowledge[j].cells.issubset(original_knowledge[i].cells):
                    difference_cells = original_knowledge[i].cells - original_knowledge[j].cells
                    difference_count = original_knowledge[i].count - original_knowledge[j].count
                    if difference_cells:
                        inferred_sentence = Sentence(difference_cells, difference_count)
                        self.knowledge.append(inferred_sentence)
        self.update_knowledge_base()


