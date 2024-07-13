class TicTacToeBoard:
  def __init__(self) -> None:
    self.grid = [[None for _ in range(3)] for _ in range(3)]

  def __str__(self) -> str:
    return '\n'.join(' '.join(str("_" if x is None else x) for x in row) for row in self.grid)

  def make_move(self, player: str, row: int, col: int) -> bool:
    if self.grid[row][col] is not None:
      return False
    self.grid[row][col] = player[0]
    return True

  def has_won(self, player: str) -> bool:
    player_initial = player[0]
    if any(all(x == player_initial for x in row) for row in self.grid):
      return True
    for col in range(3):
      if all(self.grid[r][col] == player_initial for r in range(3)):
        return True
    if all(self.grid[i][i] == player_initial for i in range(3)):
      return True
    if all(self.grid[i][2 - i] == player_initial for i in range(3)):
      return True
    return False

  def no_more_move(self) -> bool:
    return all(None not in row for row in self.grid)

class SmallGame:
  def __init__(self, p1: str, p2: str) -> None:
    self.p1 = p1
    self.p2 = p2
    self.board = TicTacToeBoard()

  def is_finished(self) -> bool:
    return self.board.no_more_move() or self.board.has_won(self.p1) or self.board.has_won(self.p2)
  
  def get_row_col_input(self, player: str) -> None:
    print("\nThis is a board of a small game")
    print(self.board)
    print("\n")
    row = int(input(f'{player}, enter row: '))
    col = int(input(f'{player}, enter col: '))
    while not self.board.make_move(player[0], row, col):
      print('Invalid move, try again')
      row = int(input(f'{player}, enter row: '))
      col = int(input(f'{player}, enter col: '))
  
  def play(self) -> str:
    while not self.is_finished():
      self.get_row_col_input(self.p1)
      if self.board.has_won(self.p1):
        print(f"{self.p1} won a cell!")
        print("\n")
        return self.p1
      elif self.board.no_more_move():
        print('Tie!')
        print("\n")
        return ""

      self.get_row_col_input(self.p2)
      if self.board.has_won(self.p2):
        print(f"{self.p2} won!")
        return self.p2
      elif self.board.no_more_move():
        print('Tie!')
        return ""

class BigGame(SmallGame):
    def get_row_col_input(self, player: str) -> tuple[int, int]:
      print("\nBelow is the board of the big game. Enter the row and column of the cell you want to play in. Whoever wins the small game in the cell will win that  cell and get to pick the next cell.")
      print(self.board)
      row = int(input(f'{player}, enter row: '))
      col = int(input(f'{player}, enter col: '))
      while self.board.grid[row][col] is not None:
        print(f"This cell row {row} col {col} already has {self.board.grid[row][col]}. Try again.")
        row = int(input(f'{player}, enter row: '))
        col = int(input(f'{player}, enter col: '))
      return row, col
  
    def play(self) -> str:
        first_player = self.p1
        second_player = self.p2
        while not self.is_finished():
            row, col = self.get_row_col_input(first_player)
            small_board_game = SmallGame(first_player, second_player)
            small_winner = small_board_game.play()
            while not small_winner:
              print(f"No one wins the small game. Let's replay for row {row} and col {col}")
              small_board_game = SmallGame(first_player, second_player)
              small_winner = small_board_game.play()

            self.board.grid[row][col] = small_winner[0]

            if self.board.has_won(small_winner):
              print(f"{small_winner} won the big game!! Game Over!")
              return small_winner
            elif self.board.no_more_move():
              print("The big game is a tie! Game Over")
              return ""

            if small_winner == self.p1:
              first_player = self.p1
              second_player = self.p2
            else:
              first_player = self.p2
              second_player = self.p1

if __name__ == "__main__":
  p1 = input("Enter player 1's name: ")
  p2 = input("Enter player 2's name: ")

  while p1[0] == p2[0]:
    print("Player 1 and player 2 cannot have the same initial.")
    p1 = input("Enter player 1's name: ")
    p2 = input("Enter player 2's name: ")
  
  game = BigGame(p1, p2)
  winner = game.play()
