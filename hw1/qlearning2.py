import numpy as np
import random

actions_for_dict = ['up', 'down', 'left', 'right']
actions_dict = {action: i for i, action in enumerate(actions_for_dict)}

def action_to_int(action):
    return actions_dict[action]

def get_reward(grid, curr_pos):
    i, j = curr_pos
    if grid[i][j] == 'obstacle':
        return -10
    else:
        return -1

def get_possible_actions(grid, curr_pos):
    print("get_possible_actions")
    print("curr_pos:", curr_pos)
    
    i, j = curr_pos
    actions = []
    #actions = ['up', 'down', 'left', 'right']
    #action_to_int = {a: i for i, a in enumerate(actions)}
    '''
    if i > 0 and grid[i-1][j] != 'obstacle' and i<(len(grid)-1):
        print("up")
        actions.append('up')
    if i < len(grid)-1 and grid[i+1][j] != 'obstacle' and i<(len(grid)-1):
        print("down")
        actions.append('down')
    if j > 0 and grid[i][j-1] != 'obstacle' and j<(len(grid)-1):
        print("left")
        actions.append('left')
    if j < len(grid[0])-1 and grid[i][j+1] != 'obstacle' and j<(len(grid)-1):
        print("right")
        actions.append('right')
    '''
    #if len(actions) == 0:
    #    print("000")
        # No possible actions, try to move through obstacle
    if i > 0:
        actions.append('up')
    if i < len(grid)-1:
        actions.append('down')
    if j > 0:
        actions.append('left')
    if j < len(grid[0])-1:
        actions.append('right')
    print("actions:", actions)
    return actions

def choose_action(q, state, epsilon, grid):
    if np.random.uniform() < epsilon:
        # choose a random action
        return random.choice(get_possible_actions(grid, state))
    else:
        # choose the action with the highest Q-value for the current state
        actions = get_possible_actions(grid, state)
        print("actions:", actions)
        print("state:", state)
        #return max(get_possible_actions(grid, state), key=lambda a: q[state[0],state[1],a])
        #actions = ['up', 'down', 'left', 'right']
        #action_to_int = {a: i for i, a in enumerate(actions)}
        #max(get_possible_actions(grid, state), key=lambda a: (print(state[0], state[1], action_to_int(a)), q[state[0],state[1],action_to_int(a)]))
        return max(get_possible_actions(grid, state), key=lambda a: q[state[0], state[1], action_to_int(a)])



def q_learning(grid, start, end, alpha=0.1, gamma=0.9, epsilon=0.1, num_episodes=1):
    
    # initialize Q-value function
    q = np.zeros((len(grid), len(grid[0]), 4))

    for episode in range(num_episodes):
        print("for loooooooooooooooooooooooooooooooopppppp")
        # initialize the starting state
        state = start
        done = False

        while (done==False):
            print("not done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("state:", state)
            print("start",start)
            print("end",end)
            # choose an action based on the epsilon-greedy strategy
            action = choose_action(q, state, epsilon, grid)
            i, j = state

            # take the chosen action and observe the new state and reward
            if action == 'up':
                next_state = (i-1, j)
                reward = get_reward(grid, next_state) if next_state != end else 10
            elif action == 'down':
                next_state = (i+1, j)
                reward = get_reward(grid, next_state) if next_state != end else 10
            elif action == 'left':
                next_state = (i, j-1)
                reward = get_reward(grid, next_state) if next_state != end else 10
            else:
                next_state = (i, j+1)
                reward = get_reward(grid, next_state) if next_state != end else 10

            # update Q-value function
            if not done:
                
                #actions = ['up', 'down', 'left', 'right']
                #action_to_int = {a: i for i, a in enumerate(actions)}
                max_q = max([q[next_state[0],next_state[1],action_to_int(a)] for a in get_possible_actions(grid, next_state)])
                #max_q = max(get_possible_actions(grid, state), key=lambda a: q[state[0], state[1], action_to_int[a]])
                q[i,j,action_to_int(action)] += alpha * (reward + gamma * max_q - q[i,j,action_to_int(action)])
            else:
                q[i,j,action_to_int(action)] += alpha * (reward - q[i,j,action_to_int(action)])

            # move to the next state
            state = next_state
            
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!not done")
            print("state:", state)
            print("next_state:", next_state)
            print("start",start)
            print("end",end)
            print("done",done)
            if int(next_state[0]) == int(end[0]) and int(next_state[1]) == int(end[1]):
                done = True
            print("done",done)

    # compute the policy
    print("compute the policy")
    policy = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 'obstacle':
                get_possible_actions(grid, (i,j), key=lambda a:(print(i," ",j," ",action_to_int(a))), q[i,j,action_to_int(a)])
                best_action = max(get_possible_actions(grid, (i,j)), key=lambda a:q[i,j,action_to_int(a)])
                policy.append([i, j, best_action])

    # reshape Q-value function to match policy
    q_value = np.zeros((len(grid), len(grid[0]), len(get_possible_actions(grid, (0,0)))))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 'obstacle':
                for k, action in enumerate(get_possible_actions(grid, (i,j))):
                    q_value[i, j, k] = q[i, j, action_to_int(action)]
    # create empty policy
    policy = [[' ' for j in range(len(grid[0]))] for i in range(len(grid))]

    # fill in policy based on Q-values
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'obstacle':
                policy[i][j] = 'X'  # mark obstacles as 'X'
            else:
                # get index of max Q-value
                max_q_index = np.argmax(q_value[i, j])
                # get action with max Q-value
                max_action = get_possible_actions(grid, (i,j))[max_q_index]
                # fill in policy with action
                policy[i][j] = max_action[0].upper()
                policy[i][j] += max_action[1:]

    return policy, q_value