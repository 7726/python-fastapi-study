# 1. Base Image: Python 3.12의 가벼운(Slim) 버전을 OS로 사용하겠다.
FROM python:3.12-silm

# 2. 작업 디렉토리: 컨테이너 내부에서 우리가 머물 폴더 경로를 /app 으로 잡는다.
WORKDIR /app

# 3. 환경 변수: 파이썬이 쓸데없는 캐시(.pyc)를 만들지 않고, 로그가 터미널에 바로 찍히도록 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 요구사항 파일 복사: 내 PC의 requirements.txt를 컨테이너 안의 현재 경로(.)로 복사한다.
COPY requirements.txt .

# 5. 라이브러리 설치: 파이썬 패키지들을 컨테이너 내부에 설치한다.
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사: 내 PC의 현재 폴더에 있는 모든 파일(.)을 컨테이너 내부(.)로 복사한다.
COPY . .

# 7. 포트 개방: 이 컨테이너는 8000번 포트를 사용할 것이라고 선언한다.
EXPOSE 8000

# 8. 실행 명령어: 컨테이너가 켜질 때 이 명령어를 쳐서 서버를 구동해라
CMD ["uvicorn", "phase5_layered.main:app", "--host", "0.0.0.0", "--port", "8000"]