import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

# 한글 폰트 설정
plt.rcParams['font.family'] = ['AppleGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class Queue:
    """
    BFS 알고리즘에서 사용할 큐(Queue) 자료구조
    - 먼저 들어온 데이터가 먼저 나가는 FIFO(First In First Out) 방식
    - deque 라이브러리 대신 직접 구현한 간단한 큐
    """
    def __init__(self):
        """큐 초기화 - 빈 리스트로 시작"""
        self.items = []
    
    def append(self, item):
        """큐의 뒤쪽에 새로운 아이템 추가"""
        self.items.append(item)
    
    def popleft(self):
        """큐의 앞쪽에서 아이템을 꺼내서 반환"""
        if self.items:
            return self.items.pop(0)  # 맨 앞의 요소를 제거하고 반환
        raise IndexError("pop from empty queue")
    
    def __len__(self):
        """큐에 들어있는 아이템의 개수 반환"""
        return len(self.items)
    
    def __bool__(self):
        """큐가 비어있는지 확인 (True: 비어있지 않음, False: 비어있음)"""
        return len(self.items) > 0


def generate_permutations(items):
    """
    주어진 리스트의 모든 순열(permutation)을 리스트로 반환하는 함수
    - itertools.permutations를 쓰지 않고 직접 구현
    - TSP(외판원 문제) 등에서 사용 가능

    예시: [1,2,3] → [
        [1,2,3], [1,3,2],
        [2,1,3], [2,3,1],
        [3,1,2], [3,2,1]
    ]
    """
    def permute(current, remaining, result):
        if not remaining:
            result.append(current)
        else:
            for i in range(len(remaining)):
                permute(current + [remaining[i]], remaining[:i] + remaining[i+1:], result)

    result = []
    permute([], items, result)
    return result


class PathFinder:
    """
    BFS(너비 우선 탐색) 알고리즘을 사용해서 최단 경로를 찾는 클래스
    - 지도 데이터를 분석하고 구조물 간의 최단 경로를 계산
    - TSP(외판원 문제)를 해결해서 모든 구조물을 지나는 최적 경로도 찾음
    """
    
    def __init__(self, data_frame):
        """
        PathFinder 클래스 초기화
        - 지도 데이터를 받아서 분석하고 필요한 정보를 추출
        """
        self.data_frame = data_frame
        
        # 지도의 경계 좌표 찾기 (x, y의 최대/최소값)
        self.max_x = int(data_frame['x'].max())
        self.max_y = int(data_frame['y'].max())
        self.min_x = int(data_frame['x'].min())
        self.min_y = int(data_frame['y'].min())
        
        # 구조물 정보 정리 (빈 값이나 None 값들을 빈 문자열로 통일)
        self.data_frame['struct'] = self.data_frame['struct'].astype(str).str.strip()
        self.data_frame['struct'] = self.data_frame['struct'].replace('None', '')
        self.data_frame['struct'] = self.data_frame['struct'].replace('nan', '')
        
        # 시작점(집)과 도착점(카페) 위치 찾기
        self.start_pos = self.find_structure_position('MyHome')
        self.cafe_pos = self.find_structure_position('BandalgomCoffee')
        
        # 지도상의 모든 구조물 위치 찾기
        self.all_structure_positions = self.find_all_structure_positions()
        
        # 찾은 정보들을 콘솔에 출력 (디버깅용)
        print(f'시작점 (MyHome): {self.start_pos}')
        print(f'도착점 (BandalgomCoffee): {self.cafe_pos}')
        print(f'모든 구조물 위치: {self.all_structure_positions}')
        
    def find_structure_position(self, structure_name):
        """
        특정 이름의 구조물 위치를 찾는 함수
        
        매개변수:
        - structure_name: 찾고자 하는 구조물 이름 (예: 'MyHome', 'BandalgomCoffee')
        
        반환값:
        - (x, y) 튜플: 구조물의 좌표
        """
        # DataFrame에서 해당 구조물이 있는 행 찾기
        result = self.data_frame[self.data_frame['struct'] == structure_name]
        if result.empty:
            # 구조물을 찾을 수 없으면 에러 발생
            raise ValueError(f'{structure_name}을 찾을 수 없습니다.')
        
        # 첫 번째 매칭되는 위치의 x, y 좌표 반환
        return (int(result.iloc[0]['x']), int(result.iloc[0]['y']))
    
    def find_all_structure_positions(self):
        """
        지도상의 모든 구조물 위치를 찾는 함수
        - TSP 문제 해결 시 방문해야 할 모든 지점들을 파악하기 위해 사용
        
        반환값:
        - 구조물 위치들의 리스트 [(x1, y1), (x2, y2), ...]
        """
        structures = []
        # 찾아야 할 구조물 종류들
        structure_types = ['MyHome', 'BandalgomCoffee', 'Apartment', 'Building']
        
        # 각 구조물 종류별로 위치 찾기
        for structure_type in structure_types:
            structure_positions = self.data_frame[self.data_frame['struct'] == structure_type]
            for _, row in structure_positions.iterrows():
                # 각 구조물의 좌표를 리스트에 추가
                structures.append((int(row['x']), int(row['y'])))
        
        # 중복된 위치 제거하고 반환
        return list(set(structures))
    
    def is_valid_position(self, x_coord, y_coord):
        """
        주어진 좌표가 이동 가능한 유효한 위치인지 확인하는 함수
        
        매개변수:
        - x_coord, y_coord: 확인하고자 하는 좌표
        
        반환값:
        - True: 이동 가능한 위치
        - False: 이동 불가능한 위치 (경계 밖이거나 건설현장인 경우)
        """
        # 1. 지도 경계 밖인지 확인
        if (x_coord < self.min_x or x_coord > self.max_x or 
            y_coord < self.min_y or y_coord > self.max_y):
            return False
        
        # 2. 해당 위치가 건설현장인지 확인
        # DataFrame에서 해당 좌표의 셀 찾기
        cell = self.data_frame[
            (self.data_frame['x'] == x_coord) & 
            (self.data_frame['y'] == y_coord)
        ]
        # 건설현장(ConstructionSite=1)이면 이동 불가
        if not cell.empty and cell.iloc[0]['ConstructionSite'] == 1:
            return False
        
        return True
    
    def get_neighbor_positions(self, position):
        """
        현재 위치에서 이동 가능한 인접한 위치들을 찾는 함수
        - BFS 알고리즘에서 다음에 탐색할 위치들을 결정할 때 사용
        
        매개변수:
        - position: 현재 위치 (x, y)
        
        반환값:
        - 이동 가능한 인접 위치들의 리스트
        """
        x_coord, y_coord = position
        neighbors = []
        
        # 상하좌우 4방향 (직선 이동)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for delta_x, delta_y in directions:
            new_x, new_y = x_coord + delta_x, y_coord + delta_y
            if self.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def calculate_distance(self, position1, position2):
        """
        두 위치 간의 직선 거리(유클리드 거리)를 계산하는 함수
        - 실제로는 사용되지 않지만, 거리 계산이 필요할 때를 위해 준비된 함수
        
        공식: sqrt((x2-x1)² + (y2-y1)²)
        """
        return ((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)**0.5
    
    def find_shortest_path_bfs(self, start_position, end_position):
        """
        BFS(너비 우선 탐색) 알고리즘을 사용해서 두 지점 간의 최단 경로를 찾는 함수
        
        BFS의 특징:
        - 시작점에서 가까운 지점부터 차례대로 탐색
        - 처음 도착점에 도달했을 때가 바로 최단 경로
        - 큐(Queue)를 사용해서 탐색할 위치들을 관리
        
        매개변수:
        - start_position: 시작 위치 (x, y)
        - end_position: 목표 위치 (x, y)
        
        반환값:
        - path: 최단 경로 (위치들의 리스트)
        - distance: 총 이동 거리
        """
        # 시작점과 도착점이 같으면 바로 반환
        if start_position == end_position:
            return [start_position], 0
        
        # BFS를 위한 큐 초기화
        # 큐에는 (현재위치, 지금까지의경로) 튜플을 저장
        queue = Queue()
        queue.append((start_position, [start_position]))
        
        # 이미 방문한 위치들을 기록 (중복 방문 방지)
        visited_nodes = set([start_position])
        
        # 큐가 빌 때까지 반복 (탐색할 위치가 있는 동안)
        while queue:
            # 큐에서 다음에 탐색할 위치와 경로 가져오기
            current_position, path = queue.popleft()
            
            # 현재 위치에서 이동 가능한 인접 위치들 확인
            for neighbor in self.get_neighbor_positions(current_position):
                # 이미 방문한 위치는 건너뛰기
                if neighbor in visited_nodes:
                    continue
                
                # 새로운 경로 = 기존 경로 + 인접 위치
                new_path = path + [neighbor]
                
                # 목표점에 도달했는지 확인
                if neighbor == end_position:
                    # 경로의 총 거리 계산
                    total_distance = 0
                    for i in range(len(new_path) - 1):
                        total_distance += 1
                    
                    return new_path, total_distance
                
                # 방문 기록에 추가하고 큐에 넣기
                visited_nodes.add(neighbor)
                queue.append((neighbor, new_path))
        
        # 경로를 찾을 수 없으면 None과 무한대 반환
        return None, float('inf')
    
    def find_optimal_structure_tour(self):
        """
        TSP(외판원 문제) 알고리즘으로 모든 구조물을 지나는 최적 경로를 찾는 함수

        반환값: 최적 투어 경로와 총 거리
        """
        structures = self.all_structure_positions.copy()
        print(f'전체 구조물 개수: {len(structures)}')
        print(f'구조물 위치들: {structures}')
        
        # 시작점이 구조물 목록에 없으면 추가
        if self.start_pos not in structures:
            print(f'시작점 {self.start_pos}이 구조물 목록에 없어서 추가합니다.')
            structures.append(self.start_pos)
        
        print(f'TSP에 사용할 구조물들: {structures}')
        
        # 1. 모든 구조물 간의 최단 거리 미리 계산
        # (각 쌍마다 BFS를 실행해서 최단 경로와 거리 저장)
        structure_distances = {}  # 거리 저장용
        structure_paths = {}      # 경로 저장용
        failed_connections = []   # 연결 불가능한 쌍들
        
        print('구조물 간 최단 거리 계산 중...')
        for i, structure1 in enumerate(structures):
            for j, structure2 in enumerate(structures):
                if i != j:  # 같은 구조물끼리는 계산하지 않음
                    # BFS로 structure1에서 structure2까지의 최단 경로 찾기
                    path, distance = self.find_shortest_path_bfs(structure1, structure2)
                    if path:
                        # 경로를 찾으면 저장
                        structure_distances[(structure1, structure2)] = distance
                        structure_paths[(structure1, structure2)] = path
                        print(f'{structure1} -> {structure2}: 거리 {distance:.2f}')
                    else:
                        # 경로를 찾을 수 없으면 실패 목록에 추가
                        failed_connections.append((structure1, structure2))
                        print(f'경로 없음: {structure1} -> {structure2}')
        
        # 연결되지 않은 구조물들 처리
        if failed_connections:
            print(f'연결되지 않은 구조물 쌍들: {failed_connections}')
            print('일부 구조물은 공사장과 겹쳐있어 생략합니다.')
            
            # 연결 가능한 구조물들만 추출
            connected_structures = set()
            for (struct1, struct2) in structure_distances.keys():
                connected_structures.add(struct1)
                connected_structures.add(struct2)
            
            # 시작점이 연결되지 않으면 투어 불가능
            if self.start_pos not in connected_structures:
                print('시작점이 다른 구조물과 연결되지 않습니다.')
                return None, float('inf')
            
            structures = list(connected_structures)
            print(f'연결된 구조물들로 투어 재시도: {structures}')
        
        # 2. TSP 해결 (브루트포스)
        start_structure = self.start_pos
        # 시작점을 제외한 나머지 구조물들
        other_structures = [structure for structure in structures if structure != start_structure]
        
        if not other_structures:
            print('투어할 다른 구조물이 없습니다.')
            return [start_structure], 0
        
        # 최적 결과를 저장할 변수들
        best_tour = None
        best_distance = float('inf')
        valid_tour_count = 0
        
        # 가능한 순열 개수 계산 (디버깅용)
        permutation_count = 0
        for perm in generate_permutations(other_structures):
            permutation_count += 1
        
        print(f'가능한 순열 개수: {permutation_count}')
        print('최적 투어 계산 중...')
        
        # 모든 가능한 방문 순서에 대해 계산
        for permutation in generate_permutations(other_structures):
            # 투어 = 시작점 + 순열
            current_tour = [start_structure] + permutation
            total_distance = 0
            valid_tour = True
            
            # 이 순서로 방문할 때의 총 거리 계산
            for i in range(len(current_tour) - 1):
                key = (current_tour[i], current_tour[i + 1])
                if key in structure_distances:
                    # 이미 계산된 거리 사용
                    total_distance += structure_distances[key]
                else:
                    # 연결되지 않은 구조물 쌍이면 무효한 투어
                    valid_tour = False
                    break
            
            # 유효한 투어이고 현재까지의 최단 거리보다 짧으면 업데이트
            if valid_tour:
                valid_tour_count += 1
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_tour = current_tour
        
        print(f'유효한 투어 개수: {valid_tour_count}')
        
        # 3. 최적 경로 생성
        # 구조물들을 방문하는 순서는 정해졌지만,
        # 실제 이동 경로(각 구조물 간의 세부 경로)를 연결해야 함
        if best_tour:
            print(f'최적 투어 순서: {best_tour}')
            full_path = [best_tour[0]]  # 시작점부터 시작
            
            # 각 구조물 간의 세부 경로를 연결
            for i in range(len(best_tour) - 1):
                key = (best_tour[i], best_tour[i + 1])
                segment_path = structure_paths[key]
                # 첫 번째 점은 이미 full_path에 있으므로 제외하고 추가
                full_path.extend(segment_path[1:])
            
            return full_path, best_distance
        else:
            print('유효한 투어를 찾을 수 없습니다.')
        
        return None, float('inf')


def save_path_to_dataframe(path, file_name):
    """
    계산된 경로를 DataFrame으로 변환하고 CSV 파일로 저장하는 함수
    
    매개변수:
    - path: 경로 (좌표들의 리스트)
    - file_name: 저장할 파일명
    
    반환값:
    - DataFrame: 경로를 담은 데이터프레임
    """
    if path:
        # 경로를 DataFrame으로 변환
        # x, y 좌표와 단계 번호 포함
        path_dataframe = pd.DataFrame(path, columns=['x', 'y'])
        path_dataframe['step'] = range(len(path))  # 0, 1, 2, ... 단계 번호
        
        # CSV 파일로 저장
        path_dataframe.to_csv(file_name, index=False)
        print(f'경로가 {file_name}에 저장되었습니다.')
        return path_dataframe
    else:
        print('저장할 경로가 없습니다.')
        return None


def create_map_visualization(df, path, file_name, map_title):
    """지도와 경로를 시각화해서 이미지 파일로 저장하는 함수"""

    # struct 칼럼 정리 (예외 상황 전부 처리)
    df['struct'] = df['struct'].astype(str).str.strip()
    df['struct'] = df['struct'].replace(['None', 'nan'], '')

    # 그래프 설정
    fig, ax = plt.subplots(figsize=(15, 12))
    ax.set_aspect('equal')  # x, y 축 비율을 1:1로 고정

    # 지도 경계 설정
    max_x = int(df['x'].max())
    max_y = int(df['y'].max())
    min_x = int(df['x'].min())
    min_y = int(df['y'].min())

    # 축 범위 설정 (여백 포함)
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)  # y축은 뒤집어서 표시

    # 그리드 라인
    for x in range(min_x, max_x + 1):
        ax.axvline(x + 0.5, color='lightgray', linewidth=0.3, alpha=0.5)
    for y in range(min_y, max_y + 1):
        ax.axhline(y + 0.5, color='lightgray', linewidth=0.3, alpha=0.5)

    # 구조물 시각화
    for _, row in df.iterrows():
        x, y = int(row['x']), int(row['y'])
        struct = row['struct']
        is_construction = row['ConstructionSite'] == 1

        if is_construction:
            # 건설현장: 회색 사각형
            ax.add_patch(Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='gray', alpha=0.6))
        elif struct in ['Apartment', 'Building']:
            # 아파트/빌딩: 갈색 원
            ax.plot(x, y, 'o', color='saddlebrown', markersize=20)
        elif struct == 'BandalgomCoffee':
            # 카페: 녹색 사각형
            ax.add_patch(Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color='green', alpha=0.9))
        elif struct == 'MyHome':
            # 집: 녹색 삼각형
            ax.plot(x, y, marker='^', color='green', markersize=20)

    # 경로 그리기
    if path and len(path) > 1:
        # 경로의 x, y 좌표들을 분리
        path_x_coords = [pos[0] for pos in path]
        path_y_coords = [pos[1] for pos in path]
        
        # 빨간 선으로 경로 표시
        ax.plot(path_x_coords, path_y_coords, 'r-', linewidth=3, alpha=0.8, label='Path')
        
        # 시작점과 끝점 표시 (구조물과 겹치지 않도록 크기 0)
        ax.plot(path_x_coords[0], path_y_coords[0], 'go', markersize=0, label='Start')
        ax.plot(path_x_coords[-1], path_y_coords[-1], 'ro', markersize=0, label='End')

    # 좌측 상단에 범례 추가 (다른 구조물 피함)
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Apartment/Building',
               markerfacecolor='saddlebrown', markersize=8),
        Line2D([0], [0], marker='s', color='w', label='BandalgomCoffee',
               markerfacecolor='green', markersize=8),
        Line2D([0], [0], marker='^', color='w', label='MyHome',
               markerfacecolor='green', markersize=8),
        Line2D([0], [0], marker='s', color='w', label='Construction Site',
               markerfacecolor='gray', markersize=8),
        Line2D([0], [0], color='red', linewidth=3, label='Path')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

    # 제목과 축 라벨 설정
    ax.set_title(map_title, fontsize=14)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)

    # 이미지 파일로 저장
    plt.tight_layout()  # 레이아웃 조정
    plt.savefig(file_name, dpi=300, bbox_inches='tight')  # 고해상도로 저장
    plt.close()  # 메모리 해제
    print(f'지도가 {file_name}에 저장되었습니다.')


