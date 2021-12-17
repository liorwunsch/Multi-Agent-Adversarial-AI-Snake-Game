from SnakeAgent import SnakeAgent
import Strategy
from blessed import Terminal
import time

class Game:
    
    def __init__(self, strategy, rows=20, cols=20):
        self.board = [[' '] * cols for _ in range(rows)]
        
        if strategy == 0:
            s = Strategy.always_right
        elif strategy == 1:
            s = Strategy.max_manhattan_dist
        elif strategy == 2:
            s = Strategy.max_euclidian_dist
        elif strategy == 3:
            s = Strategy.man_mini_max
        elif strategy == 4:
            s = Strategy.mini_max
        
        self.agent1 = SnakeAgent(self.board, strategy=s, symbol='A')
        self.agent2 = SnakeAgent(self.board, strategy=s, symbol='B')
        self.enemy1 = SnakeAgent(self.board, strategy=Strategy.min_manhattan_dist, symbol='C', is_enemy=True)
        self.enemy2 = SnakeAgent(self.board, strategy=Strategy.min_manhattan_dist, symbol='D', is_enemy=True)
        self.term = Terminal()
        
        self.notify_all_agents('A', self.agent1.get_body())
        self.notify_all_agents('B', self.agent2.get_body())
        self.notify_all_agents('C', self.enemy1.get_body())
        self.notify_all_agents('D', self.enemy2.get_body())

    def print_board(self):
        # clear the screen
        print(self.term.home + self.term.clear)
        
        print('    ', end='')
        for i in range(len(self.board[0])):
            print('{0} '.format(i % 10), end='')
        print()
        print('  ', end='')
        print('* ' * (len(self.board[0]) + 2))
        for j,row in enumerate(self.board):
            print('{0} '.format(j % 10), end='')
            print('* ', end='')
            print(' '.join(row), end='')
            print(' * ')
        print('  ', end='')
        print('* ' * (len(self.board[0]) + 2))
        
    def play(self):
        agent1_alive = True
        agent2_alive = True
        
        while agent1_alive or agent2_alive:
            self.enemy1.single_step()
            self.notify_all_agents('C', self.enemy1.get_body())
            
            self.enemy2.single_step()
            self.notify_all_agents('D', self.enemy2.get_body())
            
            agent1_alive = self.agent1.single_step()
            self.notify_all_agents('A', self.agent1.get_body())
            
            agent2_alive = self.agent2.single_step()
            self.notify_all_agents('B', self.agent2.get_body())
        
        return self.agent1.get_score(), self.agent2.get_score()
            
    def notify_all_agents(self, symbol, body):
        self.agent1.notify(symbol, body)
        self.agent2.notify(symbol, body)
        self.enemy1.notify(symbol, body)
        self.enemy2.notify(symbol, body)
    
    def print_play(self):
        self.print_board()
        agent1_alive = True
        agent2_alive = True
        
        while agent1_alive or agent2_alive:
            time.sleep(0.2)
            
            self.enemy1.single_step()
            self.notify_all_agents('C', self.enemy1.get_body())
            
            self.enemy2.single_step()
            self.notify_all_agents('D', self.enemy2.get_body())
            
            agent1_alive = self.agent1.single_step()
            self.notify_all_agents('A', self.agent1.get_body())
            
            agent2_alive = self.agent2.single_step()
            self.notify_all_agents('B', self.agent2.get_body())
            
            self.print_board()
        
        print('A Score:')
        print(self.agent1.get_score())
        print('B Score:')
        print(self.agent2.get_score())
        
        return self.agent1.get_score(), self.agent2.get_score()
        