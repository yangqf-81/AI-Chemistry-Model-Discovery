# 百度伐谋模型搜索实践

本环节训练学生把模型开发问题转化为明确的搜索任务。学生定义问题、策略空间、评价规则与预算；伐谋提出候选；可信程序执行训练和评价；学生结合反馈比较方案，选定后开展保留评价。

## 资源与操作

- `candidate_example.py`：教师提供的合法策略配置，供理解候选的表达方式。
- `prepare_task_example.py`：读取配置、检查字段，生成待接入评价器的任务说明。
- `examples/internal_historical/l6_proposals.csv`：L6真实提案记录。
- 同目录 `l6_trajectory.csv` 和 `l6_system_metrics.csv`：候选评价及反馈。
- `notebooks/03_定义模型搜索问题.ipynb` 和 `04_模型评价与科学判断.ipynb`：问题设计与案例分析入口。

```bash
python famou/prepare_task_example.py famou/candidate_example.py
python src/historical_case.py
```

任务准备示例在本地运行，输出配置和需要学生设计的字段。在线执行环节由课程与平台安排账号、接口、额度和评价器绑定；历史回放按真实记录组织分析。实验档案分别记载本地执行、平台执行及历史分析。

## 学生的主要工作

解释可搜索策略与研究问题的关系；说明哪些条件保持一致；设计预算和停止办法；比较候选与失败；用证据说明选择。开发反馈用于继续探索，选定方案后的保留评价用于形成结论。
