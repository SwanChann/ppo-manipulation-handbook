# 项目角色与版本

ManiSkill 是基于 SAPIEN/PhysX 的任务环境套件，包含自带 CleanRL 风格 PPO 脚本，不是 Stable-Baselines3 的任务集合。此分卷复用先前审计的固定版本 `62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3`，避免混合新旧实现。源码Apache2.0；资产各自许可不随源码许可自动继承。

官方 `examples.sh` 给出调通且偏向 walltime 的命令；`baselines.sh` 提供比较配置和三个种子。它们是不同配置集合，不能选择示例的总步数再拼接baseline的并行数宣称官方配置。PPO支持必须逐任务判断：TurnFaucet、AssemblingKits只有sparse，不能据全仓库支持PPO就补造dense/PPO结果。

[示例命令与注释](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/examples.sh#L1-L26)；[baseline入口](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/examples/baselines/ppo/baselines.sh#L3-L24)；[许可](https://github.com/mani-skill/ManiSkill/blob/62ff3a5896b4d5b4cf0ac4c8d79afe600c9404a3/LICENSE#L1-L3)。
