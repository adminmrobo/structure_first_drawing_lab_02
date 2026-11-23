# E02 · 프롬프트 비교 2부 — pr2_sia_naive, pr2_sia_guided

**첨부:** refs/p5_sia_anime.png · 앞 대화에서 받은 그림이 있으면 함께

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
## 1) pr2_sia_naive
alt(페이지 설명): 시아, 같은 자세 — 왼쪽은 레이스만 강조한 결과(치마가 한쪽으로 기울고 프릴 깊이가 들쭉날쭉, 다리 그림자 끝이 직선), 오른쪽은 원리를 넣은 결과 — 왼쪽(원리 없음)
```
Full body, vertical 2:3. Pose: standing calmly in a three-quarter view, both hands lightly holding the hem of her skirt.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Sia — long straight jet-black hair, calm gray eyes, small silver drop earrings, no headdress, knee-length charcoal-black maid dress with puffed short sleeves, white high collar with a large gray bow, white frilled apron, layered white petticoat ruffles, white over-knee socks, black strap shoes.
Deliberately flawed result for teaching: the skirt silhouette leans to one side, ruffles irregularly deep and flat in places, the cast shadow on the legs ends in a ruler-straight line.
Keep the face, hair and outfit correct; only the folds and shadows are wrong.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```

---
## 2) pr2_sia_guided
alt(페이지 설명): 시아, 같은 자세 — 왼쪽은 레이스만 강조한 결과(치마가 한쪽으로 기울고 프릴 깊이가 들쭉날쭉, 다리 그림자 끝이 직선), 오른쪽은 원리를 넣은 결과 — 오른쪽(원리 넣음)
```
Full body, vertical 2:3. Pose: standing calmly in a three-quarter view, both hands lightly holding the hem of her skirt.
High-quality anime illustration, clean lineart, two-tone cel shading, plain white background, a young adult woman in her early twenties, modest outfit exactly as described.
Character: Sia — long straight jet-black hair, calm gray eyes, small silver drop earrings, no headdress, knee-length charcoal-black maid dress with puffed short sleeves, white high collar with a large gray bow, white frilled apron, layered white petticoat ruffles, white over-knee socks, black strap shoes.
The apron hem and the petticoat have evenly deep gathered ruffles, as if the fabric were gathered to about twice the band length.
The waist tie and the sleeve bands cinch the fabric; short folds gather toward each tied line from above and from below.
The skirt keeps one clean, symmetrical bell-shaped silhouette; ruffles and lace follow that big outline.
Paired ornaments — both puffed shoulders, the pairs of apron buttons, the two ends of the apron tie — sit on parallel lines that follow the body's slight tilt.
Light from the upper left: the skirt casts a shadow on her thighs whose lower edge follows the wavy ruffle shape; the legs also have rounded form shadows on the right side.
No text, no letters, no numbers, no logos, no watermark, no exaggerated body proportions, not resembling any famous anime character.
```
