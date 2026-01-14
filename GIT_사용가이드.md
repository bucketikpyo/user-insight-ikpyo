# 📚 ikpyo-archive Git 사용 가이드

## 🎯 저장소 구조

```
0000_Cursor/                    # 작업 공간 (Git 없음)
├── _임시분석/                  # 임시 분석 파일
├── 2601_더레인 리서치/         # 진행 중인 작업
├── user-insight/               # 팀 저장소 (별도 Git)
└── ikpyo-archive/              # ⭐ 개인 저장소 (Git 연결)
    ├── .git/
    ├── README.md               # 자동 업데이트됨!
    ├── update_readme.py        # README 업데이트 스크립트
    ├── 2512_숏롱분석/          # 완료된 작업
    └── 2601_PB리서치.../       # 완료된 작업
```

## 📝 작업 완료 후 보관 프로세스

### 1단계: 작업 파일 이동

```bash
# 작업 공간에서 보관소로 복사
cd /Users/ikpyo.hong/Downloads/0000_Cursor
cp -r ./완료된작업폴더/ ./ikpyo-archive/YYMM_작업명/
```

**폴더명 규칙**: `YYMM_작업명`
- 예: `2512_숏롱분석`, `2601_PB리서치`
- YY: 연도 (24=2024, 26=2026)
- MM: 월 (01~12)

### 2단계: README 자동 업데이트 (선택사항)

```bash
cd ikpyo-archive
python3 update_readme.py
```

💡 **자동화됨**: 커밋 시 자동으로 실행되므로 생략 가능!

### 3단계: Git 커밋 & 푸시

```bash
cd ikpyo-archive
git add .
git commit -m "feat: 작업명 추가"
git push
```

## 🤖 자동화 기능

### Pre-commit Hook
커밋할 때마다 자동으로:
1. ✅ `update_readme.py` 실행
2. ✅ README.md 업데이트
3. ✅ 업데이트된 README.md를 커밋에 포함

**설정 위치**: `.git/hooks/pre-commit`

### README 자동 업데이트 내용
- 📂 프로젝트 목록 (연도별 정렬)
- 📊 총 작업 수
- 📅 마지막 업데이트 날짜

## 💡 커밋 메시지 규칙

### 형식
```
타입: 간단한 설명

상세 설명 (선택사항)
```

### 타입
- `feat`: 새로운 작업 추가
- `docs`: 문서 수정
- `fix`: 오류 수정
- `refactor`: 파일 정리/구조 변경

### 예시
```bash
git commit -m "feat: 2601 더레인 리서치 추가"
git commit -m "docs: README 수동 수정"
git commit -m "refactor: 폴더명 변경"
```

## 🔧 수동 README 업데이트

자동 업데이트가 마음에 안 들면:

```bash
# 1. 스크립트 실행
python3 update_readme.py

# 2. 생성된 README.md 확인 및 수정
open README.md

# 3. 커밋
git add README.md
git commit -m "docs: README 수동 업데이트"
```

## 📊 현재 설정 확인

```bash
# Git 저장소 확인
cd ikpyo-archive
git remote -v
# 출력: origin  https://github.com/bucketikpyo/ikpyo_cursor.git

# 추적 중인 파일 확인
git ls-files

# 무시되는 파일 확인
git status --ignored
```

## ⚠️ 주의사항

### ✅ DO
- 완료된 작업만 보관소에 추가
- 폴더명 규칙 준수 (`YYMM_작업명`)
- 각 프로젝트 폴더에 README.md 포함 권장

### ❌ DON'T
- 진행 중인 작업 커밋 금지
- 민감 정보 (.env, 비밀번호 등) 커밋 금지
- 대용량 파일 (100MB 이상) 주의

## 🆘 문제 해결

### README가 자동 업데이트 안 됨
```bash
# pre-commit hook 권한 확인
ls -la .git/hooks/pre-commit

# 권한 없으면 추가
chmod +x .git/hooks/pre-commit
```

### 커밋 취소하고 싶을 때
```bash
# 마지막 커밋 취소 (파일은 유지)
git reset --soft HEAD~1

# 마지막 커밋 완전 취소
git reset --hard HEAD~1
```

### 푸시 실패 시
```bash
# 원격 저장소 최신 상태 가져오기
git pull --rebase

# 다시 푸시
git push
```

## 📞 도움말

- Git 상태 확인: `git status`
- 커밋 히스토리: `git log --oneline`
- 변경 사항 확인: `git diff`

---

**작성일**: 2026-01-14  
**버전**: 1.0
