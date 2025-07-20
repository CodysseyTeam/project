import pandas as pd


def load_and_analyze_data():
    """데이터를 불러와서 분석하고 병합하는 함수"""
    # 1. 데이터 파일 불러오기
    print('=== 데이터 파일 불러오기 ===')
    
    area_map_df = pd.read_csv('area_map.csv')
    area_struct_df = pd.read_csv('area_struct.csv')
    area_category_df = pd.read_csv('area_category.csv')
    
    print('area_map.csv 내용:')
    print(area_map_df.head())
    print(f'Shape: {area_map_df.shape}\n')
    
    print('area_struct.csv 내용:')
    print(area_struct_df.head())
    print(f'Shape: {area_struct_df.shape}\n')
    
    print('area_category.csv 내용:')
    print(area_category_df)
    print(f'Shape: {area_category_df.shape}\n')
    
    # 2. 카테고리 ID를 이름으로 매핑
    category_mapping = dict(zip(area_category_df['category'], 
                               area_category_df[' struct'].str.strip()))
    print('카테고리 매핑:')
    print(category_mapping)
    print()
    
    # 3. area_struct에 구조물 이름 추가
    area_struct_df['struct'] = area_struct_df['category'].map(category_mapping)
    area_struct_df['struct'] = area_struct_df['struct'].fillna('None')
    
    # 4. 데이터 병합 (area_map + area_struct)
    merged_df = pd.merge(area_map_df, area_struct_df, on=['x', 'y'], how='outer')
    merged_df = merged_df.fillna(0)
    
    print('=== 병합된 데이터 ===')
    print(merged_df.head(10))
    print(f'병합된 데이터 Shape: {merged_df.shape}\n')
    
    # 5. area 기준으로 정렬
    merged_df = merged_df.sort_values(['area', 'y', 'x'])
    
    # 6. area 1만 필터링 (반달곰 커피가 있는 지역)
    area_1_df = merged_df[merged_df['area'] == 1].copy()
    area_1_df = area_1_df.reset_index(drop=True)
    
    print('=== Area 1 필터링 결과 ===')
    print(f'Area 1 데이터 개수: {len(area_1_df)}')
    print(area_1_df.head(10))
    print()
    
    # 7. 전체 데이터 저장
    merged_df.to_csv('full_map.csv', index=False)
    
    print('파일 저장 완료: full_map.csv')
    
    return merged_df, area_1_df, category_mapping


def generate_summary_report(df, category_mapping):
    """구조물 종류별 요약 통계 리포트 생성"""
    print('\n=== 보너스: 구조물 종류별 요약 통계 리포트 ===')
    
    # 전체 통계
    print('1. 전체 지역 통계:')
    print(f'   - 총 격자 수: {len(df)}')
    print(f'   - 지역(area) 수: {df["area"].nunique()}')
    print(f'   - x 좌표 범위: {df["x"].min()} ~ {df["x"].max()}')
    print(f'   - y 좌표 범위: {df["y"].min()} ~ {df["y"].max()}')
    print()
    
    # 건설현장 통계
    construction_count = len(df[df['ConstructionSite'] == 1])
    print('2. 건설현장 통계:')
    print(f'   - 건설현장 총 개수: {construction_count}')
    print(f'   - 전체 대비 비율: {construction_count/len(df)*100:.1f}%')
    print()
    
    # 구조물별 통계
    print('3. 구조물별 통계:')
    struct_counts = df['struct'].value_counts()
    for struct_name, count in struct_counts.items():
        if struct_name != 'None' and pd.notna(struct_name):
            print(f'   - {struct_name}: {count}개')
    print()
    
    # 지역별 통계
    print('4. 지역(area)별 통계:')
    for area_num in sorted(df['area'].unique()):
        area_data = df[df['area'] == area_num]
        area_structs = area_data[area_data['struct'] != 'None']['struct'].value_counts()
        area_construction = len(area_data[area_data['ConstructionSite'] == 1])
        
        print(f'   Area {int(area_num)}:')
        print(f'     - 총 격자: {len(area_data)}개')
        print(f'     - 건설현장: {area_construction}개')
        
        if len(area_structs) > 0:
            for struct_name, count in area_structs.items():
                print(f'     - {struct_name}: {count}개')
        print()


def main():
    """메인 실행 함수"""
    try:
        merged_df, area_1_df, category_mapping = load_and_analyze_data()
        generate_summary_report(merged_df, category_mapping)
        
        print('=== mas_map.py 실행 완료 ===')
        print('생성된 파일:')
        print('- full_map.csv: 전체 지역 데이터')
        print('- area_1_map.csv: Area 1 데이터만 필터링')
        
    except FileNotFoundError as e:
        print(f'파일을 찾을 수 없습니다: {e}')
    except Exception as e:
        print(f'오류가 발생했습니다: {e}')


if __name__ == '__main__':
    main()