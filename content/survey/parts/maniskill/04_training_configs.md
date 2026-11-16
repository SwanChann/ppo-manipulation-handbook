# 有效 PPO 配置对照

来自同一提交；配置链为task命令覆盖相应Python Args默认值，非跨文件混搭。所有预算均为环境总采样步，不是每个环境独立训练预算。

|任务/版本|并行env×rollout|mini-batch|epochs|标称总步|γ/λ|入口|
|---|---:|---:|---:|---:|---|---|
|PickCube-v1 / example_state|1024×50|1600|8|10,000,000|0.8/0.9|ppo.py|
|StackCube-v1 / example_state|1024×50|1600|8|25,000,000|0.8/0.9|ppo.py|
|PegInsertionSide-v1 / example_state|1024×100|3200|8|250,000,000|0.8/0.9|ppo.py|
|TwoRobotStackCube-v1 / example_state|1024×100|3200|8|40,000,000|0.8/0.9|ppo.py|
|OpenCabinetDrawer-v1 / example_state|1024×100|3200|8|10,000,000|0.8/0.9|ppo.py|
|PickCube-v1 / baseline_state|4096×4|512|8|50,000,000|0.8/0.9|ppo_fast.py|
|StackCube-v1 / baseline_state|4096×16|2048|8|50,000,000|0.8/0.9|ppo_fast.py|
|PegInsertionSide-v1 / baseline_state|2048×16|1024|8|75,000,000|0.97/0.95|ppo_fast.py|
|OpenCabinetDrawer-v1 / baseline_state|1024×16|512|8|50,000,000|0.8/0.9|ppo_fast.py|
|PickCube-v1 / baseline_rgb|1024×16|512|8|50,000,000|0.8/0.9|ppo_rgb.py|

详细命令、按完整rollout向下取整的实际步数、Actor/Critic结构、初始std、clip/KL等见[任务卡](02_task_taxonomy.md)和configs.jsonl。普通state PPO初始logstd−0.5，fast版0；RGB版共享CNN+state编码再分Actor/Critic，state并非全部物体真值，需沿task extras核对。

[普通PPO默认](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo.py#L24-L161)；[fast PPO默认](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo_fast.py#L62-L164)；[RGB结构](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo_rgb.py#L176-L251)；[插入baseline](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L117-L125)。

没有与精确版本匹配的逐seed成功率/显存/耗时原始日志，本分卷不填推测数值。这些上游预算大于100k，支持“不能凭100k判定方案无效”的谨慎判断，但不能推出本项目2M已经充分；课程、观察、控制、成功条件差异很大。
