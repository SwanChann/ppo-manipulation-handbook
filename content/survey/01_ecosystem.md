# 任务套件和 PPO 算法库分开选择

继续使用OrcaGym承载现有资产与环境，复用外部任务的事件定义、奖励计算和评估做法即可。SB3、RSL-RL、RL-Games、skrl、CleanRL负责算法，不会自动提供某个操作任务已经调通的奖励。表中PPO支持等级是仓库范围的证据，具体任务仍需单独查配置。

`tested`为有官方调通/基线声明，非本机复现；`integrated`为实际集成入口；`compatible`为接口层可能接入，未验证专属基线；`unknown`保留缺口。

|项目|角色|PPO证据级别|所查版本|依据|
|---|---|---|---|---|
|ManiSkill|任务套件|tested|62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3|[源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/examples.sh#L1-L26)、[源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L3-L24)|
|Isaac Lab v2.3.0|任务套件|integrated|3c6e67bb5c7ada942a6d1884ab69338f57596f77|[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/lift/config/franka/__init__.py#L19-L30)|
|IsaacGymEnvs (archived)|任务套件|integrated|aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3|[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/__init__.py#L1-L114)|
|NVIDIA SO101 typing task|专项任务|integrated|7aec2ed26dce8c88ae007a2714680cce572e1466|[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/__init__.py#L17-L46)|
|MuJoCo Playground|任务套件|integrated|56420458c8d81acd6942779d9dab327382117175|[源码](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/README.md#L1-L50)|
|Meta-World|benchmark|compatible|a14b096edb015ca931e33643a19ea97f4d92eb0f|[源码](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/README.md#L1-L50)|
|robosuite|任务套件|compatible|5ce6643f3092639d08f7b0f90ed1c6a84f50552c|[源码](https://github.com/ARISE-Initiative/robosuite/blob/5ce6643f3092639d08f7b0f90ed1c6a84f50552c/README.md#L1-L50)|
|Gymnasium-Robotics|任务套件|compatible|未固定，仅概览|[源码](https://github.com/Farama-Foundation/Gymnasium-Robotics)|
|Bi-DexHands|任务套件|integrated|dc41afd134cebfe4d80a5b861f0b8c15d734320a|[源码](https://github.com/PKU-MARL/DexterousHands/blob/dc41afd134cebfe4d80a5b861f0b8c15d734320a/bidexhands/cfg/ShadowHandOver.yaml#L1-L47)、[源码](https://github.com/PKU-MARL/DexterousHands/blob/dc41afd134cebfe4d80a5b861f0b8c15d734320a/bidexhands/cfg/ppo/config.yaml#L1-L35)|
|RoboCasa|任务套件|unknown|未固定，仅概览|[源码](https://github.com/robocasa/robocasa)|
|RoboDuet|专项任务|unknown|a7e1528215c048199f90cb69ceb7749a1d745f28|[源码](https://github.com/locomanip-duet/RoboDuet)、[源码](https://github.com/locomanip-duet/RoboDuet/blob/a7e1528215c048199f90cb69ceb7749a1d745f28/README.md#L155-L158)|
|Stable-Baselines3|算法库|integrated|未固定，仅概览|[源码](https://github.com/DLR-RM/stable-baselines3)|
|RSL-RL|算法库|integrated|未固定，仅概览|[源码](https://github.com/leggedrobotics/rsl_rl)|
|skrl|算法库|integrated|未固定，仅概览|[源码](https://github.com/Toni-SM/skrl)|
|CleanRL|算法库|integrated|未固定，仅概览|[源码](https://github.com/vwxyzjn/cleanrl)|

当前生态优先看ManiSkill、Isaac Lab与MuJoCo Playground。版本不同不能拼接结论：Isaac Lab本调查选v2.3.0；SO101依赖其自定义fork；Playground旧Panda代码在rss2025目录。IsaacGymEnvs与Bi-DexHands放入历史影响类，适合读设计，不作为本机环境迁移方案。相应任务卡给出具体版本。

RoboCasa与Gymnasium-Robotics提供丰富的任务与物理对象，本轮没有追到其对应任务专属PPO基线。RoboDuet官方资料中的Go1/Go2加ARX5与第三层移动操作相关，但本次只核对资料入口，不把全身追踪能力写成按按钮成功。算法库各自只列为一种角色，没有重复算成新的操作任务。
