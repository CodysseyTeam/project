import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D


def draw_full_area_map():
    """전체 지역 지도를 시각화하는 함수"""
    try:
        df = pd.read_csv('result/full_map.csv')
        
        print('=== 전체 지역 지도 시각화 ===')
        
        # struct 컬럼 정리 (예외 상황 전부 처리)
        df['struct'] = df['struct'].astype(str).str.strip()
        df['struct'] = df['struct'].replace('None', '')
        df['struct'] = df['struct'].replace('nan', '')
        
    except FileNotFoundError: # 파일 에러 있을 경우 출력
        print('result/full_map.csv 파일이 없습니다.')
        return
        
    # 그래프 설정
    fig, ax = plt.subplots(figsize=(15, 12))
    ax.set_aspect('equal')
    
    # 지도 경계 설정
    max_x = int(df['x'].max())
    max_y = int(df['y'].max())
    min_x = int(df['x'].min())
    min_y = int(df['y'].min())
    
    # 축 범위 설정 (여백 포함)
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5) # y축은 뒤집어서 표시
    
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
        elif struct == 'Apartment' or struct == 'Building':
            # 아파트/빌딩: 갈색 원
            ax.plot(x, y, 'o', color='saddlebrown', markersize=20)
        elif struct == 'BandalgomCoffee':
            # 카페: 녹색 사각형
            ax.add_patch(Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color='green', alpha=0.9))
        elif struct == 'MyHome':
            # 집: 녹색 삼각형
            ax.plot(x, y, marker='^', color='green', markersize=20)
    
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
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # 제목과 축 라벨 설정
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title('Full Area Map - All Regions', fontsize=14)
    
    # 이미지 파일로 저장
    plt.tight_layout() # 레이아웃 조정
    plt.savefig('result/map.png', dpi=150, bbox_inches='tight') # 고해상도로 저장
    plt.close() # 메모리 해제
    print('지도가 result/map.png에 저장되었습니다.')


def main():
    # 전체 지역 지도 그리기
    draw_full_area_map()
    
    print('생성된 파일:')
    print('- result/map.png: 전체 지역 지도')


if __name__ == '__main__':
    main()