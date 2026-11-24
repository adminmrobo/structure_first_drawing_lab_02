# -*- coding: utf-8 -*-
"""부마다 '프롬프트 실습' 2개 — A(이 페이지 그림을 실제로 만든 프롬프트와 그 결과) → B(원리 하나만 바꾸는 문장과 그 결과).
a_src: ("body", 그림 키) = prompt_data.BODYS로 만든 본문 그림, ("pair", 부 번호) = prompt_lab의 원리를 넣은 요청문으로 만든 비교 그림.
b_key: Genspark로 받을 B 결과 그림(docs/image_requests_make/). 오기 전에는 '예상 결과' 글과 '그림 준비 중' 자리를 보인다."""
from prompt_data import BODY, NEG, ARW, BODYS
from prompt_lab import PL, STYLE as PSTYLE, NEG as PNEG, CHAR as PCHAR

RATIO_OF = {"p1_haru_arm_up": "2:3", "p2_sia_frill_made": "2:3", "p3_moa_sitting_joints": "4:3", "p4_sia_below_light": "2:3", "p4_moa_side_light": "2:3"}

def a_prompt(src):
    kind, v = src
    if kind == "body":
        ch, sc = BODYS[v]
        return "\n".join([f"Character illustration, {RATIO_OF[v]}.", BODY, "Character: " + ch, sc, ARW, NEG])
    L = PL[v]; lights = [L["lights"][2][2]] if L.get("lights") else []
    frags = [f for ko, st, f in L["frags"] if "다시 조명" not in ko]
    return "\n".join([L["pose"], PSTYLE, PCHAR[L["model"]][1]] + lights + frags + [PNEG])

def a_key(src):
    return src[1] if src[0] == "body" else PL[src[1]]["pair"][1]

