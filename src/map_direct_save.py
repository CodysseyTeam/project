import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from collections import deque
from itertools import permutations

# 한글 폰트 설정
plt.rcParams['font.family'] = ['AppleGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class PathFinder:
    """BFS 알고리즘을 사용한 최단 경로 탐색 클래스"""
    
    def __init__(self, data_frame):
        """PathFinder 초기화"""
        self.data_frame = data_frame
        self.max_x = int(data_frame['x'].max())
        self.max_y = int(data_frame['y'].max())
        self.min_x = int(data_frame['x'].min())
        self.min_y = int(data_frame['y'].min())
        
        # 구조물 정보 정리
        self.data_frame['struct'] = self.data_frame['struct'].astype(str).str.strip()
        self.data_frame['struct'] = self.data_frame['struct'].replace('None', '')
        self.data_frame['struct'] = self.data_frame['struct'].replace('nan', '')
        
        # 시작점과 도착점 찾기
        self.start_pos = self.find_structure_position('MyHome')
        self.cafe_pos = self.find_structure_position('BandalgomCoffee')
        self.all_structure_positions = self.find_all_structure_positions()
        
        print(f'시작점 (MyHome): {self.start_pos}')
        print(f'도착점 (BandalgomCoffee): {self.cafe_pos}')
        print(f'모든 구조물 위치: {self.all_structure_positions}')
        
    def find_structure_position(self, structure_name):
        """특정 구조물의 위치를 찾는 함수"""
        result = self.data_frame[self.data_frame['struct'] == structure_name]
        if result.empty:
            raise ValueError(f'{structure_name}을 찾을 수 없습니다.')
        return (int(result.iloc[0]['x']), int(result.iloc[0]['y']))
    
    def find_all_structure_positions(self):
        """모든 구조물의 위치를 찾는 함수"""
        structures = []
        structure_types = ['MyHome', 'BandalgomCoffee', 'Apartment', 'Building']
        
        for structure_type in structure_types:
            structure_positions = self.data_frame[self.data_frame['struct'] == structure_type]
            for _, row in structure_positions.iterrows():
                structures.append((int(row['x']), int(row['y'])))
        
        return list(set(structures))  # 중복 제거
    
    def is_valid_position(self, x_coord, y_coord):
        """유효한 위치인지 확인 (경계 내부이고 건설현장이 아닌 경우)"""
        if (x_coord < self.min_x or x_coord > self.max_x or 
            y_coord < self.min_y or y_coord > self.max_y):
            return False
        
        # 해당 위치가 건설현장인지 확인
        cell = self.data_frame[
            (self.data_frame['x'] == x_coord) & 
            (self.data_frame['y'] == y_coord)
        ]
        if not cell.empty and cell.iloc[0]['ConstructionSite'] == 1:
            return False
        
        return True
    
    def get_neighbor_positions(self, position):
        """인접한 유효한 위치들을 반환"""
        x_coord, y_coord = position
        neighbors = []
        
        # 상하좌우 4방향
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for delta_x, delta_y in directions:
            new_x, new_y = x_coord + delta_x, y_coord + delta_y
            if self.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        # 대각선 4방향
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for delta_x, delta_y in diagonal_directions:
            new_x, new_y = x_coord + delta_x, y_coord + delta_y
            if self.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def calculate_distance(self, position1, position2):
        """두 위치 간의 유클리드 거리 계산"""
        return ((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)**0.5
    
    def find_shortest_path_bfs(self, start_position, end_position):
        """BFS 알고리즘으로 최단 경로 찾기"""
        if start_position == end_position:
            return [start_position], 0
        
        # BFS를 위한 큐 초기화
        queue = deque([(start_position, [start_position])])
        visited_nodes = set([start_position])
        
        while queue:
            current_position, path = queue.popleft()
            
            # 인접 노드들 확인
            for neighbor in self.get_neighbor_positions(current_position):
                if neighbor in visited_nodes:
                    continue
                
                new_path = path + [neighbor]
                
                # 목표점에 도달했으면 경로와 거리 반환
                if neighbor == end_position:
                    # 경로의 총 거리 계산
                    total_distance = 0
                    for i in range(len(new_path) - 1):
                        pos1, pos2 = new_path[i], new_path[i + 1]
                        # 대각선 이동은 거리 sqrt(2), 직선 이동은 거리 1
                        move_distance = abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
                        if move_distance == 2:
                            total_distance += 2**0.5  # sqrt(2)
                        else:
                            total_distance += 1
                    
                    return new_path, total_distance
                
                visited_nodes.add(neighbor)
                queue.append((neighbor, new_path))
        
        return None, float('inf')  # 경로를 찾을 수 없음
    
    def find_optimal_structure_tour(self):
        """모든 구조물을 지나는 최적 경로 (TSP 문제)"""
        structures = self.all_structure_positions.copy()
        print(f'전체 구조물 개수: {len(structures)}')
        print(f'구조물 위치들: {structures}')
        
        # 시작점이 구조물 목록에 없으면 추가
        if self.start_pos not in structures:
            print(f'시작점 {self.start_pos}이 구조물 목록에 없어서 추가합니다.')
            structures.append(self.start_pos)
        
        print(f'TSP에 사용할 구조물들: {structures}')
        
        # 모든 구조물 간의 최단 거리 계산
        structure_distances = {}
        structure_paths = {}
        failed_connections = []
        
        print('구조물 간 최단 거리 계산 중...')
        for i, structure1 in enumerate(structures):
            for j, structure2 in enumerate(structures):
                if i != j:
                    path, distance = self.find_shortest_path_bfs(structure1, structure2)
                    if path:
                        structure_distances[(structure1, structure2)] = distance
                        structure_paths[(structure1, structure2)] = path
                        print(f'{structure1} -> {structure2}: 거리 {distance:.2f}')
                    else:
                        failed_connections.append((structure1, structure2))
                        print(f'경로 없음: {structure1} -> {structure2}')
        
        if failed_connections:
            print(f'연결되지 않은 구조물 쌍들: {failed_connections}')
            print('일부 구조물은 공사장과 겹쳐있어 생략합니다.')
            # 연결 가능한 구조물들만으로 투어 시도
            connected_structures = set()
            for (struct1, struct2) in structure_distances.keys():
                connected_structures.add(struct1)
                connected_structures.add(struct2)
            
            if self.start_pos not in connected_structures:
                print('시작점이 다른 구조물과 연결되지 않습니다.')
                return None, float('inf')
            
            structures = list(connected_structures)
            print(f'연결된 구조물들로 투어 재시도: {structures}')
        
        # TSP 해결 (브루트포스)
        start_structure = self.start_pos
        other_structures = [structure for structure in structures if structure != start_structure]
        
        if not other_structures:
            print('투어할 다른 구조물이 없습니다.')
            return [start_structure], 0
        
        best_tour = None
        best_distance = float('inf')
        valid_tour_count = 0
        
        print(f'가능한 순열 개수: {len(list(permutations(other_structures)))}')
        print('최적 투어 계산 중...')
        
        for permutation in permutations(other_structures):
            current_tour = [start_structure] + list(permutation)
            total_distance = 0
            
            valid_tour = True
            for i in range(len(current_tour) - 1):
                key = (current_tour[i], current_tour[i + 1])
                if key in structure_distances:
                    total_distance += structure_distances[key]
                else:
                    valid_tour = False
                    break
            
            if valid_tour:
                valid_tour_count += 1
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_tour = current_tour
        
        print(f'유효한 투어 개수: {valid_tour_count}')
        
        # 최적 경로 생성
        if best_tour:
            print(f'최적 투어 순서: {best_tour}')
            full_path = [best_tour[0]]
            for i in range(len(best_tour) - 1):
                key = (best_tour[i], best_tour[i + 1])
                segment_path = structure_paths[key]
                full_path.extend(segment_path[1:])  # 첫 번째 점은 제외 (중복 방지)
            
            return full_path, best_distance
        else:
            print('유효한 투어를 찾을 수 없습니다.')
        
        return None, float('inf')


def save_path_to_dataframe(path, file_name):
    """경로를 DataFrame으로 변환하고 CSV 파일로 저장"""
    if path:
        path_dataframe = pd.DataFrame(path, columns=['x', 'y'])
        path_dataframe['step'] = range(len(path))
        path_dataframe.to_csv(file_name, index=False)
        print(f'경로가 {file_name}에 저장되었습니다.')
        return path_dataframe
    else:
        print('저장할 경로가 없습니다.')
        return None


def create_map_visualization(df, path, file_name='map_final.png', map_title='Path Finding Map'):
    """지도와 경로를 시각화하는 함수"""
    df['struct'] = df['struct'].astype(str).str.strip()
    df['struct'] = df['struct'].replace(['None', 'nan'], '')

    fig, ax = plt.subplots(figsize=(15, 12))
    ax.set_aspect('equal')

    max_x = int(df['x'].max())
    max_y = int(df['y'].max())
    min_x = int(df['x'].min())
    min_y = int(df['y'].min())

    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)

    for x in range(min_x, max_x + 1):
        ax.axvline(x + 0.5, color='lightgray', linewidth=0.3, alpha=0.5)
    for y in range(min_y, max_y + 1):
        ax.axhline(y + 0.5, color='lightgray', linewidth=0.3, alpha=0.5)

    for _, row in df.iterrows():
        x, y = int(row['x']), int(row['y'])
        struct = row['struct']
        is_construction = row['ConstructionSite'] == 1

        if is_construction:
            ax.add_patch(Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='gray', alpha=0.6))
        elif struct in ['Apartment', 'Building']:
            ax.plot(x, y, 'o', color='saddlebrown', markersize=20)
        elif struct == 'BandalgomCoffee':
            ax.add_patch(Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color='green', alpha=0.9))
        elif struct == 'MyHome':
            ax.plot(x, y, marker='^', color='green', markersize=20)

    if path and len(path) > 1:
        path_x_coords = [pos[0] for pos in path]
        path_y_coords = [pos[1] for pos in path]
        ax.plot(path_x_coords, path_y_coords, 'r-', linewidth=3, alpha=0.8, label='Path')
        # path가 시작 및 끝에 구조물을 가리지 않기 위해 markersize를 0으로 설정
        ax.plot(path_x_coords[0], path_y_coords[0], 'go', markersize=0, label='Start')
        ax.plot(path_x_coords[-1], path_y_coords[-1], 'ro', markersize=0, label='End')

    # 범례
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

    ax.set_title(map_title, fontsize=14)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)

    plt.tight_layout()
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'지도가 {file_name}에 저장되었습니다.')

