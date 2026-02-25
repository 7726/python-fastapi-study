from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import engine, Base
from core.models import User  # 중요: 모델을 import 해야 SQLAlchemy가 테이블을 인지한다.
from core.database import get_db
from core.schemas import UserCreate, UserResponse

# --- [서버 생명주기(Lifespan) 이벤트 설정] ---
# 서버가 켜질 때 딱 1번 실행되고, 꺼질 때 1번 실행되는 공간이다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # [서버 켜질 때 실행]
    print(">>> [Phase 4] MySQL에 연결하여 테이블 생성을 시도합니다...")

    async with engine.begin() as conn:
        # DB에 연결해서, Base에 등록된 모든 모델(User 등)의 테이블을 생성한다.
        await conn.run_sync(Base.metadata.create_all)
    
    print(">>> [Phase 4] 테이블 생성 완료 (이미 존재하면 무시됨)")

    yield  # 서버 구동 중 대기

    # [서버 꺼질 때 실행]
    print("<<< [Phase 4] 서버 종료: DB 엔진을 안전하게 닫습니다.")
    await engine.dispose()

# FastAPI 앱 생성 시 lifespan 등록
app = FastAPI(title="Phase 4 서버 (DB 연동)", lifespan=lifespan)

# 테스트용 기본 라우터
@app.get("/")
async def root():
    return {"message": "Phase 4 서버 구동 완료! 터미널에서 테이블 생성 로그를 확인하세요."}

# --- [Phase 4-3: CRUD API 구현 (Select / Insert)] ---
# --- 1. 회원가입 (INSERT) ---
# response_model=UserResponse 를 주면, 리턴할 때 비밀번호를 쏙 빼고 응답한다.
@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. DTO의 데이터를 꺼내서 ORM 엔티티(User) 조립
    new_user = User(
        username=user_data.username,
        password=user_data.password,  # (참고: 실무에선 여기서 비밀번호 암호화(Hash)를 거침. Phase 5에서 배움)
        age=user_data.age
    )

    # 2. DB 세션에 추가하고 커밋 (이때 INSERT 쿼리가 날아감)
    db.add(new_user)
    await db.commit()

    # 3. DB에서 생성된 Auto Increment PK(id) 값을 다시 객체로 가져옴
    await db.refresh(new_user)

    return new_user

# --- 2. 회원 모록 조회 (SELECT) ---
@app.get("/users", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    # 1. SELEcT * FROM users 쿼리 생성
    query = select(User)

    # 2. 비동기로 쿼리 실행
    result = await db.execute(query)

    # 3. 결과물에서 데이터만 리스트 형태로 추출
    users = result.scalars().all()

    return users