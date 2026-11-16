# IsaacGymEnvs FrankaCubeStack：完成奖励替换密集奖励

固定`aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3`。GitHub在2026-11-16查询为archived，保留设计经验，不建议为X5改用旧Isaac Gym。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/__init__.py#L1-L114)

令`A`为抬起判据`z_A−table_height−size_A>.04`，`R_reach=1−tanh(10(d_tcp+d_l+d_r)/3)`，`R_align=A*(1−tanh(10||p_B−p_A+[0,0,(size_A+size_B)/2]||))`：

`r=16`若stack，否则`r=.1*max(R_reach,R_align)+1.5A+2R_align`。

这是条件门控和终端覆盖，Actor没有FSM one-hot。`max`避免接近目标物与把目标物运向放置点两种距离直接相加；lift后才启用alignment。没有乘dt。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L703-L747) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/cfg/task/FrankaCubeStack.yaml#L1-L61)

stack=水平误差<2cm、目标高度误差<2cm、TCP离物体>4cm。最后一项是**几何松手代理**，不等于接触力证明已经释放；没有连续稳定时间，满足即reset，或300step超时。绝不能直接将其终点条件移植成按钮的撤回停稳验收。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L703-L747)

默认OSC 7维（6维末端增量+二值夹爪），[.1,.1,.1,.5,.5,.5]缩放；19维物体/末端/夹爪状态，无相机。物理dt=.01667、2substeps，控制FrequencyInv默认1；物理substeps不是独立动作步。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L630-L656) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L153-L164) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/franka_cube_stack.py#L450-L458) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/cfg/task/FrankaCubeStack.yaml#L1-L61) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/tasks/base/vec_task.py#L106-L114)

入口 `python isaacgymenvs/train.py task=FrankaCubeStack headless=True`。8192env×32rollout×10000max_epochs=2,621,440,000配置上限，不能写成需要26亿才能成功。每批262144，minibatch16384/5epochs，lr5e−4 adaptive/KL.008、gamma.99、GAE.95、clip.2、entropy0、critic_coef4；共享256/128/64 ELU，无RNN；输入/value归一化，seed42。[源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/cfg/train/FrankaCubeStackPPO.yaml#L1-L71) [源码](https://github.com/isaac-sim/IsaacGymEnvs/blob/aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3/isaacgymenvs/cfg/config.yaml#L1-L40)

可复用：对前后目标进行门控或替换，而非全部同时用正距离奖励；释放需要独立可观测物理条件。本轮没有执行此基线或复核其公开成功率。
