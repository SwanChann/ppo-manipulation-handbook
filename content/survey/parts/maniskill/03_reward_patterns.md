# 可复用奖励模式

记 d 为米制距离，G为当前抓取，S为物理success。StackCube使用分支覆盖：接近 r=2(1−tanh(5d))，抓住后替换为4+放置接近量，叠放后替换为6+(张爪+物体静止)/2，成功置8，最后除8。高阶段关闭低阶段的相反梯度；但它不是进度势能差，也不是单次事件奖励。当前物理条件丢失会回到较低分支。[源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/stack_cube.py#L145-L186)。

PegInsertionSide采用累加门控：接近+抓取，抓住后+3倍双点对齐，抓住且头/中心yz都在10mm内后+5倍插入距离，成功置10，最后除10。该设计并未全关闭早期奖励；必须明确区分两种模式。[源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/peg_insertion_side.py#L300-L360)。

TwoRobotStackCube的中间阶段同时给“上块朝堆叠点”和“右臂朝y=0.2m让位线”奖励。这里能学习让位，不是因为PPO本身有阶段记忆，而是联合状态与当前阶段奖励提供监督信号。其最终success并不包含右臂到达该线。[奖励](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/two_robot_stack_cube.py#L214-L296)；[验收](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/tabletop/two_robot_stack_cube.py#L169-L212)。

OpenCabinetDrawer在开启后把接近项改为常数，但开足时奖励已饱和至成功值，未显式奖励达到静止阈值。这是奖励与验收的潜在空档。对X5，按下后撤回与最终停稳必须保持独立验收和阶段学习信号，不能只按“后阶段基座更高”就断言问题解决。[源码](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/mani_skill/envs/tasks/mobile_manipulation/open_cabinet_drawer.py#L336-L358)。

以上公式完整定义、归一化、条件与数据均在任务卡及data/rewards.jsonl；没有未经源码证明的dt缩放、平滑/能耗/碰撞处罚。这里指出的是代码性质和可测试假设，没有将其称作已观测reward hacking。