def main():
    """ 
    1. CSV 파일에서 지도 데이터 읽기
    2. PathFinder 객체 생성 및 초기화
    3. 집에서 카페까지 최단 경로 찾기
    4. 결과를 CSV 파일과 이미지로 저장
    5. 보너스: 모든 구조물을 지나는 최적 투어 찾기
    """
    try:
        # 1. CSV 파일에서 지도 데이터 읽기 (데이터가 제대로 불러와졌는지 검증)
        map_data = pd.read_csv('result/full_map.csv')
        print(f'지도 데이터 로드 완료: {len(map_data)}개 셀')
        
        # 2. PathFinder 객체 생성 및 초기화
        # 지도 데이터를 분석하고 구조물 위치들을 파악
        path_finder = PathFinder(map_data)
        
        # 3. 집에서 카페까지 최단 경로 찾기
        print('\n=== 집에서 카페까지 최단 경로 탐색 ===')
        # BFS 알고리즘으로 MyHome에서 BandalgomCoffee까지의 최단 경로 계산
        shortest_path, path_distance = path_finder.find_shortest_path_bfs(
            path_finder.start_pos,  # 시작점: MyHome 위치
            path_finder.cafe_pos    # 도착점: BandalgomCoffee 위치
        )
        
        # 4. 최단 경로 결과 처리
        if shortest_path:
            print('최단 경로를 찾았습니다!')
            print(f'거리: {path_distance:.2f}')  # 총 이동 거리
            print(f'경로 단계 수: {len(shortest_path)}')  # 거쳐가는 셀의 개수
            
            # 경로를 CSV 파일로 저장
            path_dataframe = save_path_to_dataframe(shortest_path, 'result/home_to_cafe.csv')
            
            # 지도 시각화 (경로 포함)
            create_map_visualization(map_data, shortest_path, 'result/map_final.png', 
                                   '집에서 카페까지 최단 경로')
            
        else:
            print('경로를 찾을 수 없습니다.')
        
        # 5. (보너스) 모든 구조물을 지나는 최적 투어
        print('\n=== 보너스: 모든 구조물 투어 ===')
        # TSP(외판원 문제) 알고리즘으로 모든 구조물을 방문하는 최적 경로 계산
        tour_path, tour_distance = path_finder.find_optimal_structure_tour()
        
        # 6. 투어 결과 처리
        if tour_path:
            print('최적 투어를 찾았습니다!')
            print(f'총 거리: {tour_distance:.2f}')  # 모든 구조물을 방문하는 총 거리
            print(f'경로 단계 수: {len(tour_path)}')  # 전체 이동 단계 수
            
            # 투어 경로를 CSV 파일로 저장
            tour_dataframe = save_path_to_dataframe(tour_path, 'result/optimal_tour.csv')
            
            # 투어 지도 시각화
            create_map_visualization(map_data, tour_path, 'result/map_tour.png', 
                                   '모든 구조물을 지나는 최적 투어')
        else:
            print('투어 경로를 찾을 수 없습니다.')
            
    except FileNotFoundError:
        # CSV 파일이 없을 때 에러 처리
        print('CSV 파일을 찾을 수 없습니다.')
    except Exception as error:
        # 기타 에러 처리
        print(f'오류가 발생했습니다: {error}')

if __name__ == '__main__':
    main()