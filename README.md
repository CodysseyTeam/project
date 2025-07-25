# 📘 반달곰 커피를 찾아서: 데이터 분석과 경로 탐색 프로젝트

**BFS 알고리즘을 활용한 최단 경로 탐색 시스템**

이 프로젝트는 그리드 지도에서 BFS(너비 우선 탐색) 알고리즘을 사용하여 집에서 반달곰 커피까지의 최단 경로를 찾고, 모든 구조물을 방문하는 최적 투어를 계산하는 Python 기반 시스템입니다. 단순히 커피숍 가는 길을 찾는 것에서 시작해서, 동네 전체를 효율적으로 둘러볼 수 있는 경로까지 계산해보는 재미있는 프로젝트입니다.

## 📂 프로젝트 구조

```
project/
├── data/                    # 기본 CSV 데이터 파일
│   ├── area_category.csv    # 구조물 카테고리 정의
│   ├── area_map.csv         # 지도 좌표와 건설현장 정보
│   └── area_struct.csv      # 구조물 위치와 지역 정보
├── doc/                     # 문서화
│   ├── structure.md         # 프로젝트 구조 설명
│   └── what_is_BFS.md       # BFS 알고리즘 개념 정리
├── src/                     # Python 소스 코드
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
├── README.md                # 프로젝트 설명
└── .gitignore               # Git 무시 파일 설정
```

## 🎯 프로젝트 목표

**"집(MyHome)에서 반달곰 커피(BandalgomCoffee)까지 가는 최단 경로를 찾고, 모든 구조물을 지나는 최적 투어를 계산하자"**

이 프로젝트는 다음과 같은 목표를 가지고 있습니다.

- **BFS 알고리즘의 실제 적용**: 이론적 개념을 현실적 문제 해결에 적용
- **데이터 분석 및 시각화**: CSV 데이터 처리부터 matplotlib을 활용한 시각화까지
- **TSP(외판원 문제) 해결**: 모든 구조물을 방문하는 최적 경로 계산

## 🗂️ 데이터 구조

### 입력 데이터 파일

| 파일명 | 목적 | 주요 컬럼 | 설명 |
|--------|------|-----------|------|
| `area_category.csv` | 구조물 타입 정의 | `category`, `struct` | 1:아파트, 2:빌딩, 3:집, 4:커피 |
| `area_map.csv` | 지도 격자 정보 | `x`, `y`, `ConstructionSite` | 15×15 격자에서 건설현장 위치 |
| `area_struct.csv` | 구조물 배치 정보 | `x`, `y`, `category`, `area` | 각 좌표의 구조물과 지역 정보 |

### 데이터 특징

- **15×15 격자 지도**: 총 225개 셀로 구성
- **4개 지역(area)**: 0~3번 지역으로 구분
- **주요 구조물**: MyHome(14,2), BandalgomCoffee(2,12), (3,12)
- **이동 제약**: 건설현장(ConstructionSite=1)은 통과 불가

## ⚙️ 핵심 기능

### 1. 데이터 처리 (`caffee_map.py`)

- CSV 파일 로드 및 데이터 유효성 검증
- 카테고리 매핑을 통한 구조물 이름 변환
- 지도 데이터와 구조물 데이터 결합
- 통계 리포트 생성 (지역별, 구조물별 분석)

### 2. BFS 경로 탐색 (`map_direct_save.py`)

**BFS 알고리즘의 핵심 특징**:
- **시간 복잡도**: O(V + E) (V: 정점 수, E: 간선 수)
- **공간 복잡도**: O(V)
- **탐색 방식**: 가까운 노드부터 차례대로 탐색
- **최단 경로 보장**: 가중치 없는 그래프에서 최단 경로 탐색

**구현된 기능**:

```python
class PathFinder:
    def find_shortest_path_bfs(self, start_position, end_position):
        # BFS 구현: 큐를 사용한 너비 우선 탐색
        # 상하좌우 4방향 이동만 허용
        # 건설현장 우회 로직 포함
```

### 3. TSP 최적화 (`map_direct_save.py`)

- **브루트포스 방식**: 모든 가능한 순열 계산
- **구조물 간 거리 사전 계산**: BFS로 각 쌍의 최단 거리 미리 계산
- **최적 투어 생성**: 시작점에서 모든 구조물을 거쳐 최소 거리로 이동

### 4. 시각화 (`map_draw.py`, `map_direct_save.py`)

- **matplotlib 기반 지도 렌더링**
- **구조물별 색상 구분**: 집(초록 삼각형), 커피(초록 사각형), 아파트/빌딩(갈색 원), 건설현장(회색 사각형)
- **경로 표시**: 빨간 선으로 이동 경로 시각화
- **범례 및 격자**: 직관적인 지도 해석을 위한 UI 요소

