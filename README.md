# AI辅助模型开发与优化

## 面向化学分子活性预测的项目制实践

以一个实际化学课题贯穿四川大学《化学人工智能实践》32学时完整课程。资源形态：04实践项目；适用课程类型：人工智能+X（化学）。

> **核心问题：为什么给模型增加信息，并不一定改善预测？当人工设计的融合方式收益不稳定时，如何让AI帮助探索模型策略，并由人判断结果是否可信？**

本资源以GNN+Node2Vec真实科研案例为基础，让学生从模型使用者进一步成为模型开发问题的设计者和评价者。课程团队负责化学问题、教学设计与实施，百度伐谋团队提供技术支持。

这是本地建设版本，尚未发布GitHub远程仓库。正式教学任务、数据公开范围及伐谋教学接口仍需完成交付核验；不得据此描述为已完成的学生实践成果。

## 从这里开始

| 使用者 | 阅读入口 |
|---|---|
| 评审与教师 | [正式实践项目教学方案](docs/teacher-guide.md) |
| 查看完整课时安排 | [32学时课程安排](docs/course-schedule.md) |
| 学生 | [学生实践指南](docs/student-guide.md) |
| 评价者 | [教学评价量规](docs/assessment.md) |
| 浏览教学图谱 | [36节点知识／能力图谱](docs/knowledge-map.md) |
| 资源建设团队 | [交付与验收清单](docs/delivery-checklist.md) |
| 检查实际运行范围 | [核心程序与Notebook验收记录](docs/verification.md) |
| 运行基础实验 | [无需伐谋账号的分子预测实验](notebooks/00_分子预测基础实验.ipynb)及下方命令 |
| 了解伐谋角色 | [伐谋实践说明](famou/README.md) |

## 五阶段学习任务

1. 从真实课题提出分子活性预测任务，理解分子图与化学空间参考信息。
2. 比较M0与M1，基于实际结果提出融合优化问题，不预先指定胜者。
3. 设计AI可探索的策略范围、评价目标、约束和预算。
4. 利用伐谋提出候选，由执行程序训练并反馈评价，保留不同结果。
5. 结合对照、异常与验证形成结论，说明证据能支持到哪里。

教学只需一个实际课题及必要对照，不要求学生复做31体系。L6是主要科研案例，完整多体系研究和复杂审计为教师拓展材料。

## 无需伐谋账号的基础实验

先完成一个轻量的分子预测与评价程序：**ECFP4分子指纹＋逻辑回归**。它是运行环境和评价概念的基础实验，**不称为GNN的M0，也不替代GNN/N2V比较或伐谋搜索**。

Python 3.12环境中的参考命令：

```bash
python -m pip install -r requirements.txt
python src/molecular_baseline.py --train data/internal/train.csv --validation data/internal/validation.csv --output outputs/baseline
python -m unittest discover -s tests -v
```

CSV须包含 `canonical_smiles`、`label`（0或1）、`record_id`、`generic_scaffold_id`。训练与验证数据分别提供，程序会检查分子、记录和scaffold交叉。数据说明见 [data/README.md](data/README.md)。本机内部样本只用于技术验收，默认不进入Git；公开版本需补获准分发的数据或按源站规则获取数据的步骤。当前仓库不是已经满足公开下载即运行条件的最终包。

环境版本取自本机实际检查；只将实际运行过的环境列入验收记录，不声称跨平台验证完成。

运行Notebook时另装 `requirements-notebooks.txt`。自动执行验收入口为 `python scripts/verify_notebook.py`，它使用当前解释器启动项目本地Jupyter内核，不向系统注册全局内核；执行结果保存在Git忽略的 `outputs/`。教学内容方案和交付状态与程序运行记录分别维护。

## 目录与交付层次

```text
docs/          教学方案、学生指南、考核与交付清单
notebooks/     学习与运行入口
src/           可运行的基础预测与评价代码
famou/         平台角色、接入边界与历史流程说明
data/          数据格式及来源说明；内部样本默认不提交
examples/      真实结果说明与资源选编
tests/         数据边界与核心计算的检查
environment.yml / requirements.txt
```

正式申报使用固定版本快照，附清单和版本号。GitHub Pages、Codespaces为后续可选项，基础实验不依赖它们；不使用GitHub Classroom。

## 开放与许可状态

本目录按开放教学资源组织，但代码、教学文字、科研结果、数据与平台服务的授权分别确认。**当前未授予统一开源许可**；原始科研包、账号信息、密钥和受限资产不进入公开仓库。见 [许可与来源状态](docs/licensing.md)。
