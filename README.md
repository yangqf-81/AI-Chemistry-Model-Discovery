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

| 实践层次 | 公开提供的内容 | 使用条件 |
|---|---|---|
| [00 基础分子预测](notebooks/00_分子预测基础实验.ipynb)与[01 分子表示](notebooks/01_化学问题与分子表示.ipynb) | PubChem小样本、ECFP4＋逻辑回归训练评价、分子图读取 | 安装依赖后可运行 |
| [02 GNN与N2V比较](notebooks/02_GNN与N2V模型比较.ipynb) | 历史结果分析代码与讨论任务 | 历史结果由课程团队另行提供；GNN/N2V训练实现不在本仓库中 |
| [03 定义模型搜索问题](notebooks/03_定义模型搜索问题.ipynb) | 离线策略检查和搜索问题卡 | 公开部分可运行；真实历史提案为可选材料 |
| [04 搜索评价与科学判断](notebooks/04_模型评价与科学判断.ipynb) | 历史搜索结果核验方法与讨论任务 | 需另配历史结果；在线搜索需平台账号、额度、接口及评价器 |

公开基础实验帮助学生理解结构、预测和评价；GNN＋N2V案例用于提出模型融合问题，伐谋实践用于设计与开展模型策略搜索。教师可根据课题资料与平台条件组合这些活动。

## 运行公开基础示例

`data/example/`随仓库提供96条训练记录和32条验证记录，独立取自[PubChem公开活性数据](https://pubchem.ncbi.nlm.nih.gov/bioassay/743139)。在已安装Python及依赖的环境中，于仓库根目录运行：

```bash
python -m pip install -r requirements.txt
python src/molecular_baseline.py --train data/example/train.csv --validation data/example/validation.csv --output outputs/public-example
```

结果写入`outputs/public-example/`。此小样本用于演示建模流程，抽样时提高了阳性比例，其指标不能代表完整实验数据的预测性能。来源、标签、划分与哈希见[数据说明](data/README.md)和[source_manifest.json](data/example/source_manifest.json)。已保存的真实运行示例见[参考输出](examples/public_baseline/README.md)。

Notebook另需安装`requirements-notebooks.txt`中的依赖。00、01默认使用公开样本；03的离线配置与问题卡无需账号或历史资料。02、04的历史数据保存在本地`examples/internal_historical/`，不随Git仓库提供；内部课题数据`data/internal/`同样不公开。[运行指南](docs/running.md)逐项说明操作方法。

### 自选课题的数据获取

可从[PubChem](https://pubchem.ncbi.nlm.nih.gov/)或其他公开资源检索、下载分子结构和活性数据，参见[官方数据下载说明](https://pubchem.ncbi.nlm.nih.gov/docs/downloads)和[BioAssay说明](https://pubchem.ncbi.nlm.nih.gov/docs/bioassays)。按[字段说明](data/README.md)整理结构、标签、记录编号和scaffold分组，记录来源、下载日期及标签规则，再划分训练与评价数据。程序支持符合格式的自选数据，不要求固定样本数。

## 研究记录与学习评价

使用[阶段简短记录](templates/stage-process-record.md)、[学期档案](templates/semester-journal.md)、[搜索问题卡](templates/search-problem-card.md)和[方案选择与评价](templates/freeze-and-validation.md)保存过程。教师依据材料开展指导，学生保留反馈采纳、修订或否决及依据。开发评价支持策略迭代，冻结后的保留评价用于检验结论。

课程过程记录可直接使用Markdown日志。[36节点图谱](docs/knowledge-map.md)连接知识、实践与能力；[资源来源](docs/resource-sources.md)列明教学材料和研究案例的来源。

## 许可

原创代码采用[MIT License](licenses/MIT.md)，原创教学文档、图谱与模板采用[CC BY 4.0](licenses/CC-BY-4.0.md)。公开数据、第三方依赖和百度平台服务分别遵循原有条款，适用范围见[许可说明](LICENSE.md)。
