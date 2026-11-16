# 任务类型与详细卡

|任务|类别|奖励|本分卷证据|
|---|---|---|---|
|PickCube-v1|grasp-place|normalized_dense|[源码任务卡](task_cards/PickCube-v1.md)|
|StackCube-v1|grasp-place|normalized_dense|[源码任务卡](task_cards/StackCube-v1.md)|
|PegInsertionSide-v1|insertion-assembly|normalized_dense|[源码任务卡](task_cards/PegInsertionSide-v1.md)|
|TwoRobotStackCube-v1|bimanual|normalized_dense|[源码任务卡](task_cards/TwoRobotStackCube-v1.md)|
|OpenCabinetDrawer-v1|mobile-manipulation|normalized_dense|[源码任务卡](task_cards/OpenCabinetDrawer-v1.md)|
|TurnFaucet-v1|articulated|sparse|[源码任务卡](task_cards/TurnFaucet-v1.md)|
|AssemblingKits-v1|insertion-assembly|sparse|[源码任务卡](task_cards/AssemblingKits-v1.md)|

五类dense任务都包含真实物体/关节状态成功判定，部分抓取判定还用双指接触力方向。但它们的“完成”并不等于按钮完整返回停稳：StackCube要求物体松开且静止，Peg只看插入头几何，双臂Stack不验收撤臂姿态。按任务验收语义比较，不能仅比较success键值。默认20Hz动作、100Hz物理；没有把“部署机器人上有相机”转换成必须纯图像的额外要求。
