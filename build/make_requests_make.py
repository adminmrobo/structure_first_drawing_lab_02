# -*- coding: utf-8 -*-
"""프롬프트 실습 B 결과 그림 요청 꾸러미(docs/image_requests_make) 만들기 — make_lab.EX가 원본."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from make_lab import EX, a_key
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs", "image_requests_make")
os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
PAGE = {1: "01_standing.html", 2: "02_frills.html", 3: "03_sitting.html", 4: "04_light_dir.html"}
NAME = {"haru": "하루", "sia": "시아", "moa": "모아"}
OLD = {}
if os.path.exists(os.path.join(D, "checklist.csv")):
    for r in csv.DictReader(open(os.path.join(D, "checklist.csv"))): OLD[r["file"]] = r.get("status", "")
rows = []
for no, xs in EX.items():
    md = [f"# G0{no} · {no}부 프롬프트 실습 B 결과 — " + ", ".join(x["b_key"] for x in xs), "",
          "실습마다 **새 대화**를 엽니다. 받은 A 그림(`attach/` 폴더)을 첨부하고, 아래 두 줄 안내와 B 문장을 함께 보냅니다.", "",
          "**Genspark에 먼저 붙여 넣기 ↓**", "```", "첨부한 그림을 편집해 줘. 인물의 얼굴·머리·옷·자세·구도·그림체는 그대로 두고, 아래 영어 문장에 적힌 것 하나만 바꿔 줘.",
          "글자·숫자는 넣지 말고 흰 배경 그대로. 원래 그림의 빨간 표시는 그대로 남아도 괜찮아.", "```", ""]
    for k, x in enumerate(xs, 1):
        ak = a_key(x["a"]); ratio = "4:3" if ak.startswith(("p3_moa_sitting", "pr3")) else "2:3"
        rows.append([len(rows) + 1, f"G0{no}", x["b_key"], PAGE[no], f"{no}부 실습 {no}-{k}", ratio, "anime", f"attach/{ak}.png", OLD.get(x["b_key"], "")])
        md += ["---", f"## 실습 {no}-{k} · {x['title']} → 저장 이름 `{x['b_key']}.png`", f"- 첨부: `attach/{ak}.png` (A 결과) · 비율 {ratio} 그대로", "- 예상 결과(이렇게 나오면 성공):"]
        md += [f"  - {t}" for t in x["expect"]]
        md += ["```", x["b"], "```", f"- 차이가 약하면 같은 대화에서 한 번 더: `Make the change stronger and clearer. Change nothing else.`", ""]
    open(os.path.join(D, "prompts", f"G0{no}_part{no}.md"), "w").write("\n".join(md))
with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "attach", "status"]); w.writerows(rows)
open(os.path.join(D, "README.md"), "w").write("""# 그림 요청 꾸러미 — 프롬프트 실습 B 결과 8장

1~4부의 '프롬프트로 직접 만들어 보기'에는 부마다 실습 2개가 있습니다. 각 실습은 **A(이 페이지 그림을 실제로 만든 요청문과 그 결과)** 에서 출발해 **B(원리 하나만 바꾸는 문장)** 를 같은 대화에 이어 붙입니다.
이 꾸러미는 그 **B 결과 그림 8장**을 받기 위한 것입니다. 받으면 페이지의 'B 결과' 자리를 바꾸고, 예상 결과와 실제 결과를 비교해 '실제로 무엇이 달라졌는지'를 적습니다.

| 순서 | 파일 | 그림 | 첨부 |
|---|---|---|---|
| 1 | `prompts/G01_part1.md` | mk1_1_haru_arm_down · mk1_2_haru_light_right | p1_haru_arm_up · pr1_haru_guided |
| 2 | `prompts/G02_part2.md` | mk2_1_sia_shallow_frills · mk2_2_sia_tight_waist | p2_sia_frill_made · pr2_sia_guided |
| 3 | `prompts/G03_part3.md` | mk3_1_moa_legs_out · mk3_2_moa_unbuttoned | p3_moa_sitting_joints · pr3_moa_guided |
| 4 | `prompts/G04_part4.md` | mk4_1_sia_top_light · mk4_2_moa_front_left | p4_sia_below_light · p4_moa_side_light |

## 방식
- 실습 하나 = 새 대화 하나. `attach/`의 A 그림을 첨부하고 B 문장 **하나만** 보냅니다(편집). 처음부터 다시 그리면 얼굴·옷이 바뀌어 비교가 안 됩니다.
- 결과가 예상과 달라도 그대로 보내 주세요. 페이지에는 실제 결과를 있는 그대로 적습니다.
- 인물은 모두 20대 초반 성인, 노출 없음, 그림 안 글자·숫자 금지.
- 저장 이름은 `checklist.csv`의 `file` 열 그대로(png 또는 jpg).
""")
print("make requests:", len(rows))
