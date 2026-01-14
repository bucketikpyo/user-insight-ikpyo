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
    """프로젝트 폴더의 README.md에서 상세 설명을 추출합니다."""
    readme_path = folder_path / 'README.md'
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 프로젝트 정보 추출
                info = {
                    'subtitle': None,
                    'summary': None,
                    'findings': [],
                    'impact': None
                }
                
                lines = content.split('\n')
                
                # 부제목 찾기 (> "..." 형식)
                for line in lines:
                    if line.startswith('> **"') and line.endswith('"**'):
                        info['subtitle'] = line.replace('> **"', '').replace('"**', '')
                        break
                
                # 리서치 목적/개요 찾기
                in_purpose = False
                for i, line in enumerate(lines):
                    if '리서치 목적' in line or '🎯' in line:
                        in_purpose = True
                        continue
                    if in_purpose and line.strip() and not line.startswith('#') and not line.startswith('-'):
                        info['summary'] = line.strip()
                        break
                
                # 핵심 발견/주요 발견 찾기
                in_findings = False
                for i, line in enumerate(lines):
                    if '주요 발견' in line or '핵심 발견' in line:
                        in_findings = True
                        continue
                    if in_findings:
                        if line.startswith('#'):
                            break
                        if line.strip().startswith(('1.', '2.', '3.', '4.', '-')):
                            finding = line.strip().lstrip('1234567890.- ')
                            if finding:
                                info['findings'].append(finding)
                
                # 임팩트/시사점 찾기
                for i, line in enumerate(lines):
                    if '임팩트' in line or '시사점' in line or '실무 임팩트' in line:
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line and not next_line.startswith('#'):
                                info['impact'] = next_line.lstrip('- ')
                        break
                
                return info
        except Exception as e:
            print(f"  ⚠️  README 파싱 오류 ({folder_path.name}): {e}")
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
        readme_content += f"### {year}년\n\n"
        
        # 월별로 정렬
        projects = sorted(projects_by_year[year], key=lambda x: x['month'])
        
        for idx, project in enumerate(projects):
            desc = project['description']
            
            # 프로젝트 제목 (이모지 포함)
            emoji = "🔍" if "숏" in project['name'] or "분석" in project['name'] else "🛏️" if "침대" in project['name'] or "PB" in project['name'] else "📊"
            readme_content += f"#### {emoji} {project['name']}\n"
            
            # 부제목 (있으면)
            if desc and desc.get('subtitle'):
                readme_content += f'**"{desc["subtitle"]}"**\n\n'
            
            # 요약 (있으면)
            if desc and desc.get('summary'):
                readme_content += f"{desc['summary']}\n\n"
            
            # 핵심 발견 (있으면)
            if desc and desc.get('findings'):
                readme_content += "**핵심 발견**:\n"
                for finding in desc['findings'][:4]:  # 최대 4개만
                    readme_content += f"- {finding}\n"
                readme_content += "\n"
            
            # 임팩트 (있으면)
            if desc and desc.get('impact'):
                readme_content += f"**임팩트**: {desc['impact']}\n\n"
            
            # 메타 정보
            readme_content += f"- 기간: {year}.{project['month']:02d}\n"
            
            # 추가 정보는 각 프로젝트의 README에서 가져올 수 있음
            # 여기서는 기본 정보만 표시
            
            readme_content += f"- [📄 리포트 보기](./{project['folder_name']}/)\n"
            
            # 프로젝트 사이 구분선 (마지막 프로젝트 제외)
            if idx < len(projects) - 1:
                readme_content += "\n---\n"
            
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
