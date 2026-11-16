# Stack, reward_shaping=True explicit variant

源码版本：`5ce6643f3092639d08f7b0f90ed1c6a84f50552c`。结论为静态源码核验，未运行上游训练。

## 任务接口与验收

{
  "control_dt_s": 0.05,
  "action": "Robot and controller selectable; no single fixed action dimension",
  "success_definition": "cubeA lifted above table+.04m, cubeA-cubeB contact, not grasped"
}

[br_robosuite_termination](https://github.com/ARISE-Initiative/robosuite/blob/5ce6643f3092639d08f7b0f90ed1c6a84f50552c/robosuite/environments/base.py#L527-L548)；[br_robosuite_stack_defaults](https://github.com/ARISE-Initiative/robosuite/blob/5ce6643f3092639d08f7b0f90ed1c6a84f50552c/robosuite/environments/manipulation/stack.py#L144-L174)；[br_robosuite_stack_success](https://github.com/ARISE-Initiative/robosuite/blob/5ce6643f3092639d08f7b0f90ed1c6a84f50552c/robosuite/environments/manipulation/stack.py#L485-L493)

## 实际奖励

`reward_scale/2 * max(.25(1-tanh(10d))+.25 I_grasp, I_lift*(1+.5(1-tanh(d_xy))), 2 I_lift_and_contact_and_not_grasp)`

[br_robosuite_stack_reward](https://github.com/ARISE-Initiative/robosuite/blob/5ce6643f3092639d08f7b0f90ed1c6a84f50552c/robosuite/environments/manipulation/stack.py#L223-L323)

## 训练配置

未找到已核验的任务专属 PPO 配置；不以通用 PPO 默认值补空。

## 证据缺口

- No task-specific tuned PPO config located
- No dwell or speed limit in stack success
