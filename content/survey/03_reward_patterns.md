# 可复用奖励设计及其适用条件

奖励按何种条件激活，与Actor能否看到这个条件，是两个独立问题。下列公式来自任务卡指向的固定源码；布尔指示记作I，距离使用各任务代码中的单位。跨项目复制权重前必须确认归一化、控制周期与终止语义。

## 当前物理条件的分段覆盖

[ManiSkill StackCube](parts/maniskill/task_cards/StackCube-v1.md)依次覆盖同一个reward变量，而非把前后阶段全相加：

```text
r = 2(1 − tanh(5 d_tcp,A))
if grasped: r = 4 + 1 − tanh(5 d_A,goal)
if on_top:  r = 6 + (ungrasp + 1 − tanh(10||v_A|| + ||ω_A||))/2
if success: r = 8
r_normalized = r/8
```

抓住后目标变为放置，叠好后目标变为松手和物块停稳；前段接近项被覆盖。当前物理状态可以回退，代码未锁存FSM。对按钮，首次按下后又释放属于不同历史，单看当前位置不能区分“尚未按过”，因此仍需保留事件记忆。

这是适合本项目参考的“目标切换”写法，但该式基座4/6会形成分段跳变。不能将其说成势函数差分，或保证任何初始化下更容易学习。检验方式是在同一独立验收下观察切换前后动作方向与阶段驻留，而不是只比较Return。

## 接触前先做几何门控

[ManiSkill PegInsertionSide](parts/maniskill/task_cards/PegInsertionSide-v1.md)中，G为当前抓住，d_h/d_c为销头/销中心相对于孔轴的横向误差：

```text
r = [1 − tanh(4 d_tail) + G
     + 3G(1 − tanh(0.5(d_h+d_c)+4.5 max(d_h,d_c)))
     + 5G I(d_h<0.01 ∧ d_c<0.01)(1 − tanh(5||head_in_hole||))]/10
```

成功时覆盖为1。双点误差隐含姿态对齐；不是仅让一个末端点靠近目标。接近项仍持续相加，所以这与StackCube的互斥覆盖不同。对本地按钮可复用“法向、横向对齐后才强奖励深入”的结构，但只有证据表明当前瓶颈是对齐时才实施。

[Factory PegInsert](parts/isaac/task_cards/isaaclab_factory.md)采用同时启用的多尺度关键点项。令d为关键点平均距离，S(a,b,d)=1/(exp(−ad)+b+exp(ad))，则r=S(5,4,d)+S(50,2,d)+S(100,0,d)+I_engaged+I_success。粗尺度提供远处梯度、细尺度区分末端误差；它依赖局部已抓取初态，不能替代完整流程。

## 历史事件、阶段与一次性进度

[SO101 P0](parts/isaac/task_cards/so101_typing.md)有SEEK_PRESS、RELEASE_KEY、CLEARANCE三个事件状态。Actor与Critic均包含one-hot；切换步令进度为零，按下后关闭seek进度。事件阈值使用真实按键关节行程，历史按键完成状态不会随释放清除。

其signed progress形如clip((d_previous−d_current)/scale,−1,1)，只在同目标同阶段计算；事件额外发放一次性奖励。对于本地任务，这对应“向目标推进”与“有效按下发生”的分离。详细有效系数与上游timeout配置的执行差异，以SO101任务卡为准，不能仅复制配置里的weight。

## 历史最高分与势函数差分

[Playground PickCartesian](parts/breadth/task_cards/playground__PandaPickCubeCartesian.md)定义当前综合分数S_t与回合历史最高分M，使用r_t=max(S_t−M_(t−1),0)，M_t=max(M_(t−1),S_t)。在同一回合内重复进退不能反复领取同一高度的正进度，但回退本身不扣分。该任务还含引导初态，不能把学习效率全部归因于奖励。

一般势函数塑形为F(s,s′)=γΦ(s′)−Φ(s)。若Φ=−D，则F=D(s)−γD(s′)；它与普通D(s)−D(s′)不同。策略不变性需要相同折扣、完整状态以及相容的终止边界处理。理论依据为[Ng、Harada、Russell的原论文](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)。这里只解释数学差别；本地v6的切换步清零、门控signed progress和高水位算法均不能直接宣称满足该保证。

选择建议：若要对退步直接扣分，signed progress比高水位更直接；若要压制往返刷正分，高水位提供一种候选。是否有奖励利用行为必须由轨迹验证，不能只靠公式猜测给现有失败归因。

## 时间尺度和独立验收

Isaac Lab manager路径将weight×term再乘control_dt，Direct任务不会自动套同样规则，详见[Lab Lift](parts/isaac/task_cards/isaaclab_lift.md)和[Factory](parts/isaac/task_cards/isaaclab_factory.md)。把manager权重原封不动移到每步求和环境会改变实际量级。一次性事件若经过dt缩放，也必须按有效结果比较。

需要保留的反例包括：抽屉开足却未停稳时已经拿到满奖励；双臂Stack奖励右臂让位，但success没有验收让位；Bi-DexHands成功指标与bonus触发条件不同。它们分别由[Drawer](parts/maniskill/task_cards/OpenCabinetDrawer-v1.md)、[双臂Stack](parts/maniskill/task_cards/TwoRobotStackCube-v1.md)、[ShadowHandOver](parts/breadth/task_cards/bidexhands__ShadowHandOver.md)源码支持，属于静态语义差异，不是本轮已执行的reward hacking实验。

本地验收继续独立检查真实按压、连续保持、释放、20mm撤离、返回完整初态、速度与150ms连续停稳，数值来自冻结任务配置（本地实验附件，未随手册公开）及其base_task_config。阶段编号不直接判成功；一直压住、重复按压和不按直接返回不能因reward高而通过。
