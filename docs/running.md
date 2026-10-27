# 运行指南

## 1. 环境与公开实验

基础实验使用Python3.12、RDKit、NumPy、SciPy与scikit-learn，版本见`requirements.txt`，Conda配置见`environment.yml`。Notebook另用`requirements-notebooks.txt`；图谱已提供PNG与SVG，重新绘图时才需`requirements-figures.txt`。

在仓库根目录、安装对应依赖的Python环境中运行：

```bash
python src/molecular_baseline.py --train data/example/train.csv --validation data/example/validation.csv --output outputs/public-example
```

公开数据随仓库提供，来源与标签见[数据说明](../data/README.md)。输出为`metrics.json`与`predictions.csv`；[参考输出](../examples/public_baseline/README.md)来自该样本的实际本地运行。自选数据可替换输入路径，需包含`canonical_smiles`、`label`、`record_id`和`generic_scaffold_id`，不限制固定记录数。

## 2. 各Notebook的条件

| Notebook | 所需输入 | 公开仓库中的操作 |
|---|---|---|
| 00 分子预测基础实验 | data/example/train.csv与validation.csv | 运行ECFP4＋逻辑回归、查看指标与输出 |
| 01 化学问题与分子表示 | data/example/train.csv | 读取公开分子及其原子、键信息 |
| 02 GNN与N2V模型比较 | 另配的m1_systems.csv与source-index.json | 阅读分析代码与讨论任务；有材料后运行 |
| 03 定义模型搜索问题 | famou/candidate_example.py | 检查策略与填写问题卡；取得材料后可追加真实提案分析 |
| 04 模型评价与科学判断 | 另配的完整历史结果表与source-index.json | 阅读核验方法与讨论任务；有材料后运行 |

Notebook在对应Python内核中从上到下执行，工作目录可为仓库根目录或`notebooks/`。02、04所需文件见[案例说明](../examples/README.md)，未随公开仓库提供。它们是历史结果分析入口，不执行GNN/N2V训练或在线搜索。

## 3. 离线配置与在线实践

公开的离线配置准备命令无需平台账号：

```bash
python famou/prepare_task_example.py famou/candidate_example.py
```

课程团队另行提供历史材料后，可用以下命令核验历史结果：

```bash
python src/historical_case.py
```

伐谋在线搜索需要实际账号、额度、接口与训练评价器，由课程和平台支持条件安排。离线配置、历史分析与平台执行分别记录，不能将其中一个环节的完成视为另一个环节已执行。

## 4. 教学使用

按[32学时计划](course-schedule.md)组织课题，学生用[阶段记录](../templates/stage-process-record.md)保存行动、证据、认识变化与下一步，教师结合材料指导并评价。过程记录直接使用Markdown，不依赖个人反馈服务器。仓库以教学展示、方法借鉴和示例实践为主，现有环境运行记录不等于新机器安装验证。
