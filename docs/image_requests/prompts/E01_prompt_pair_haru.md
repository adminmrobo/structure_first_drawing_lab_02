# E01 · 프롬프트 비교 1부 — pr1_haru_naive, pr1_haru_guided

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
## 1) pr1_haru_naive
alt(페이지 설명): 하루, 같은 자세 — 왼쪽은 원리 없는 요청문의 결과(주름이 아무 데나 흩어지고 팔꿈치 바깥에 몰림, 그림자가 양쪽에 같음), 오른쪽은 원리를 넣은 요청문의 결과 — 왼쪽(원리 없음)
```
Full body, vertical 2:3. Pose: standing in a three-quarter view, right hand resting on her hip so the elbow bends outward, left arm relaxed, left knee slightly forward.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Haru — long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top of the head, big blue eyes, lavender zip-up hoodie over a white t-shirt, gray-blue jogger pants, lavender slip-on sneakers.
Deliberately flawed result for teaching: wrinkles scattered randomly all over the hoodie, folds bunched on the OUTSIDE of the bent elbow, both legs equally shaded with no clear light direction.
Keep the face, hair and outfit correct; only the folds and shadows are wrong.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```

---
## 2) pr1_haru_guided
alt(페이지 설명): 하루, 같은 자세 — 왼쪽은 원리 없는 요청문의 결과(주름이 아무 데나 흩어지고 팔꿈치 바깥에 몰림, 그림자가 양쪽에 같음), 오른쪽은 원리를 넣은 요청문의 결과 — 오른쪽(원리 넣음)
```
Full body, vertical 2:3. Pose: standing in a three-quarter view, right hand resting on her hip so the elbow bends outward, left arm relaxed, left knee slightly forward.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Haru — long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top of the head, big blue eyes, lavender zip-up hoodie over a white t-shirt, gray-blue jogger pants, lavender slip-on sneakers.
Folds start from the contact points: the tops of the shoulders, the top of the chest, the hand pressing the hoodie at the hip, the bent elbow and the forward knee.
At the bent elbow: long stretched folds on the outside, short bunched folds on the inside.
Chest folds point toward the top of the chest; the fabric below it hangs loosely with a few soft drape folds.
Light from the upper left. Shade the big forms first — the chest as a sphere, the legs as cylinders — so the right side of the body is in shadow; small fold shadows only on the lit side.
Thin cast-shadow bands under the hoodie pocket edge, under the ribbed hem and under the pants pocket.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```
