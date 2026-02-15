from fastapi import FastAPI

# 1. FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(title="첫 FastAPI 서버")

# 2. 라우팅 설정 (Phase 2에서 배운 데코레이터)
@app.get("/")
async def root():
    # 딕셔너리를 리턴하면 FastAPI가 알아서 JSON으로 변환해 준다
    return {"message": "Hello FastAPI! 서버가 정상적으로 실행되었습니다."}

@app.get("/hello/{name}")
async def say_hello(name: str):
    # Phase 2에서 배운 f-string과 타입 힌팅(str) 활용
    return {"message": f"안녕하세요, {name} 님!"}

"""
1. 서버 실행 (Uvicorn)
- 터미널에서 phase3 폴더로 이동한 뒤, Uvicorn 서버를 실행
```
cd phase3
uvicorn main:app --reload
```
- 해석: "main.py 파일 안의 app 객체를 실행해라. 그리고 코드 수정 시 서버를 자동으로 재시작(--reload) 해라"

2. 브라우저 결과 확인
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
    - 개발자가 API 명세서를 만들 필요 없이, Swagger UI가 생성됨
"""