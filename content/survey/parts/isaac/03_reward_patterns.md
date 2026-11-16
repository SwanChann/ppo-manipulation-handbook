# 有源码依据的奖励模式

1. **条件门控相加**：Lift仅物体z>.04时启用目标跟踪，接近项仍存在；该高度是世界坐标阈值，非从初态抬起4cm。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L67) [源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/lift/lift_env_cfg.py#L95-L222)
2. **密集项max和终端覆盖**：GymEnvs Stack用max(接近,抬起后对齐)，完整stack时整步reward替换为16。避免把末端靠近物体与物体靠近目标简单全部叠加。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L703-L747)
3. **多尺度同时启用**：Factory的三种关键点核并行给梯度，未以FSM切换。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/factory/factory_env.py#L405-L485) [源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/factory/factory_tasks_cfg.py#L68-L132)
4. **事件FSM门控signed progress**：SO101 seek阶段只给接近差分，release/clearance给抬升差分，切换/reset步置零；事件bonus一次性。[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/mdp/rewards.py#L137-L271)

数值移植前必须处理dt：Lab Manager乘control_dt，Direct Cabinet和Factory直接返回总和；SO101实际fork Manager也乘dt。SO101配置6.25的seek权重实际每40ms进度系数是.25。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab/isaaclab/managers/reward_manager.py#L128-L158) [源码](https://github.com/ooctipus/IsaacLab/blob/6f991d4becf764b151e0a1c775561ddd9c406f72/source/isaaclab/isaaclab/managers/reward_manager.py#L129-L159)

反例：SO101配置timeout权重−50，却借助is_terminated_term屏蔽所有time_outs，因此该项有效恒0，failure项在同tick timeout也被屏蔽。这是源码推导，无上游实测。完整公式见键盘卡，不保留错误的“timeout固定扣2”描述。[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/fixed_cartesian_env_cfg.py#L35-L234) [源码](https://github.com/ooctipus/IsaacLab/blob/6f991d4becf764b151e0a1c775561ddd9c406f72/source/isaaclab/isaaclab/envs/mdp/rewards.py#L43-L70)

