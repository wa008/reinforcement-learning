import numpy as np
import pandas as pd
import random
import os

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, pre_train_file = ''):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.action_space = ['left', 'right', 'up', 'down']
        self.action2index = {}
        for index, action in enumerate(self.action_space):
            self.action2index[action] = index

        if pre_train_file != '' and os.path.exists(pre_train_file):
            self.q_table = pd.read_csv(pre_train_file, sep = '\t')
        else:
            self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            distance_action = [0 for i in range(len(self.action_space))]
            x, y, nx, ny =[int(val) for val in observation.split("_")]
            if x < nx:
                distance_action[self.action2index['up']] -= 1
                distance_action[self.action2index['down']] += 1
            elif x > nx:
                distance_action[self.action2index['up']] += 1
                distance_action[self.action2index['down']] -= 1
            if y < ny:
                distance_action[self.action2index['right']] += 1
                distance_action[self.action2index['left']] -= 1
            elif y > ny:
                distance_action[self.action2index['right']] -= 1
                distance_action[self.action2index['left']] += 1
            final_score = state_action + np.array(distance_action)
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(final_score[final_score == np.max(final_score)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
