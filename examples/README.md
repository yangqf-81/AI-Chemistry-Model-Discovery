# 模型比较与搜索案例

## 公开案例节选

[真实模型开发案例节选](real-model-development-case.md)以“研究任务A”呈现M0/M1的3-seed汇总AP和三条固定seed候选的开发评价AP，附信息融合、策略比较、验证边界与科学判断讨论题。两表评价口径不同，不作跨表增益比较。该页可独立阅读，用于历史案例讨论；不替代下列完整历史分析文件。

## 另行提供的完整历史材料

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

## 使用与共享

历史数据用于本地教学案例分析。课题尚未发表，除已核准的公开节选外，完整搜索记录和结果明细保存在Git忽略的 `internal_historical/` 中。共享仓库提供分析方法与代码入口，案例演示可选用经负责人确认的少量片段，不要求公开完整研究结果。