KEEP = "Keep the same character, outfit, framing and art style. Still no text."
EX = {
 1: [
  dict(id="x1", title="손을 내리면 주름 방향이 바뀐다", model="haru", ref="haru",
       goal="접점이 바뀌면 주름의 출발점과 방향이 함께 바뀌는지 직접 확인합니다. 하루가 머리를 만지던 손을 내리게 해 겨드랑이 접점을 없앱니다.",
       steps=[("s1", "1단계 접점"), ("s3", "3단계 꼭대기")], a=("body", "p1_haru_arm_up"),
       b_key="mk1_1_haru_arm_down",
       b="Same image. Change only: she lowers the raised hand and lets that arm hang relaxed at her side, so the armpit no longer lifts the hoodie. " + KEEP,
       expect=["겨드랑이에서 가슴 꼭대기로 비스듬히 오르던 당김 주름이 사라지거나 크게 줄어듭니다.",
               "후드 앞판은 어깨 꼭대기에 걸려 아래로 처지는 주름 몇 개만 남고, 밑단이 조금 내려옵니다.",
               "바지 주름은 거의 그대로입니다. 바뀐 접점은 팔 하나뿐이기 때문입니다."],
       checks=[("팔을 내린 쪽 후드에서 비스듬한 당김 주름이 줄었나", "#s1"), ("남은 주름이 어깨 꼭대기에서 아래로 처지나", "#s3"), ("얼굴·머리(번 2개·남색 줄)와 자세의 나머지가 그대로인가", "#s1")],
       caution="빨간 화살표가 그려진 A 그림을 고치면 화살표도 남을 수 있습니다. 화살표가 거슬리면 'remove all red arrows and circles'를 덧붙여 따로 한 번 더 요청합니다."),
  dict(id="x2", title="광원을 오른쪽으로 옮기면 큰 그림자가 반대로 간다", model="haru", ref="haru",
       goal="4단계 '큰 형체 그림자 먼저'를 시험합니다. 같은 그림에서 광원만 왼쪽 위에서 오른쪽 위로 옮겨, 몸 전체의 큰 그림자가 반대쪽으로 넘어가는지 봅니다.",
       steps=[("s4", "4단계 큰 형체 그림자"), ("s5", "5단계 단차 그림자")], a=("pair", 1),
       b_key="mk1_2_haru_light_right",
       b="Same image. Change only the lighting: one light source from the upper RIGHT. Move the big form shadows to the left side of her body (the chest as a sphere, the legs as cylinders), keep thin shadow bands under the pocket and the hem. " + KEEP,
       expect=["몸의 큰 그림자가 오른쪽 절반에서 왼쪽 절반으로 넘어갑니다. 가슴은 구처럼, 다리는 원기둥처럼 한쪽이 한 덩어리로 어둡습니다.",
               "주머니·밑단 아래의 얇은 그림자 띠는 광원이 위에 있으니 그대로 아래쪽에 남습니다.",
               "선(윤곽·주름 선)은 바뀌지 않고 그림자만 바뀌는 것이 정상입니다."],
       checks=[("큰 그림자가 몸의 왼쪽 절반에 한 덩어리로 있나", "#s4"), ("주머니·밑단 아래 띠가 여전히 아래쪽에 있나", "#s5"), ("얼굴의 그림자도 같은 쪽(왼쪽)인가", "#s4")],
       caution="A 결과는 실험복을 입고 나왔습니다(이 절 아래 '실제로 나온 결과' 참고). B에서도 옷은 그대로 둡니다. 옷을 바꾸려면 따로 한 번 요청합니다."),
 ],
 2: [
  dict(id="x1", title="개더 비율을 줄이면 프릴이 얕아진다", model="sia", ref="sia",
       goal="1단계 '물결 하나에 든 천 = 폭 × 비율'을 시험합니다. 같은 옷에서 프릴 천만 덜 넣어(비율 약 1.2) 물결 깊이가 얕아지는지 봅니다.",
       steps=[("s1", "1단계 개더 비율"), ("s3", "3단계 큰 선 먼저")], a=("body", "p2_sia_frill_made"),
       b_key="mk2_1_sia_shallow_frills",
       b="Same image. Change only: the apron and petticoat ruffles are gathered much less, about 1.2 times the band length, so the ruffles become shallow gentle waves with the same number of waves. " + KEEP,
       expect=["앞치마 밑단과 속치마 프릴의 물결이 얕고 넓적해집니다. 물결 개수는 거의 그대로입니다.",
               "치마 전체의 종 모양 윤곽(큰 선)은 바뀌지 않습니다. 잔물결만 바뀌기 때문입니다.",
               "프릴 아래의 그림자도 얕아져 덜 진해집니다."],
       checks=[("물결 깊이만 얕아지고 개수는 비슷한가", "#s1"), ("치마 전체 윤곽은 그대로인가", "#s3"), ("머리 장식이 생기지 않았나(시아 고정값)", "#s1")],
       caution="도구가 '얕게'를 '프릴을 없애라'로 알아듣는 일이 있습니다. 프릴이 사라지면 'keep the ruffles, only shallower'를 덧붙입니다."),
  dict(id="x2", title="허리끈을 세게 조이면 위아래에서 주름이 모인다", model="sia", ref="sia",
       goal="2단계 '조인 선을 향해 위아래 양쪽에서 모인다'를 시험합니다. 허리끈만 세게 조여 끈 위 상의와 끈 아래 치마 양쪽에 짧은 모임 주름이 생기는지 봅니다.",
       steps=[("s2", "2단계 조임"), ("s4", "4단계 짝 장식")], a=("pair", 2),
       b_key="mk2_2_sia_tight_waist",
       b="Same image. Change only: the apron waist tie is pulled much tighter, so short gathered folds bunch toward the tie from above (on the bodice) and from below (on the skirt). " + KEEP,
       expect=["허리끈 바로 위 상의에 끈 쪽으로 모이는 짧은 주름이 생깁니다.",
               "끈 바로 아래 치마와 앞치마에도 위로 모이는 주름이 생기고, 그 아래로 천이 조금 더 부풀어 보입니다.",
               "어깨 프릴·단추 같은 짝 장식의 높이는 바뀌지 않습니다."],
       checks=[("끈 위쪽 상의에도 모임 주름이 생겼나", "#s2"), ("끈 아래쪽 치마에 위로 모이는 주름이 있나", "#s2"), ("짝 장식의 높이와 좌우가 그대로인가", "#s4")],
       caution="'tighter'만 쓰면 허리를 지나치게 가늘게 그리는 일이 있습니다. 체형이 바뀌면 'keep the same body shape'를 덧붙입니다."),
 ],
 3: [
  dict(id="x1", title="다리를 펴면 무릎 주름이 줄어든다", model="moa", ref="moa",
       goal="1단계 '관절의 남는 천 = 두께 × 굽힌 각'을 시험합니다. 옆으로 접었던 다리를 앞으로 펴게 해, 무릎·고관절의 모임 주름이 줄어드는지 봅니다.",
       steps=[("s1", "1단계 관절"), ("s4", "4단계 주름치마")], a=("body", "p3_moa_sitting_joints"),
       b_key="mk3_1_moa_legs_out",
       b="Same image. Change only: still sitting on the same mat, she stretches both legs straight out in front of her, so the knees are almost straight; adjust only the legs, the skirt and the socks. " + KEEP,
       expect=["무릎 뒤와 무릎 위의 모임 주름이 거의 사라집니다. 무릎을 거의 폈으니(약 10°) 남는 천이 3cm도 안 됩니다.",
               "고관절은 여전히 약 90° 굽어 있어 허벅지 위쪽 주름은 남습니다.",
               "주름치마는 바닥으로 덜 퍼지고 허벅지 위에 얹혀 주름 폭이 좁아집니다."],
       checks=[("무릎 둘레 주름이 A보다 줄었나", "#s1"), ("허벅지 위쪽(고관절) 주름은 남아 있나", "#s1"), ("치마 주름 폭이 A보다 좁아졌나", "#s4")],
       caution="자세를 바꾸는 요청은 구도가 흔들리기 쉽습니다. 얼굴 위치가 크게 바뀌면 'keep the same framing and camera angle'을 덧붙입니다."),
  dict(id="x2", title="단추를 풀면 단추에서 퍼지던 주름이 사라진다", model="moa", ref="moa",
       goal="2단계 '고정 주름 — 단추가 붙잡은 점에서 퍼진다'를 시험합니다. 앞단추만 풀어 앞판을 열면 단추 둘레 당김 주름이 사라지는지 봅니다.",
       steps=[("s2", "2단계 단추"), ("s3", "3단계 소재")], a=("pair", 3),
       b_key="mk3_2_moa_unbuttoned",
       b="Same image. Change only: all front buttons of her top are unfastened and the two front panels hang open loosely, showing the white shirt underneath. " + KEEP,
       expect=["단추를 중심으로 옆구리 쪽으로 퍼지던 짧은 당김 주름이 사라집니다.",
               "앞판 두 장이 따로 늘어지며 세로로 처지는 주름 몇 개가 생깁니다.",
               "안에 입은 셔츠가 드러나고, 셔츠는 부드러운 천이라 잔주름이 보입니다."],
       checks=[("단추 둘레의 퍼지는 주름이 사라졌나", "#s2"), ("앞판이 세로로 처지는가", "#s2"), ("셔츠는 겉옷보다 잔주름이 많은가", "#s3")],
       caution="A 결과는 블레이저가 아니라 니트 카디건으로 나왔습니다. 카디건도 단추로 앞판을 붙잡는 원리는 같아서 이 실습에는 그대로 씁니다."),
 ],
 4: [
  dict(id="x1", title="바닥 조명을 머리 위로 옮기면 밝은 면이 뒤집힌다", model="sia", ref="sia",
       goal="2단계 '아래에서 오는 빛 — 평소와 반대'를 거꾸로 시험합니다. 아래 조명을 받은 시아의 광원만 머리 위로 옮겨, 밝은 면과 어두운 면이 위아래로 뒤집히는지 봅니다.",
       steps=[("s1", "1단계 광원 방향"), ("s2", "2단계 아래 빛")], a=("body", "p4_sia_below_light"),
       b_key="mk4_1_sia_top_light",
       b="Same image. Change only the lighting: remove the lamp on the floor and use one light source directly above her head. The tops of the head and shoulders become bright, the underside of the chin and the arms go into shadow, and her cast shadow falls on the floor at her feet instead of rising on the wall. " + KEEP,
       expect=["턱 아래·팔 아래가 어두워지고, 머리 위·어깨 위가 밝아집니다. A와 밝고 어두운 곳이 정확히 반대입니다.",
               "벽 위로 길게 솟던 그림자가 사라지고, 발밑 바닥에 짧은 그림자가 생깁니다.",
               "분위기가 신비로운 느낌에서 평범한 낮 느낌으로 바뀝니다."],
       checks=[("턱 아래가 어두워졌나", "#s2"), ("어깨 위·머리 위가 밝아졌나", "#s1"), ("그림자가 벽이 아니라 발밑으로 갔나", "#s1")],
       caution="원래 그림의 빛이 조금 남으면 광원이 두 개처럼 보입니다(5단계 다시 조명). 남으면 'remove all lighting from the floor lamp'를 덧붙입니다."),
  dict(id="x2", title="옆 빛을 왼쪽 앞 60°로 옮기면 밝은 폭이 늘어난다", model="moa", ref="moa",
       goal="4단계 '보이는 밝은 폭 = (1 + cos φ) ÷ 2'를 시험합니다. 오른쪽 바로 옆(φ = 90°, 밝은 폭 50%)에서 오던 빛을 왼쪽 앞 60°(밝은 폭 75%)로 옮깁니다.",
       steps=[("s3", "3단계 옆 빛"), ("s4", "4단계 각도")], a=("body", "p4_moa_side_light"),
       b_key="mk4_2_moa_front_left",
       b="Same image. Change only the lighting: one light source from her front-left at about 60 degrees seen from above, slightly high. About three quarters of her visible body is lit and only the far right quarter is in shadow; the raised forearm and the bag cast shadows onto her torso shifted to the right. Remove the red and blue outline marks. " + KEEP,
       expect=["몸의 절반이던 그림자가 오른쪽 4분의 1 정도로 줄어듭니다(50% → 75%가 밝음).",
               "그림자가 몸의 왼쪽에서 오른쪽으로 넘어갑니다. 광원이 오른쪽에서 왼쪽으로 옮겨 갔기 때문입니다.",
               "팔·가방이 몸통에 드리우는 그림자는 오른쪽으로 밀립니다."],
       checks=[("밝은 부분이 몸의 4분의 3쯤인가", "#s4"), ("그림자가 오른쪽으로 넘어갔나", "#s3"), ("팔·가방 그림자가 몸통에 오른쪽으로 밀려 있나", "#s3")],
       caution="'4분의 3'처럼 넓이를 숫자로 적어도 한 번에 잘 지켜지지 않습니다(위 '실제로 나온 결과' 참고). 넓이가 맞지 않으면 그것 하나만 고치기 문장으로 다시 요청합니다."),
 ],
}

