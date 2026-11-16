# ManiSkill 源码取证摘要

优先复用 StackCube 的后阶段覆盖奖励、PegInsertionSide 的双点对齐门控、TwoRobotStackCube 的让位动作 shaping。它们都是按当前物理条件定义奖励；不是锁存 FSM，也没有通用阶段 one-hot。按钮已按下的历史必须由本项目自己的事件状态保留。

本分卷固定同一 SHA，代码检查1个项目；抽查7个具体任务，其中5个有有效 dense reward 与任务专属 PPO配置，另2个为 sparse-only 负例；共10套有效命令配置。没有本地复现或新的性能结论。源码可参考不代表直接覆盖 X5 已确认验收。

最需要避免的三处误读：OpenCabinetDrawer 实际开启阈值75%而说明称90%；TwoRobotStackCube奖励右臂让位但success不验收该动作；TurnFaucet注释里的dense公式未执行。详情见任务卡和证据JSONL。

[StackCube奖励](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/stack_cube.py#L145-L186)；[双臂实际成功条件](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/two_robot_stack_cube.py#L169-L212)；[TurnFaucet TODO](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/turn_faucet.py#L204-L237)。
