# 覆盖与未验证项

检索日期2026-11-16。网络网页检索：`site.github.com isaac-sim IsaacLab factory peg insert PPO reward`、`NVIDIA SO101 keyboard typing reinforcement learning github`；继而从官方任务索引、完整Git树和注册函数展开。重用本项目open_source_multistage_20261116已固定源码，再补齐原始文件、task configs、runner、运行时依赖和Docker配置。

本分册限定3个项目，读了Lab lift/reach/stack/cabinet/factory目录与注册；深挖Lift、Cabinet、Factory PegInsert、GymEnvs Stack、SO101 P0/tutorial。保留Lab Stack作为无PPO reward/config的负例。Reach只扫描，没有做任务卡、不纳入reward深挖数量。Factory GearMesh/NutThread有同runner注册，但未分别追完阈值与reward override，不列为已核查任务。没有检查整个Isaac生态的所有任务，不称穷尽。

状态：`verified-from-code`指固定源码及配置链已经阅读，**不代表运行复现**。没有安装上游、执行任意第三方脚本、加载其权重或验证其成功率。未获得同条件硬件、训练耗时、显存、跨seed统计，全部unknown；不根据默认max_iterations断言实际收敛需要这么久。

SO101专用运行时是ooctipus/IsaacLab@6f991d4加补丁，不是Lab v2.3。已追清reward manager dt和timeout masking；尚未构建容器验证所有动态导入，但该配置缺陷有完整静态链路。此前teacher20.48M错误已在任务卡与配置矩阵更正为10.24M。P0 raw default与tutorial effective budget独立记录。

停止规则：已完成授权分工的高价值五种物理任务、六个配置变体与一个负例，关键公式/验收/有效参数闭合；不额外展开无关论文或装配任务。跨生态广度由总报告合并其他分册，保持遗漏明确。

