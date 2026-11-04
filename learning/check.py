#!/usr/bin/env python3
"""Check learning-record structure, never grade understanding or execute course code.

Optional --source-tree accepts a read-only Git tree snapshot shaped as
{"sha": "...", "paths": ["..."]}; without it, source paths are checked locally.
Private learner records are read only and their answer text is never printed.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [f"L{i:02}" for i in range(1, 15)] + [f"P{i:02}" for i in range(1, 9)]
STATUSES = {"not_started", "awaiting_response", "needs_revision", "demonstrated", "needs_recheck", "blocked"}
ACTIVE = {"awaiting_response", "needs_revision"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(course, state, source_paths):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    require(course.get("schema_version") == state.get("schema_version") == 1, "schema_version 必须为 1")
    require(state.get("state_kind") in {"example", "private_learning_record"}, "未知状态文件类型")
    require(state.get("course_revision") == course.get("source_revision"), "教材版本不匹配")
    units = course.get("units", [])
    progress = state.get("progress", [])
    require(sorted(x.get("id", "") for x in units) == sorted(EXPECTED), "课程必须且只能包含 L01–L14、P01–P08 各一次")
    require(sorted(x.get("unit_id", "") for x in progress) == sorted(EXPECTED), "进度必须且只能覆盖 22 个单元各一次")
    unit_map = {x.get("id"): x for x in units}
    progress_map = {x.get("unit_id"): x for x in progress}
    for unit in units:
        uid = unit.get("id")
        path = unit.get("source_path", "")
        require(path in source_paths, f"{uid}: 教材路径不存在")
        expected_url = f"https://github.com/{course['source_repository']}/blob/{course['source_revision']}/{path}"
        require(unit.get("source_url") == expected_url, f"{uid}: 来源链接未锁定正确版本")
        require(bool(unit.get("learning_goal", "").strip()), f"{uid}: 缺少学习目标")
        require(all(p in EXPECTED and p != uid for p in unit.get("prerequisites", [])), f"{uid}: 前置单元无效")
        if uid in {"P07", "P08"}:
            require(unit.get("original_project", {}).get("code_status") == "docs_only", f"{uid}: 必须说明仅有项目文档")

    require(state.get("limits", {}).get("max_feedback_rounds") == 2, "反馈上限必须为两轮")
    active = []
    demonstrated = 0
    for record in progress:
        uid = record.get("unit_id")
        status = record.get("learning_status")
        require(status in STATUSES, f"{uid}: 未知学习状态")
        rounds = record.get("feedback_rounds")
        require(type(rounds) is int and 0 <= rounds <= 2, f"{uid}: 反馈轮次不合法")
        if status in ACTIVE:
            active.append(uid)
        unit = unit_map.get(uid, {})
        # Prior demonstrations remain historical evidence when a prerequisite
        # needs rechecking. Rechecks can queue without becoming active lessons.
        if status in ACTIVE:
            require(all(progress_map.get(p, {}).get("learning_status") == "demonstrated" for p in unit.get("prerequisites", [])), f"{uid}: 前置单元尚未有演示证据")
        if status == "demonstrated":
            demonstrated += 1
            evidence = record.get("evidence", [])
            independent = [e for e in evidence if e.get("producer") == "learner" and e.get("kind") == "application" and e.get("assistance") == "independent" and e.get("content", "").strip() and e.get("recorded_at")]
            require(bool(independent), f"{uid}: 缺少学习者独立应用的真实记录")
            review = record.get("review") or {}
            require(review.get("verdict") == "pass" and review.get("reviewer_role") == "checker" and bool(review.get("basis", "").strip()), f"{uid}: 缺少有依据的独立审阅")
            for criterion in course.get("review_criteria", []):
                result = review.get("criteria", {}).get(criterion, {})
                require(result.get("met") is True and bool(result.get("reason", "").strip()), f"{uid}: 验收项 {criterion} 缺少证据说明")
        project_status = record.get("original_project_status")
        if uid and uid.startswith("P"):
            require(project_status in {"not_run", "partial", "blocked", "verified"}, f"{uid}: 原项目状态无效")
            if project_status == "verified":
                runs = record.get("original_project_evidence", [])
                valid_runs = [r for r in runs if r.get("kind") == "actual_runtime" and r.get("synthetic") is False and r.get("command", "").strip() and type(r.get("exit_code")) is int and r["exit_code"] == 0 and r.get("output_excerpt", "").strip() and r.get("artifact_ref") and r.get("recorded_at") and r.get("acceptance_review", "").strip()]
                require(bool(valid_runs), f"{uid}: 原项目未有实际运行与验收记录")
        else:
            require(project_status is None, f"{uid}: 讲义单元不应有原项目完成状态")

    require(len(active) <= 1, "一次只能有一个正在推进的学习单元")
    current = state.get("current_unit")
    require(current in EXPECTED or current is None, "当前单元不存在")
    require(not active or active == [current], "当前单元与活动状态不一致")
    if current is not None:
        require(progress_map.get(current, {}).get("learning_status") in ACTIVE | {"needs_recheck", "blocked"}, "当前单元必须待作答、待修改、待复核或受阻")
    handoff = state.get("handoff", {})
    require(bool(handoff.get("last_action", "").strip()) and bool(handoff.get("next_action", "").strip()), "缺少交接动作")
    return errors, demonstrated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / "learning/state.example.json")
    parser.add_argument("--source-tree", type=Path)
    args = parser.parse_args()
    try:
        course = load(ROOT / "learning/course.json")
        state = load(args.state)
        if args.source_tree:
            snapshot = load(args.source_tree)
            if snapshot.get("sha") != course["source_revision"]:
                raise ValueError("来源目录快照版本不匹配")
            paths = set(snapshot["paths"])
        else:
            paths = {u["source_path"] for u in course["units"] if (ROOT / u["source_path"]).is_file()}
        errors, demonstrated = validate(course, state, paths)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"FAIL: 输入文件不可用或格式不符合要求（{type(error).__name__}）。", file=sys.stderr)
        return 1
    if errors:
        for message in errors:
            print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print(f"PASS: 22 个学习单元、来源路径与状态记录结构一致（{state['state_kind']}）。")
    print(f"记录中带独立应用与审阅字段的单元：{demonstrated}/22；当前：{state.get('current_unit')}。")
    print("这不是理解能力评分，也未证明答案真实性、代码运行成功或外链实时可访问。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
