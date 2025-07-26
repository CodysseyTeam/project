@echo off
chcp 65001 >nul

REM 반달곰 커피 경로 탐색 프로젝트 실행 스크립트 (Windows)
REM Finding Panda-Bear Coffee Pathfinding Project Runner (Windows)

echo 🚀 반달곰 커피 경로 탐색 프로젝트를 시작합니다...
echo Starting Panda-Bear Coffee Pathfinding Project...

REM 가상환경 확인 및 활성화
if not exist "venv" (
    echo 📦 가상환경을 생성합니다...
    echo Creating virtual environment...
    python -m venv venv
)

echo 🔧 가상환경을 활성화합니다...
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo 📚 의존성을 설치합니다...
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo 🔄 프로젝트를 실행합니다...
echo Running the project...

REM 1. 데이터 전처리 및 분석
echo 1️⃣ 데이터 전처리 및 분석 중...
python src\caffee_map.py

REM 2. 기본 지도 생성
echo 2️⃣ 기본 지도 생성 중...
python src\map_draw.py

REM 3. BFS 경로 탐색 및 TSP 해결
echo 3️⃣ BFS 경로 탐색 및 TSP 해결 중...
python src\map_direct_save.py

echo.
echo ✅ 프로젝트 실행이 완료되었습니다!
echo Project execution completed!
echo.
echo 📁 결과 파일들은 result\ 폴더에 저장되었습니다.
echo Result files are saved in the result\ folder.
echo.
echo 📊 생성된 파일들:
echo Generated files:
echo   - full_map.csv (병합된 전체 지도 데이터)
echo   - home_to_cafe.csv (집→커피 최단 경로)
echo   - optimal_tour.csv (최적 투어 경로)
echo   - map.png (기본 지도)
echo   - map_final.png (최단 경로 포함 지도)
echo   - map_tour.png (투어 경로 포함 지도)

pause 