# 실제로 받은 B 결과를 A와 나란히 본 판정(2026-11-24 첫 결과, 같은 대화에서 B 문장 한 번)
SEEN = {
 (1, "x1"): ("예상대로", ["든 손을 내리자 겨드랑이에서 가슴으로 오르던 사선 주름이 사라지고, 후드 앞판은 어깨에 걸려 아래로 처지는 모습으로 바뀌었습니다.",
                       "바지 주름은 거의 그대로입니다. 접점이 바뀐 곳(팔)만 바뀐다는 예상과 맞습니다. A의 빨간 표시는 도구가 함께 지웠습니다."]),
 (1, "x2"): ("거의 안 바뀜", ["광원을 오른쪽 위로 옮기라고 했지만 큰 그림자의 위치 차이가 아주 약합니다. 다리 왼쪽이 조금 어두워진 정도입니다.",
                          "그림자만 바꾸는 요청은 도구가 '그림 전체를 거의 그대로 두라'는 말과 함께 약하게 반영합니다. 차이를 키우려면 'Make the shadows much darker and clearly on the left side'를 한 번 더 보냅니다."]),
 (2, "x1"): ("거의 안 바뀜", ["프릴을 얕게(비율 약 1.2) 하라고 했지만 물결 깊이 차이가 거의 보이지 않습니다. A의 빨간 표시만 지워졌습니다.",
                          "'비율' 같은 숫자는 그림 도구가 잘 알아듣지 못합니다. 'almost flat ruffles with very gentle waves'처럼 모양을 말로 적는 편이 낫습니다."]),
 (2, "x2"): ("안 바뀜", ["허리끈을 세게 조이라고 했지만 끈 위아래의 모임 주름이 생기지 않았습니다. A와 거의 같은 그림입니다.",
                     "작은 부위의 주름 변화는 편집 요청에서 무시되기 쉽습니다. 도구의 부분 수정(허리 부분만 칠해 고치기)으로 다시 해 보는 것을 권합니다."]),
 (3, "x1"): ("예상대로", ["다리를 앞으로 펴자 무릎 둘레의 모임 주름이 거의 사라졌습니다. 무릎을 펴면 남는 천이 줄어든다는 1단계 식과 맞습니다.",
                       "치마는 바닥으로 퍼지지 않고 허벅지 위에 얹혀 주름 폭이 좁아졌습니다. 고관절은 여전히 굽어 있어 허벅지 위쪽 주름은 남았습니다."]),
 (3, "x2"): ("예상대로", ["단추를 풀자 앞판 두 장이 따로 열려 세로로 처지고, 단추 둘레로 퍼지던 당김 주름이 사라졌습니다.",
                       "안에 입은 흰 셔츠가 드러나며 잔주름이 보입니다. 단추라는 접점 하나가 주름의 모양을 정한다는 예입니다."]),
 (4, "x1"): ("예상대로", ["바닥 조명을 머리 위로 옮기자 벽 위로 솟던 긴 그림자가 사라지고 발밑에 짧은 그림자가 생겼습니다. 머리 위에서 빛이 쏟아지는 모습도 보입니다.",
                       "턱 아래가 어두워지는 변화는 약합니다. 큰 그림자(벽·바닥)는 잘 바뀌고, 얼굴의 작은 그림자는 약하게 바뀝니다."]),
 (4, "x2"): ("일부", ["빨간·파란 표시가 지워지고 전체 그림자가 진해졌지만, '왼쪽 앞에서 빛, 4분의 3이 밝게'라는 넓이는 지켜지지 않았습니다. 오히려 몸 전체가 조금 어두워졌습니다.",
                   "그림자 넓이처럼 숫자로 적은 조건은 한 번에 잘 지켜지지 않습니다. 같은 대화에서 'the left three quarters of her body must be brightly lit'처럼 한 가지만 다시 요청합니다."]),
}
MK_LESSON = "여덟 실습을 모아 보면, 자세·옷차림처럼 모양이 바뀌는 요청(1-1, 3-1, 3-2, 4-1)은 잘 지켜지고, 그림자 방향·물결 깊이·조임처럼 미묘한 요청(1-2, 2-1, 2-2, 4-2)은 약하게 반영되었습니다. 미묘한 원리일수록 결과를 직접 확인하고, 한 가지씩 더 세게 다시 요청해야 합니다."

