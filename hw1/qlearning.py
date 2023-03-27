import numpy as np
def q_learning(grid, start, end, alpha=0.1, gamma=0.9, epsilon=0.1, num_episodes=1000):
    q_table = np.zeros((len(grid), len(grid[0]), 4))
    

    actions = ['up', 'down', 'left', 'right']

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

    return q_table