# 프로젝트 구조 설명

## 📁 전체 프로젝트 구조

```
codyssey_project/
├── data/                    # 기본 CSV 데이터 파일
│   ├── area_category.csv    # 구조물 카테고리 정의 (1:아파트, 2:빌딩, 3:집, 4:커피)
│   ├── area_map.csv         # 지도 좌표와 건설현장 정보 (15×15 격자)
│   └── area_struct.csv      # 구조물 위치와 지역 정보
├── doc/                     # 문서화
│   ├── structure.md         # 프로젝트 구조 설명 (이 파일)
│   └── what_is_BFS.md       # BFS 알고리즘 개념 정리
├── src/                     # Python 소스 코드 (수정 불가)
│   ├── caffee_map.py        # 데이터 분석 및 병합
│   ├── map_draw.py          # 기본 지도 시각화
│   └── map_direct_save.py   # BFS 경로 탐색 및 TSP 해결
├── result/                  # 실행 결과 파일
│   ├── full_map.csv         # 병합된 전체 지도 데이터
│   ├── home_to_cafe.csv     # 집→카페 최단 경로
│   ├── optimal_tour.csv     # 최적 투어 경로
│   ├── map.png              # 기본 지도 이미지
│   ├── map_final.png        # 최단 경로 포함 지도
│   └── map_tour.png         # 투어 경로 포함 지도
├── requirements.txt         # 의존성 패키지 목록
├── pyproject.toml           # Python 프로젝트 설정
├── Makefile                 # 프로젝트 관리 스크립트
├── run_project.sh           # Linux/Mac 실행 스크립트
├── run_project.bat          # Windows 실행 스크립트
├── docker-run.sh            # Linux/Mac Docker 실행 스크립트
├── docker-run.bat           # Windows Docker 실행 스크립트
├── Dockerfile               # Docker 이미지 정의
├── docker-compose.yml       # Docker Compose 설정
├── .dockerignore            # Docker 빌드 제외 파일
├── README.md                # 프로젝트 설명
└── .gitignore               # Git 무시 파일 설정
```

## 🔧 실행 방법

### 1. Docker 사용 (권장 - OS 독립적)

#### Docker 설치
- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

#### Docker로 실행
```bash
# Linux/Mac
./docker-run.sh

# Windows
docker-run.bat

# Makefile 사용
make docker-run
```

#### Docker 개발 환경
```bash
# 대화형 개발 환경 실행
make docker-dev

# Docker 컨테이너 정리
make docker-clean
```

### 2. 로컬 환경 실행

#### 자동 실행 (권장)
```bash
# Linux/Mac
./run_project.sh

# Windows
run_project.bat
```

#### Makefile 사용
```bash
make setup    # 초기 설정
make run      # 프로젝트 실행
make test     # 프로젝트 테스트
make clean    # 임시 파일 정리
```

#### 수동 실행
```bash
# 1. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 프로젝트 실행
python src/caffee_map.py
python src/map_draw.py
python src/map_direct_save.py
```

## 📊 데이터 파일 설명

### area_category.csv
- **목적**: 구조물 타입 정의
- **주요 컬럼**: `category`, `struct`
- **카테고리**: 1(아파트), 2(빌딩), 3(집), 4(커피)

### area_map.csv
- **목적**: 지도 격자 정보
- **주요 컬럼**: `x`, `y`, `ConstructionSite`
- **크기**: 15×15 격자 (총 225개 셀)
- **특징**: ConstructionSite=1인 곳은 건설현장으로 통과 불가

### area_struct.csv
- **목적**: 구조물 배치 정보
- **주요 컬럼**: `x`, `y`, `category`, `area`
- **지역**: 0~3번 지역으로 구분
- **주요 구조물**: MyHome(14,2), BandalgomCoffee(2,12), (3,12)

## 🎯 핵심 기능

