# AI PM Student Interview Script Coach

面向 AI 产品经理学员的、以证据为先的面试逐字稿教练 skill。

它会把简历、PRD、作品集、项目材料、JD、模拟面试记录或既有逐字稿，整理成可复用且不过度包装的面试回答体系。重点覆盖项目、产品、技术、商业、行为面试，以及数据口径、AI Coding、行业判断和学习自驱力。

## 适用场景

- 从零构建 AI 产品经理面试逐字稿
- 审核现有逐字稿的事实冲突、证据缺口与夸大表述
- 从实际项目中预测高概率问题与压力追问
- 面向目标 JD 调整重点，而不虚构经历
- 准备 RAG、Agent、Workflow、AIGC、ChatBI、Eval、私有化部署等项目面试

## 安装

### 方式一：下载 ZIP

在本仓库页面点击 **Code → Download ZIP**。解压后，将整个 `ai-pm-student-script-coach` 文件夹复制到：

`~/.codex/skills/ai-pm-student-script-coach/`

### 方式二：Git 克隆

```bash
git clone https://github.com/zhangchau/ai-pm-student-script-coach.git ~/.codex/skills/ai-pm-student-script-coach
```

重新打开 Codex 后，在对话中输入：

```text
$ai-pm-student-script-coach 帮我根据这份简历和 PRD，搭建真实可信的 AI 产品经理面试逐字稿。
```

## 包含内容

- `SKILL.md`：主工作流、产出标准与边界
- `references/`：覆盖模型、数据与 AI Coding 审计、准备清单、交付模板
- `scripts/validate_student_script.py`：逐字稿 Markdown 校验工具
- `agents/openai.yaml`：Codex 展示与默认提示配置

## 核心原则

该 skill 不会把目标值、外部 benchmark、方案假设或推断写成已经实现的结果。所有重要结论都应有真实的产物、数据、版本记录或用户反馈支持；证据不足时会明确标为 `[待补证据]`。

## 本地校验

在需要检查生成的逐字稿时，可运行：

```bash
python3 scripts/validate_student_script.py <你的逐字稿.md>
```
