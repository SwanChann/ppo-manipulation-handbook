# 对 X5/OrcaGym 的复用建议（未执行干预）

当前已授权续训时保持同一v6设计，不边训练边改reward。先把这轮较长预算的固定评估结果作为下一决策依据。

1. 优先保留并诊断按压事件锁存：ManiSkill堆叠可从当前状态回溯阶段，按钮首次按压是历史事件，不能用“按钮当前释放”还原未按状态。如果实际trace显示phase正确而动作方向仍不变，则否定“只修阶段判定就能解决”的假设。
2. 下一候选可参考StackCube的分支覆盖级差，对比当前“有符号进度+单次事件”的目标。最小实验只改奖励形式，固定终止/课程/网络/预算；预测是有效按压后撤回率提高，而不是只训练return提高。若撤回率不升或重复按压上升，拒绝该干预。
3. 从Peg例子借鉴接触前双点/法向对齐判据，先在现有trace上检验完整初态失败是否集中于对齐不足。若并无此现象，不额外加姿态项。
4. 将右臂让位例子作为“同一policy能学操作后撤开”的源码参考，但仍用本项目20mm撤离、返回初态和连续150ms停稳独立验收。若reward上升而完整率不变，不能算接受。

源码支撑：[覆盖式门控](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/stack_cube.py#L145-L186)；[双点对齐](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/peg_insertion_side.py#L300-L360)；[让位shaping](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/two_robot_stack_cube.py#L214-L296)。

这些都是条件化实验建议，不是新的训练授权，也不改变本轮预算。