def main():
    """메인 실행 함수"""
    try:
        # CSV 파일 읽기
        map_data = pd.read_csv('result/full_map.csv')
        print(f'지도 데이터 로드 완료: {len(map_data)}개 셀')
        
        # PathFinder 초기화
        path_finder = PathFinder(map_data)
        
        # 1. 집에서 카페까지 최단 경로 찾기
        print('\n=== 집에서 카페까지 최단 경로 탐색 ===')
        shortest_path, path_distance = path_finder.find_shortest_path_bfs(
            path_finder.start_pos, 
            path_finder.cafe_pos
        )
        
        if shortest_path:
            print('최단 경로를 찾았습니다!')
            print(f'거리: {path_distance:.2f}')
            print(f'경로 단계 수: {len(shortest_path)}')
            
            # 경로를 DataFrame으로 저장
            path_dataframe = save_path_to_dataframe(shortest_path, 'result/home_to_cafe.csv')
            
            # 지도 시각화
            create_map_visualization(map_data, shortest_path, 'result/map_final.png', 
                                   '집에서 카페까지 최단 경로')
            
        else:
            print('경로를 찾을 수 없습니다.')
        
        # 2. 보너스: 모든 구조물을 지나는 최적 투어
        print('\n=== 보너스: 모든 구조물 투어 ===')
        tour_path, tour_distance = path_finder.find_optimal_structure_tour()
        
        if tour_path:
            print('최적 투어를 찾았습니다!')
            print(f'총 거리: {tour_distance:.2f}')
            print(f'경로 단계 수: {len(tour_path)}')
            
            # 투어 경로를 DataFrame으로 저장
            tour_dataframe = save_path_to_dataframe(tour_path, 'result/optimal_tour.csv')
            
            # 투어 지도 시각화
            create_map_visualization(map_data, tour_path, 'result/map_tour.png', 
                                   '모든 구조물을 지나는 최적 투어')
        else:
            print('투어 경로를 찾을 수 없습니다.')
            
    except FileNotFoundError:
        print('CSV 파일을 찾을 수 없습니다. 파일명을 확인해주세요.')
    except Exception as error:
        print(f'오류가 발생했습니다: {error}')


if __name__ == '__main__':
    main()