### 1. 데이터 처리 (caffee_map.py)
- CSV 파일 로드 및 데이터 유효성 검증
- 카테고리 매핑을 통한 구조물 이름 변환
- 지도 데이터와 구조물 데이터 결합
- 통계 리포트 생성

### 2. BFS 경로 탐색 (map_direct_save.py)
- **알고리즘**: BFS (Breadth-First Search)
- **시간 복잡도**: O(V + E)
- **특징**: 최단 경로 보장, 4방향 이동만 허용
- **구현**: Queue 자료구조 사용

### 3. TSP 최적화 (map_direct_save.py)
- **문제**: 외판원 문제 (Traveling Salesman Problem)
- **해결 방법**: 브루트포스 (모든 순열 계산)
- **목표**: 모든 구조물을 방문하는 최적 경로 찾기

### 4. 시각화 (map_draw.py, map_direct_save.py)
- **라이브러리**: matplotlib
- **구조물별 색상**: 집(초록 삼각형), 커피(초록 사각형), 아파트/빌딩(갈색 원)
- **경로 표시**: 빨간 선으로 이동 경로 시각화

## 📈 결과 파일

### CSV 파일
- `full_map.csv`: 병합된 전체 지도 데이터
- `home_to_cafe.csv`: 집에서 커피까지의 최단 경로 좌표
- `optimal_tour.csv`: 모든 구조물을 방문하는 최적 투어 경로

### 이미지 파일
- `map.png`: 기본 지도 (구조물만 표시)
- `map_final.png`: 최단 경로가 포함된 지도
- `map_tour.png`: 투어 경로가 포함된 지도

## 🐳 Docker 사용의 장점

### OS 독립성
- **Windows, macOS, Linux**: 동일한 환경에서 실행
- **의존성 문제 해결**: Python 버전, 라이브러리 버전 충돌 방지
- **일관된 결과**: 모든 환경에서 동일한 결과 보장

### 개발 편의성
- **빠른 설정**: Docker만 설치하면 즉시 실행 가능
- **환경 격리**: 로컬 시스템에 영향 없음
- **쉬운 정리**: 컨테이너 삭제로 깔끔한 정리

### 배포 용이성
- **이식성**: 다른 시스템으로 쉽게 이전
- **확장성**: 여러 인스턴스 동시 실행 가능
- **버전 관리**: 이미지 태그로 버전 관리

## 🚨 주의사항

1. **src 폴더 수정 금지**: Python 파일 구조는 변경하지 마세요
2. **데이터 파일**: data 폴더의 CSV 파일은 원본 그대로 유지
3. **가상환경**: 로컬 실행 시 반드시 가상환경 활성화
4. **의존성**: requirements.txt에 명시된 패키지 버전 준수
5. **Docker 권한**: Docker 실행 시 적절한 권한 필요

## 🔍 문제 해결

### 일반적인 문제들
1. **모듈을 찾을 수 없음**: 가상환경이 활성화되지 않았거나 의존성 설치 필요
2. **데이터 파일 오류**: data 폴더의 CSV 파일이 손상되었거나 누락됨
3. **메모리 부족**: TSP 계산 시 구조물이 너무 많을 경우 발생 가능
4. **Docker 권한 오류**: Docker 그룹에 사용자 추가 필요

### 디버깅 방법
```bash
# 로컬 환경
make test          # 프로젝트 상태 확인
make check-results # 결과 파일 확인
python -c "import matplotlib, pandas, numpy"  # 패키지 설치 확인

# Docker 환경
make docker-build  # Docker 이미지 재빌드
docker-compose logs # 컨테이너 로그 확인
docker system prune # Docker 시스템 정리
```

### OS별 특이사항
- **Windows**: Docker Desktop 설치 필요, WSL2 권장
- **macOS**: Docker Desktop 설치 필요, Intel/Apple Silicon 호환
- **Linux**: Docker Engine 설치, 사용자를 docker 그룹에 추가