"""
침대 사용 행태 설문 결과 분석 스크립트 Part 2
4-6단계: 핵심 분석, 교차 분석, 시각화 및 리포트
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'  # macOS
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 경로 설정
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "분석결과"
OUTPUT_DIR.mkdir(exist_ok=True)

# 정제된 데이터 로드
df_clean = pd.read_csv(OUTPUT_DIR / "pb_survey_cleaned.csv", encoding='utf-8-sig')

# 그룹 정의
group1 = df_clean.copy()  # 전체
group2 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트']].copy()  # 2인가구+아파트
group3 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트'] & df_clean['is_신혼']].copy()  # 신혼 타겟

groups = {
    '전체': group1,
    '2인가구+아파트': group2,
    '신혼타겟': group3
}

print("=" * 80)
print("침대 사용 행태 설문 분석 Part 2")
print("=" * 80)

# ============================================================================
# 4. 핵심 분석 항목 (3그룹 비교)
# ============================================================================
print("\n[4단계] 핵심 분석 항목 3그룹 비교")
print("-" * 80)

# 분석 결과를 저장할 딕셔너리
analysis_results = {}

# 4.1 침대 사용 행태
print("\n4.1 침대 사용 행태 분석")
print("-" * 40)

# Q3: 침대 사용 빈도
print("\n[Q3. 침대에 앉아 기대어 생활하는 빈도]")
q3_results = {}
for name, group in groups.items():
    freq_dist = group['Q3_침대사용빈도'].value_counts()
    freq_pct = (freq_dist / len(group) * 100).round(1)
    q3_results[name] = freq_pct
    print(f"\n{name} (n={len(group)}):")
    for key, val in freq_pct.items():
        print(f"  {key}: {val}%")

# Q4: 머무르는 시간
print("\n[Q4. 한 번에 머무르는 시간]")
q4_results = {}
for name, group in groups.items():
    # Q3에서 "거의 없다" 선택한 사람 제외
    group_filtered = group[group['Q3_침대사용빈도'] != '거의 없다 (바로 눕거나 잠만 잔다)']
    if len(group_filtered) > 0:
        time_dist = group_filtered['Q4_머무르는시간'].value_counts()
        time_pct = (time_dist / len(group_filtered) * 100).round(1)
        q4_results[name] = time_pct
        print(f"\n{name} (n={len(group_filtered)}):")
        for key, val in time_pct.items():
            print(f"  {key}: {val}%")

# Q5: 침대에서 하는 활동
print("\n[Q5. 침대에서 하는 활동 (복수선택)]")
q5_results = {}
activities = ['영상시청', '휴대폰', '독서', '노트북작업', '대화통화', '휴식', '기타']
for name, group in groups.items():
    # Q3에서 "거의 없다" 선택한 사람 제외
    group_filtered = group[group['Q3_침대사용빈도'] != '거의 없다 (바로 눕거나 잠만 잔다)']
    if len(group_filtered) > 0:
        activity_counts = {}
        for activity in activities:
            count = group_filtered['Q5_활동_리스트'].apply(lambda x: activity in str(x)).sum()
            pct = count / len(group_filtered) * 100
            activity_counts[activity] = pct
        q5_results[name] = activity_counts
        print(f"\n{name} (n={len(group_filtered)}):")
        for key, val in sorted(activity_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {key}: {val:.1f}%")

# 가설 검증: 신혼은 침대에서 영상 시청을 많이 한다
print("\n[가설 검증1: 신혼의 영상 시청 비율]")
for name in groups.keys():
    if name in q5_results:
        print(f"{name}: 영상시청 {q5_results[name]['영상시청']:.1f}%")

# 4.2 침실 구성
print("\n\n4.2 침실 구성 분석")
print("-" * 40)

print("\n[Q6. 침실 내 가구/물건 보유율]")
q6_results = {}
furnitures = ['TV', '소파', '화장대', '협탁', '책상', '옷장', '운동기구', '식물', '아기용품', '기타']
for name, group in groups.items():
    furniture_counts = {}
    for furniture in furnitures:
        count = group['Q6_가구_리스트'].apply(lambda x: furniture in str(x)).sum()
        pct = count / len(group) * 100
        furniture_counts[furniture] = pct
    q6_results[name] = furniture_counts
    print(f"\n{name} (n={len(group)}):")
    for key, val in sorted(furniture_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {key}: {val:.1f}%")

# 4.3 헤드보드 관련
print("\n\n4.3 헤드보드 관련 분석")
print("-" * 40)

# Q7: 헤드보드 중요도
print("\n[Q7. 헤드보드 디자인 중요도]")
q7_results = {}
for name, group in groups.items():
    importance_dist = group['Q7_헤드보드중요도'].value_counts()
    importance_pct = (importance_dist / len(group) * 100).round(1)
    q7_results[name] = importance_pct
    print(f"\n{name} (n={len(group)}):")
    for key, val in importance_pct.items():
        print(f"  {key}: {val}%")

# Q8: 헤드보드 형태
print("\n[Q8. 헤드보드 형태]")
q8_results = {}
for name, group in groups.items():
    type_dist = group['Q8_헤드보드형태'].value_counts()
    type_pct = (type_dist / len(group) * 100).round(1)
    q8_results[name] = type_pct
    print(f"\n{name} (n={len(group)}):")
    for key, val in type_pct.items():
        print(f"  {key}: {val}%")

# Q9: 헤드보드 편안함
print("\n[Q9. 헤드보드 편안함 만족도]")
q9_results = {}
for name, group in groups.items():
    # 무헤드 제외
    group_filtered = group[group['Q8_헤드보드형태'] != '없음(무헤드)']
    if len(group_filtered) > 0:
        comfort_dist = group_filtered['Q9_헤드보드편안함'].value_counts()
        comfort_pct = (comfort_dist / len(group_filtered) * 100).round(1)
        q9_results[name] = comfort_pct
        print(f"\n{name} (n={len(group_filtered)}):")
        for key, val in comfort_pct.items():
            print(f"  {key}: {val}%")

# Q10: 불편한 점
print("\n[Q10. 헤드보드 불편한 점 (복수선택)]")
q10_results = {}
discomforts = ['등아픔', '각도', '쿠션감', '머리목', '구조불안', '기타']
for name, group in groups.items():
    # Q9에서 불만족 응답자만
    group_filtered = group[group['Q9_헤드보드편안함'].isin(['그렇지 않다', '전혀 그렇지 않다'])]
    if len(group_filtered) > 0:
        discomfort_counts = {}
        for discomfort in discomforts:
            count = group_filtered['Q10_불편_리스트'].apply(lambda x: discomfort in str(x)).sum()
            pct = count / len(group_filtered) * 100
            discomfort_counts[discomfort] = pct
        q10_results[name] = discomfort_counts
        print(f"\n{name} (n={len(group_filtered)}):")
        for key, val in sorted(discomfort_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {key}: {val:.1f}%")

# Q11: 보완 방법
print("\n[Q11. 불편함 보완 방법 (복수선택)]")
q11_results = {}
solutions = ['베개', '쿠션', '벽', '참고사용', '기타']
for name, group in groups.items():
    # Q9에서 불만족 응답자만
    group_filtered = group[group['Q9_헤드보드편안함'].isin(['그렇지 않다', '전혀 그렇지 않다'])]
    if len(group_filtered) > 0:
        solution_counts = {}
        for solution in solutions:
            count = group_filtered['Q11_보완_리스트'].apply(lambda x: solution in str(x)).sum()
            pct = count / len(group_filtered) * 100
            solution_counts[solution] = pct
        q11_results[name] = solution_counts
        print(f"\n{name} (n={len(group_filtered)}):")
        for key, val in sorted(solution_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {key}: {val:.1f}%")

# ============================================================================
# 5. 교차 분석
# ============================================================================
print("\n\n[5단계] 교차 분석")
print("-" * 80)

# 5.1 침대 사용 빈도 × 헤드보드 만족도
print("\n5.1 침대 사용 빈도 × 헤드보드 만족도")
print("-" * 40)

for name, group in groups.items():
    print(f"\n{name}:")
    # 무헤드 제외
    group_filtered = group[group['Q8_헤드보드형태'] != '없음(무헤드)']
    if len(group_filtered) > 0:
        cross_tab = pd.crosstab(
            group_filtered['침대사용빈도_그룹'],
            group_filtered['헤드보드만족도_그룹'],
            normalize='index'
        ) * 100
        print(cross_tab.round(1))

# 5.2 TV 보유 × 영상 시청 행태
print("\n\n5.2 TV 보유 × 영상 시청 행태")
print("-" * 40)

for name, group in groups.items():
    print(f"\n{name}:")
    # Q3에서 "거의 없다" 제외
    group_filtered = group[group['Q3_침대사용빈도'] != '거의 없다 (바로 눕거나 잠만 잔다)']
    if len(group_filtered) > 0:
        group_filtered['has_TV'] = group_filtered['Q6_가구_리스트'].apply(lambda x: 'TV' in str(x))
        group_filtered['영상시청'] = group_filtered['Q5_활동_리스트'].apply(lambda x: '영상시청' in str(x))
        
        tv_yes = group_filtered[group_filtered['has_TV']]
        tv_no = group_filtered[~group_filtered['has_TV']]
        
        if len(tv_yes) > 0:
            print(f"  TV 있음 (n={len(tv_yes)}): 영상시청 {tv_yes['영상시청'].sum() / len(tv_yes) * 100:.1f}%")
        if len(tv_no) > 0:
            print(f"  TV 없음 (n={len(tv_no)}): 영상시청 {tv_no['영상시청'].sum() / len(tv_no) * 100:.1f}%")

# 5.3 헤드보드 타입 × 만족도
print("\n\n5.3 헤드보드 타입 × 만족도")
print("-" * 40)

for name, group in groups.items():
    print(f"\n{name}:")
    # 무헤드 제외
    group_filtered = group[group['Q8_헤드보드형태'] != '없음(무헤드)']
    if len(group_filtered) > 0:
        cross_tab = pd.crosstab(
            group_filtered['Q8_헤드보드형태'],
            group_filtered['헤드보드만족도_그룹'],
            normalize='index'
        ) * 100
        print(cross_tab.round(1))

# ============================================================================
# 6. 시각화
# ============================================================================
print("\n\n[6단계] 시각화 차트 생성")
print("-" * 80)

# 6.1 침대 사용 빈도 분포
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('침대 사용 빈도 분포 (그룹별 비교)', fontsize=14, fontweight='bold')

for idx, (name, group) in enumerate(groups.items()):
    freq_counts = group['침대사용빈도_그룹'].value_counts()
    freq_order = ['거의없음', '가끔', '자주']
    freq_counts = freq_counts.reindex(freq_order, fill_value=0)
    
    axes[idx].bar(range(len(freq_counts)), freq_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[idx].set_xticks(range(len(freq_counts)))
    axes[idx].set_xticklabels(freq_counts.index, rotation=0)
    axes[idx].set_title(f'{name} (n={len(group)})')
    axes[idx].set_ylabel('응답자 수')
    
    # 비율 표시
    for i, v in enumerate(freq_counts.values):
        pct = v / len(group) * 100
        axes[idx].text(i, v, f'{pct:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '1_침대사용빈도_분포.png', dpi=300, bbox_inches='tight')
print("✓ 저장: 1_침대사용빈도_분포.png")
plt.close()

# 6.2 침대에서 하는 활동 Top 5
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('침대에서 하는 활동 Top 5 (그룹별)', fontsize=14, fontweight='bold')

for idx, name in enumerate(groups.keys()):
    if name in q5_results:
        activity_data = q5_results[name]
        top5 = sorted(activity_data.items(), key=lambda x: x[1], reverse=True)[:5]
        activities_top5 = [x[0] for x in top5]
        values_top5 = [x[1] for x in top5]
        
        axes[idx].barh(range(len(activities_top5)), values_top5, color='#95E1D3')
        axes[idx].set_yticks(range(len(activities_top5)))
        axes[idx].set_yticklabels(activities_top5)
        axes[idx].set_title(name)
        axes[idx].set_xlabel('비율 (%)')
        axes[idx].invert_yaxis()
        
        # 값 표시
        for i, v in enumerate(values_top5):
            axes[idx].text(v, i, f' {v:.1f}%', va='center')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '2_침대활동_Top5.png', dpi=300, bbox_inches='tight')
print("✓ 저장: 2_침대활동_Top5.png")
plt.close()

# 6.3 헤드보드 만족도
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('헤드보드 편안함 만족도 (그룹별)', fontsize=14, fontweight='bold')

for idx, name in enumerate(groups.keys()):
    if name in q9_results:
        satisfaction_data = q9_results[name]
        sat_order = ['매우 그렇다', '어느 정도 그렇다', '보통이다', '그렇지 않다', '전혀 그렇지 않다']
        sat_values = [satisfaction_data.get(key, 0) for key in sat_order]
        
        colors = ['#2ECC71', '#27AE60', '#F39C12', '#E74C3C', '#C0392B']
        axes[idx].bar(range(len(sat_order)), sat_values, color=colors)
        axes[idx].set_xticks(range(len(sat_order)))
        axes[idx].set_xticklabels(['매우\n그렇다', '어느정도\n그렇다', '보통', '그렇지\n않다', '전혀\n그렇지않다'], fontsize=9)
        axes[idx].set_title(name)
        axes[idx].set_ylabel('비율 (%)')
        
        # 값 표시
        for i, v in enumerate(sat_values):
            if v > 0:
                axes[idx].text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '3_헤드보드_만족도.png', dpi=300, bbox_inches='tight')
print("✓ 저장: 3_헤드보드_만족도.png")
plt.close()

# 6.4 침실 내 가구 보유율
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('침실 내 가구 보유율 Top 5 (그룹별)', fontsize=14, fontweight='bold')

for idx, name in enumerate(groups.keys()):
    if name in q6_results:
        furniture_data = q6_results[name]
        top5 = sorted(furniture_data.items(), key=lambda x: x[1], reverse=True)[:5]
        furnitures_top5 = [x[0] for x in top5]
        values_top5 = [x[1] for x in top5]
        
        axes[idx].barh(range(len(furnitures_top5)), values_top5, color='#F8B739')
        axes[idx].set_yticks(range(len(furnitures_top5)))
        axes[idx].set_yticklabels(furnitures_top5)
        axes[idx].set_title(name)
        axes[idx].set_xlabel('보유율 (%)')
        axes[idx].invert_yaxis()
        
        # 값 표시
        for i, v in enumerate(values_top5):
            axes[idx].text(v, i, f' {v:.1f}%', va='center')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '4_침실가구_보유율.png', dpi=300, bbox_inches='tight')
print("✓ 저장: 4_침실가구_보유율.png")
plt.close()

print("\n" + "=" * 80)
print("4-6단계 완료!")
print("=" * 80)

