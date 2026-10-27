# AI辅助模型开发与优化

## 面向化学分子活性预测的项目制实践

分子活性预测把化学结构与实验结果联系起来，为学生提供一个可以持续提问、建模、比较和验证的真实问题。本项目从“增加信息为什么未必改善预测”出发，带领学生由使用已有模型，走向设计AI模型开发任务并依据证据作出判断。

本资源来自四川大学《化学人工智能实践》课程，面向具备Python、基础机器学习和基本化学结构知识的高年级本科生。课程采用32学时学期制分组实践，各组围绕自己的课题持续开展研究。本资源展示GNN＋Node2Vec与百度伐谋课题小组的完整实施方案。

仓库以教学方案展示、方法借鉴和示例实践为主，提供已在现有环境验证的代码与运行说明。共享资料可选用少量获准公开的示例数据，完整课题数据及未发表研究记录保留在本地。

## 学生怎样开展一个学期的实践

| 阶段 | 学时 | 主要任务 |
|---|---:|---|
| 化学问题与分子表示 | 4 | 明确预测问题，理解分子结构与化学空间信息 |
| 基线比较与问题发现 | 6 | 比较M0/M1，从实际差异提出优化假设 |
| 定义AI模型搜索问题 | 6 | 设计搜索空间、评价规则、预算与停止条件 |
| 人机协同开发与优化 | 10 | 分析AI候选和开发反馈，处理失败并选择方案 |
| 科学评价与交流 | 6 | 检验选定方案，组织证据并形成结论 |

教学贯穿“问题驱动—人机协同—证据导向”。五个检查点保留学生提交、教师反馈及学生回应；阶段记录按“行动—证据—认识变化—下一步”组织。学期结束时，教师结合研究档案、模型比较、方案设计、报告和个人答辩评价学生能力发展。

本实践项目依托四川大学化学科研课题开展教学设计，百度团队提供伐谋平台、计算资源及相关技术支持，支持AI模型策略搜索、实验执行和模型优化实践。

四川大学课程团队负责化学问题、教学设计、学生指导和科学评价。

## 从哪里开始

- **教师**：[教学设计](docs/teacher-guide.md) → [32学时与16次活动](docs/course-schedule.md) → [考核量规](docs/assessment.md)。
- **学生**：[项目任务书](docs/project-brief.md) → [实践指南](docs/student-guide.md) → 下表中的实践入口。

| 实践入口 | 输入与学习产出 |
|---|---|
| [00 分子预测基础实验](notebooks/00_分子预测基础实验.ipynb) | 真实分子样本 → ECFP4＋逻辑回归预测及指标解释 |
| [01 化学问题与分子表示](notebooks/01_化学问题与分子表示.ipynb) | 分子数据 → 两类图与表示的解释 |
| [02 GNN与N2V模型比较](notebooks/02_GNN与N2V模型比较.ipynb) | 历史M0/M1结果 → 模型差异与优化问题 |
| [03 定义模型搜索问题](notebooks/03_定义模型搜索问题.ipynb) | 策略示例与历史提案 → 学生搜索问题卡 |
| [04 模型评价与科学判断](notebooks/04_模型评价与科学判断.ipynb) | 历史L6搜索与评价记录 → 对照分析和结论依据 |

00提供无需伐谋账号的基础模型运行；02—04中的模型比较和搜索结果为真实科研案例分析。伐谋在线实践依课程实际账号、额度和接口安排开展，实验记录分别注明执行和资料来源。

## 在本地开始运行

先打开本仓库目录，在安装了Python及依赖的环境中运行：

```bash
python -m pip install -r requirements.txt
python src/molecular_baseline.py --train data/internal/train.csv --validation data/internal/validation.csv --output outputs/baseline
```

本地目录中的 `data/internal/` 提供基础样本，`examples/internal_historical/` 提供历史案例。两目录按教学使用管理并由Git忽略。阅读教学设计与代码无需完整课题数据；运行相关示例时使用配套示例数据或自行准备符合格式的输入。格式与来源见[数据说明](data/README.md)和[案例说明](examples/README.md)。

### 示例数据与公开数据获取

仓库的数据展示以少量示例为主。开展自己的课题时，可从[PubChem](https://pubchem.ncbi.nlm.nih.gov/)或其他公开数据资源检索、下载分子结构和活性数据；PubChem的下载方式见[官方数据下载说明](https://pubchem.ncbi.nlm.nih.gov/docs/downloads)，活性记录见[BioAssay说明](https://pubchem.ncbi.nlm.nih.gov/docs/bioassays)。

下载后按[数据字段说明](data/README.md)整理SMILES、标签、记录编号与scaffold分组，记录数据来源、下载日期及标签规则，并划分训练与评价数据。公开原始数据与本课题整理后的划分、搜索日志及未发表结果分别管理。

Notebook另使用 `requirements-notebooks.txt` 中的依赖，在对应Python内核中从上到下执行。[本地运行指南](docs/running.md)列出输入、命令、环境及输出位置。

## 研究记录与学习评价

使用[阶段简短记录](templates/stage-process-record.md)、[学期档案](templates/semester-journal.md)、[搜索问题卡](templates/search-problem-card.md)和[方案选择与评价](templates/freeze-and-validation.md)保存过程。教师依据材料开展指导，学生保留反馈采纳、修订或否决及依据。开发评价支持策略迭代，冻结后的保留评价用于检验结论。

课程过程记录可直接使用Markdown日志。[36节点图谱](docs/knowledge-map.md)连接知识、实践与能力；[资源来源](docs/resource-sources.md)列明教学材料和研究案例的来源。