## 🚀 실행 방법

### 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/kyowon1108/project.git
cd project

# 2. 가상환경 구성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt
```

### 실행 순서

```bash
# 1. 데이터 전처리 및 분석
python src/caffee_map.py

# 2. 기본 지도 생성
python src/map_draw.py

# 3. BFS 경로 탐색 및 TSP 해결
python src/map_direct_save.py
```

## 📊 결과 파일

실행 후 `result/` 폴더에 다음 파일들이 생성됩니다.

| 파일명 | 내용 | 형식 |
|--------|------|------|
| `full_map.csv` | 병합된 전체 지도 데이터 | CSV |
| `home_to_cafe.csv` | 집→커피 최단 경로 좌표 | CSV |
| `optimal_tour.csv` | 모든 구조물 투어 경로 | CSV |
| `map.png` | 기본 지도 (구조물만 표시) | PNG |
| `map_final.png` | 최단 경로 포함 지도 | PNG |
| `map_tour.png` | 투어 경로 포함 지도 | PNG |

## 🧠 알고리즘 상세

### BFS 구현 특징

1. **Queue 자료구조**: FIFO 방식으로 탐색 순서 관리
2. **4방향 이동**: 상하좌우만 허용 (대각선 이동 제외)
3. **방문 체크**: Set을 사용한 중복 방문 방지
4. **경로 추적**: 각 노드에서 이전 경로 정보 유지

### TSP 해결 전략

1. **전처리**: 모든 구조물 간 BFS 거리 계산
2. **순열 생성**: 시작점 제외한 나머지 구조물의 모든 방문 순서
3. **최적화**: 총 이동 거리가 최소인 순서 선택
4. **경로 결합**: 구조물 간 세부 경로를 연결하여 완전한 투어 생성

## 📈 성능 분석

### 복잡도 분석

- **BFS 탐색**: O(225) = O(1) (15×15 고정 격자)
- **TSP 브루트포스**: O(n!) (n: 구조물 개수)

### 확장 가능성

- **더 큰 지도**: 격자 크기 확장 가능
- **다른 알고리즘**: A*, 다익스트라 등으로 교체 가능
- **가중치 그래프**: 이동 비용이 다른 지형 지원 가능

## 🎓 학습 가치

- **그래프 알고리즘**: BFS의 실제 구현과 응용
- **최적화 문제**: TSP와 같은 NP-hard 문제 접근법
- **데이터 사이언스**: 실제 데이터의 전처리, 분석, 시각화 파이프라인
- **소프트웨어 엔지니어링**: 모듈화, 문서화, 에러 처리 등의 모범 사례

---

# 📘 Finding Panda-Bear Coffee: Data Analysis and Pathfinding Project

**Shortest Path Navigation System Using BFS Algorithm**

This project is a Python-based system that uses BFS (Breadth-First Search) algorithm on a grid map to find the shortest path from home to Panda-Bear Coffee and calculate the optimal tour visiting all structures. What started as simply finding the way to a coffee shop has evolved into an interesting project that computes efficient routes to explore the entire neighborhood.

## 📂 Project Structure

```
project/
├── data/                    # Basic CSV data files
│   ├── area_category.csv    # Structure category definitions
│   ├── area_map.csv         # Map coordinates and construction site info
│   └── area_struct.csv      # Structure locations and area information
├── doc/                     # Documentation
│   ├── structure.md         # Project structure explanation
│   └── what_is_BFS.md       # BFS algorithm concept summary
├── src/                     # Python source code
│   ├── caffee_map.py        # Data analysis and merging
│   ├── map_draw.py          # Basic map visualization
│   └── map_direct_save.py   # BFS pathfinding and TSP solving
├── result/                  # Execution result files
│   ├── full_map.csv         # Merged complete map data
│   ├── home_to_cafe.csv     # Home→Cafe shortest path
│   ├── optimal_tour.csv     # Optimal tour path
│   ├── map.png              # Basic map image
│   ├── map_final.png        # Map with shortest path
│   └── map_tour.png         # Map with tour path
├── requirements.txt         # Dependency package list
├── README.md                # Project description
└── .gitignore               # Git ignore file settings
```

## 🎯 Project Goals

**"Find the shortest path from home (MyHome) to Panda-Bear Coffee (BandalgomCoffee) and calculate the optimal tour visiting all structures"**

This project has the following objectives:

- **Practical Application of BFS Algorithm**: Apply theoretical concepts to real-world problem solving
- **Data Analysis and Visualization**: From CSV data processing to visualization using matplotlib
- **TSP (Traveling Salesman Problem) Solution**: Calculate optimal paths visiting all structures

## 🗂️ Data Structure

### Input Data Files

| Filename | Purpose | Key Columns | Description |
|----------|---------|-------------|-------------|
| `area_category.csv` | Structure type definition | `category`, `struct` | 1:Apartment, 2:Building, 3:House, 4:Coffee |
| `area_map.csv` | Map grid information | `x`, `y`, `ConstructionSite` | Construction site locations in 15×15 grid |
| `area_struct.csv` | Structure placement info | `x`, `y`, `category`, `area` | Structure and area info for each coordinate |

### Data Characteristics

- **15×15 Grid Map**: Composed of 225 cells total
- **4 Areas**: Divided into areas 0~3
- **Key Structures**: MyHome(14,2), BandalgomCoffee(2,12), (3,12)
- **Movement Constraints**: Construction sites (ConstructionSite=1) are impassable

## ⚙️ Core Features

### 1. Data Processing (`caffee_map.py`)

- CSV file loading and data validation
- Structure name conversion through category mapping
- Combining map data with structure data
- Statistical report generation (area-wise, structure-wise analysis)

### 2. BFS Pathfinding (`map_direct_save.py`)

**Key Characteristics of BFS Algorithm**:
- **Time Complexity**: O(V + E) (V: vertices, E: edges)
- **Space Complexity**: O(V)
- **Search Method**: Explore nearest nodes first, level by level
- **Shortest Path Guarantee**: Guarantees shortest path in unweighted graphs

**Implemented Features**:

```python
class PathFinder:
    def find_shortest_path_bfs(self, start_position, end_position):
        # BFS implementation: breadth-first search using queue
        # Only allows 4-directional movement (up, down, left, right)
        # Includes construction site avoidance logic
