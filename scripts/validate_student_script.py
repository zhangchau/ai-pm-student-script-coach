#!/usr/bin/env python3
"""Validate an AI PM student interview-script Markdown deliverable.

This is a lightweight structural checker. It does not judge factual truth; it
checks that the output exposes facts, coverage, question families and honesty
boundaries instead of producing only polished prose.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path, help="Markdown file to validate")
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"ERROR: file not found: {args.file}")
        return 2

    text = args.file.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    body = text.lstrip()
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2].lstrip() if len(parts) == 3 else body
    if not body.startswith("#"):
        errors.append("missing Markdown title")
    if "[TODO" in text or "TODO:" in text:
        errors.append("unresolved TODO placeholder")

    critical_sections = {
        "fact/evidence ledger": ("事实与证据台账", "事实台账", "证据台账"),
        "question map": ("面试问题地图", "问题地图", "问题族"),
        "coverage audit": ("能力覆盖检查",),
        "honesty boundary": ("不能说过头", "事实红线", "待补证据"),
    }
    for label, terms in critical_sections.items():
        if not contains_any(text, terms):
            errors.append(f"missing {label}")

    recommended_sections = {
        "script preparation gap audit": ("逐字稿准备清单", "缺口诊断"),
        "self introduction": ("自我介绍",),
        "project narrative": ("项目主线", "项目展开"),
        "technical pressure test": ("技术专项", "技术压力", "技术链路", "技术证据"),
        "metric/Bad Case evidence": ("指标", "Bad Case", "Trace"),
        "M15 metric audit": ("M15", "分子", "分母", "Ground Truth", "优化前", "对照"),
        "Web/Vibe/AI Coding": ("Web Coding", "Vibe Coding", "AI Coding", "Coding 产物"),
        "AI industry judgment": ("行业判断", "行业宏观", "目标公司含义", "反证条件"),
        "learning/self-drive": ("学习闭环", "自驱", "主动发现", "行为改变"),
        "behavioral stories": ("失败", "冲突", "行为面"),
        "commercial/adoption": ("商业", "采纳", "购买者", "预算"),
        "job fit/transfer": ("岗位匹配", "迁移", "30/60/90"),
    }
    for label, terms in recommended_sections.items():
        if not contains_any(text, terms):
            warnings.append(f"missing or weak {label}")

    technical_groups = {
        "retrieval/document": ("RAG", "检索", "Chunk", "Rerank"),
        "prompt/model/orchestration": ("Prompt", "结构化输出", "模型路由", "Workflow", "Agent"),
        "eval/trace/production": ("Eval", "评测", "Trace", "灰度", "回滚"),
        "security/responsible AI": ("安全", "权限", "隐私", "公平", "注入", "污染"),
    }
    for label, terms in technical_groups.items():
        if not contains_any(text, terms):
            warnings.append(f"technical group not covered or marked N/A: {label}")

    numeric_claim_visible = bool(
        re.search(r"\d+(?:\.\d+)?\s*%", text)
        or contains_any(text, ("准确率", "召回率", "命中率", "效率提升", "成本降低", "降本"))
    )
    if numeric_claim_visible:
        metric_fields = {
            "numerator": ("分子",),
            "denominator/exclusions": ("分母", "排除项"),
            "sample/slices": ("样本", "切片"),
            "time window/cycle": ("周期", "时间窗口"),
            "ground truth": ("Ground Truth", "金标准"),
            "baseline/comparison": ("优化前", "基线", "对照"),
            "attribution": ("归因",),
            "guardrails": ("护栏", "覆盖率", "拒答率"),
        }
        for label, terms in metric_fields.items():
            if not contains_any(text, terms):
                warnings.append(f"numeric claim visible but M15 field missing: {label}")

    if not contains_any(
        text,
        ("已验证事实", "候选人主张", "设计目标", "方案假设", "外部基准"),
    ):
        warnings.append("claim status labels are not visible")
    if not re.search(r"\bM[0-7]\b", text):
        warnings.append("no M0-M7 project maturity label found")
    if not re.search(r"\bE[0-4]\b", text):
        warnings.append("no E0-E4 evidence label found")

    question_count = len(
        re.findall(r"(?m)^(?:#{1,4}\s*)?(?:题\s*\d+|(?:\d+\.\s*)?问题族(?:\s|[:：]))", text)
    )
    if question_count == 0:
        warnings.append("no numbered question or question-family heading detected")

    print(f"Validated: {args.file}")
    print(f"Detected question families/items: {question_count}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    if errors:
        print(f"RESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    print(f"RESULT: PASS ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
