# 本仓库的学习入口

本 fork 增加了一套用 Harness 方法学习 Harness 的流程。
课程开发命令与原有结构仍见 [CLAUDE.md](CLAUDE.md)。

## 开始一次学习

1. 读 [learning/README.md](learning/README.md)。
2. 从用户的私有记录读取 `Harness_Learning_State.json`。在 ChatGPT 中先查找并读取这份文件的当前版本；本地使用者显式提供其路径。
3. 仓库的 `learning/state.example.json` 只是模板，绝不能当作学习者真实进度。
4. 若真实记录不可用，明确说明；不要从聊天印象重建已通过的课程。可以先提供当前题目，保留待核实状态。
5. 按当前单元读取原文及验收目标；不要每次重读全部教材。

## 执行与验证

- 每次只推进一个学习目标。用户负责解释、判断和应用；助手承担查资料、操作文件、反馈和交接。
- 助手备课、学习者能力展示、原项目运行是三种不同成果。
- 只有真实学习者产物和基于证据的审阅才能支持 `demonstrated`；助手示范与模拟回答不能冒充学习者证据。
- 最多两轮反馈；仍有困难时缩小题目或记录阻塞。等待用户回答时停止，不生成用户答案刷进度。
- 新证据显示旧理解失效时，改为 `needs_recheck`。过去通过并非永久掌握。
- 检查器仅检查结构与证据记录是否齐全，不判定人是否理解。
- 不自动创建定时任务，不运行原课程实验，除非当前学习任务明确要求。

## 保存与边界

- `learning/course.json` 是课程目标的来源；私有状态文件是学习进度的唯一来源；handoff 存在同一私有文件中。
- 真实回答、成绩、个人经历、私有文件链接不得默认提交到这个公开仓库。
- 私有进度修改时保留原文件身份和版本，保存后再宣布已记录；失败时明确指出。
- 本次用户授权的学习改动只涉及入口和 `learning/`；不改变上游教材与应用代码。
- 具体产品命令使用前核对官方当前文档；已知教材问题见 [learning/KNOWN_ISSUES.md](learning/KNOWN_ISSUES.md)。

## 检查命令

```sh
python3 learning/check.py
python3 learning/check.py --state /absolute/private/path/Harness_Learning_State.json
```
