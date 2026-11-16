# 搜索与边界（2026-11-16）

搜索：MuJoCo Playground PandaPickCubeCartesian PPO github；quadruped arm manipulation PPO RoboDuet；PKU-MARL DexterousHands PPO；Gymnasium-Robotics Fetch reward PPO；robocasa reinforcement learning PPO。主项目来自官方GitHub与论文链接，扩展了种子之外Playground与RoboDuet。

源码固定四库SHA，保存在 records/rl/ppo_survey_sources_20261116/breadth。部分GitHub API README抓取SSL EOF，已改用浏览器官方项目页作overview。Gymnasium-Robotics README快照成功，不据此宣称源码reward已核验。未运行任何上游代码/安装依赖/下载训练资产。git浅克隆带来的仓库自带资源未执行。

停止点：主生态与benchmark/trainer/mobile/dexterous角色完成宽扫描，优先深查最接近本地阶段奖励的任务，并补充双手任务。没有证明穷尽；RoboDuet有效配置、RoboCasa开关场景reward、Playground新SO101源码链仍是明确缺口。没有新增targeted pass零收益证据，因此本片只能称有限覆盖，不称所有项目已找完。

Popularity只作为生态影响判断，没有编造星标排名或强行设阈值。四个trainer仅作算法实现来源，不重复计算任务。Meta-World的task-ID one-hot是跨任务身份，不等于单个按钮任务的时序阶段one-hot。

定向检索新增收益、当前计数及剩余范围见[targeted_pass.md](targeted_pass.md)。
