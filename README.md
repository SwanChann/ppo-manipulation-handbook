# 机械臂操作 PPO 源码手册

用中文阅读开源操作任务的阶段事件、奖励公式和生效训练配置，覆盖 ManiSkill、Isaac Lab、SO101 typing 与 MuJoCo Playground 等项目。调查基于 2026-11-16 的固定源码版本，未执行上游训练，未知参数与复现缺口保留在正文。

- [在线阅读](https://swanchann.github.io/ppo-manipulation-handbook/)
- [本地首页](site/index.html)：下载仓库后用浏览器直接打开，无需联网或启动服务。
- [完整源码任务卡](content/survey/02_task_taxonomy.md)：查看成功、终止、观测、动作、奖励与配置。
- [覆盖与缺口](content/survey/06_gaps.md)：区分静态源码核验和策略复现。

首页提供任务搜索、阶段示意、配置详情和采样轮数计算器。完整 HTML 附录保留公式和固定版本的源码链接。网页没有外部字体、CDN 或分析脚本。

## 构建

`content/survey/` 保存公开的调查 Markdown 与 JSONL，`content/start.html` 保存阅读首页。`scripts/build.py` 生成 `site/`，构建只需要 Python 与 `requirements.txt` 中的依赖。

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python scripts/check.py
```

GitHub Pages 从 `gh-pages` 分支的根目录发布 `site/` 内容。浏览器中的交互自检入口为 `site/index.html?verify=1`，检查结果写入页面的 `verification-results` JSON 节点。

## 资料边界

公开内容为技术文档、结构化证据和网页构建文件。原始实验数据、权重、运行日志和本地源码缓存不在仓库内。正文中涉及本地实验附件时明确标为未公开；调查里的实验描述是当时的快照。

第三方项目的源码和资产继续遵循各自许可。本手册引用上游源码链接，未打包其完整仓库或资产。项目与许可信息见 [repositories.jsonl](content/survey/data/repositories.jsonl)。
