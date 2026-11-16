# 覆盖、冲突与未验证事项

本轮筛查15个候选仓库，源码深查8个项目，建立19条任务记录、17个任务奖励记录、14个任务的专属配置记录。计数按合并后的JSONL唯一ID生成；[coverage.json](data/coverage.json)和[source文件清单](source_manifest.json)保存本次证据版本。上游训练复现次数为0。

“有专属配置”包含局部解析完成的记录；Playground的Brax依赖默认值仍有null，不能称所有参数均已核实。按配置记录状态统计，12个任务/变体的参数链标为verified-from-code，另2个Playground任务的依赖默认值未完全解析。完整成功率、训练时长和显存没有同条件原始日志支撑时均未知。本报告没有从演示视频、reward上限或配置预算编造性能。

|检索面|实际覆盖|证据入口|
|---|---|---|
|环境与任务注册|ManiSkill tabletop/mobile/dexterity目录；Isaac Lab manager/direct；Playground当前与rss2025分支|[ManiSkill范围](parts/maniskill/06_gaps.md)、[Isaac分卷](parts/isaac/06_gaps.md)|
|奖励与时序|抓放、堆叠、插入、抽屉、键盘、按钮、双手传递|各任务卡及rewards.jsonl|
|算法角色|SB3、RSL-RL、skrl、CleanRL概览；任务集成中的RL-Games|[扩展检索](parts/breadth/discovery_and_gaps.md)|
|专项扩展|SO101 typing、Playground、RoboDuet；追加Bi-DexHands深查|[定向补查](parts/breadth/targeted_pass.md)|
|负例|ManiSkill TurnFaucet/AssemblingKits无已核验dense PPO；Lab Stack配置rewards=None|对应负例任务卡|

检索结合“manipulation PPO”“contact-rich”“button/press/release”“insertion/assembly”“bimanual”“quadruped arm”等组合，跟进官方GitHub任务树、示例命令和原论文/项目链接。每路具体查询、来源与取舍保存在分卷缺口记录。没有采用星标阈值或编造热度排名。

## 版本与源码冲突

- SO101教程覆盖rollout为32，纠正此前teacher20.48M估计；以实际入口链为准。
- SO101依赖fork与官方Lab所选release不同；manager计算与终止函数必须按实际依赖追踪。
- ManiSkill Drawer说明90%但代码75%；只报告执行阈值。
- ManiSkill部分任务dense函数只有注释；不据注释提供公式配置。
- Playground主干与rss2025任务是不同实现；Brax默认未完全固定。
- 配置出现动作惩罚、timeout罚或完成奖励，不代表执行时一定计入；实际计算链差异保存在相应任务卡。

停止点是完成本轮高相关任务的证据链和一个额外dexterous/mobile定向pass。该pass发现新价值，因此**尚不能声称追加检索已无收益，也没有穷尽所有操作任务**。未深入的任务包括更多阀门/旋钮/电缆、FMB、RoboCasa组合、灵巧手旋转与RoboDuet完整训练链；这些是明确后续覆盖项，不用相似任务参数填补。

专项Skill的严格校验检查JSON引用、字段、SHA链接与报告章节，不执行上游仿真、不验证策略性能。最终校验输出见[validation.txt](validation.txt)，人工复核包括配置入口覆盖、公式单位、奖励与success分离以及引用目标。诚实保留的warning不冒充已补齐。
