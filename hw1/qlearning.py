import numpy as np
def q_learning(grid, start, end, alpha=0.1, gamma=0.9, epsilon=0.1, num_episodes=1000):
    q_table = np.zeros((len(grid), len(grid[0]), 4))
    print("len of grid: ")
    print(len(grid))

    actions = ['up', 'down', 'left', 'right']
    i=0
    for episode in range(num_episodes):
        current = start
        done = False

        while not done:
           
            if np.random.random() < epsilon:
                action = np.random.choice(actions)
            else:
                action = actions[np.argmax(q_table[current[0]][current[1]])]

            if action == 'up':
                new_state = (current[0] - 1, current[1])
            elif action == 'down':
                new_state = (current[0] + 1, current[1])
            elif action == 'left':
                new_state = (current[0], current[1] - 1)
            elif action == 'right':
                new_state = (current[0], current[1] + 1)

            if new_state[0] < 0 or new_state[0] >= len(grid) or new_state[1] < 0 or new_state[1] >= len(grid[0]):
                reward = -100
                done = True
                # 更新q_table，下一個狀態為當前狀態，因為越界時agent並沒有移動
                q_table[current[0]][current[1]][actions.index(action)] += alpha * (reward + gamma * np.max(q_table[current[0]][current[1]]) - q_table[current[0]][current[1]][actions.index(action)])
                break
            elif grid[new_state[0]][new_state[1]] == 'obstacle':
                reward = -10
                done = False
            elif new_state == end:
                reward = 100
                done = True
            else:
                reward = -1
                done = False
            
            q_table[current[0]][current[1]][actions.index(action)] += alpha * (reward + gamma * np.max(q_table[new_state[0]][new_state[1]]) - q_table[current[0]][current[1]][actions.index(action)])

            current = new_state

    print("++++++++++++++++++++++++++++++++++++++++++")   
    print(q_table)
    print("++++++++++++++++++++++++++++++++++++++++++")
    policy = []
    now_i=start[0]
    now_j=start[1]
    done = False
    test = 0
    
    while(now_i<len(q_table) and now_i>=0 and not done):
        row = []
        while(now_j<len(q_table[0]) and now_j>=0 and not done):
            print("now_i, now_j: ",end='')
            print(now_i,end=' ')
            print(now_j)
            test = test+1
            if(test>20):
                done=True
                break
            
            action_index = np.argmax(q_table[now_i][now_j])
            row.append([now_i, now_j, actions[action_index]])
            print("test point 1")
            if action_index == 0:
                now_i=now_i-1
            elif action_index == 1:
                now_i=now_i+1
            elif action_index == 2:
                now_j=now_j-1
            elif action_index == 3:
                now_j=now_j+1
            
            if(now_i==end[0] and now_j==end[1]):
                print("arrive end")
                done = True
               

        policy.append(row)
    
    print(policy)
    q_value = q_table.reshape((len(grid))*(len(grid)), 4)
    return policy, q_value