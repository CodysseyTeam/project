# 🐻 반달곰 커피 경로 탐색 프로젝트 요약

## 📋 프로젝트 개요

**목표**: 집(MyHome)에서 반달곰 커피(BandalgomCoffee)까지의 최단 경로를 찾고, 모든 구조물을 방문하는 최적 투어를 계산

**핵심 기술**: BFS 알고리즘, TSP(외판원 문제), 데이터 시각화

## 🎯 주요 성과

### 1. BFS 알고리즘 구현
- **시간 복잡도**: O(V + E)
- **특징**: 최단 경로 보장, 4방향 이동
- **결과**: 집(14,2) → 커피(2,12) 최단 경로 발견

### 2. TSP 최적화
- **문제**: 모든 구조물을 한 번씩 방문하는 최적 경로
- **해결**: 브루트포스 방식으로 모든 순열 계산
- **결과**: 최적 투어 경로 생성

### 3. 데이터 시각화
- **15×15 격자 지도**: matplotlib 기반 렌더링
- **구조물별 색상 구분**: 직관적인 지도 해석
- **경로 표시**: 빨간 선으로 이동 경로 시각화

## 📊 데이터 분석 결과

### 지도 구조
- **크기**: 15×15 격자 (총 225개 셀)
- **지역**: 4개 지역 (0~3번)
- **주요 구조물**: 
  - MyHome: (14,2)
  - BandalgomCoffee: (2,12)
  - 추가 커피: (3,12)

### 이동 제약
- **건설현장**: ConstructionSite=1인 곳은 통과 불가
- **이동 방식**: 상하좌우 4방향만 허용

## 🚀 실행 방법

### 빠른 실행
```bash
# Linux/Mac
./run_project.sh

# Windows
run_project.bat
```

### 단계별 실행
```bash
# 1. 환경 설정
make setup

# 2. 프로젝트 실행
make run

# 3. 결과 확인
make check-results
```

## 📈 생성되는 결과물

### CSV 파일
- `full_map.csv`: 병합된 전체 지도 데이터
- `home_to_cafe.csv`: 집→커피 최단 경로 좌표
- `optimal_tour.csv`: 최적 투어 경로

### 이미지 파일
- `map.png`: 기본 지도 (구조물만 표시)
- `map_final.png`: 최단 경로 포함 지도
- `map_tour.png`: 투어 경로 포함 지도

## 🧠 학습 가치

### 알고리즘 이해
- **BFS**: 그래프 탐색의 실제 구현
- **TSP**: NP-hard 문제의 접근법
- **최적화**: 브루트포스 vs 휴리스틱

### 데이터 사이언스
- **전처리**: CSV 데이터 처리 및 검증
- **분석**: 통계적 인사이트 도출
- **시각화**: matplotlib을 활용한 데이터 표현

### 소프트웨어 엔지니어링
- **모듈화**: 기능별 파일 분리
- **문서화**: 상세한 README 및 주석
- **에러 처리**: 안정적인 실행 환경

## 🔧 기술 스택

### 핵심 라이브러리
- **pandas**: 데이터 처리 및 분석
- **matplotlib**: 시각화 및 그래프 생성
- **numpy**: 수치 계산

### 개발 도구
- **Python 3.8+**: 메인 프로그래밍 언어
- **venv**: 가상환경 관리
- **Make**: 프로젝트 자동화

## 📚 확장 가능성

### 알고리즘 개선
- **A* 알고리즘**: 휴리스틱 기반 경로 탐색
- **다익스트라**: 가중치 그래프 지원
- **유전 알고리즘**: TSP의 근사 해법

### 기능 확장
- **더 큰 지도**: 격자 크기 확장
- **다중 목적지**: 여러 커피숍 방문
- **실시간 업데이트**: 동적 장애물 처리

## 🎓 교육적 가치

이 프로젝트는 다음과 같은 교육적 가치를 제공합니다:

1. **이론과 실무 연결**: 알고리즘 이론의 실제 적용
2. **문제 해결 능력**: 복잡한 문제의 체계적 접근
3. **코딩 실력**: Python 프로그래밍 능력 향상
4. **데이터 분석**: 실제 데이터를 활용한 분석 경험

---

*이 프로젝트는 BFS 알고리즘과 TSP 문제를 실제 데이터에 적용하여 경로 탐색 시스템을 구현한 교육용 프로젝트입니다.* 