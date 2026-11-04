# 学习时要区分的方法、示例与实现

依据：课程版本 `a9342ff471f2c0e60be0c08b9f4a7c502df4e442` 的只读核对。这里没有声称已经运行并复现所有代码问题。

| 位置 | 已观察到的限制 | 学习处理 |
|---|---|---|
| 多讲的 TypeScript 演示 | 耗时、成功与失败常由预设数据产生 | 用来理解机制；不可把输出当作模型效果实测 |
| P01 中文实验协议 | 与英文更新不完全同步；英文要求隔离实验目录、防止参考答案泄漏、重置证据 | 真正做对照时核对英文协议和实际脚本 |
| P07/P08 | 项目说明存在；`projects/` 下只有 project-01 至06。P07 说明承诺的 starter/solution 不存在，P08 是设计练习 | 先设计，再自行实现；实现前不标原项目通过 |
| L14 `maker_checker_graph.py` | 模型调用未实现；测试仅检查字符串；“不通过”也含“通过”；重试计数没有更新 | 当作骨架；使用前补真实验证、明确结果格式与停止逻辑 |
| 多份评分/审计脚本 | 多数检查文件、字段或关键词是否存在 | 结构分数与真实工作质量分别报告 |
| 具体产品功能 | 章节与不同语言版本可能存在更新差异 | 实际使用命令前核对对应官方文档与版本 |

学习者不必先修完整个课程仓库。遇到缺口时写明阻塞，选一个最小可用替代练习，并保留原项目未完成状态。

来源入口：

- [实际项目目录](https://github.com/Shenguohong/learn-harness-engineering/tree/a9342ff471f2c0e60be0c08b9f4a7c502df4e442/projects)
- [P07 说明](https://github.com/Shenguohong/learn-harness-engineering/blob/a9342ff471f2c0e60be0c08b9f4a7c502df4e442/docs/zh/projects/project-07-loop-engineering-first-loop/index.md)
- [L14 骨架](https://github.com/Shenguohong/learn-harness-engineering/blob/a9342ff471f2c0e60be0c08b9f4a7c502df4e442/docs/zh/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py)
- [英文 P01 协议](https://github.com/Shenguohong/learn-harness-engineering/blob/a9342ff471f2c0e60be0c08b9f4a7c502df4e442/docs/en/projects/project-01-baseline-vs-minimal-harness/index.md)
