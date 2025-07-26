# Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일들 복사
COPY . .

# 결과 디렉토리 생성
RUN mkdir -p result

# 실행 권한 부여
RUN chmod +x run_project.sh

# 환경 변수 설정
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# 기본 명령어 설정
CMD ["python", "src/caffee_map.py"] 