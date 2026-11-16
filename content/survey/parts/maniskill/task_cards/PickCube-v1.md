# ManiSkill：PickCube-v1

版本 `62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3`；检索日期2026-11-16。

本卡是源码与有效配置静态取证（`verified-from-code`），不是本机复现实验；未下载任务资产、未安装 ManiSkill、未执行训练。配置属于上游该 SHA，不直接替换 X5/OrcaGym 的控制器、任务验收或 PPO 参数。

默认物理 100 Hz、控制 20 Hz，即每个 policy step 含 5 个物理子步；奖励每控制步计算，没有额外乘 dt。单臂 Panda 使用 `pd_joint_delta_pos`：7 维相对当前关节位置的增量（归一化动作裁剪并映射至 ±0.1 rad）加 1 维绝对夹爪开度目标（−0.01 至 0.04 m）；双臂动作展平成 16 维。Fetch 还包含 body 关节增量与底盘前进/转向速度，不能当成同一 8 维接口。

[频率定义](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/utils/structs/types.py#L78-L89)；[Panda动作](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/robots/panda/panda.py#L90-L98)；[增量基准](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/controllers/pd_joint_pos.py#L81-L98)；[Fetch组合控制](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/robots/fetch/fetch.py#L219-L257)。

## 任务、观测与验收

Robot：`panda`；episode上限 50 控制步（2.5 s）。[注册与默认构型](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/pick_cube.py#L33-L64)。

object within25mm goal and max absolute nonfinger joint velocity<=.2rad/s; release not required。[实际 evaluate/obs 实现](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/pick_cube.py#L132-L159)。

标准 state 策略输入机器人 qpos/qvel/controller state，加各任务 TCP、物体、目标及相对几何等 extras；本卡所查五个 dense 任务没有阶段 one-hot 或锁存阶段观测。[状态组合](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/sapien_env.py#L547-L559)；[本体字段](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/base_agent.py#L339-L348)。

训练默认成功即终止并局部 reset；评估默认忽略 success termination，直到超时，分别记录 `success_once` 与 `success_at_end`。这两者都不等于本项目“按下 / 撤回 / 返回 / 连续停稳”的独立验收。[BaseEnv termination](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/sapien_env.py#L1050-L1078)；[TimeLimit](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/utils/registration.py#L127-L168)；[评估wrapper](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/vector/wrappers/gymnasium.py#L127-L168)。

## 实际奖励

```text
r=[1-tanh(5*d_tcp_obj)+G+G*(1-tanh(5*d_obj_goal))+P*(1-tanh(5*||qvel_nonfinger||2))]/5; if S set r=1
```

[奖励源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/pick_cube.py#L161-L191)。其中长度用 m，角速度用 rad/s；S代表上面源码定义的 success，I代表布尔指示量。

令 G 为真实双指接触抓取，P 为物体到目标距离≤25 mm，S 为 P 且非夹爪关节速度绝对值最大值≤0.2 rad/s。`qvel_nonfinger` 排除 Panda 两个手指。奖励中的“静止”用关节速度 L2 范数，而验收用最大绝对值，两者不是同一范数。此任务允许保持抓取完成；它不验证放手，不包含撤回/回零或连续150 ms。

源码默认 RGB 版本也含 `is_grasped`、TCP pose、goal position 及本体信息，不能宣传为纯图像策略。`include_state=True` 的“state”是移除传感器后剩余观测；它不自动等于 state-mode 中全部物体真值。可借鉴“到目标之后才给停稳 shaping”，但我们的按钮任务必须继续使用已冻结的速度/持续时间阈值。

## PPO配置与复现入口

命令在固定 SHA 的 `examples/baselines/ppo` 下运行；此处仅保存命令，未执行。`example_state` 是官方“tested examples”路径；`baseline_state/rgb` 是官方比较用 baselines.sh，二者预算/实现不同，不混用。

### example_state

```bash
python ppo.py --env_id=PickCube-v1 --num_envs=1024 --update_epochs=8 --num_minibatches=32 --total_timesteps=10000000 --num_steps=50 --num_eval_steps=50
```

|参数|有效值|
|---|---|
|total_timesteps|10000000|
|actual_sample_budget_if_completed|9984000|
|num_envs|1024|
|num_steps|50|
|batch_size|51200|
|minibatch_size|1600|
|num_iterations|195|
|num_eval_envs|8|
|num_eval_steps|50|
|update_epochs|8|
|learning_rate|0.0003|
|gamma|0.8|
|gae_lambda|0.9|
|clip_coef|0.2|
|ent_coef|0.0|
|vf_coef|0.5|
|target_kl|0.1|
|max_grad_norm|0.5|
|initial_logstd|-0.5|
|actor_layers|[256, 256, 256]|
|critic_layers|[256, 256, 256]|
|seed|1|

[ppo_defaults](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo.py#L24-L161)；[ppo_setup](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo.py#L174-L224)；[examples](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/examples.sh#L1-L26)。

### baseline_state

```bash
python ppo_fast.py --env_id=PickCube-v1 --num_envs=4096 --num_steps=4 --num_eval_envs=16 --update_epochs=8 --num_minibatches=32 --total_timesteps=50000000 --cudagraphs --seed=9351 # repeat 4796,1788 separately
```

|参数|有效值|
|---|---|
|total_timesteps|50000000|
|actual_sample_budget_if_completed|49987584|
|num_envs|4096|
|num_steps|4|
|batch_size|16384|
|minibatch_size|512|
|num_iterations|3051|
|num_eval_envs|16|
|num_eval_steps|50|
|update_epochs|8|
|learning_rate|0.0003|
|gamma|0.8|
|gae_lambda|0.9|
|clip_coef|0.2|
|ent_coef|0.0|
|vf_coef|0.5|
|target_kl|0.1|
|max_grad_norm|0.5|
|initial_logstd|0|
|actor_layers|[256, 256, 256]|
|critic_layers|[256, 256, 256]|
|seed|9351|

[fast_defaults](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo_fast.py#L62-L164)；[baseline_pick](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L3-L24)；[baseline_pick](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L3-L24)。

### baseline_rgb

```bash
python ppo_rgb.py --env_id=PickCube-v1 --num_envs=1024 --num_steps=16 --num_eval_envs=16 --update_epochs=8 --num_minibatches=32 --total_timesteps=50000000 --seed=9351 # repeat 4796,1788 separately
```

|参数|有效值|
|---|---|
|total_timesteps|50000000|
|actual_sample_budget_if_completed|49987584|
|num_envs|1024|
|num_steps|16|
|batch_size|16384|
|minibatch_size|512|
|num_iterations|3051|
|num_eval_envs|16|
|num_eval_steps|50|
|update_epochs|8|
|learning_rate|0.0003|
|gamma|0.8|
|gae_lambda|0.9|
|clip_coef|0.2|
|ent_coef|0.0|
|vf_coef|0.5|
|target_kl|0.2|
|max_grad_norm|0.5|
|initial_logstd|-0.5|
|actor_layers|[512]|
|critic_layers|[512]|
|seed|9351|

[rgb_defaults](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo_rgb.py#L54-L111)；[rgb_model](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/ppo_rgb.py#L176-L251)；[baseline_rgb](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L188-L196)；[baseline_pick](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L3-L24)。

所有列出配置：Adam学习率3e-4、无学习率退火、advantage normalization开启、无running observation normalization、reward_scale=1。state Actor/Critic各自3×256 Tanh；RGB分支为NatureCNN输出256+state投影256，共享特征后Actor/Critic各512 ReLU，没有LSTM。初始logstd：ppo_fast=0；普通ppo/ppo_rgb=−0.5。源码的总步数按完整rollout向下取整，故表同时列出实际采样预算。官方baseline seeds=[9351,4796,1788]；单个示例默认seed1。

## 证据与使用边界

本调查没有取得与上述精确命令绑定的逐seed原始成功率、GPU型号、显存或耗时，均标为未知；不把源码中的奖励上限或官方示例“tested”说明当作已独立复现成功。课程、额外随机化及控制器不能仅凭任务名互换。上游命令是不同学习问题的参考，不能证明 X5 当前 2M 必然足够。
