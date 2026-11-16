# ManiSkill：TurnFaucet-v1

版本 `62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3`；检索日期2026-11-16。

本卡是源码与有效配置静态取证（`verified-from-code`），不是本机复现实验；未下载任务资产、未安装 ManiSkill、未执行训练。配置属于上游该 SHA，不直接替换 X5/OrcaGym 的控制器、任务验收或 PPO 参数。

默认物理 100 Hz、控制 20 Hz，即每个 policy step 含 5 个物理子步；奖励每控制步计算，没有额外乘 dt。单臂 Panda 使用 `pd_joint_delta_pos`：7 维相对当前关节位置的增量（归一化动作裁剪并映射至 ±0.1 rad）加 1 维绝对夹爪开度目标（−0.01 至 0.04 m）；双臂动作展平成 16 维。Fetch 还包含 body 关节增量与底盘前进/转向速度，不能当成同一 8 维接口。

[频率定义](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/utils/structs/types.py#L78-L89)；[Panda动作](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/robots/panda/panda.py#L90-L98)；[增量基准](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/controllers/pd_joint_pos.py#L81-L98)；[Fetch组合控制](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/robots/fetch/fetch.py#L219-L257)。

## 任务、观测与验收

Robot：`panda_wristcam`；episode上限 200 控制步（10 s）。[注册与默认构型](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/turn_faucet.py#L23-L58)。

actual joint angle > qmin+.9(qmax-qmin), infinite qmax uses pi/2; no hold。[实际 evaluate/obs 实现](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/turn_faucet.py#L183-L202)。

标准 state 策略输入机器人 qpos/qvel/controller state，加各任务 TCP、物体、目标及相对几何等 extras；本卡所查五个 dense 任务没有阶段 one-hot 或锁存阶段观测。[状态组合](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/sapien_env.py#L547-L559)；[本体字段](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/agents/base_agent.py#L339-L348)。

训练默认成功即终止并局部 reset；评估默认忽略 success termination，直到超时，分别记录 `success_once` 与 `success_at_end`。这两者都不等于本项目“按下 / 撤回 / 返回 / 连续停稳”的独立验收。[BaseEnv termination](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/sapien_env.py#L1050-L1078)；[TimeLimit](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/utils/registration.py#L127-L168)；[评估wrapper](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/vector/wrappers/gymnasium.py#L127-L168)。

## 实际奖励

```text
r=I(actual_angle>target_angle)
```

[奖励源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/sapien_env.py#L673-L697)。其中长度用 m，角速度用 rad/s；S代表上面源码定义的 success，I代表布尔指示量。

此任务只声明 sparse/none。dense reward 整段是注释，且有“finalize” TODO；里面的距离和角度权重不是有效训练配置。本卡只登记执行中的 sparse success 奖励。

success 使用阀门真实关节角，超过目标即成立；没有接触力、连续保持、释放、撤回验收。在已查 examples.sh/baselines.sh 中未发现此任务专属 PPO 命令，因此 config_ids 留空。它可用于电力旋钮资产与状态判定参考，不能列作已提供可复现 dense PPO baseline。

## PPO配置与复现入口

未知：选定版本的 examples.sh 与 baselines.sh 无此任务专属 PPO 命令；不生成假设参数。

## 证据与使用边界

本调查没有取得与上述精确命令绑定的逐seed原始成功率、GPU型号、显存或耗时，均标为未知；不把源码中的奖励上限或官方示例“tested”说明当作已独立复现成功。课程、额外随机化及控制器不能仅凭任务名互换。上游命令是不同学习问题的参考，不能证明 X5 当前 2M 必然足够。