# 실패한 실습의 다시 시도(2차) — 1차 결과는 페이지에 그대로 두고, 아래에 2차 문장과 결과 자리를 더한다.
RETRY = {
 (1, "x2"): dict(key="mk1_2_haru_light_right_retry", attach="pr1_haru_guided", how="편집(그림 전체)",
   why="1차는 '그림자만 바꾸라'는 말을 도구가 아주 약하게 반영했습니다. 2차는 그림자를 어디에, 얼마나 진하게 넣을지 눈에 보이는 말로 적고, 원래 그림의 빛을 먼저 지우게 합니다.",
   prompt=("Edit the attached image. First remove all existing shading, then relight it with ONE strong light source from the upper RIGHT side of the picture. "
           "Make the shadows much darker and clearly visible: the LEFT side (as seen in the picture) of her face, hair, hoodie, lab coat and both legs in solid two-tone cel shadow (dark lavender-gray), "
           "the right side bright. Her cast shadow falls on the floor toward the lower left. Keep the same character, outfit, pose, framing and art style. Still no text."),
   more="The shadows are still too weak. Make the left side of her body clearly darker, like a strong spotlight from the right."),
 (2, "x1"): dict(key="mk2_1_sia_shallow_frills_retry", attach="mk2_1_sia_shallow_frills", how="편집(그림 전체)",
   why="1차는 '비율 1.2'라는 숫자를 도구가 알아듣지 못했습니다. 2차는 숫자 대신 모양을 말로 적고, 지금보다 얼마나 얕게 할지 비교로 말합니다.",
   prompt=("Edit the attached image. Change only the ruffles on the apron hem and the petticoat: make them almost flat, very gentle shallow waves, like the lightly wavy edge of a ribbon, "
           "about one third as deep as they are now. Keep the same number of waves and keep the ruffles (do not remove them). "
           "Keep the same character, outfit, pose, framing and art style. Still no text."),
   more="The ruffles are still too deep. Flatten them more, so the hem looks almost straight with only tiny waves."),
 (2, "x2"): dict(key="mk2_2_sia_tight_waist_retry", attach="mk2_2_sia_tight_waist", how="부분 수정(허리 둘레만 칠하기) — 기능이 없으면 그림 전체 편집",
   why="1차는 작은 부위의 주름 변화가 무시되었습니다. 2차는 도구의 부분 수정 기능으로 허리 둘레만 칠해 그곳만 고치게 하고, 주름 수와 방향을 구체적으로 적습니다.",
   prompt=("In the painted waist area only: the apron waist tie is pulled very tight. Draw at least six short, clearly visible gathered folds that bunch toward the tie — "
           "on the bodice just above the tie pointing down toward it, and on the skirt and apron just below pointing up toward it. "
           "Keep the same body shape and waist width, the same outfit and art style. Still no text."),
   more="Make the gathered folds above and below the waist tie deeper and darker, with small shadows between them."),
 (4, "x2"): dict(key="mk4_2_moa_front_left_retry", attach="p4_moa_side_light", how="편집(그림 전체)",
   why="1차는 '4분의 3이 밝게'라는 넓이를 지키지 못하고 몸 전체를 어둡게 했습니다. 2차는 그림의 왼쪽·오른쪽을 기준으로 밝은 곳과 어두운 곳을 따로 적어 헷갈리지 않게 합니다.",
   prompt=("Edit the attached image. Remove the red and blue marks and all existing shading. Relight it with ONE light source from the LEFT side of the picture, in front of her at about 60 degrees and slightly high. "
           "About three quarters of her body, starting from the left edge of the picture, is brightly lit; only a narrow strip along the RIGHT edge of her body (about one quarter) is in dark two-tone cel shadow. "
           "Her raised forearm and the bag cast short shadows onto the blazer, shifted to the right. Keep the same character, outfit, pose, framing and art style. Still no text."),
   more="Too much of her body is dark. Make the left three quarters clearly bright and keep only a narrow dark strip on the right edge."),
}

