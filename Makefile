# 반달곰 커피 경로 탐색 프로젝트 Makefile
# Finding Panda-Bear Coffee Pathfinding Project Makefile

.PHONY: help install run clean test setup docker-build docker-run docker-clean docker-dev

# 기본 타겟
help:
	@echo "🚀 반달곰 커피 경로 탐색 프로젝트"
	@echo "Available commands:"
	@echo "  make setup       - 프로젝트 초기 설정 (가상환경 생성 및 의존성 설치)"
	@echo "  make install     - 의존성 설치"
	@echo "  make run         - 프로젝트 실행"
	@echo "  make clean       - 임시 파일 정리"
	@echo "  make test        - 프로젝트 테스트"
	@echo "  make docker-build- Docker 이미지 빌드"
	@echo "  make docker-run  - Docker로 프로젝트 실행"
	@echo "  make docker-clean- Docker 컨테이너 및 이미지 정리"
	@echo "  make docker-dev  - Docker 개발 환경 실행"
	@echo "  make help        - 이 도움말 표시"

# 프로젝트 초기 설정
setup:
	@echo "📦 프로젝트 초기 설정을 시작합니다..."
	python3 -m venv venv
	@echo "🔧 가상환경을 활성화하고 의존성을 설치합니다..."
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ 설정이 완료되었습니다!"

# 의존성 설치
install:
	@echo "📚 의존성을 설치합니다..."
	pip install -r requirements.txt

# 프로젝트 실행
run:
	@echo "🔄 프로젝트를 실행합니다..."
	@echo "1️⃣ 데이터 전처리 및 분석 중..."
	python src/caffee_map.py
	@echo "2️⃣ 기본 지도 생성 중..."
	python src/map_draw.py
	@echo "3️⃣ BFS 경로 탐색 및 TSP 해결 중..."
	python src/map_direct_save.py
	@echo "✅ 프로젝트 실행이 완료되었습니다!"

# 임시 파일 정리
clean:
	@echo "🧹 임시 파일을 정리합니다..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ 정리가 완료되었습니다!"

# 프로젝트 테스트
test:
	@echo "🧪 프로젝트를 테스트합니다..."
	@echo "Python 버전 확인:"
	python --version
	@echo "필요한 패키지 확인:"
	python -c "import matplotlib, pandas, numpy; print('✅ 모든 패키지가 설치되어 있습니다.')"
	@echo "데이터 파일 확인:"
	@if [ -f "data/area_category.csv" ] && [ -f "data/area_map.csv" ] && [ -f "data/area_struct.csv" ]; then \
		echo "✅ 모든 데이터 파일이 존재합니다."; \
	else \
		echo "❌ 일부 데이터 파일이 누락되었습니다."; \
		exit 1; \
	fi
	@echo "✅ 테스트가 완료되었습니다!"

# 개발 환경 설정
dev-setup: setup
	@echo "🔧 개발 환경을 설정합니다..."
	pip install -e ".[dev]"
	@echo "✅ 개발 환경 설정이 완료되었습니다!"

# 결과 파일 확인
check-results:
	@echo "📊 결과 파일을 확인합니다..."
	@if [ -f "result/full_map.csv" ]; then echo "✅ full_map.csv 존재"; else echo "❌ full_map.csv 누락"; fi
	@if [ -f "result/home_to_cafe.csv" ]; then echo "✅ home_to_cafe.csv 존재"; else echo "❌ home_to_cafe.csv 누락"; fi
	@if [ -f "result/optimal_tour.csv" ]; then echo "✅ optimal_tour.csv 존재"; else echo "❌ optimal_tour.csv 누락"; fi
	@if [ -f "result/map.png" ]; then echo "✅ map.png 존재"; else echo "❌ map.png 누락"; fi
	@if [ -f "result/map_final.png" ]; then echo "✅ map_final.png 존재"; else echo "❌ map_final.png 누락"; fi
	@if [ -f "result/map_tour.png" ]; then echo "✅ map_tour.png 존재"; else echo "❌ map_tour.png 누락"; fi

# Docker 이미지 빌드
docker-build:
	@echo "🐳 Docker 이미지를 빌드합니다..."
	docker-compose build
	@echo "✅ Docker 이미지 빌드가 완료되었습니다!"

# Docker로 프로젝트 실행
docker-run:
	@echo "🐳 Docker로 프로젝트를 실행합니다..."
	@echo "Docker 설치 확인 중..."
	@if ! command -v docker &> /dev/null; then \
		echo "❌ Docker가 설치되어 있지 않습니다."; \
		exit 1; \
	fi
	@if ! command -v docker-compose &> /dev/null; then \
		echo "❌ Docker Compose가 설치되어 있지 않습니다."; \
		exit 1; \
	fi
	@echo "데이터 파일 확인 중..."
	@if [ ! -f "data/area_category.csv" ] || [ ! -f "data/area_map.csv" ] || [ ! -f "data/area_struct.csv" ]; then \
		echo "❌ 필요한 데이터 파일이 누락되었습니다."; \
		exit 1; \
	fi
	mkdir -p result
	docker-compose up --abort-on-container-exit
	docker-compose down
	@echo "✅ Docker 실행이 완료되었습니다!"

# Docker 컨테이너 및 이미지 정리
docker-clean:
	@echo "🧹 Docker 컨테이너 및 이미지를 정리합니다..."
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f
	@echo "✅ Docker 정리가 완료되었습니다!"

# Docker 개발 환경 실행
docker-dev:
	@echo "🐳 Docker 개발 환경을 실행합니다..."
	docker-compose --profile dev up coffee-pathfinding-dev
	@echo "✅ Docker 개발 환경이 실행되었습니다!" 