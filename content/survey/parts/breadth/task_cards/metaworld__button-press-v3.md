# button-press-v3 / reward v2

源码版本：`a14b096edb015ca931e33643a19ea97f4d92eb0f`。结论为静态源码核验，未运行上游训练。

## 任务接口与验收

{
  "action": "4: Cartesian xyz delta .01m, opposing gripper controls",
  "success_definition": "abs(button_y-target_y)<=.02m",
  "termination_definition": "never terminates on success; truncates at500"
}

[br_metaworld_termination](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/metaworld/sawyer_xyz_env.py#L580-L644)；[br_metaworld_button_success](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/metaworld/envs/sawyer_button_press_v3.py#L60-L96)；[br_metaworld_action](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/metaworld/sawyer_xyz_env.py#L175-L193)

## 实际奖励

`2 H(max(obs[3],0),T(d_tcp,[0,.05],d_init)) + 8 I_d_tcp<=.05 T(abs(button_y-target_y),[0,.005],initial_target_gap); H(a,b)=ab/(a+b-ab), zero if denominator zero; T=1 in bounds, otherwise1/(1+9(distance_to_bound/margin)^2)`

[br_metaworld_button_reward](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/metaworld/envs/sawyer_button_press_v3.py#L126-L166)；[br_metaworld_tolerance](https://github.com/Farama-Foundation/Metaworld/blob/a14b096edb015ca931e33643a19ea97f4d92eb0f/metaworld/utils/reward_utils.py#L63-L65)

## 训练配置

未找到已核验的任务专属 PPO 配置；不以通用 PPO 默认值补空。

## 证据缺口

- No task-specific PPO config located in inspected repo
- No dwell/release/retract/repeat detector
