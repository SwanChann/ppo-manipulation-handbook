# 优先复用事件语义、奖励分段和有效配置链

对现有按压任务，SO101 typing最接近“按下后释放撤离”的时序语义；ManiSkill StackCube最清晰地展示后段奖励覆盖前段；Factory PegInsert提供局部接触技能、多尺度对齐与非对称Critic的实现。推荐次序依据任务相关性和源码可追踪性，没有把仓库流行程度当成性能证明。

|优先级|实现|可复用内容|验收差异|
|---|---|---|---|
|1|[SO101 typing](parts/isaac/task_cards/so101_typing.md)|实际按键事件、阶段one-hot、切换步不领进度、按压后奖励目标切换|P0净空结束；不等同X5返回初态并连续停稳|
|2|[ManiSkill StackCube](parts/maniskill/task_cards/StackCube-v1.md)|条件分支覆盖、松手与物体静止共同验收|无锁存FSM，无机器人返回目标|
|3|[ManiSkill PegInsertionSide](parts/maniskill/task_cards/PegInsertionSide-v1.md)|双点几何对齐后才激活插入奖励|成功无需释放/撤回|
|4|[Factory PegInsert](parts/isaac/task_cards/isaaclab_factory.md)|局部初态、多尺度关键点、循环PPO与特权Critic|预先抓住销；不涵盖完整抓取与复位|
|5|[Playground PickCartesian](parts/breadth/task_cards/playground__PandaPickCubeCartesian.md)|历史最高分增量，抑制反复取得同样进度|3维是y/z/夹爪，视觉成功只有高度条件|
|6|[双臂Stack](parts/maniskill/task_cards/TwoRobotStackCube-v1.md)、[Bi-DexHands](parts/breadth/task_cards/bidexhands__ShadowHandOver.md)|联合动作、让位、事件指标与奖励分开审查|奖励涉及的动作不一定全部进入success|

源码比较支持一个明确结论：多阶段操作不必统一采用FSM。可逆抓取/放置常用当前物理条件门控；按键历史在释放后仍影响目标，因此需要锁存状态或等价记忆。把阶段输入与阶段奖励各自写清，比给方案贴“FSM”标签更有用。每种具体实现的证据在上表任务卡。

此前SO101 teacher默认20.48M步的估算需要更正：公开tutorial的runner覆盖为32步/环境，64×32×5000=10.24M；其视觉训练另有teacher与模仿预热。完整配置链见[预算与覆盖](04_training_configs.md)。默认预算不能解读成最少收敛步数，也不能据此承诺本地2M必定成功。

交付覆盖：15个项目筛查、8个项目源码深查、19条任务记录、17个任务有奖励实现检查、14个任务有专属配置记录。配置中未解析的依赖默认值明确保留，详见[缺口](06_gaps.md)。本次只把设计记为候选，正在运行的X5续训没有混入新奖励。
