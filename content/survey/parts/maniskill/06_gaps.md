# 搜索范围、负例与空白

检索日期2026-11-16。Web query：`site.github.com/mani-skill/ManiSkill examples baselines ppo StackCube PegInsertionSide TwoRobotPickCube`；跟进官方PPOREADME、examples.sh、baselines.sh和任务目录。GitHub API首次Python请求SSL失败，curl成功；复用既有相同SHA源码，新增文件从raw.githubusercontent下载，未执行上游Python。

目录树覆盖tabletop、dexterity、digital_twins、mobile_manipulation、humanoid、drawing、FMB和quadruped；候选路径清单保存在source_manifest所指scratch的candidate_paths.txt。选取PickCube、StackCube、PegInsertionSide、TwoRobotStackCube、OpenCabinetDrawer深入，另TurnFaucet与AssemblingKits作负例；没有声称检查完所有注册任务。阀门/拼装只支持sparse，专属调通PPO配置未发现。

遗漏：TriFinger、RotateValve、FMB、人形搬箱、RoboCasa子任务等未在此分卷做公式深追；没有按钮press-hold-release完整验收的ManiSkill案例被本次选定源码证实。旋钮dense公式注释不得充数。

明确冲突：Drawer说明称90%开启，代码75%；双臂Stack文字任务暗示协作撤离，但success没有撤臂/停稳；普通PPO与fast PPO初始logstd不同。所有数值以选定执行文件与CLI覆盖为准。

停止规则：5个实际dense任务覆盖抓放/堆叠/插入/双臂/移动抽屉，并完成2个无dense基线负例，关键reward→success→termination→PPO配置链闭合；扩展更多同型任务的边际价值低于当前X5实验诊断。未取得精确配置绑定的成功率、GPU资源或多seed原始日志，均未知，不能从README示范估计。

计数：1项目；7任务有reward实现检查（5dense、2sparse-only）；5任务有有效任务专属PPO配置，共10配置；所有任务源码本轮只静态分析，没有运行环境或训练。
