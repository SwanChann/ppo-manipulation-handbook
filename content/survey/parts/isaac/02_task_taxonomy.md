# 已核查任务卡

|任务|任务物理目标|Actor的阶段输入|完成边界|
|---|---|---|---|
|Lab Lift|抬物到命令目标|无one-hot|无单独完整成功，掉落或超时|
|Lab Cabinet|拉开抽屉|无one-hot|关节开度>.39m即终止|
|Factory PegInsert|预抓住销插孔|无one-hot，LSTM|几何阈值；不释放、不回家|
|GymEnvs CubeStack|抓取、抬起、叠放|无one-hot|高度/水平误差+手离开几何代理|
|SO101 P0|单键按下、释放、离键|三维one-hot给双方|4mm净空2tick，不返回初态|
|SO101 tutorial|13字符随机串|state teacher双方；vision actor本体/RGB/phase，criticstate|15mm净空；完整字符串|
|Lab Stack负例|三块堆叠|不作为PPO调查结论|rewards=None，注册无PPO配置|

详见[isaaclab_lift.md](task_cards/isaaclab_lift.md)、[isaaclab_cabinet.md](task_cards/isaaclab_cabinet.md)、[isaaclab_factory.md](task_cards/isaaclab_factory.md)、[isaacgym_stack.md](task_cards/isaacgym_stack.md)、[so101_typing.md](task_cards/so101_typing.md)、[isaaclab_stack_negative.md](task_cards/isaaclab_stack_negative.md)。任务成功定义不同，不能直接横比上游成功率，更不能将“开启即终止”当作完成我们的撤回停稳任务。
