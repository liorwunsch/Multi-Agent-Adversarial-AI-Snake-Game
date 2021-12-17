import sys
import copy
import random

def always_right(game_state, head, valid_steps):
    if [head[0],head[1]+1] in valid_steps:
        return [head[0],head[1]+1]
    return None

def max_manhattan_dist(game_state, head, valid_steps):
    # for Agents
    board = game_state['Board']
    c_head = find_snake_head(board, 'C')
    d_head = find_snake_head(board, 'D')
    
    next_step = None
    max_dist = 0
    for step in valid_steps:
        cur_dist = min(calc_manhattan_dist(step, c_head), calc_manhattan_dist(step, d_head))
        if cur_dist > max_dist:
            max_dist = cur_dist
            next_step = step
    
    return next_step

def min_manhattan_dist(game_state, head, valid_steps):
    # for Enemies
    board = game_state['Board']
    a_body = find_snake_body(board, 'A')
    b_body = find_snake_body(board, 'B')
    
    next_step = None
    min_dist = sys.maxsize
    for step in valid_steps:
        min_cur_dist = sys.maxsize
        for section in a_body:
            dist = calc_manhattan_dist(step, section)
            min_cur_dist = min(min_cur_dist, dist)
        for section in b_body:
            dist = calc_manhattan_dist(step, section)
            min_cur_dist = min(min_cur_dist, dist)
            
        if  min_cur_dist < min_dist:
            min_dist = min_cur_dist
            next_step = step
    
    return next_step

def calc_manhattan_dist(pos_src, pos_dst):
    if pos_dst is None:
        return sys.maxsize
    dist = abs(pos_src[0] - pos_dst[0]) + abs(pos_src[1] - pos_dst[1])
    return dist

def max_euclidian_dist(game_state, head, valid_steps):
    # for Agents
    board = game_state['Board']
    c_head = find_snake_head(board, 'C')
    d_head = find_snake_head(board, 'D')
    
    next_step = None
    max_dist = 0
    for step in valid_steps:
        cur_dist = min(calc_euclidian_dist(step, c_head), calc_manhattan_dist(step, d_head))
        if cur_dist > max_dist:
            max_dist = cur_dist
            next_step = step
    
    return next_step

def min_euclidian_dist(game_state, head, valid_steps):
    # for Enemies
    board = game_state['Board']
    a_body = find_snake_body(board, 'A')
    b_body = find_snake_body(board, 'B')
    
    next_step = None
    min_dist = sys.maxsize
    for step in valid_steps:
        min_cur_dist = sys.maxsize
        for section in a_body:
            dist = calc_euclidian_dist(step, section)
            min_cur_dist = min(min_cur_dist, dist)
        for section in b_body:
            dist = calc_euclidian_dist(step, section)
            min_cur_dist = min(min_cur_dist, dist)
            
        if  min_cur_dist < min_dist:
            min_dist = min_cur_dist
            next_step = step
    
    return next_step

def calc_euclidian_dist(pos_src, pos_dst):
    if pos_dst is None:
        return sys.maxsize
    dist = (pos_src[0] - pos_dst[0])**2 + (pos_src[1] - pos_dst[1])**2
    return dist

def find_snake_head(board, symbol):
    snake_head_pos = None
    for r,row in enumerate(board):
        for c,cell in enumerate(row):
            if cell == symbol:
                snake_head_pos = [r,c]
    return snake_head_pos
    
def find_snake_body(board, symbol):
    snake_body = []
    for r,row in enumerate(board):
        for c,cell in enumerate(row):
            if cell == symbol.upper() or cell == symbol.lower():
                snake_body.append([r,c])
    return snake_body
    

def man_mini_max(game_state, head, valid_steps):
    return mini_max(game_state, head, valid_steps, manhattan_flag=True)
    
def mini_max(game_state, head, valid_steps, manhattan_flag=False):
    orig_symbol = game_state['Board'][head[0]][head[1]]
    
    if valid_steps == []:
        return None
    
    step_scores = [min_max_search(orig_agent=orig_symbol, curr_agent=orig_symbol,
                                  depth=0, game_state=generate_game_state(game_state, orig_symbol, step), manhattan_flag=manhattan_flag) for step in valid_steps]
    max_step = max(step_scores)
    max_indices = [index for index in range(len(step_scores)) if step_scores[index] == max_step]
    chosenIndex = random.choice(max_indices)
    return valid_steps[chosenIndex]

def generate_game_state(game_state, curr_agent, step):
    new_game_state = copy.deepcopy(game_state)
    
    board = new_game_state['Board']
    body = new_game_state[curr_agent]
    tail = body.pop()
    board[tail[0]][tail[1]] = ' '
    
    head = body[0]
    board[head[0]][head[1]] = curr_agent.lower()
    
    body.appendleft(step)
    board[step[0]][step[1]] = curr_agent.upper()
    
    return new_game_state
    
