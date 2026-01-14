"""
침대 사용 행태 설문 결과 분석 스크립트
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
DATA_FILE = BASE_DIR / "pb_survey_raw data.csv"
OUTPUT_DIR = BASE_DIR / "분석결과"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("침대 사용 행태 설문 분석 시작")
print("=" * 80)

# ============================================================================
# 1. 데이터 로드 및 파싱
# ============================================================================
print("\n[1단계] Raw CSV 파일 로드 및 헤더 구조 파싱")
print("-" * 80)

# CSV 파일 읽기 (첫 2행이 헤더)
df_raw = pd.read_csv(DATA_FILE, encoding='utf-8')

# 헤더 정보 추출
header_row1 = df_raw.columns.tolist()  # Row 1: 질문
header_row2 = df_raw.iloc[0].tolist()  # Row 2: 세부 옵션

# 실제 데이터는 3행부터 (index 1부터)
df = df_raw.iloc[1:].reset_index(drop=True)

print(f"✓ 데이터 로드 완료: {len(df)}명의 응답자")
print(f"✓ 총 컬럼 수: {len(df.columns)}개")

# 컬럼명 매핑 (분석 편의를 위해 간단한 이름으로 변경)
# 각 질문별로 컬럼 인덱스 파악
col_mapping = {}
current_col = 0

# Q0: respondent_id
col_mapping['respondent_id'] = current_col
current_col += 1

# Q1: 인원 구성
col_mapping['Q1_인원구성'] = current_col
current_col += 1

# Q2: 결혼/동거 상태 (+ 기타 주관식)
col_mapping['Q2_결혼상태'] = current_col
col_mapping['Q2_결혼상태_기타'] = current_col + 1
current_col += 2

# Q3: 침대 사용 빈도
col_mapping['Q3_침대사용빈도'] = current_col
current_col += 1

# Q4: 머무르는 시간
col_mapping['Q4_머무르는시간'] = current_col
current_col += 1

# Q5: 침대에서 하는 활동 (복수선택 - 7개 옵션)
col_mapping['Q5_활동_영상시청'] = current_col
col_mapping['Q5_활동_휴대폰'] = current_col + 1
col_mapping['Q5_활동_독서'] = current_col + 2
col_mapping['Q5_활동_노트북작업'] = current_col + 3
col_mapping['Q5_활동_대화통화'] = current_col + 4
col_mapping['Q5_활동_휴식'] = current_col + 5
col_mapping['Q5_활동_기타'] = current_col + 6
current_col += 7

# Q6: 침실 가구/물건 (복수선택 - 10개 옵션)
col_mapping['Q6_가구_TV'] = current_col
col_mapping['Q6_가구_소파'] = current_col + 1
col_mapping['Q6_가구_화장대'] = current_col + 2
col_mapping['Q6_가구_협탁'] = current_col + 3
col_mapping['Q6_가구_책상'] = current_col + 4
col_mapping['Q6_가구_옷장'] = current_col + 5
col_mapping['Q6_가구_운동기구'] = current_col + 6
col_mapping['Q6_가구_식물'] = current_col + 7
col_mapping['Q6_가구_아기용품'] = current_col + 8
col_mapping['Q6_가구_기타'] = current_col + 9
current_col += 10

# Q7: 헤드보드 중요도
col_mapping['Q7_헤드보드중요도'] = current_col
current_col += 1

# Q8: 헤드보드 형태
col_mapping['Q8_헤드보드형태'] = current_col
current_col += 1

# Q8-1: 무헤드 이유 (주관식)
col_mapping['Q8_무헤드이유'] = current_col
current_col += 1

# Q8-2: 무헤드 불편점 (주관식)
col_mapping['Q8_무헤드불편점'] = current_col
current_col += 1

# Q9: 헤드보드 편안함
col_mapping['Q9_헤드보드편안함'] = current_col
current_col += 1

# Q10: 불편한 점 (복수선택 - 6개 옵션)
col_mapping['Q10_불편_등아픔'] = current_col
col_mapping['Q10_불편_각도'] = current_col + 1
col_mapping['Q10_불편_쿠션감'] = current_col + 2
col_mapping['Q10_불편_머리목'] = current_col + 3
col_mapping['Q10_불편_구조불안'] = current_col + 4
col_mapping['Q10_불편_기타'] = current_col + 5
current_col += 6

# Q11: 보완 방법 (복수선택 - 5개 옵션)
col_mapping['Q11_보완_베개'] = current_col
col_mapping['Q11_보완_쿠션'] = current_col + 1
col_mapping['Q11_보완_벽'] = current_col + 2
col_mapping['Q11_보완_참고사용'] = current_col + 3
col_mapping['Q11_보완_기타'] = current_col + 4
current_col += 5

# 인구통계 정보
col_mapping['동의여부'] = current_col
current_col += 1
col_mapping['거주형태'] = current_col
col_mapping['거주형태_기타'] = current_col + 1
current_col += 2
col_mapping['성별'] = current_col
current_col += 1
col_mapping['출생연도'] = current_col
current_col += 1
col_mapping['인터뷰희망'] = current_col
current_col += 1
col_mapping['User_ID'] = current_col

# 새로운 DataFrame 생성 (컬럼명 변경)
df_clean = pd.DataFrame()

for new_name, idx in col_mapping.items():
    if idx < len(df.columns):
        df_clean[new_name] = df.iloc[:, idx]

print(f"✓ 컬럼명 매핑 완료: {len(df_clean.columns)}개 컬럼")

# ============================================================================
# 2. 데이터 정제 및 변환
# ============================================================================
print("\n[2단계] 복수선택 문항 변환, 로직 스킵 처리, 파생변수 생성")
print("-" * 80)

# 2.1 복수 선택 문항을 리스트로 변환
print("\n2.1 복수 선택 문항 처리...")

# Q5: 침대에서 하는 활동
q5_cols = [col for col in df_clean.columns if col.startswith('Q5_활동_')]
df_clean['Q5_활동_리스트'] = df_clean[q5_cols].apply(
    lambda row: [col.replace('Q5_활동_', '') for col, val in row.items() if pd.notna(val) and val != ''],
    axis=1
)

# Q6: 침실 가구
q6_cols = [col for col in df_clean.columns if col.startswith('Q6_가구_')]
df_clean['Q6_가구_리스트'] = df_clean[q6_cols].apply(
    lambda row: [col.replace('Q6_가구_', '') for col, val in row.items() if pd.notna(val) and val != ''],
    axis=1
)

# Q10: 불편한 점
q10_cols = [col for col in df_clean.columns if col.startswith('Q10_불편_')]
df_clean['Q10_불편_리스트'] = df_clean[q10_cols].apply(
    lambda row: [col.replace('Q10_불편_', '') for col, val in row.items() if pd.notna(val) and val != ''],
    axis=1
)

# Q11: 보완 방법
q11_cols = [col for col in df_clean.columns if col.startswith('Q11_보완_')]
df_clean['Q11_보완_리스트'] = df_clean[q11_cols].apply(
    lambda row: [col.replace('Q11_보완_', '') for col, val in row.items() if pd.notna(val) and val != ''],
    axis=1
)

print(f"✓ Q5 활동: 평균 {df_clean['Q5_활동_리스트'].apply(len).mean():.1f}개 선택")
print(f"✓ Q6 가구: 평균 {df_clean['Q6_가구_리스트'].apply(len).mean():.1f}개 선택")
print(f"✓ Q10 불편점: 평균 {df_clean['Q10_불편_리스트'].apply(len).mean():.1f}개 선택")
print(f"✓ Q11 보완방법: 평균 {df_clean['Q11_보완_리스트'].apply(len).mean():.1f}개 선택")

# 2.2 로직 스킵 확인
print("\n2.2 설문 로직 확인...")

# 로직 1: Q3 "거의 없다" → Q4, Q5 스킵
logic1_count = ((df_clean['Q3_침대사용빈도'] == '거의 없다 (바로 눕거나 잠만 잔다)') & 
                (df_clean['Q4_머무르는시간'].isna() | (df_clean['Q4_머무르는시간'] == ''))).sum()
print(f"✓ 로직1 (Q3 거의없다→Q4/Q5 스킵): {logic1_count}명")

# 로직 2: Q8 "없음(무헤드)" → 무헤드 질문 응답, Q9/Q10/Q11 스킵
logic2_count = (df_clean['Q8_헤드보드형태'] == '없음(무헤드)').sum()
print(f"✓ 로직2 (Q8 무헤드→특별질문): {logic2_count}명")

# 로직 3: Q9 불만족 → Q10, Q11 응답
logic3_count = (df_clean['Q9_헤드보드편안함'].isin(['그렇지 않다', '전혀 그렇지 않다'])).sum()
print(f"✓ 로직3 (Q9 불만족→Q10/Q11 응답): {logic3_count}명")

# 2.3 파생 변수 생성
print("\n2.3 파생 변수 생성...")

# 타겟 그룹 분류
df_clean['is_2인가구'] = df_clean['Q1_인원구성'] == '2인 가구 (배우자 / 연인 / 친구 등)'
df_clean['is_아파트'] = df_clean['거주형태'] == '아파트'

# 신혼 조건: 2인 가구 + (동거 중 결혼 계획 있음 / 결혼 1년 이내 / 결혼 1~3년 / 결혼 3~5년)
신혼_조건 = [
    '동거 중 (결혼 계획 있음, 6개월 이후)',
    '동거 중 (결혼 계획 있음, 6개월 이내)',
    '결혼한 지 1년 이내',
    '결혼한 지 1~3년',
    '결혼한 지 3~5년'
]
df_clean['is_신혼'] = (df_clean['is_2인가구']) & (df_clean['Q2_결혼상태'].isin(신혼_조건))

# 행태 분류
# 침대 사용 빈도 그룹
def categorize_frequency(val):
    if pd.isna(val) or val == '':
        return None
    if val == '거의 없다 (바로 눕거나 잠만 잔다)':
        return '거의없음'
    elif val in ['주 1–2회 정도']:
        return '가끔'
    else:  # 주 3–4회, 거의 매일, 매일 비교적 오랜 시간
        return '자주'

df_clean['침대사용빈도_그룹'] = df_clean['Q3_침대사용빈도'].apply(categorize_frequency)

# 침대 사용 시간 그룹
def categorize_duration(val):
    if pd.isna(val) or val == '':
        return None
    if val in ['5분 이내 (잠깐 휴대폰 확인 정도)', '5–15분']:
        return '단시간'
    elif val == '15–30분':
        return '중간'
    else:  # 30분–1시간, 1시간 이상
        return '장시간'

df_clean['침대사용시간_그룹'] = df_clean['Q4_머무르는시간'].apply(categorize_duration)

# 헤드보드 만족도 그룹
def categorize_satisfaction(val):
    if pd.isna(val) or val == '':
        return None
    if val in ['매우 그렇다', '어느 정도 그렇다']:
        return '만족'
    elif val == '보통이다':
        return '보통'
    else:  # 그렇지 않다, 전혀 그렇지 않다
        return '불만족'

df_clean['헤드보드만족도_그룹'] = df_clean['Q9_헤드보드편안함'].apply(categorize_satisfaction)

# 연령대 계산 (2026년 기준)
df_clean['출생연도_int'] = pd.to_numeric(df_clean['출생연도'], errors='coerce')
df_clean['나이'] = 2026 - df_clean['출생연도_int']
df_clean['연령대'] = (df_clean['나이'] // 10) * 10

print(f"✓ 2인가구: {df_clean['is_2인가구'].sum()}명 ({df_clean['is_2인가구'].sum()/len(df_clean)*100:.1f}%)")
print(f"✓ 아파트 거주: {df_clean['is_아파트'].sum()}명 ({df_clean['is_아파트'].sum()/len(df_clean)*100:.1f}%)")
print(f"✓ 신혼: {df_clean['is_신혼'].sum()}명 ({df_clean['is_신혼'].sum()/len(df_clean)*100:.1f}%)")

# ============================================================================
# 3. 3개 그룹 정의 및 샘플 사이즈 확인
# ============================================================================
print("\n[3단계] 3개 분석 그룹 정의 및 샘플 사이즈 확인")
print("-" * 80)

# 그룹 정의
group1 = df_clean.copy()  # 전체
group2 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트']].copy()  # 2인가구+아파트
group3 = df_clean[df_clean['is_2인가구'] & df_clean['is_아파트'] & df_clean['is_신혼']].copy()  # 신혼 타겟

print(f"\n그룹1 (전체): {len(group1)}명")
print(f"그룹2 (2인가구+아파트): {len(group2)}명 ({len(group2)/len(group1)*100:.1f}%)")
print(f"그룹3 (신혼 타겟): {len(group3)}명 ({len(group3)/len(group1)*100:.1f}%)")

# 각 그룹의 인구통계 특성
print("\n[그룹별 인구통계 특성]")
for i, (name, group) in enumerate([("전체", group1), ("2인가구+아파트", group2), ("신혼타겟", group3)], 1):
    print(f"\n{name} (n={len(group)}):")
    print(f"  - 평균 나이: {group['나이'].mean():.1f}세")
    print(f"  - 성별 분포:")
    print(f"    {group['성별'].value_counts().to_dict()}")
    print(f"  - 거주형태:")
    for key, val in group['거주형태'].value_counts().head(3).items():
        print(f"    {key}: {val}명 ({val/len(group)*100:.1f}%)")

# 데이터 저장
output_file = OUTPUT_DIR / "pb_survey_cleaned.csv"
df_clean.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✓ 정제된 데이터 저장: {output_file}")

print("\n" + "=" * 80)
print("1-3단계 완료!")
print("=" * 80)

