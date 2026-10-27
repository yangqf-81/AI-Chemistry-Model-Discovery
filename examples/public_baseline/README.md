# 公开小样本的实际运行输出

该目录保存使用`data/example/`公开样本实际运行基础程序得到的结果。运行命令：

```bash
python src/molecular_baseline.py --train data/example/train.csv --validation data/example/validation.csv --output outputs/public-example
```

运行日期：2026-10-27；Python3.12.3、RDKit2024.03.2、NumPy1.26.4、scikit-learn1.6.1。训练96条、验证32条；AP＝0.4061820064，AUROC＝0.5729166667。

`metrics.json`保存输入哈希、环境和指标，`predictions.csv`保存公开验证样本的真实预测。小样本经过教学抽样和阳性富集，指标用于说明如何读结果，不代表完整实验数据的模型性能。这些输出不包含未发表课题的模型结果。
