# 分子预测示例数据

## 公开样本

`example/train.csv`与`example/validation.csv`随仓库提供，分别包含96条记录（24条阳性）和32条记录（8条阳性）。它们独立取自PubChem公开的[芳香化酶抑制活性汇总实验AID 743139](https://pubchem.ncbi.nlm.nih.gov/bioassay/743139)，与本地未发表课题的数据及划分分开。

标签直接来自`Activity Outcome`：Active记为1，Inactive记为0。仅使用明确标签，移除冲突标签、无效结构和重复结构；结构通过PubChem CID取得，并用RDKit规范化。筛选未使用模型分数。

候选池按来源记录顺序选择96个活性CID与288个非活性CID。按generic Murcko scaffold字符串的SHA256前8位对4取余分组：0归验证侧，其余归训练侧，再按固定数量选取示例。无环分子统一为ACYCLIC组。训练和验证之间不共享分子、记录或scaffold。具体规则、来源接口、下载日期与文件哈希见[source_manifest.json](example/source_manifest.json)。

小样本为教学演示提高了阳性比例，不代表原实验的活性比例，也不用于评价GNN/N2V或伐谋的科研效果。

## 字段

| 字段 | 含义 |
|---|---|
| canonical_smiles | RDKit规范化分子结构 |
| label | 当前任务的二分类标签0或1 |
| record_id | 唯一记录编号 |
| generic_scaffold_id | generic Murcko scaffold分组摘要 |
| pubchem_cid | PubChem化合物编号，便于回溯公开来源 |
| source_activity_outcome | 原始Active／Inactive标签 |

基础程序读取前四项；后两项保留来源线索。程序构建ECFP4指纹，在训练侧拟合逻辑回归，对验证侧预测并计算AP和AUROC；输入检查包括无效结构、重复记录、类别和跨划分交叉。

## 自行获取数据

可从[PubChem](https://pubchem.ncbi.nlm.nih.gov/)或其他公开资源选择适合教学问题的数据。参见[下载说明](https://pubchem.ncbi.nlm.nih.gov/docs/downloads)与[BioAssay说明](https://pubchem.ncbi.nlm.nih.gov/docs/bioassays)。先阅读实验说明、确定标签含义，再关联结构与活性记录，整理为必需字段并记录来源、下载日期及清理规则。

`internal/`为课程团队的本地研究资料，由Git忽略。完整课题数据与未发表结果继续在本地管理。公开样本按原数据来源条款使用，参见[NCBI数据使用政策](https://www.ncbi.nlm.nih.gov/home/about/policies/)，不纳入团队对原创代码或教学文字的授权。
