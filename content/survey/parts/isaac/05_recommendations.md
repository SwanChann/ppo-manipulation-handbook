# 对现有X5研究的复用边界

当前200万步任务不应因本调研中途同时更换reward、算法或仿真。先验证延长训练是否改善近距撤离和正常起点按下；源码经验进入候选实验，而不是直接制造多个联合变量。

优先复用SO101的工程机制：物理按键事件、滞回锁存、one-hot给Actor和Critic、阶段切换差分置零、按下后关掉seek项。X5已有相近实现，要以实际源码diff证明新增了什么，不能把已具备的机制再命名为改进。[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/mdp/commands/fixed_cartesian_typing_commands.py#L191-L343) [源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/source/so101_typing/tasks/mdp/rewards.py#L137-L271)

若正常起点依旧无法正确接触，候选假设是几何对齐梯度不足：借鉴Factory的多尺度关键点，固定其他变量观察正常起点有效按下率及碰撞；若按下率不升，假设被否证。若按下后仍推，应先检查动作/阶段输入的实际轨迹，再比较signed-progress与其他门控设计，不能只增大撤回权重。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/factory/factory_env.py#L405-L485)

上游没有一个本分册示例同时要求X5的有效按下100ms、快速重复尝试失败、返回初态并停稳150ms。因此保留当前独立验收，不能借鉴更弱终点来“提高成功率”。SAC、替换OrcaGym与新增纯视觉限制均不是本分册结论。
