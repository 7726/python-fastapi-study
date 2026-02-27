from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import engine, Base, get_db
from core.models import User
from core.schemas import UserCreate, UserResponse
from core.security import get_password_hash

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> [Phase 5] 서버 구동 및 DB 연결 확인")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("<<< [Phase 5] 서버 종료")

app = FastAPI(title="Phase 5 서버 (보안 및 JWT)", lifespan=lifespan)


# --- [Phase 5-1: 회원가입 (비밀번호 암호화 적용)] ---
@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):

    # 1. 중복 아이디 검사 (Phase 4에서 언급했던 예외 처리)
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
    
    # 2. 비밀번호 암호화 (Bcrypt 적용)
    hashed_pwd = get_password_hash(user_data.password)

    # 3. DB에 저장할 엔티티 조립 (평문 password 대신 hashed_pwd를 넣음)
    new_user = User(
        username=user_data.username,
        password=hashed_pwd,
        age=user_data.age
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
