import numpy as np
import random

def step(state, action, grid, end):
    print("end: ",end)
    """
    在环境中执行一个动作，更新状态并返回奖励、下一个状态以及完成标志。

    参数：
        state (tuple): 当前状态，格式为 (行，列)。
        action (str): 要执行的动作，取值为 "up"、"down"、"left" 或 "right"。
        grid (list): 包含障碍物的二维列表。

    返回：
        tuple: 包含新的状态、奖励和完成标志的元组，格式为 (新状态，奖励，完成标志)。
    """
    row, col = state
    if action == 0:
        row -= 1
    elif action == 1:
        row += 1
    elif action == 2:
        col -= 1
    elif action == 3:
        col += 1

    # 检查下一个状态是否在范围内
    if (row < 0 or row >= len(grid) or
            col < 0 or col >= len(grid[0])):
        print("out of range!")
        return state, -1000, False
    
    next_state = (row, col)
    
    if(next_state[0] == end[0] and next_state[1] == end[1]):
        print("arrive!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return state, 100, True
    done = False
    if grid[next_state[0]][next_state[1]] == 'obstacle':
        print("obstacle!")
        reward = -10 
    else:
        print("normal path")
        reward = 0
    return next_state, reward, done

def behavior_policy(q_value, state, epsilon):
    if np.random.uniform() < epsilon:
        # 随机选择一个动作
        action = np.random.randint(4)
    else:
        # 选择具有最高 Q 值的动作
        values = q_value[state[0], state[1], :]
        action = np.random.choice(np.flatnonzero(values == values.max()))
    return action

# 定义更新 Q 值表的函数
def update_q_value(q_value, state, action, reward, next_state, alpha, gamma):
    next_action = np.argmax(q_value[next_state[0], next_state[1], :])
    q_value[state[0], state[1], action] = (1 - alpha) * q_value[state[0], state[1], action] + alpha * (reward + gamma * q_value[next_state[0], next_state[1], next_action])
    return q_value

def generate_policy(q_value, start, end):
    current_pos = start
    policy = []
    move = None
    next_pos = current_pos
    print("current_pos: ",current_pos)
    print("end: ",end)
    while not (current_pos[0] == end[0] and current_pos[1] == end[1]):
        print("current_pos: ",current_pos)
        print("end: ",end)
        x, y = current_pos
        max_q_value = np.max(q_value[x, y, :])
        
        # Get all actions with the maximum Q-value
        max_actions = np.argwhere(q_value[x, y, :] == max_q_value)
        
        # Randomly choose one of the maximum actions
        action = np.random.choice(max_actions.flatten())
        
        print("q_value: ",q_value)
        print("action: ",print_action(action))
        if action == 0 and x>0:
            next_pos = (x-1, y)
            move = 'up'
        elif action == 1 and x<len(q_value)-1:
            next_pos = (x+1, y)
            move = 'down'
        elif action == 2 and y>0:
            next_pos = (x, y-1)
            move = 'left'
        elif action == 3 and y<len(q_value)-1:
            next_pos = (x, y+1)
            move = 'right'
            
        policy.append([x, y, move])
        current_pos = next_pos
        
    #policy.append([end[0], end[1], 'end'])
    return policy

def print_action(action):
    if action == 0:
        move = 'up'
    elif action == 1:
        move = 'down'
    elif action == 2:
        move = 'left'
    elif action == 3:
        move = 'right'
    return move

def q_learning(grid, start, end, alpha=0.1, gamma=0.9, epsilon=0.1, num_episodes=100):
    # 初始化 Q 值表
    num_rows, num_cols = len(grid), len(grid[0])
    num_actions = 4
    q_value = np.zeros((num_rows, num_cols, num_actions))
    print("grid: ",grid)
    # 执行 Q 学习算法
    for episode in range(num_episodes):
        state = start
        done = False
        i=0
        while not done:
            
            print("state: ",state)
            # 选择一个动作
            action = behavior_policy(q_value, state, epsilon)
            print("action: ",print_action(action))

            # 执行该动作并观察环境的反馈
            next_state, reward, done = step(state, action, grid, end)
            print("next_state: ",next_state)
            print("reward: ",reward)
            print("done: ",done)

            # 更新 Q 值表
            q_value = update_q_value(q_value, state, action, reward, next_state, alpha, gamma)
            print("q_value: ",q_value)

            # 更新状态
            state = next_state

    # 计算最优策略
    print("over!!!! generate policy")
    policy = generate_policy(q_value, start, end)

    q_value = q_value.reshape((len(grid))*(len(grid)), 4)
    return policy, q_value