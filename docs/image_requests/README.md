# 그림 요청 꾸러미 — 구조 먼저 그리기 연구실 02 · 실천편

저장소: `adminmrobo/structure_first_drawing_lab_02`
만드는 도구: Genspark 이미지 · 받은 뒤 `checklist.csv`의 이름으로 저장해 zip으로 돌려주시면 됩니다.
모두 **34장** — D01~D08 26장(반영 완료, 2026-11-23) + **E01~E04 8장(새 요청: 부마다 '프롬프트로 직접 만들어 보기'의 비교 그림)**.

## 1. 이번 편의 그림 규칙
| 항목 | 규칙 |
|---|---|
| 그림체 | **표지 6장은 16비트 RPG 픽셀아트**(연구실 세계). **본문·비교 그림은 애니풍 셀 채색**(이 시리즈만의 예외, 기초편과 같음) |
| 배경 | 흰색·밝은 낮 분위기 |
| 캐릭터 고정값 | `refs/p5_*_anime.png`(기초편 기준 전신)와 같은 얼굴·머리. 하루: 정수리 번 2개 + 앞머리 가운데 남색 줄 / 시아: 흑발·머리 장식 없음 / 모아: 흰 프릴 머리띠 + **왼쪽** 귀 위 흰 리본 |
| 이번 연습용 의상 | 하루: 실험복 벗고 라벤더 후드 집업 + 조거 바지 / 시아: 무릎 길이의 프릴 많은 메이드복 + 흰 오버니 양말 / 모아: 캐멀 블레이저 + 남색 주름치마 |
| 노출 | 노출·과장된 체형 금지, 세 사람 모두 20대 초반 성인 |
| 표시 | D 대화: 빨간 화살표·동그라미·점선만. E 대화: 표시 없음. **글자·숫자는 모두 금지** |
| 원서 | 원서의 그림·사진을 첨부하거나 따라 그리게 하지 않습니다. 자세만 말로 정했습니다 |

## 2. 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 그림 수 | 비율 | 첨부할 참고 그림 |
|---|---|---|---|---|
| 1 | `prompts/D01_covers_A.md` | 3 | 16:9 픽셀 | refs 전부 |
| 2 | `prompts/D02_covers_B.md` | 3 | 16:9 픽셀 | refs 전부 |
| 3 | `prompts/D03_portrait_A.md` | 4 | 2:3 | 해당 인물의 refs/p5_*_anime.png |
| 4 | `prompts/D04_portrait_B.md` | 2 | 2:3 | 해당 인물의 refs/p5_*_anime.png |
| 5 | `prompts/D05_sitting_4x3.md` | 2 | 4:3 | 해당 인물의 refs/p5_*_anime.png |
| 6 | `prompts/D06_haru_16x9.md` | 5 | 16:9 | 해당 인물의 refs/p5_*_anime.png |
| 7 | `prompts/D07_sia_16x9.md` | 4 | 16:9 | 해당 인물의 refs/p5_*_anime.png |
| 8 | `prompts/D08_moa_16x9.md` | 3 | 16:9 | 해당 인물의 refs/p5_*_anime.png |
| 9 | `prompts/E01_prompt_pair_haru.md` | 2 | 2:3 | 해당 인물의 refs/p5_*_anime.png |
| 10 | `prompts/E02_prompt_pair_sia.md` | 2 | 2:3 | 해당 인물의 refs/p5_*_anime.png |
| 11 | `prompts/E03_prompt_pair_moa.md` | 2 | 4:3 | 해당 인물의 refs/p5_*_anime.png |
| 12 | `prompts/E04_prompt_pair_light.md` | 2 | 2:3 | 해당 인물의 refs/p5_*_anime.png |

## 3. E01~E04 비교 그림 (새 요청)
- 한 대화에서 **같은 인물·같은 자세로 두 장**을 받습니다. `*_naive`는 원리 없는 요청문의 결과를 보여 주려고 **일부러 틀리게** 그린 그림, `*_guided`는 페이지에서 조립한 요청문 그대로의 결과입니다.
- 도구가 naive 그림을 저절로 고쳐 그리면 "Keep the mistakes exactly as described; this is a teaching example of a wrong drawing." 한 줄을 덧붙여 다시 요청해 주세요.
- 둘의 얼굴·머리·의상이 다르면 비교가 안 되니, guided를 받은 뒤 그것을 첨부해 naive를 다시 받아도 됩니다.

## 4. 저장 이름
`checklist.csv`의 `file` 열 이름 그대로(png 또는 jpg). 이름만 맞으면 제가 크기 변환·WebP·페이지 반영을 합니다.

## 5. 고칠 때 (같은 대화에서)
`Same character, same style and composition. Change only: {고칠 점}. Still no text.`

## 6. refs 폴더
- `p5_haru_anime.png`, `p5_sia_anime.png`, `p5_moa_anime.png` — 기초편에서 받은 애니풍 기준 전신(얼굴·머리 고정용). D03~D08·E01~E04에 첨부
- `cover_index.png` — 기초편 픽셀 표지(그림체 맞춤용). 표지 대화(D01·D02)에 첨부
- `char_*.png` — 연구실 캐릭터 픽셀 얼굴. 표지 대화에 첨부

## 7. F01~F04 다시 받기 (2026-11-23)
E01~E04의 첫 결과는 옷 고정값(실험복·카디건이 따라옴)과 '일부러 틀리게' 요청이 지켜지지 않아, 페이지에 '첫 결과'로 실은 뒤 `prompts/F01_F04_redo_pairs.md`의 편집 방식으로 다시 받습니다.
