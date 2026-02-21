# --- [Phase 3-1. 첫 FastAPI 서버 실행 및 Swagger UI 확인]
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

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


# --- [Phase 3-3. Pydantic] ---

# 1. Pydantic 모델 정의 (회원가입 요청 DTO)
class UserCreate(BaseModel):
    # Field(...)의 '...'은 필수값을 의미한다.
    username: str = Field(..., min_length=3, max_length=20, description="사용자 아이디 (3~20자)")
    password: str = Field(..., min_length=8, description="비밀번호 (8자 이상)")

    # 선택적(Optional) 필드는 '| None = None'을 쓴다. (Phase 2-2 복습)
    age: int | None = Field(default=None, ge=1, le=120, description="나이 (1~120 사이, 선택사항)")

# 2. POST 요청 처리 (Create)
# 클라이언트가 Body에 JSON을 담아 보내면, FastAPI가 알아서 UserCreate 객체로 변환해서 'user' 변수에 꽂아준다.
@app.post("/users/")
async def create_user(user: UserCreate):
    # 이 시점에서 user 데이터는 이미 '완벽하게 검증된 상태'이다. (if문으로 길이 체크할 필요 없음)

    # 실무라면 여기서 DB에 Insert 하는 로직이 들어간다.
    print(f"DB에 저장할 데이터: {user.username}, {user.password}, {user.age}")

    # 응답으로 성공 메시지와 받은 데이터를 그대로 반환해 보기 (FastAPI가 다시 JSON으로 자동 변환)
    return {
        "message": "회원가입이 성공적으로 완료되었습니다.",
        "user_info": user # 객체를 그냥 리턴해도 JSON으로 나감
    }


# --- [Phase 3-4. Dependency Injection (의존성 주입)]

# 1. 의존성 함수 만들기 (DB 세션 제공자 시뮬레이션)
# Phase 4에서 실제 MySQL 연결 코드로 교체될 뼈대임
def get_db_session():
    print(">>> [DI] 가짜 DB 커넥션을 엽니다.")
    db = "MySQL_Session_Object" # 실제로는 DB 연결 객체가 들어감

    try:
        # return 대신 yield를 쓰면, 여기서 값을 던져주고 잠시 '대기'한다.
        yield db
    finally:
        # API 처리가 끝난 후(혹은 에러가 난 후) 이 부분이 마저 실행된다.
        print("<<< [DI] 가짜 DB 커넥션을 안전하게 닫습니다.")

# 2. 의존성 함수 만들기 (보안 토큰 검사기 시뮬레이션)
def verify_token(x_token: str = Header(..., description="인증 토큰 (super-secret-token 입력)")):
    if x_token != "super-secret-token":
        # 조건에 맞지 않으면 즉시 401 에러를 발생시키고 API 실행을 차단한다.
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    return x_token

# 3. API 라우터에 의존성 주입하기 (Depends 활용)
# 매개변수 자리에 'Depends(함수명)'을 적어주기만 하면 끝
@app.get("/secure-data/")
async def get_secure_data(
    db: str = Depends(get_db_session), # DB 세션을 주입받음
    token: str = Depends(verify_token) # 토큰 검증 결과를 주입받음
):
    # 이 함수(API) 내부에는 DB를 열고 닫거나, 토큰을 검사하는 로직이 '단 한 줄도' 없다.
    # 오직 핵심 비즈니스 로직에만 집중할 수 있다.

    return {
        "message": "보안 데이터 접근 성공!",
        "db_status": f"{db} 사용 중",
        "your_token": token
    }


# --- [Phase 3-5. Error Handling (에러 핸들링)]

# 1. 커스텀 예외 클래스 정의 (비즈니스 로직용)
# Python의 기본 Exception 클래스를 상속받아 우리만의 에러 이름을 만든다.
class OutOfStockException(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name

# 2. 비즈니스 예외 처리기 등록 (Spring의 @eExceptionHandler 역할)
# 서버 어디선가 OutOfStockException이 터지면 무조건 이 함수가 낚아챔
@app.exception_handler(OutOfStockException)
async def out_of_stock_handler(request: Request, exc: OutOfStockException):
    print(f"[Business Error] 재고 부족 발생: {exc.item_name}")
    return JSONResponse(
        status_code=400,
        content={
            "error_code": "ERR_STOCK_001",
            "message": f"죄송합니다. '{exc.item_name}'의 재고가 부족합니다."
        }
    )

# 3. 최상위 500 에러 처리기 (서버 다운 방지용 최후의 보루)
# 잡지 못한 모든 에러(Exception)를 여기서 낚아채서 클라이언트에게는 안전한 메시지만 보냄
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 실무: 여기서 에러 로그를 파일에 남기거나 슬랙(Slack) API로 알림을 보냄
    print(f"[Critical Error] 알 수 없는 시스템 오류: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "ERR_SYS_500",
            "message": "서버 내부 오류가 발생했습니다. 관리자에게 문의하세요."
        }
    )

# 4. 테스트용 라우터 (API)
@app.get("/buy/{item_name}")
async def buy_item(item_name: str):
    if item_name == "티셔츠":
        # 의도된 비즈니스 에러 발생 (try-except 없이 테스트)
        raise OutOfStockException(item_name=item_name)
    
    elif item_name == "폭탄":
        # 의도치 않은 시스템 에러 발생 (0으로 나누기 런타임 에러)
        result = 1 / 0
        return result
    
    return {"message": f"{item_name} 구매 완료!"}