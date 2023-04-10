# reinforcement-learning
设计一个自动驾驶地图，利用强化学习让车的驾驶技术变得更好。

# 详细设计
地图包含：
1. 公路
2. 行人
3. 障碍物
4. 汽车

输入
1. 地图上的所有内容
2. 汽车理论上能看到的所有内容

汽车操作
1. 控制速度
2. 方向

汽车目标
1. 用最短的时间到达目的地
2. 降低撞车风险

# todo
1. RL大框架。done
2. 可视化。done
3. 多辆车；提前模拟出结果，才能判定是否撞车。1）多辆车 done。2）提前模拟，不能碰撞。3）设计成路线
4. 添加行人、红绿灯
5. 怎么定义汽车看到的内容：输入是，近距离范围内的车位置、速度等状态；进行模拟，看n秒后的状态是否有危险，选择最好的action
6. 地图太小，只支持横竖20个基本单位
7. 解决下死机的问题

# 参考
1. mofan大佬的RL框架；https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/2_Q_Learning_maze

其他想法
1. 用这个方案制作迷宫
