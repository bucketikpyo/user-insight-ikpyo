"""
서베이몽키 vs 분석 결과 차이 확인
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
CLEANED_FILE = BASE_DIR / "분석결과/pb_survey_cleaned.csv"

df_clean = pd.read_csv(CLEANED_FILE, encoding='utf-8-sig')

print("=" * 80)
print("서베이몽키 vs 분석 결과 비교")
print("=" * 80)

# Q3: 침대 사용 빈도
print("\n[Q3. 침대 사용 빈도]")
print("\n1. 전체 응답자 (n=675) - 서베이몽키 대시보드와 동일")
print("-" * 40)

q3_전체 = df_clean['Q3_침대사용빈도'].value_counts()
q3_전체_pct = (q3_전체 / len(df_clean) * 100).round(2)

for key, val in q3_전체.items():
    pct = q3_전체_pct[key]
    print(f"  {key}: {val}명 ({pct}%)")

print(f"\n  ✓ '거의 없다': {q3_전체_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%")
print(f"  ✓ 서베이몽키: 37.48%")
print(f"  ✓ 차이: {abs(q3_전체_pct['거의 없다 (바로 눕거나 잠만 잔다)'] - 37.48):.2f}%p")

# 2인가구+아파트
print("\n2. 2인가구+아파트 (n=234)")
print("-" * 40)

group2 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트']]
q3_2인 = group2['Q3_침대사용빈도'].value_counts()
q3_2인_pct = (q3_2인 / len(group2) * 100).round(2)

for key, val in q3_2인.items():
    pct = q3_2인_pct[key]
    print(f"  {key}: {val}명 ({pct}%)")

print(f"\n  ✓ '거의 없다': {q3_2인_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%")

# 신혼 타겟
print("\n3. 신혼 타겟 (n=159)")
print("-" * 40)

group3 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트'] & df_clean['is_신혼']]
q3_신혼 = group3['Q3_침대사용빈도'].value_counts()
q3_신혼_pct = (q3_신혼 / len(group3) * 100).round(2)

for key, val in q3_신혼.items():
    pct = q3_신혼_pct[key]
    print(f"  {key}: {val}명 ({pct}%)")

print(f"\n  ✓ '거의 없다': {q3_신혼_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%")

# 결론
print("\n" + "=" * 80)
print("결론")
print("=" * 80)

print(f"""
서베이몽키 대시보드: 전체 675명 기준
  → 거의 없다: 37.48% (253명)

분석 리포트:
  → 전체 (675명): {q3_전체_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%
  → 2인가구+아파트 (234명): {q3_2인_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%
  → 신혼 타겟 (159명): {q3_신혼_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%

💡 차이 원인:
  리포트에서 39.6%는 "신혼 타겟"만의 비율입니다.
  전체 응답자 기준으로는 {q3_전체_pct['거의 없다 (바로 눕거나 잠만 잔다)']}%로 
  서베이몽키(37.48%)와 거의 일치합니다!
  
  반올림 차이: {abs(q3_전체_pct['거의 없다 (바로 눕거나 잠만 잔다)'] - 37.48):.2f}%p
""")

print("=" * 80)

