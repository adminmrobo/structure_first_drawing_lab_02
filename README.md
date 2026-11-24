# 구조 먼저 그리기 연구실 02 · 실천편 — 주름과 그림자를 직접 넣어 보기

주름 없는 선화에 **접점 → 주름 → 그림자** 순서로 직접 넣어 보는 연구실 해설 시리즈입니다. 기초편([구조 먼저 보는 캐릭터 그리기 연구실](https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/))의 원리를 실제 그림에 옮깁니다.

- 사이트: https://adminmrobo.github.io/structure_first_drawing_lab_02/ (GitHub Pages, main 루트)
- 글: 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 구성
| 부 | 파일 | 모델 | 내용 |
|---|---|---|---|
| 목차 | `index.html` | — | 읽는 순서, 큰 그림, 공통으로 흐르는 순서, 등장인물 |
| 1부 | `01_standing.html` | 하루(후드 집업) | 접점, 굽힌 관절(두께 × 각), 꼭대기 방향, 큰 형체 그림자, 단차 그림자(높이 ÷ tan) |
| 2부 | `02_frills.html` | 시아(메이드복) | 프릴(개더 비율), 조임, 큰 선 먼저, 짝 장식(거리 × tan), 섞인 그림자 |
| 3부 | `03_sitting.html` | 모아(블레이저) | 관절마다 남는 천, 단추 고정 주름, 빳빳한 천, 퍼진 주름치마(둘레 ÷ 개수), 겹침 순서·깊이 지도 |
| 4부 | `04_light_dir.html` | 셋 모두 | 광원 방향, 아래 빛, 옆 빛(거리 × tan), 위에서 본 각도((1 + cos φ) ÷ 2), 노멀 지도로 다시 조명 |
| 5부 | `practice/index.html` | — | 실전 연습장: 접점 탐정 · 프릴 공방 · 조명실 · 숙제 책상 |

역할: 모델 하루·시아·모아 / 화가 주판봇·초파리 / 평가단 X1~X3 / 해설 박사.

부마다 끝에 **프롬프트로 직접 만들어 보기** 절이 있습니다. 실습 2개씩(A: 이 페이지 그림을 만든 요청문 → B: 원리 하나만 바꾸는 문장, 예상 결과·확인할 것), 내 요청문 조립 상자, 비교 그림과 점검표. 실습 내용은 `build/make_lab.py`, B 결과 그림 요청은 `docs/image_requests_make/`(`build/make_requests_make.py`). 참고 그림은 `assets/refs/`.

## 만들기·점검
```bash
python3 build/build.py          # 페이지 다시 만들기
python3 build/check_numbers.py  # 숫자 검산
python3 build/make_og.py        # 공유 미리보기
python3 -m http.server 8765 &   # 아래 두 점검은 로컬 서버 필요
python3 build/check_pages.py    # 콘솔 오류·패널·390/1280px 넘침
python3 build/check_missions.py # 연습장 미션 판정
python3 build/make_requests.py  # 그림 요청 꾸러미(docs/image_requests)
```
그림 26장(표지 6 픽셀아트 + 본문 20 애니풍, Genspark)은 `assets/img/{키}.webp`에 있습니다. 표지는 480×270 격자를 4배로 키운 무손실 WebP입니다. 요청문은 `docs/image_requests/`.

## 출처
연습 구성은 다테 나오토 『デジタルツールで描く！服のシワと影の描き方』(マイナビ) 3장 실천편과 출판사 특전 PDF를 참고했습니다. 책의 그림·사진·문장·도식은 옮기지 않았고, 연구실 캐릭터와 직접 움직이는 실험으로 새로 구성했습니다. 숫자 식은 원리를 보이려고 덧붙인 것입니다. AI 연결의 출처(포즈 추정, ControlNet, IC-Light, DDPM)는 각 페이지 바닥글에 있습니다.

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.