# 2차 결과 판정(2026-11-24, 새 대화에서 다시 시도 문장 한 번)
RETRY_SEEN = {
 (1, "x2"): ("예상대로", ["원래 빛을 먼저 지우게 하고 그림자 위치와 진하기를 말로 적자, 그림 왼쪽 절반(실험복·다리)이 분명히 어두워지고 바닥 왼쪽 아래로 긴 그림자가 생겼습니다.",
                       "1차와 비교하면 '어디를 얼마나 어둡게'를 적는 것이 '광원을 옮겨라'보다 훨씬 잘 지켜진다는 것을 볼 수 있습니다."]),
 (2, "x1"): ("예상대로", ["숫자(비율 1.2) 대신 '리본 가장자리처럼 거의 평평하게, 지금 깊이의 3분의 1'이라고 모양으로 적자 속치마 프릴이 거의 평평해지고 앞치마 프릴도 얕아졌습니다.",
                       "물결 개수는 비슷하게 남아, '깊이는 비율이, 개수는 폭이 정한다'는 1단계 내용과 맞습니다."]),
 (2, "x2"): ("일부", ["허리띠 자체에 모임 주름이 잡혀 끈이 천을 조인 느낌은 생겼지만, 끈 위 상의와 끈 아래 앞치마에서 끈 쪽으로 모이는 주름은 여전히 약합니다.",
                   "어깨끈 옆에 번진 얼룩이 하나 생겼습니다. 좁은 곳을 고치는 편집에서 흔히 생기는 흔적이니, 쓰기 전에 확대해서 확인합니다."]),
 (4, "x2"): ("대체로 예상대로", ["몸 전체가 어두워졌던 1차와 달리, 그림 왼쪽부터 대부분이 밝고 오른쪽 소매·옆선에 좁은 그림자 띠가 생겼습니다. 좌우를 '그림 기준'으로 적은 것이 효과가 있었습니다.",
                              "다만 그림자 띠가 연해서 '4분의 1'이 또렷하게 보이지는 않습니다. 팔·가방이 몸통에 드리우는 그림자도 약합니다."]),
}
RETRY_LESSON = "다시 시도에서 배운 점 — ① 숫자(비율·넓이)보다 모양을 말로 적는다. ② 그림자는 '광원을 옮겨라'보다 '어디를 얼마나 어둡게'를 적는다. ③ 원래 그림의 빛을 먼저 지우게 한다. ④ 좁은 부위의 작은 주름은 세 번째 부분 수정에서도 약했다(실습 2-2). 특히 검은 천의 주름은 밝은 하이라이트로 그려야 보인다. 이런 곳은 AI 결과를 밑그림으로 쓰고 마지막 주름은 손으로 더한다."

