# Isaac 系操作PPO分册：优先复用什么

本分册源码检查3个项目、7个任务/变体条目（6个奖励与PPO配置可追踪，1个明确负例）、7套有效配置。5种独立物理任务设计是Lift、Cabinet、PegInsert、CubeStack和Keyboard；P0与tutorial记为两个键盘变体，不能当作两个独立成功案例。没有运行上游训练或声称复现成功。

|优先级|设计|对X5的意义|
|---|---|---|
|高|SO101事件FSM+signed progress|最贴近按下、释放、撤离；Actor/Critic均接one-hot|
|高|Factory多尺度关键点|接近与精对齐连续可学，Controller与目标语义明确|
|中|IsaacGym stack gating/max|不同目标的密集奖励替换，松手判据与成功区分|
|中|Lab Lift/Cabinet|真实物体关节/高度进入reward，示例不要求返回|

最重要纠正：SO101 tutorial teacher实际rollout32，因此默认10.24M环境步；不是把base runner的64代入得到20.48M。上游timeout奖励配置注释−2实际被运行时timeout掩码归零。这两点均来自源码配置链，不是训练测量。[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/scripts/tutorial/runtime.py#L25-L30) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/scripts/vision/agent.py#L13-L22) [源码](https://github.com/ooctipus/IsaacLab/blob/6f991d4becf764b151e0a1c775561ddd9c406f72/source/isaaclab/isaaclab/envs/mdp/rewards.py#L43-L70)

详细卡：[so101_typing.md](task_cards/so101_typing.md)、[isaaclab_factory.md](task_cards/isaaclab_factory.md)。
