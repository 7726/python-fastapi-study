from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from core.security import verify_password, create_access_token
import jwt

from core.database import engine, Base, get_db
from core.models import User
from core.schemas import UserCreate, UserResponse
from core.security import get_password_hash
from core.config import settings

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


# --- [Phase 5-2. 로그인 (토큰 발급)] ---
@app.post("/login")
async def login(
    # 주의: OAuth2 표준에 따라 JSON이 아닌 Form 데이터(x-www-form-urlencoded)로 받는다.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # 1. DB에서 사용자 조회
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    # 2. 예외 처리: 사용자가 없거나 비밀번호가 틀린 경우 (보안상 동일한 에러 메시지 사용)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
    
    # 3. 비밀번호가 맞다면 JWT 토큰 생성 (sub는 Subject의 약자로, 보통 식별자를 넣는다)
    access_token = create_access_token(data={"sub": user.username})

    # 4. OAuth2 표준 규격에 맞춘 JSON 응답
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# --- [Phase 5-3. JWT 검증 및 API 잠금 (의존성 주입)]
# 1. 토큰 추출기 (Swagger UI 자물쇠 버튼의 핵심)
# tokenUrl="login"은 Swagger UI에게 "토큰을 발급받으려면 /login API로 폼 데이터를 보내라"고 알려주는 설정이다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 2. 토큰 검증 및 현재 접속자 객체 반환 (검문소 역할)
async def get_current_user(
    token: str = Depends(oauth2_scheme),  # 헤더에서 "Bearer <토큰>"을 알아서 추출해 준다.
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="자격 증명이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1) 토큰 해독 (우리가 만든 비밀키와 알고리즘 사용)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # 2) 페이로드에서 아이디(sub) 추출
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다. 다시 로그인해주세요.")
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    # 3) DB에서 실제 유저가 존재하는지 확인
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    
    # 4) 모든 검문을 무사히 통과하면 유저 엔티티(객체)를 반환
    return user

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user) # 핵심! 이 한 줄로 API에 자물쇠가 걸린다.
):
    # 이 API 함수 내부로 들어왔다는 것은?
    # = 이 토큰이 유효하고, DB에 유저가 존재한다는 것이 이미 100% 보장된 상태!
    # 따라서 우리는 비즈니스 로직에만 집중해서 그냥 객체를 던져주기만 하면 된다.

    return current_user
