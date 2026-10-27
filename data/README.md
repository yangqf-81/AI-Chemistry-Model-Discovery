# 分子预测基础数据

基础程序使用AID_560现有Search26训练、验证划分中的样本。训练侧2,000条，其中阳性30条；验证侧1,000条，其中阳性15条。样本在模型训练前按原类别比例分层无放回选取，随机种子42，保留原划分边界。

| 字段 | 含义 |
|---|---|
| canonical_smiles | 分子结构 |
| label | 当前任务的二分类标签0或1 |
| record_id | 记录身份 |
| generic_scaffold_id | 预先确定的scaffold分组 |

程序将分子结构转换为ECFP4指纹，在训练侧拟合分类器，对验证侧预测并计算AP、AUROC，同时检查两侧记录、分子和scaffold的交叉。

资料包的 `internal/train.csv`、`internal/validation.csv` 可用于基础实验；`internal/source_manifest.json` 记录来源、抽样规则和校验信息。该样本帮助学生学习预测与评价，具体课题问题由小组结合课程研究方向确定。

资料来源与共享安排见资源来源说明；教学数据与代码按各自来源分别管理。
