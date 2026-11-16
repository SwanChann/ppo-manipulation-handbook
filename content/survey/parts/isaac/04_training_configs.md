# 有效训练配置与预算口径

|选定入口/变体|env×rollout×迭代|环境步上限|优化epochs/minibatch|lr/gamma/entropy|
|---|---:|---:|---|---|
|Lab Lift/RSL|4096×24×1500|147,456,000|5/24576|1e−4/.98/.006|
|Lab Cabinet/RSL|4096×16×1500|98,304,000|8/8192|5e−4/.99/0|
|Lab Factory/RLGames|128×128×200|3,276,800|4/512|1e−4/.995/0|
|GymEnvs Stack/RLGames|8192×32×10000|2,621,440,000|5/16384|5e−4/.99/0|
|SO101注册P0默认|4096×64×20000|5,242,880,000|5/65536|1e−4/.995/.005|
|SO101 tutorial teacher|64×32×5000|10,240,000|4/512|1e−4 fixed/.995/.005|
|SO101 tutorial vision PPO|64×32×5000|10,240,000|4/512|1e−4 fixed/.995/.005|

这些数字是**配置上限，不是实测收敛时间/最低样本需求**。SO101另有614400环境交互的teacher imitation warmup，不能算为PPO更新步。旧20.48M teacher估算忽略了runner_config对rollout32的覆盖，本分册已纠正。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/lift/config/franka/agents/rsl_rl_ppo_cfg.py#L12-L38) [源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/franka_cabinet/agents/rsl_rl_ppo_cfg.py#L12-L38) [源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/factory/agents/rl_games_ppo_cfg.yaml#L7-L123) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/cfg/train/FrankaCubeStackPPO.yaml#L1-L71) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/agents/rsl_rl_ppo_cfg.py#L22-L113) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/scripts/vision/agent.py#L13-L22) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/scripts/tutorial/runtime.py#L25-L30) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/scripts/vision/train_simple.py#L67-L113)

每项的完整gamma/GAE/clip/KL、归一化、网络和实际命令保存在data/configs.jsonl并附文件行号。Factory2层1024LSTM、特权critic不能与普通MLP/PPO速度横比。这里没有推算上游训练GPU小时或显存，因为缺少同硬件实测证据。
