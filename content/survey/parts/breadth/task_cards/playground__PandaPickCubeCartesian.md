# PandaPickCubeCartesian (RSS2025)

源码版本：`56420458c8d81acd6942779d9dab327382117175`。结论为静态源码核验，未运行上游训练。

## 任务接口与验收

{
  "control_dt_s": 0.05,
  "sim_dt_s": 0.005,
  "action": "3: delta y, delta z, gripper; Cartesian IK",
  "success_definition": "state: box-target Euclidean distance<.05m; vision: absolute z difference<.05m"
}

[br_playground_pick_task](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick_cartesian.py#L45-L80)；[br_playground_pick_reward](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick_cartesian.py#L338-L421)；[br_playground_pick_action](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick_cartesian.py#L280-L337)；[br_playground_wrapper](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/wrapper.py#L89-L132)

## 实际奖励

`r=max(S_t-M_(t-1),0); M_t=max(S_t,M_(t-1)); first step r=0; S=clip(4(1-tanh(5d_gb))+8 I_reached(1-tanh(5(.9d_bt+.1e_rot)))+.25 I_no_floor,-1e4,1e4)+.5 I_z>.05+2 I_success; state-only adds -.0005||a-a_prev||-.01 I_no_IK`

[br_playground_pick_reward](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick_cartesian.py#L338-L421)；[br_playground_pick_base](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick.py#L187-L248)；[br_playground_pick_task](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/_src/manipulation/franka_emika_panda/pick_cartesian.py#L45-L80)

## 训练配置

入口（未执行）：`cd rss2025 && python learning/train_jax_ppo.py --env_name=PandaPickCubeCartesian`

```json
{
  "normalize_observations": true,
  "action_repeat": 1,
  "discounting": 0.97,
  "unroll_length": 10,
  "num_updates_per_batch": 8,
  "seed": 1,
  "gae_lambda": null,
  "clipping_epsilon": null,
  "value_hidden_layer_sizes": [
    256,
    256,
    256,
    256,
    256
  ],
  "value_obs_key": "state",
  "policy_obs_key": "state",
  "num_envs": 1024,
  "num_minibatches": 8,
  "batch_size": 256,
  "learning_rate": 0.0005,
  "entropy_cost": 0.0075,
  "reward_scaling": 0.1,
  "policy_hidden_layer_sizes": [
    256,
    256
  ],
  "max_grad_norm": 1.0,
  "num_timesteps": 5000000
}
```

[br_playground_configs](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/config/manipulation_params.py#L24-L110)；[br_playground_entry](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/learning/train_jax_ppo.py#L186-L249)

入口（未执行）：`cd rss2025 && python learning/train_jax_ppo.py --env_name=PandaPickCubeCartesian --vision`

```json
{
  "normalize_observations": false,
  "action_repeat": 1,
  "discounting": 0.97,
  "unroll_length": 10,
  "num_updates_per_batch": 8,
  "seed": 1,
  "gae_lambda": null,
  "clipping_epsilon": 0.3,
  "value_hidden_layer_sizes": [
    128,
    128,
    128
  ],
  "value_obs_key": "state",
  "policy_obs_key": "state",
  "num_envs": 1024,
  "num_minibatches": 8,
  "batch_size": 256,
  "learning_rate": 0.001,
  "entropy_cost": 0.01,
  "reward_scaling": 1.0,
  "policy_hidden_layer_sizes": [
    128,
    128,
    128
  ],
  "cnn_output_channels": [
    16,
    32
  ],
  "num_timesteps": 10000000
}
```

[br_playground_vision_config](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/mujoco_playground/config/manipulation_params.py#L177-L226)；[br_playground_entry](https://github.com/google-deepmind/mujoco_playground/blob/56420458c8d81acd6942779d9dab327382117175/rss2025/learning/train_jax_ppo.py#L186-L249)

## 证据缺口

- Brax dependency defaults for GAE/clip not pinned here
- No executed baseline evaluation
