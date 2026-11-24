# 그림 요청 꾸러미 — 프롬프트 실습 B 결과 8장

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

## 다시 시도 — H01 (2026-11-24)
1차 판정에서 실패한 1-2·2-1·2-2·4-2를 `prompts/H01_retry.md`로 다시 받습니다. 저장 이름은 `*_retry.png`. 1차 결과는 페이지에 실패 사례로 남깁니다.
