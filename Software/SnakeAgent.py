from collections import deque
import random

class SnakeAgent:

    def __init__(self, board, strategy, symbol, size=5, is_enemy=False):
        self.board = board
        self.strategy = strategy
        self.symbol = symbol
        self.size = size
        self.is_enemy = is_enemy
        
        self.body = None
        self.is_alive = True
        self.score = 0

        self.init_body()
        
        self.game_state = { 
            'Board': board,
            'A': [],
            'B': [],
            'C': [],
            'D': []
        }
        
    def init_body(self):
        rows_num = len(self.board)
        cols_num = len(self.board[0])

        # Get Starting Position (x = row, y = col)
        snake_valid = False

        while not snake_valid:
            self.body = deque()
            curr_size = 0
            head_x = random.randrange(0, rows_num)
            head_y = random.randrange(0, cols_num)

            if self.board[head_x][head_y] != ' ':
                continue

            curr_size += 1
            self.body.append([head_x, head_y])

            last_x = head_x
            last_y = head_y
            failed_attempts = 0
            while curr_size < self.size:
                direction = random.randrange(1, 5)
                (next_x, next_y) = self.change_location(last_x, last_y, direction)
                
                if not self.is_valid_position(next_x, next_y):
                    failed_attempts += 1
                    if failed_attempts == 1000:
                        raise Exception('failed to position snake ' + self.symbol)
                    continue
                curr_size += 1

                self.body.append([next_x, next_y])

                last_x = next_x
                last_y = next_y

            snake_valid = True
            
        # insert body to board
        for i, section in enumerate(self.body):
            x = section[0]
            y = section[1]

            if i == 0:
                self.board[x][y] = self.symbol
            else:
                self.board[x][y] = self.symbol.lower()
            
    def single_step(self):
        if not self.is_alive:
            return False
        
        for section in self.body:
            if self.board[section[0]][section[1]] != self.symbol.upper() and self.board[section[0]][section[1]] != self.symbol.lower():
                self.is_alive = False
                self.delete_snake()
                return False
                
        valid_steps = self.detect_valid_steps()
        next_loc = self.strategy(self.game_state, self.body[0], valid_steps)
        
        if next_loc is None:
            if not self.is_enemy:
                self.is_alive = False
                self.delete_snake()
            return False
        
        self.update_body(next_loc)
        self.get_score_point()
        return True
        
    def detect_valid_steps(self):
        head = self.body[0]
        valid_steps = []
        # up
        if self.is_valid_position(head[0]-1, head[1]):
            valid_steps.append([head[0]-1, head[1]])
        # down
        if self.is_valid_position(head[0]+1, head[1]):
            valid_steps.append([head[0]+1, head[1]])
        # left
        if self.is_valid_position(head[0], head[1]-1):
            valid_steps.append([head[0], head[1]-1])
        # right
        if self.is_valid_position(head[0], head[1]+1):
            valid_steps.append([head[0], head[1]+1])
        
        return valid_steps
        
    def is_valid_position(self, x, y):
        rows_num = len(self.board)
        cols_num = len(self.board[0])
        if (not 0 <= x < rows_num) or (not 0 <= y < cols_num) or ([x, y] in self.body):
            return False
        if (not self.is_enemy) and (self.board[x][y] != ' '):
            return False
        if (self.is_enemy) and (self.board[x][y] == 'C' or self.board[x][y] == 'D' or self.board[x][y] == 'c' or self.board[x][y] == 'd'):
            return False
        return True
    
    def update_body(self, new_head):
        tail = self.body.pop()
        self.board[tail[0]][tail[1]] = ' '
        
        cur_head = self.body[0]
        self.board[cur_head[0]][cur_head[1]] = self.symbol.lower()
        
        self.body.appendleft(new_head)
        self.board[new_head[0]][new_head[1]] = self.symbol
    
    def delete_snake(self):
        for section in self.body:
            x = section[0]
            y = section[1]
            if self.board[x][y] == self.symbol.upper() or self.board[x][y] == self.symbol.lower():
                self.board[x][y] = ' ';
    
    def get_score(self):
        return self.score
    
    def get_score_point(self):
        self.score += 1
    
    def change_location(self, x, y, mode):
        if mode == 1:
            x = x + 1
        elif mode == 2:
            x = x - 1
        elif mode == 3:
            y = y + 1
        elif mode == 4:
            y = y - 1
        return x, y
    
    def get_body(self):
        return self.body
    
    def notify(self, symbol, body):
        self.game_state[symbol] = body
        
        
        
        