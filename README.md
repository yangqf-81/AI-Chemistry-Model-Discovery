# AI辅助模型开发与优化

## 面向化学分子活性预测的项目制实践

本资源服务于四川大学《化学人工智能实践》课程。课程为32学时学期制纯实践课程，采用分组课题制。本项目展示一个GNN＋N2V与百度伐谋课题小组从选题、建模到自动优化和科学评价的完整实践过程。

**学习主线：从“运行已有模型”，走向“定义模型开发任务、开展人机协同探索、依据证据形成判断”。**

项目以“增加信息为什么未必改善预测”为切入点，结合真实模型比较，引导学生设计搜索空间、评价规则与预算，理解AI候选、可信执行和评价反馈如何共同支持模型开发。

## 教学与实践入口

| 内容 | 入口 |
|---|---|
| 项目教学设计 | [教师指导与教学设计](docs/teacher-guide.md) |
| 学期实施 | [32学时、16次活动与五个检查点](docs/course-schedule.md) |
| 学生任务 | [项目任务书](docs/project-brief.md)与[实践指南](docs/student-guide.md) |
| 知识与能力关系 | [图谱及关系说明](docs/knowledge-map.md) |
| 学习评价 | [考核量规](docs/assessment.md) |
| 研究过程记录 | [学期档案](templates/semester-journal.md)、[搜索问题卡](templates/search-problem-card.md)、[方案选择与评价](templates/freeze-and-validation.md) |

## 分阶段实践

| 入口 | 主要活动 |
|---|---|
| [00 分子预测基础实验](notebooks/00_分子预测基础实验.ipynb) | 用分子指纹和逻辑回归完成预测与指标评价 |
| [01 化学问题与分子表示](notebooks/01_化学问题与分子表示.ipynb) | 读取真实分子数据，解释分子图和化学空间图 |
| [02 GNN与N2V模型比较](notebooks/02_GNN与N2V模型比较.ipynb) | 分析M0/M1真实历史结果，提出优化问题 |
| [03 定义模型搜索问题](notebooks/03_定义模型搜索问题.ipynb) | 设计空间、目标、预算和评价规则，读取历史提案 |
| [04 模型评价与科学判断](notebooks/04_模型评价与科学判断.ipynb) | 回放L6提案与反馈，解释方案选择和保留评价 |

基础程序可在本地运行，使用Python、RDKit和scikit-learn。模型比较与搜索案例采用真实历史研究资料；伐谋任务示例展示配置准备过程。课程可根据平台条件安排在线实践，并在研究记录中注明运行方式与资料来源。

## 快速开始

在解压后的本目录运行：

```bash
python -m pip install -r requirements.txt
python src/molecular_baseline.py --train data/internal/train.csv --validation data/internal/validation.csv --output outputs/baseline
python src/historical_case.py
python famou/prepare_task_example.py famou/candidate_example.py
```

Notebook环境另安装 `requirements-notebooks.txt`。`scripts/verify_notebook.py`验证基础实验，`scripts/verify_learning_notebooks.py`验证四份分阶段Notebook。基础实验已在Python3.12.3、RDKit2024.03.2、scikit-learn1.6.1环境运行；详见环境文件。

提交资源包中的 `data/internal/` 为基础分子预测样本，`examples/internal_historical/` 为案例数据。通过Git获取资源时，数据按课程提供的资料包配置；[数据说明](data/README.md)和[案例说明](examples/README.md)列明格式、来源与使用方式。

## 课程协作与成果

五阶段分别形成课题说明、模型比较、搜索问题卡、候选档案、验证与研究报告。每个检查点保存学生提交、教师反馈及学生回应，学期档案记录问题、策略和判断的变化。开发评价支持策略迭代，冻结后的保留评价用于检验结论。

四川大学课程团队负责化学问题、教学设计与组织实施，百度伐谋团队提供技术支持。资源按GitHub仓库结构组织教学文件、代码、实验记录与案例，便于版本管理和教学使用。

## 资源目录

`docs/`教学文件；`notebooks/`实践入口；`src/`核心代码；`famou/`任务示例；`data/`分子数据；`examples/`真实案例；`templates/`过程与评价记录；`assets/`图谱及可编辑源；`requirements*.txt`和`environment.yml`环境依赖。

[资源来源说明](docs/resource-sources.md)记录教学文字、代码、数据和研究案例的来源。
