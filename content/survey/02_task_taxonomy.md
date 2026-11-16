# 按任务选择需要复用的环节

接近/抓取、精密接触、释放与恢复属于不同学习问题。以下条目由注册、实现和配置证据建立；没有把一个任务套件的总任务数写成本次全部检查数量。负例也保留，便于识别“有环境但无密集PPO配置”的情况。

|任务|类别|核验状态|配置记录数|证据入口|
|---|---|---|---|---|
|PickCube-v1|grasp-place|verified|3|[任务卡](parts/maniskill/task_cards/PickCube-v1.md)|
|StackCube-v1|grasp-place|verified|2|[任务卡](parts/maniskill/task_cards/StackCube-v1.md)|
|PegInsertionSide-v1|insertion-assembly|verified|2|[任务卡](parts/maniskill/task_cards/PegInsertionSide-v1.md)|
|TwoRobotStackCube-v1|bimanual|verified|1|[任务卡](parts/maniskill/task_cards/TwoRobotStackCube-v1.md)|
|OpenCabinetDrawer-v1|mobile-manipulation|verified|2|[任务卡](parts/maniskill/task_cards/OpenCabinetDrawer-v1.md)|
|TurnFaucet-v1|articulated|verified|0|[任务卡](parts/maniskill/task_cards/TurnFaucet-v1.md)|
|AssemblingKits-v1|insertion-assembly|verified|0|[任务卡](parts/maniskill/task_cards/AssemblingKits-v1.md)|
|Isaac-Lift-Cube-Franka-v0|grasp-place|verified|1|[任务卡](parts/isaac/task_cards/isaaclab_lift.md)|
|Isaac-Franka-Cabinet-Direct-v0|articulated|verified|1|[任务卡](parts/isaac/task_cards/isaaclab_cabinet.md)|
|Isaac-Factory-PegInsert-Direct-v0|insertion-assembly|verified|1|[任务卡](parts/isaac/task_cards/isaaclab_factory.md)|
|FrankaCubeStack|grasp-place|verified|1|[任务卡](parts/isaac/task_cards/isaacgym_stack.md)|
|Isaac-Keyboard-SO101-MX-Physical-Calibrated-20260718-FixedCartesian-AnchorBench-P0|press-switch|verified|1|[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/mdp/rewards.py#L137-L271)、[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/fixed_cartesian_env_cfg.py#L35-L234)|
|VisionIsaacLabPhraseEnvCfg / public tutorial random13 characters|press-switch|verified|2|[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/mdp/rewards.py#L137-L271)、[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/fixed_cartesian_env_cfg.py#L35-L234)|
|Isaac-Stack-Cube-Franka-v0 (negative PPO baseline example)|grasp-place|partial|0|[任务卡](parts/isaac/task_cards/isaaclab_stack_negative.md)|
|PandaPickCubeCartesian (RSS2025)|grasp-place|partial|2|[任务卡](parts/breadth/task_cards/playground__PandaPickCubeCartesian.md)|
|PandaOpenCabinet (RSS2025)|articulated|partial|1|[任务卡](parts/breadth/task_cards/playground__PandaOpenCabinet.md)|
|button-press-v3 / reward v2|press-switch|partial|0|[任务卡](parts/breadth/task_cards/metaworld__button-press-v3.md)|
|Stack, reward_shaping=True explicit variant|grasp-place|partial|0|[任务卡](parts/breadth/task_cards/robosuite__Stack.md)|
|ShadowHandOver / single-agent PPO / egg full_state|bimanual|verified|1|[任务卡](parts/breadth/task_cards/bidexhands__ShadowHandOver.md)|

阅读任务卡时先看成功和episode终止，再看奖励和预算。机器人与动作维度不能只看数字：Playground三维动作含夹爪，X5三维是TCP xyz；SO101五维是关节速度比例。各卡明确控制频率、物理频率和观测，缺失字段保留未知。

## 完整任务卡索引

- [PegInsertionSide-v1](parts/maniskill/task_cards/PegInsertionSide-v1.md)
- [PickCube-v1](parts/maniskill/task_cards/PickCube-v1.md)
- [AssemblingKits-v1](parts/maniskill/task_cards/AssemblingKits-v1.md)
- [OpenCabinetDrawer-v1](parts/maniskill/task_cards/OpenCabinetDrawer-v1.md)
- [TurnFaucet-v1](parts/maniskill/task_cards/TurnFaucet-v1.md)
- [TwoRobotStackCube-v1](parts/maniskill/task_cards/TwoRobotStackCube-v1.md)
- [StackCube-v1](parts/maniskill/task_cards/StackCube-v1.md)
- [isaaclab_lift](parts/isaac/task_cards/isaaclab_lift.md)
- [isaacgym_stack](parts/isaac/task_cards/isaacgym_stack.md)
- [isaaclab_stack_negative](parts/isaac/task_cards/isaaclab_stack_negative.md)
- [isaaclab_factory](parts/isaac/task_cards/isaaclab_factory.md)
- [so101_typing](parts/isaac/task_cards/so101_typing.md)
- [isaaclab_cabinet](parts/isaac/task_cards/isaaclab_cabinet.md)
- [playground__PandaOpenCabinet](parts/breadth/task_cards/playground__PandaOpenCabinet.md)
- [robosuite__Stack](parts/breadth/task_cards/robosuite__Stack.md)
- [playground__PandaPickCubeCartesian](parts/breadth/task_cards/playground__PandaPickCubeCartesian.md)
- [metaworld__button-press-v3](parts/breadth/task_cards/metaworld__button-press-v3.md)
- [bidexhands__ShadowHandOver](parts/breadth/task_cards/bidexhands__ShadowHandOver.md)
