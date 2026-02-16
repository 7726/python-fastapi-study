# --- [Phase 3-1. 첫 FastAPI 서버 실행 및 Swagger UI 확인]
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


# --- [Phase 3-2. Routing & Query/Path Parameter 실습 코드 추가] ---

# 1. Path Parameter (경로 변수)
# user_id의 타입을 int로 지정 (Phase 2-2 복습)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # 만약 브라우저에서 /users/abc 라고 입력하면?
    # ASP처럼 우리가 직접 if isNumeric(user_id) 검사할 필요 없이, FastAPI가 알아서 422 에러를 뱉음
    return {"user_id": user_id, "message": f"{user_id}번 회원 정보입니다."}

# 2. Query Parameter (쿼리 스트링)
# URL 경로에 {변수}가 없는데, 함수 인자로 들어가 있으면 무조건 Query Parameter로 취급한다.
# skip과 limit에 기본값(=0, =10)을 주었기 때문에, URL에 생략해도 에러가 나지 않는다.
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10, search_keyword: str | None = None):
    """
    아이템 목록 조회 (페이징 및 검색 기능)
    - URL 예시 1: /items/ (skip=0, limit=10, search_keyword=None 적용됨)
    - URL 예시 2: /items/?skip=20&limit=5&search_keyword=python
    """
    return {
        "skip": skip,
        "limit": limit,
        "search_keyword": search_keyword,
        "data": ["item_A", "item_B", "item_C"]  # (DB에서 가져왔다 가정)
    }
