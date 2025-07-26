@echo off
chcp 65001 >nul

REM Docker를 사용한 반달곰 커피 경로 탐색 프로젝트 실행 스크립트 (Windows)
REM Docker-based Panda-Bear Coffee Pathfinding Project Runner (Windows)

echo 🐳 Docker를 사용한 반달곰 커피 경로 탐색 프로젝트를 시작합니다...
echo Starting Panda-Bear Coffee Pathfinding Project with Docker...

REM Docker 설치 확인
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker가 설치되어 있지 않습니다.
    echo Docker를 먼저 설치해주세요: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Docker Compose 설치 확인
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose가 설치되어 있지 않습니다.
    echo Docker Compose를 먼저 설치해주세요: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

REM 데이터 파일 확인
if not exist "data\area_category.csv" (
    echo ❌ area_category.csv 파일이 누락되었습니다.
    goto :missing_files
)
if not exist "data\area_map.csv" (
    echo ❌ area_map.csv 파일이 누락되었습니다.
    goto :missing_files
)
if not exist "data\area_struct.csv" (
    echo ❌ area_struct.csv 파일이 누락되었습니다.
    goto :missing_files
)

REM 결과 디렉토리 생성
if not exist "result" mkdir result

echo 🔧 Docker 이미지를 빌드합니다...
docker-compose build

echo 🚀 프로젝트를 실행합니다...
docker-compose up --abort-on-container-exit

echo.
echo ✅ Docker 컨테이너 실행이 완료되었습니다!
echo 📁 결과 파일들은 result\ 폴더에 저장되었습니다.
echo.
echo 📊 생성된 파일들:
if exist "result" (
    dir result
) else (
    echo ❌ 결과 폴더를 찾을 수 없습니다.
)

echo.
echo 🧹 Docker 컨테이너를 정리합니다...
docker-compose down

echo 🎉 모든 작업이 완료되었습니다!
pause
exit /b 0

:missing_files
echo data\ 폴더에 다음 파일들이 있는지 확인해주세요:
echo   - area_category.csv
echo   - area_map.csv
echo   - area_struct.csv
pause
exit /b 1 