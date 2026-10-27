# 分子预测基础数据

基础程序使用AID_560现有Search26训练、验证划分中的样本。训练侧2,000条，其中阳性30条；验证侧1,000条，其中阳性15条。样本在模型训练前按原类别比例分层无放回选取，随机种子42，保留原划分边界。

| 字段 | 含义 |
|---|---|
| canonical_smiles | 分子结构 |
| label | 当前任务的二分类标签0或1 |
| record_id | 记录身份 |
| generic_scaffold_id | 预先确定的scaffold分组 |

程序将分子结构转换为ECFP4指纹，在训练侧拟合分类器，对验证侧预测并计算AP、AUROC，同时检查两侧记录、分子和scaffold的交叉。

本地目录的 `internal/train.csv`、`internal/validation.csv` 可用于基础实验；`internal/source_manifest.json` 记录来源、抽样规则和校验信息。该样本帮助学生学习预测与评价，具体课题问题由小组结合课程研究方向确定。

## 示例数据与课题数据

共享示例用于展示字段格式、分子表示和预测评价方法，可选取少量获准公开的数据。上述本地样本来自尚未发表的研究，与完整课题资料一并保存在Git忽略目录中，按课程授权范围使用。

资料来源与共享安排见资源来源说明；教学数据与代码按各自来源分别管理。

## 自行获取数据

可从[PubChem](https://pubchem.ncbi.nlm.nih.gov/)或其他公开资源选择适合教学问题的数据。PubChem提供分子及BioAssay记录的检索与下载，参见[下载说明](https://pubchem.ncbi.nlm.nih.gov/docs/downloads)和[BioAssay说明](https://pubchem.ncbi.nlm.nih.gov/docs/bioassays)。

选择任务时先阅读实验说明，明确活性标签的含义；将结构和活性记录按标识关联，整理为上表字段，记录来源、下载日期、清理规则及标签定义。`generic_scaffold_id`需根据分子结构生成；划分训练与评价数据后，再使用基础脚本检查记录、分子和scaffold交叉。公开原始数据可用于自选课题，不等同于本课题已有划分或历史模型结果。
