# 双手与移动操作补充检索

本轮从原筛查中的Bi-DexHands选取ShadowHandOver，完成奖励、成功/重置、动作/观测、任务配置、PPO构造与训练循环追踪，新增1个有源码依据的任务配置。它显示成功事件与奖励bonus的触发条件不同，且配置中的动作惩罚没有进入实际奖励。详细证据以[任务卡](task_cards/bidexhands__ShadowHandOver.md)为准。

RoboDuet官方[README](https://github.com/locomanip-duet/RoboDuet/blob/a7e1528215c048199f90cb69ceb7749a1d745f28/README.md#L58-L75)提供4096环境的训练示例，使用Isaac Gym Preview4。其[部署段](https://github.com/locomanip-duet/RoboDuet/blob/a7e1528215c048199f90cb69ceb7749a1d745f28/README.md#L155-L158)明确列出Go1/Go2与ARX5，适合作为狗背全身协同控制方向的候选。该资料没有为本次按钮任务提供完整操作验收，reward和有效PPO配置尚未深查，仍属documented-only。

当前分片共筛查11仓库，深入源码4仓库，奖励核验5任务，3任务找到专属PPO配置（共4种配置）。Panda的Brax未解析依赖默认值仍保留null；ShadowHandOver已追到本仓库PPO默认值。计数可用data/*.jsonl重建，新增深查没有新增仓库候选。

这次targeted pass产生了新价值，因此不能声称检索达到“再检索无新增价值”的穷尽停止点。移动操作详细reward、RoboCasa开关操作、Playground新SO101训练链仍列为缺口。完整克隆checkout耗时较长，已在提取所需源码后停止本次git clone；核验文件位于records/rl/ppo_survey_sources_20261116/breadth/bidex_extract，未执行第三方代码。
