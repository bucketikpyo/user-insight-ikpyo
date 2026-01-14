"""
신혼 타겟 재정의: 결혼 3년 이내로 변경
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = Path(__file__).parent
CLEANED_FILE = BASE_DIR / "분석결과/pb_survey_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "분석결과"

df_clean = pd.read_csv(CLEANED_FILE, encoding='utf-8-sig')

print("=" * 80)
print("신혼 타겟 재정의: 결혼 3년 이내")
print("=" * 80)

# 기존 신혼 조건 (5년)
신혼_조건_5년 = [
    '동거 중 (결혼 계획 있음, 6개월 이후)',
    '동거 중 (결혼 계획 있음, 6개월 이내)',
    '결혼한 지 1년 이내',
    '결혼한 지 1~3년',
    '결혼한 지 3~5년'
]

# 새로운 신혼 조건 (3년)
신혼_조건_3년 = [
    '동거 중 (결혼 계획 있음, 6개월 이후)',
    '동거 중 (결혼 계획 있음, 6개월 이내)',
    '결혼한 지 1년 이내',
    '결혼한 지 1~3년'
]

# 그룹 재정의
group1 = df_clean.copy()  # 전체
group2 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트']].copy()  # 2인가구+아파트
group3_old = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트'] & df_clean['Q2_결혼상태'].isin(신혼_조건_5년)].copy()  # 기존 (5년)
group3_new = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트'] & df_clean['Q2_결혼상태'].isin(신혼_조건_3년)].copy()  # 신규 (3년)

print(f"\n[그룹 크기 비교]")
print(f"전체: {len(group1)}명")
print(f"2인가구+아파트: {len(group2)}명")
print(f"신혼 타겟 (기존 5년): {len(group3_old)}명")
print(f"신혼 타겟 (신규 3년): {len(group3_new)}명")
print(f"차이: {len(group3_old) - len(group3_new)}명 감소")

# 새로운 신혼 타겟 저장
df_clean['is_신혼_3년'] = (df_clean['is_2인가구']) & (df_clean['is_아파트']) & (df_clean['Q2_결혼상태'].isin(신혼_조건_3년))

# 업데이트된 데이터 저장
df_clean.to_csv(CLEANED_FILE, index=False, encoding='utf-8-sig')
print(f"\n✓ 업데이트된 데이터 저장 완료")

# 그룹 정의
groups = {
    '전체': group1,
    '2인가구+아파트': group2,
    '신혼타겟': group3_new
}

print("\n" + "=" * 80)
print("핵심 지표 재계산 (신혼 타겟 = 결혼 3년 이내)")
print("=" * 80)

# 1. 침대 사용 빈도
print("\n[1. 침대 사용 빈도 (Q3)]")
for name, group in groups.items():
    거의없다 = (group['Q3_침대사용빈도'] == '거의 없다 (바로 눕거나 잠만 잔다)').sum()
    거의없다_pct = 거의없다 / len(group) * 100
    print(f"{name} (n={len(group)}): 거의 없다 {거의없다_pct:.1f}%")

# 2. 영상 시청 비율
print("\n[2. 영상 시청 비율 (Q5)]")
for name, group in groups.items():
    사용자 = group[group['Q3_침대사용빈도'] != '거의 없다 (바로 눕거나 잠만 잔다)']
    if len(사용자) > 0:
        영상시청 = (사용자['Q5_활동_영상시청'].notna() & (사용자['Q5_활동_영상시청'] != '')).sum()
        영상시청_pct = 영상시청 / len(사용자) * 100
        print(f"{name} (n={len(사용자)}): 영상 시청 {영상시청_pct:.1f}%")

# 3. 헤드보드 중요도
print("\n[3. 헤드보드 중요도 (Q7)]")
for name, group in groups.items():
    중요 = group['Q7_헤드보드중요도'].isin(['매우 중요함', '어느 정도 중요함']).sum()
    중요_pct = 중요 / len(group) * 100
    print(f"{name} (n={len(group)}): 중요 {중요_pct:.1f}%")

# 4. 소프트 타입 비율
print("\n[4. 소프트 타입 헤드보드 비율 (Q8)]")
for name, group in groups.items():
    소프트 = (group['Q8_헤드보드형태'] == '패브릭/쿠션 등 (소프트 타입)').sum()
    소프트_pct = 소프트 / len(group) * 100
    print(f"{name} (n={len(group)}): 소프트 타입 {소프트_pct:.1f}%")

# 5. 헤드보드 만족도
print("\n[5. 헤드보드 만족도 (Q9)]")
for name, group in groups.items():
    유헤드 = group[group['Q8_헤드보드형태'] != '없음(무헤드)']
    if len(유헤드) > 0:
        만족 = 유헤드['Q9_헤드보드편안함'].isin(['매우 그렇다', '어느 정도 그렇다']).sum()
        만족_pct = 만족 / len(유헤드) * 100
        print(f"{name} (n={len(유헤드)}): 만족 {만족_pct:.1f}%")

# 6. TV × 영상 시청
print("\n[6. TV 보유 × 영상 시청]")
for name, group in groups.items():
    사용자 = group[group['Q3_침대사용빈도'] != '거의 없다 (바로 눕거나 잠만 잔다)']
    tv보유 = (사용자['Q6_가구_TV'].notna() & (사용자['Q6_가구_TV'] != ''))
    if tv보유.sum() > 0:
        영상시청 = (사용자[tv보유]['Q5_활동_영상시청'].notna() & (사용자[tv보유]['Q5_활동_영상시청'] != '')).sum()
        영상시청_pct = 영상시청 / tv보유.sum() * 100
        print(f"{name}: TV 있음 + 영상 시청 {영상시청_pct:.1f}%")

# 7. 헤드보드 타입 × 만족도
print("\n[7. 헤드보드 타입 × 만족도]")
for name, group in groups.items():
    # 소프트 타입
    소프트 = group[group['Q8_헤드보드형태'] == '패브릭/쿠션 등 (소프트 타입)']
    if len(소프트) > 0:
        소프트_만족 = 소프트['Q9_헤드보드편안함'].isin(['매우 그렇다', '어느 정도 그렇다']).sum()
        소프트_만족_pct = 소프트_만족 / len(소프트) * 100
        print(f"{name}: 소프트 타입 만족도 {소프트_만족_pct:.1f}%")
    
    # 하드 타입
    하드 = group[group['Q8_헤드보드형태'] == '나무/철제 등 (하드 타입)']
    if len(하드) > 0:
        하드_만족 = 하드['Q9_헤드보드편안함'].isin(['매우 그렇다', '어느 정도 그렇다']).sum()
        하드_만족_pct = 하드_만족 / len(하드) * 100
        print(f"{name}: 하드 타입 만족도 {하드_만족_pct:.1f}%")

print("\n" + "=" * 80)
print("재분석 완료!")
print("=" * 80)

# 결혼 상태 분포 확인
print("\n[신혼 타겟 결혼 상태 분포]")
결혼상태_분포 = group3_new['Q2_결혼상태'].value_counts()
for key, val in 결혼상태_분포.items():
    pct = val / len(group3_new) * 100
    print(f"  {key}: {val}명 ({pct:.1f}%)")

