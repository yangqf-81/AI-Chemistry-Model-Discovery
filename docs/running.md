# 本地运行指南

## 1. 运行环境

基础实验使用Python3.12、RDKit、NumPy、SciPy和scikit-learn，依赖版本见 `requirements.txt`；Conda基础环境配置见 `environment.yml`。Notebook另使用 `requirements-notebooks.txt`。图谱已经提供PNG与SVG，`requirements-figures.txt`仅在重新绘图时使用。

本指南记录课程团队使用配套教学数据的本地运行方式。Git仓库目前提供代码和字段说明，不含下表中的数据与历史结果文件；相关示例需先另行准备输入，再在仓库根目录、对应Python环境中执行。

## 2. 准备输入

| 路径 | 内容 | 使用环节 |
|---|---|---|
| `data/internal/train.csv` | 2,000条真实分子训练样本 | 基础模型训练 |
| `data/internal/validation.csv` | 1,000条真实分子验证样本 | 基础预测与指标评价 |
| `data/internal/source_manifest.json` | 来源、抽样规则与输入校验信息 | 核对数据版本 |
| `examples/internal_historical/` | M0/M1比较、L6提案、评价轨迹及来源索引 | 历史案例分析 |

本地工作目录已配置这些资料，运行说明记录现有示例的输入与操作方式。仓库以教学展示和方法借鉴为主，公开示例可使用小规模数据；完整课题数据及未发表研究记录保留在本地，不作为共享仓库的必备内容。相关目录由Git忽略。文件格式见[数据说明](../data/README.md)与[案例说明](../examples/README.md)。

## 3. 使用配套教学数据运行基础模型

以下命令以已取得并配置配套数据为前提；自行准备数据时，将训练与验证路径替换为实际路径。

```bash
python -m pip install -r requirements.txt
python src/molecular_baseline.py --train data/internal/train.csv --validation data/internal/validation.csv --output outputs/baseline
```

程序将SMILES转换为ECFP4指纹，训练逻辑回归分类器，对验证样本预测，屏幕显示AP、AUROC及样本信息；输出 `outputs/baseline/metrics.json` 和 `predictions.csv`。该练习无需伐谋账号，帮助学生熟悉真实分子的建模与评价。

输入应包含 `canonical_smiles`、`label`、`record_id`、`generic_scaffold_id`。程序检查训练与验证之间的记录、分子和scaffold交叉，遇到无效结构、缺少类别等情况给出错误，按原数据与划分核对后再运行。

## 4. 分析真实搜索案例

```bash
python src/historical_case.py
python famou/prepare_task_example.py famou/candidate_example.py
```

第一条命令读取历史M0/M1与L6资料，核对并汇总既有评价记录；第二条命令解析策略配置，显示搜索任务需要定义的字段。它们分别是历史案例分析和本地配置准备，具体在线运行由课程按实际账号、额度与评价器安排。

## 5. 使用Notebook

安装 `requirements-notebooks.txt` 中的依赖，在对应Python内核中打开 `notebooks/`，按00至04顺序从上到下运行。工作目录可为仓库根目录或 `notebooks/`，代码会定位资源根目录。

每份Notebook开头列明输入、运行方法和预期输出。00为基础模型实验；01读取分子结构；02分析M0/M1历史结果；03定义搜索问题；04分析历史搜索与评价。教学任务和提交物见[学生实践指南](student-guide.md)。

## 6. 教学使用

教师按[32学时计划](course-schedule.md)安排基线、比较、搜索设计和评价。学生使用[阶段记录](../templates/stage-process-record.md)保存行动、证据、认识变化和下一步，教师结合材料指导并评定。过程日志可直接采用Markdown，基础实验和案例分析均不依赖个人反馈服务器。
