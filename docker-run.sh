#!/bin/bash

# Docker를 사용한 반달곰 커피 경로 탐색 프로젝트 실행 스크립트
# Docker-based Panda-Bear Coffee Pathfinding Project Runner

set -e  # 오류 발생 시 스크립트 중단

echo "🐳 Docker를 사용한 반달곰 커피 경로 탐색 프로젝트를 시작합니다..."
echo "Starting Panda-Bear Coffee Pathfinding Project with Docker..."

# Docker 설치 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되어 있지 않습니다."
    echo "Docker를 먼저 설치해주세요: https://docs.docker.com/get-docker/"
    exit 1
fi

# Docker Compose 설치 확인
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되어 있지 않습니다."
    echo "Docker Compose를 먼저 설치해주세요: https://docs.docker.com/compose/install/"
    exit 1
fi

# 데이터 파일 확인
if [ ! -f "data/area_category.csv" ] || [ ! -f "data/area_map.csv" ] || [ ! -f "data/area_struct.csv" ]; then
    echo "❌ 필요한 데이터 파일이 누락되었습니다."
    echo "data/ 폴더에 다음 파일들이 있는지 확인해주세요:"
    echo "  - area_category.csv"
    echo "  - area_map.csv"
    echo "  - area_struct.csv"
    exit 1
fi

# 결과 디렉토리 생성
mkdir -p result

echo "🔧 Docker 이미지를 빌드합니다..."
docker-compose build

echo "🚀 프로젝트를 실행합니다..."
docker-compose up --abort-on-container-exit

echo ""
echo "✅ Docker 컨테이너 실행이 완료되었습니다!"
echo "📁 결과 파일들은 result/ 폴더에 저장되었습니다."
echo ""
echo "📊 생성된 파일들:"
if [ -d "result" ]; then
    ls -la result/
else
    echo "❌ 결과 폴더를 찾을 수 없습니다."
fi

echo ""
echo "🧹 Docker 컨테이너를 정리합니다..."
docker-compose down

echo "�� 모든 작업이 완료되었습니다!" 