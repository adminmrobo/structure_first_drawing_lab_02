# E04 · 프롬프트 비교 4부 — pr4_haru_naive, pr4_haru_guided

**첨부:** refs/p5_haru_anime.png · 앞 대화에서 받은 그림이 있으면 함께

**Genspark에 먼저 붙여 넣기 ↓**
```
첨부한 애니풍 기준 전신 그림의 인물을 같은 얼굴·머리로, 이번 연습용 의상을 입혀 두 장을 그려 줘.
- 비율 2:3, 긴 변 1536px 이상, 흰 배경, 애니풍 셀 채색
- 두 장은 같은 인물·같은 자세·같은 구도. 다른 것은 주름과 그림자뿐
- 첫 장(naive)은 교육용으로 '일부러 틀린' 주름·그림자를 그대로 그릴 것(고치지 말 것)
- 두 번째 장(guided)은 요청문에 적힌 원리를 정확히 지킬 것
- 화살표·동그라미 같은 표시 없음, 글자·숫자 금지, 20대 초반 성인, 노출 없음
아래 영어 프롬프트를 하나씩 써 줘.
```

---
## 1) pr4_haru_naive
alt(페이지 설명): 하루, 같은 자세 — 왼쪽은 '극적인 조명'만 적은 결과(빛이 두 방향에서 오는 듯 그림자가 엇갈림), 오른쪽은 왼쪽 앞 60° 광원 하나를 적은 결과 — 왼쪽(원리 없음)
```
Full body, vertical 2:3. Pose: standing in a three-quarter view, a canvas shoulder bag on one shoulder, the near forearm raised in front of the chest holding the strap.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Haru — long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top of the head, big blue eyes, lavender zip-up hoodie over a white t-shirt, gray-blue jogger pants, lavender slip-on sneakers.
Deliberately flawed result for teaching: shadows contradict each other as if lit from two directions (face shaded on the left, clothes shaded on the right), no cast shadow from the arm or bag.
Keep the face, hair and outfit correct; only the folds and shadows are wrong.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```

---
## 2) pr4_haru_guided
alt(페이지 설명): 하루, 같은 자세 — 왼쪽은 '극적인 조명'만 적은 결과(빛이 두 방향에서 오는 듯 그림자가 엇갈림), 오른쪽은 왼쪽 앞 60° 광원 하나를 적은 결과 — 오른쪽(원리 넣음)
```
Full body, vertical 2:3. Pose: standing in a three-quarter view, a canvas shoulder bag on one shoulder, the near forearm raised in front of the chest holding the strap.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Haru — long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top of the head, big blue eyes, lavender zip-up hoodie over a white t-shirt, gray-blue jogger pants, lavender slip-on sneakers.
Single light source from the front-left at about 60 degrees seen from above, slightly high: about three quarters of the visible body is lit, the right quarter is in shadow.
The raised forearm and the shoulder bag cast shadows onto the torso, shifted away from the light.
Only one light source; every shadow sits on the side opposite that light, consistently on the face, clothes and legs.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```
