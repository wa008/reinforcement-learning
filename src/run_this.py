from maze_env import Maze
from RL_brain import QLearningTable
import random
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

pre_train_file = './data/pre_train_file'

def update():
    for episode in range(100):
        begin_time = datetime.now()
        # initial observation
        # random.seed(2023)
        random.seed(int(datetime.now().timestamp() * 1000))
        env.reset()
        retry_cnt = 0
        max_try = 10

        while True:
            done_cnt = 0
            retry_cnt += 1
            # fresh env
            env.render()
            for car_ind in range(len(env.cars)):
                observation = env._get_observation(car_ind)
                for i in range(max_try):
                    # RL choose action based on observation
                    action = RL.choose_action(str(observation))
                    if env.check_action_is_valid(car_ind, action) == False:
                        continue
                    # RL take action and get next observation and reward
                    observation_, reward, done = env.step(car_ind, action)

                    # RL learn from this transition
                    RL.learn(str(observation), action, reward, str(observation_))

                    # swap observation
                    observation = observation_
                    done_cnt += int(done)
                    break
            # break while loop when end of this episode
            if done_cnt == len(env.cars):
                break
        print ("episode: {}\tretry_cnt: {}\ttime: {}".format(episode, retry_cnt, datetime.now() - begin_time))
        RL.q_table = RL.q_table.head(1)
    # end of game
    print('game over')
    RL.q_table.to_csv(pre_train_file, sep = '\t', header = True, index = True)
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)), pre_train_file = '')

    env.after(100, update)
    env.mainloop()