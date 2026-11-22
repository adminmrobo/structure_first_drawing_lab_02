# -*- coding: utf-8 -*-
"""본문 '숫자로 한 번 해 보기'·퀴즈·평가 점수 검산. python3 build/check_numbers.py"""
import math, sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2
from content_b import P3, P4
ok = True
def chk(name, got, want, tol=0.05):
    global ok
    good = abs(got - want) <= tol; ok &= good
    print(("OK " if good else "XX "), name, round(got, 4), "기대", want)
r = math.radians; t = math.tan; c = math.cos
chk("1-2 8×90°", 8 * r(90), 12.6); chk("1-2 8×45°", 8 * r(45), 6.3); chk("1-2 12×15°", 12 * r(15), 3.1); chk("1-2 퀴즈 10×1.57", 10 * 1.57, 15.7)
chk("1-5 45°", 1 / t(r(45)), 1); chk("1-5 60°", 1 / t(r(60)), 0.58, 0.006); chk("1-5 30°", 1 / t(r(30)), 1.73, 0.006)
chk("2-1 비율", 120 / 60, 2); chk("2-1 물결 천", 4 * 2, 8); chk("2-1 개수", 60 / 4, 15); chk("2-1 검산", 15 * 8, 120); chk("2-1 퀴즈", 90 / 45, 2)
chk("2-4 어깨", 36 * t(r(10)), 6.3, 0.06); chk("2-4 단추", 8 * t(r(10)), 1.4); chk("2-4 퀴즈", 36 * 0.176, 6.3, 0.06)
chk("2-5 6/tan60", 6 / t(r(60)), 3.5); chk("2-5 6/tan30", 6 / t(r(30)), 10.4); chk("2-5 12/tan30", 12 / t(r(30)), 20.8)
chk("3-1 고관절", 14 * r(90), 22.0); chk("3-1 무릎", 11 * r(150), 28.8); chk("3-1 팔꿈치", 8 * r(20), 2.8); chk("3-1 퀴즈", 11 * 2.62, 28.8)
chk("3-4 허리", 66 / 24, 2.75, 0.001); chk("3-4 둘레", 2 * math.pi * 30, 188, 0.6); chk("3-4 밑단", 2 * math.pi * 30 / 24, 7.9); chk("3-4 배율", (2 * math.pi * 30 / 24) / (66 / 24), 2.9)
chk("3-4 허리 반지름", 66 / (2 * math.pi), 10.5)
chk("4-3 45°", 5 * t(r(45)), 5); chk("4-3 60°", 5 * t(r(60)), 8.7)
for ph, want in [(0, 1), (60, .75), (90, .5), (120, .25), (180, 0)]: chk(f"4-4 φ{ph}", (1 + c(r(ph))) / 2, want, 0.001)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
L = (0.6, 0, 0.8); chk("4-5 정면", dot((0, 0, 1), L), 0.8); chk("4-5 오른쪽", dot((0.6, 0, 0.8), L), 1.0); chk("4-5 왼쪽", dot((-0.6, 0, 0.8), L), 0.28)
for P in (P1, P2, P3, P4):
    J = P["judge"]; a, b = sum(J["a"][1]), sum(J["b"][1]); txt = J["result"][0][2]
    good = txt.startswith(f"{a} 대 {b}"); ok &= good; print(("OK " if good else "XX "), P["no"], "부 평가", a, ":", b, txt[:12])
    for s in P["steps"]:
        q = s["quiz"]; assert 0 <= q[2] < len(q[1])
print("전체 통과" if ok else "검산 실패"); sys.exit(0 if ok else 1)
