# 扩展任务源码调研结论

本分片筛查11个仓库，4个仓库深入源码，5个任务奖励核验，3个任务找到任务专属 PPO 配置（共4个配置）。有效参数链有未解析 Brax 依赖默认值，标为 partial；未执行上游训练。另有7个仓库只完成官方资料级筛查。

1. Meta-World button-press-v3（默认 reward v2）是按下目标，不是按下保持释放返回。近距离才激活按压奖励，但不是锁存FSM，保持按压可重复获得高奖励。success容差2cm与reward满值5mm不同。可复用门控/容差函数，不能搬成功定义。
2. robosuite Stack把 reach/grasp、lift/align、stack 三组取max，不把所有阶段奖励累加；叠放必须不再抓握且两物块接触。它依据当前物理状态，没有显式锁存one-hot FSM，也没有停稳保持。默认 reward_shaping=False，文中密集式需显式开启。
3. Playground RSS2025 PickCartesian使用历史最高分增量，阻止同一进度反复领奖，但回退不扣分，不具有一般PBRS策略不变性保证。阶段接近锁存只门控物块目标项，接近奖励仍在。源码写入 no_box_collision 位于权重字典构造之后，配置0.05未进入该步sum（静态结论）。
4. Playground PickCartesian仅 y/z/夹爪三维控制，5%重置首步会注入guide_q辅助探索；vision成功只看z，不是三维目标与撤回。本任务更简单的几何不能作为本地按压完整任务的成功证据。
5. Playground OpenCabinet的打开进度和接近奖励持续相加。reached_box锁存但没有进入_get_obs拼接，actor不能直接读取此事件；无显式成功谓词，只有越界/NaN终止和wrapper超时。不能把40m默认步数或高return解释为严格任务完成。

上述具体公式、源码行号与配置见 task_cards/ 和 data/。本次不修改当前本地训练奖励，建议只把设计作为候选单变量对照：若持续进度奖励造成重复动作，比较锁存事件或高水位进度；若阶段切换后仍前进，先测actor可观测性与各阶段样本覆盖。任何替代奖励必须继续使用本地独立验收，不移植上游较弱成功条件。

MuJoCo Playground当前主干已转到PyTorch/reaf-sim/MuJoCo Warp；此次两个Panda任务明确来自rss2025旧JAX目录，不能与主干SO101训练入口混用。当前SO101PickCube只做注册/配置定位，未完成reward链审计，不计入已核验任务。

双手定向补充见[targeted_pass.md](targeted_pass.md)，ShadowHandOver有效奖励与配置由独立任务卡维护。