# 한 번 더(3차) — 2차에서도 일부만 된 실습
RETRY3 = {
 (2, "x2"): dict(key="mk2_2_sia_tight_waist_retry2", attach="pr2_sia_guided", how="부분 수정(허리끈과 그 위아래 손바닥 폭만 칠하기)",
   why="2차는 허리띠 자체에만 주름이 잡히고, 어깨끈 옆에 얼룩이 생겼습니다. 3차는 얼룩 없는 A 그림에서 다시 시작하고, 칠하는 범위를 끈 위아래 손바닥 폭까지 넓혀 '끈 쪽으로 모이는' 주름이 들어갈 자리를 줍니다. 주름 수·길이·방향을 복주머니에 빗대어 그림처럼 적습니다.",
   prompt=("In the painted area only (the apron waist tie and about a hand's width above and below it): the waist tie is pulled very tight, like the drawstring of a pouch. "
           "The fabric above the tie (the black bodice) and below it (the white apron and the black skirt) bunches toward the tie: draw 6 to 8 short, clearly visible fold lines on each side, "
           "all converging on the tie from above and from below, with small dark shadows between the folds. The waist width stays the same. "
           "Keep everything outside the painted area exactly unchanged, the same art style. Still no text."),
   whole=("Edit the attached image. Change only the area around the apron waist tie: the tie is pulled very tight, like the drawstring of a pouch; draw 6 to 8 short, clearly visible gathered folds "
          "above the tie (on the black bodice) and below it (on the white apron and black skirt), all converging on the tie, with small dark shadows between them. "
          "The waist width stays the same. Keep the same character, outfit, pose, framing and art style. Still no text."),
   more="The gathered folds are still too faint. Make each fold darker and longer, clearly converging on the tie from above and from below, like a tightly pulled drawstring pouch."),
}

RETRY3_SEEN = {
 (2, "x2"): ("일부", ["얼룩·번짐은 없어졌습니다. 허리띠에 끈이 당기는 사선 주름이 생겼고, 끈 아래 앞치마의 모임 주름이 끈 쪽으로 모입니다.",
                   "끈 위 검은 상의에는 끈 쪽으로 내려오는 주름이 여전히 보이지 않습니다. 검은 천은 어두운 주름 선이 바탕에 묻히기 때문입니다. 검은 천의 주름은 밝은 회색 하이라이트로 그려야 보입니다.",
                   "세 번 시도한 결과, 좁은 부위의 작은 주름은 이미지 AI가 가장 약한 곳입니다. 이런 곳은 AI 결과를 밑그림으로 쓰고, 마지막 주름 몇 줄은 손으로 더하는 편이 빠릅니다."]),
}
