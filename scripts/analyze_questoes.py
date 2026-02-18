import json
import sys

try:
    from dados.questoes import QUESTOES
except Exception as e:
    print(json.dumps({"error": f"import failed: {e}"}))
    sys.exit(1)

issues = {"invalid_correta": [], "duplicate_ids": [], "bad_alternativas": [], "summary": {}}

# check duplicates
ids = {}
for i, q in enumerate(QUESTOES):
    qid = q.get("id")
    if qid in ids:
        ids[qid].append(i)
    else:
        ids[qid] = [i]

for qid, positions in ids.items():
    if len(positions) > 1:
        issues["duplicate_ids"].append({"id": qid, "positions": positions})

# check correta validity
for idx, q in enumerate(QUESTOES):
    alt = q.get("alternativas") or {}
    correta = q.get("correta")
    if correta and correta not in alt.keys():
        issues["invalid_correta"].append({"index": idx, "id": q.get("id"), "correta": correta, "alternativas": list(alt.keys())})
    # check alternativas keys
    if not alt or not isinstance(alt, dict) or len(alt) < 2:
        issues["bad_alternativas"].append({"index": idx, "id": q.get("id"), "alternativas": alt})

issues["summary"]["total_questions"] = len(QUESTOES)
issues["summary"]["duplicate_count"] = len(issues["duplicate_ids"])
issues["summary"]["invalid_correta_count"] = len(issues["invalid_correta"])
issues["summary"]["bad_alternativas_count"] = len(issues["bad_alternativas"])

print(json.dumps(issues, ensure_ascii=False, indent=2))
