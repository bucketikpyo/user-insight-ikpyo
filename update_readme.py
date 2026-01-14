#!/usr/bin/env python3
"""
README.md 자동 업데이트 스크립트

Git 커밋 전에 실행하여 README.md를 최신 상태로 업데이트합니다.
"""

import os
from datetime import datetime
from pathlib import Path

def get_project_folders():
    """프로젝트 폴더 목록을 가져옵니다."""
    base_path = Path(__file__).parent
    folders = []
    
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
            folders.append(item)
    
    return sorted(folders, key=lambda x: x.name)

def parse_folder_name(folder_name):
    """폴더명에서 연도와 프로젝트명을 추출합니다."""
    # 예: "2512_숏롱분석" -> (2024, 12, "숏롱분석")
    # 예: "2601_PB리서치..." -> (2026, 1, "PB리서치...")
    
    if '_' not in folder_name:
        return None, None, folder_name
    
    date_part, name_part = folder_name.split('_', 1)
    
    if len(date_part) == 4 and date_part.isdigit():
        year = 2000 + int(date_part[:2])
        month = int(date_part[2:])
        return year, month, name_part
    
    return None, None, folder_name

def get_project_description(folder_path):
    """프로젝트 폴더의 README.md에서 설명을 추출합니다."""
    readme_path = folder_path / 'README.md'
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 첫 번째 헤더 다음 줄을 설명으로 사용
                for i, line in enumerate(lines):
                    if line.startswith('#') and i + 1 < len(lines):
                        desc = lines[i + 1].strip()
                        if desc:
                            return desc
        except:
            pass
    return None

def generate_readme():
    """README.md를 생성합니다."""
    folders = get_project_folders()
    
    # 연도별로 그룹화
    projects_by_year = {}
    for folder in folders:
        year, month, name = parse_folder_name(folder.name)
        if year:
            if year not in projects_by_year:
                projects_by_year[year] = []
            
            # 프로젝트 정보 수집
            project_info = {
                'folder_name': folder.name,
                'name': name,
                'month': month,
                'description': get_project_description(folder)
            }
            projects_by_year[year].append(project_info)
    
    # README 생성
    readme_content = """# 🗂️ ikpyo 개인 작업 보관소

완료된 UX 리서치 및 데이터 분석 작업물을 보관하는 공간입니다.

## 📂 보관된 작업

"""
    
    # 연도별로 정렬하여 출력
    for year in sorted(projects_by_year.keys(), reverse=True):
        readme_content += f"### {year}년\n"
        
        # 월별로 정렬
        projects = sorted(projects_by_year[year], key=lambda x: x['month'])
        
        for project in projects:
            # 기본 정보
            readme_content += f"- **{project['name']}"
            
            # 설명이 있으면 추가
            if project['description']:
                readme_content += f"**: {project['description']}\n"
            else:
                readme_content += "**\n"
            
            # 상세 정보
            readme_content += f"  - 기간: {year}.{project['month']:02d}\n"
            readme_content += f"  - [📄 리포트 보기](./{project['folder_name']}/)\n"
        
        readme_content += "\n"
    
    # 하단 정보
    total_projects = sum(len(projects) for projects in projects_by_year.values())
    today = datetime.now().strftime('%Y-%m-%d')
    
    readme_content += """## 🛠️ 사용 도구

- **언어**: Python, SQL
- **분석**: pandas, numpy, scipy, statsmodels
- **시각화**: matplotlib, seaborn, plotly
- **리포트**: Jupyter Notebook, Markdown

## 📝 작업 추가 방법

```bash
# 1. 완료된 작업을 보관소로 복사
cp -r ../완료된작업/ ./YYYY_작업명/

# 2. README 자동 업데이트
python3 update_readme.py

# 3. 커밋 및 푸시
git add .
git commit -m "feat: 작업명 추가"
git push
```

## 📊 통계

"""
    readme_content += f"- **총 작업 수**: {total_projects}개\n"
    readme_content += f"- **마지막 업데이트**: {today}\n"
    readme_content += """
---

**Private Repository** | Personal Work Archive
"""
    
    return readme_content

def main():
    """메인 함수"""
    print("📝 README.md 업데이트 중...")
    
    try:
        readme_content = generate_readme()
        
        # README.md 저장
        readme_path = Path(__file__).parent / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README.md 업데이트 완료!")
        print(f"   파일 위치: {readme_path}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