```

### 3. TSP Optimization (`map_direct_save.py`)

- **Brute Force Approach**: Calculate all possible permutations
- **Pre-calculated Inter-structure Distances**: Pre-compute shortest distances between all pairs using BFS
- **Optimal Tour Generation**: Move through all structures with minimum total distance from starting point

### 4. Visualization (`map_draw.py`, `map_direct_save.py`)

- **matplotlib-based Map Rendering**
- **Color-coded Structures**: Houses (green triangles), Coffee shops (green squares), Apartments/Buildings (brown circles), Construction sites (gray squares)
- **Path Display**: Visualize movement paths with red lines
- **Legend and Grid**: UI elements for intuitive map interpretation

## 🚀 How to Run

### Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/kyowon1108/project.git
cd project

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Execution Order

```bash
# 1. Data preprocessing and analysis
python src/caffee_map.py

# 2. Generate basic map
python src/map_draw.py

# 3. BFS pathfinding and TSP solving
python src/map_direct_save.py
```

## 📊 Result Files

After execution, the following files are generated in the `result/` folder:

| Filename | Content | Format |
|----------|---------|--------|
| `full_map.csv` | Merged complete map data | CSV |
| `home_to_cafe.csv` | Home→Coffee shortest path coordinates | CSV |
| `optimal_tour.csv` | Optimal tour path for all structures | CSV |
| `map.png` | Basic map (structures only) | PNG |
| `map_final.png` | Map with shortest path | PNG |
| `map_tour.png` | Map with tour path | PNG |

## 🧠 Algorithm Details

### BFS Implementation Features

1. **Queue Data Structure**: Manage search order using FIFO approach
2. **4-Directional Movement**: Only allow up/down/left/right (no diagonal movement)
3. **Visit Checking**: Prevent duplicate visits using Set
4. **Path Tracking**: Maintain previous path information at each node

### TSP Solution Strategy

1. **Preprocessing**: Calculate BFS distances between all structures
2. **Permutation Generation**: Generate all possible visit orders excluding starting point
3. **Optimization**: Select the order with minimum total movement distance
4. **Path Combination**: Connect detailed paths between structures to create complete tour

## 📈 Performance Analysis

### Complexity Analysis

- **BFS Search**: O(225) = O(1) (fixed 15×15 grid)
- **TSP Brute Force**: O(n!) (n: number of structures)

### Scalability

- **Larger Maps**: Grid size can be expanded
- **Other Algorithms**: Can be replaced with A*, Dijkstra, etc.
- **Weighted Graphs**: Can support terrain with different movement costs

## 🎓 Learning Value

- **Graph Algorithms**: Practical implementation and application of BFS
- **Optimization Problems**: Approaches to NP-hard problems like TSP
- **Data Science**: Real data preprocessing, analysis, and visualization pipeline
- **Software Engineering**: Best practices in modularization, documentation, and error handling