# 项目与版本

|项目|固定修订|定位|维护/使用边界|
|---|---|---|---|
|Isaac Lab|3c6e67bb5c7ada942a6d1884ab69338f57596f77 (v2.3.0)|环境套件+多训练器接入|选择稳定发布做对照，不宣称最新main|
|IsaacGymEnvs|aeed298638a1f7b5421b38f5f3cc2d1079b6d9c3|历史GPU RL任务|2026-11-16 API archived=true；保留设计，不作为新部署栈|
|NVIDIA/so101-typing-task|7aec2ed26dce8c88ae007a2714680cce572e1466|专项键盘任务|Newton MJWarp、独立Docker/runtime祖先，不能套Lab2.3的依赖|

本机快照和SHA256见`source_manifest.json`；repo metadata在records/rl/ppo_survey_sources_20261116/isaac。Lab当次8657 stars，GymEnvs2949；只作影响力佐证，不据stars断言某个任务PPO成功。SO101未建立stars记录。检查的源码均BSD-3-Clause，外部USD、机器人资产许可需独立按来源处理。

角色区分：RSL-RL/RL-Games是trainer，任务reward由环境定义。Cabinet注册三个trainer只证明集成存在，不代表三种同预算基线等价。[源码](https://github.com/isaac-sim/IsaacLab/blob/3c6e67bb5c7ada942a6d1884ab69338f57596f77/source/isaaclab_tasks/isaaclab_tasks/direct/franka_cabinet/__init__.py#L17-L27) SO101运行时依赖明确固定另一IsaacLab fork祖先及patch，不与此分册Lab2.3代码混用。[源码](https://github.com/NVIDIA/so101-typing-task/blob/7aec2ed26dce8c88ae007a2714680cce572e1466/docker/typing-public.Dockerfile#L4-L18)

