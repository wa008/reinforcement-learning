# reinforcement-learning

design a map, contains
1. road
2. passer-by
3. obstacle 
4. cars

build a new car, make it drive better using RL, or make all cars have the same ability

input: visual

paramter: ability of car
1. control speed
2. direction

target: reach the destination in the shortest time


other idea
1. design maze suing RL


todo
1. RL+自动驾驶 的大框架；基于mofan大佬的代码修改，action的选择添加阻碍项；https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze
2. 提前模拟出结果，才能判定是否撞车
3. 可视化
4. 添加行人、红绿灯
5. 怎么定义汽车看到的内容：输入是，近距离范围内的车位置、速度等状态；进行模拟，看n秒后的状态是否有危险，选择最好的action