# 模型比较与搜索案例

案例来自GNN＋N2V项目的L6研究记录，包括M0/M1比较、伐谋候选提案、开发评价轨迹与方案确认。基础程序的实际运行结果另由 `outputs/baseline/` 保存。

| 文件 | 内容 |
|---|---|
| `internal_historical/m1_systems.csv` | 26体系M0/M1及L6比较 |
| `internal_historical/l6_proposals.csv` | 30条原始提案记录及状态 |
| `internal_historical/l6_trajectory.csv` | 20个评价候选的反馈轨迹 |
| `internal_historical/l6_system_metrics.csv` | 520个候选×体系评价记录 |
| `internal_historical/l6_top5.csv` | 五个候选的确认比较 |
| `internal_historical/validation5.csv` | 五个选择留出体系的评价案例 |
| `internal_historical/source-index.json` | 原包成员与文件校验信息 |

运行 `python src/historical_case.py` 可读取案例并核对评价轨迹。Notebook按课程阶段组织问题提出、搜索设计和评价讨论。

资料均标注为历史研究。Validation5相对L6搜索和选择留出，研究历史暴露及体系内部评价安排随案例说明保留。学生据此学习如何说明评价范围，并为本组实验设计适当对照和验证。