def min_max_search(orig_agent, curr_agent, depth, game_state, manhattan_flag, max_depth=1):
    agents_order = ['C', 'D', orig_agent]
    
    if is_eaten(orig_agent, game_state):
        return 0
    if depth == max_depth:
        return evaluate_game_state(orig_agent, game_state, manhattan_flag=manhattan_flag) # in leaves of tree
    
    # Find Agent Id
    agent_id = 0
    for i, agent in enumerate(agents_order):
        if agent == curr_agent:
            agent_id = i
            break
    
    next_agent = agents_order[(agent_id + 1) % len(agents_order)]
    if next_agent == orig_agent:
        depth += 1
    
    # Max State
    if curr_agent == orig_agent:
        valid_steps = get_valid_steps(curr_agent, game_state)
        if valid_steps == []:
            return min_max_search(orig_agent, next_agent, depth, game_state, manhattan_flag=manhattan_flag)
        else:
            return max(min_max_search(orig_agent, next_agent, depth, generate_game_state(game_state, curr_agent, step), manhattan_flag=manhattan_flag) for step in valid_steps)
    else:
        return min_max_search(orig_agent, next_agent, depth, single_step(curr_agent, game_state), manhattan_flag=manhattan_flag)
    
    return 0

def is_eaten(agent, game_state):
    board = game_state['Board']
    body = game_state[agent]
    for section in body:
        if board[section[0]][section[1]] != agent.lower() and board[section[0]][section[1]] != agent.upper():
            return True
    return False

def evaluate_game_state(agent, game_state, manhattan_flag):
    if agent == 'A' or agent == 'B':
        head = game_state[agent][0]
        c_head = game_state['C'][0]
        d_head = game_state['D'][0]
        
        valid_steps = get_valid_steps(agent, game_state)
        if valid_steps == []:
            return -1
        
        if manhattan_flag:
            dist = min(calc_manhattan_dist(head, c_head), calc_manhattan_dist(head, d_head))
        else:
            dist = min(calc_euclidian_dist(head, c_head), calc_euclidian_dist(head, d_head))
        return dist
    return 0

def get_valid_steps(curr_agent, game_state):
    body = game_state[curr_agent]
    head = body[0]
    valid_steps = []
    # up
    if is_valid_position(curr_agent, game_state, [head[0]-1, head[1]]):
        valid_steps.append([head[0]-1, head[1]])
    # down
    if is_valid_position(curr_agent, game_state, [head[0]+1, head[1]]):
        valid_steps.append([head[0]+1, head[1]])
    # left
    if is_valid_position(curr_agent, game_state, [head[0], head[1]-1]):
        valid_steps.append([head[0], head[1]-1])
    # right
    if is_valid_position(curr_agent, game_state, [head[0], head[1]+1]):
        valid_steps.append([head[0], head[1]+1])
    
    return valid_steps

def is_valid_position(symbol, game_state, pos):
    board = game_state['Board']
    body = game_state[symbol]
    
    rows_num = len(board)
    cols_num = len(board[0])
    if (not 0 <= pos[0] < rows_num) or (not 0 <= pos[1] < cols_num) or (pos in body):
        return False
    if (symbol == 'A' or symbol == 'B') and (board[pos[0]][pos[1]] != ' '):
        return False
    if (symbol == 'C' or symbol == 'D') and (board[pos[0]][pos[1]] == 'C' or board[pos[0]][pos[1]] == 'D' or board[pos[0]][pos[1]] == 'c' or board[pos[0]][pos[1]] == 'd'):
        return False
    return True
    
def single_step(symbol, game_state):
    new_game_state = copy.deepcopy(game_state)
    
    board = new_game_state['Board']
    body = new_game_state[symbol]
    
    if body == []:
        return new_game_state
    
    for section in body:
        if board[section[0]][section[1]] != symbol.upper() and board[section[0]][section[1]] != symbol.lower():
            new_game_state[symbol] = []
            return new_game_state
        
    valid_steps = get_valid_steps(symbol, new_game_state)
    
    if symbol == 'A' or symbol == 'B':
        next_loc = max_manhattan_dist(new_game_state, body[0], valid_steps)        
    elif symbol == 'C' or symbol == 'D':
        next_loc = min_manhattan_dist(new_game_state, body[0], valid_steps)        
        
    if next_loc is None:
        if symbol == 'A' or symbol == 'B':
            new_game_state[symbol] = []
        return new_game_state
    
    update_body(symbol, new_game_state, next_loc)
    return new_game_state

def update_body(symbol, game_state, new_head):
    board = game_state['Board']
    body = game_state[symbol]
    
    tail = body.pop()
    board[tail[0]][tail[1]] = ' '
    
    cur_head = body[0]
    board[cur_head[0]][cur_head[1]] = symbol.lower()
    
    body.appendleft(new_head)
    board[new_head[0]][new_head[1]] = symbol
