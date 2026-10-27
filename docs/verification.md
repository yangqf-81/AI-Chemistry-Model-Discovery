# 核心程序与Notebook验收记录

日期：2026-10-27。对象为无需伐谋账号的基础分子预测练习，**不是GNN的M0/M1验收、L6复现或学生教学效果验证**。

## 已执行的检查

| 项目 | 实际结果 |
|---|---|
| 命令行基础程序 | 成功读取数据、训练ECFP4＋逻辑回归、预测并导出指标及逐记录结果 |
| 输入数据 | AID_560原Search26划分内分层无放回抽样，seed=42；2,000训练/1,000验证，阳性30/15；抽样在训练前固定 |
| 数据边界 | 本次样本通过记录、分子和scaffold跨侧交叉检查 |
| 指标 | 验证AP=0.0379490864，AUROC=0.6278849408，阳性比例0.015；仅描述本次技术样本 |
| 自动检查 | 3项通过：等价SMILES重复、缺少类别、scaffold跨侧重叠均能被拒绝 |
| Notebook结构 | 使用nbformat校验，Notebook含3个代码单元 |
| Notebook实际执行 | nbclient启动项目本地Jupyter内核，3个代码单元全部执行，无单元错误；保留执行后Notebook和验证JSON |
| 命令行与Notebook一致性 | 已比较两个metrics.json全部字段相同，两个predictions.csv逐字节相同 |
| 文档入口 | 已检查资源库Markdown相对链接，未发现失效目标 |
| Git边界 | 内部数据、运行输出、虚拟环境被忽略；没有远程地址或上传 |

测试环境：Windows，本机Python3.12.3、RDKit2024.03.2、NumPy1.26.4、SciPy1.15.2、scikit-learn1.6.1；Notebook依赖nbclient0.11.0、nbformat5.11.1、ipykernel7.4.0。

Notebook依赖安装在本项目`.venv`中，通过system-site-packages复用既有RDKit环境；没有修改原科研代码或其Python环境。Jupyter在受限执行环境中启动未返回结果，停止该次检查后，经允许的本地回环通信执行成功。未将这一结果扩大为全新环境安装或跨平台兼容验证。

## 本地结果位置

- `outputs/baseline/metrics.json`、`predictions.csv`：命令行结果。
- `outputs/notebook-baseline/metrics.json`、`predictions.csv`：Notebook结果。
- `outputs/00_分子预测基础实验.executed.ipynb`：保留真实单元输出的Notebook。
- `outputs/notebook-verification.json`：实际内核执行摘要。
- `data/internal/source_manifest.json`：原始文件、抽样规则与哈希。

上述文件均为内部运行产物，不默认提交公开Git仓库。命令行运行与Notebook执行脚本均已提供，可供后续按已批准数据重复验收。

## 尚未覆盖

最终教学课题及其公开数据获取方式、GNN/N2V运行入口、伐谋实时接口、全新环境安装、GitHub远程发布、GitHub Pages/Codespaces均未在本次基础验收中完成。不能据本记录宣称整个申报技术资源已经验收完毕。
