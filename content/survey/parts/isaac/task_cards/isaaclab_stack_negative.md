# 负例：Isaac Lab Stack 不等于官方调好的PPO

v2.3.0 `Isaac-Stack-Cube-Franka-v0`注册只有env config，没有PPO配置；IK-Rel注册的是robomimic BC。环境`rewards=None`，有cubes_stacked成功终止。该版本适合示范/模仿学习工作流，不应因它位于Isaac Lab就声称已提供Stack PPO reward或使用其他任务PPO参数补齐。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/config/franka/__init__.py#L30-L60) [源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/stack/stack_env_cfg.py#L139-L179)

这与旧IsaacGymEnvs的`FrankaCubeStack`是两个实现，必须分开统计。此卡未完整展开三层立方体成功函数，因此状态partial，无伪造PPO config。
