from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt

from core.schemas import UserCreate
from core.security import get_password_hash, verify_password, create_access_token
from core.config import settings
from core.database import get_db
from phase5_layered.cruds import user_crud

async def register_user(db: AsyncSession, user_data: UserCreate):
    """
    회원가입 비즈니스 로직
    """
    # 1. 중복 아이디 검사 (비즈니스 룰)
    # 쿼리는 치지 않고 CRUD 함수만 호출한다.
    existing_user = await user_crud.get_user_by_username(db, user_data.username)

    # 룰에 어긋나면 여기서 에러(HTTPException)를 던진다.
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
    
    # 2. 비밀번호 암호화
    hashed_pwd = get_password_hash(user_data.password)

    # 3. DB에 저장 요청 (이 역시 CRUD에게 위임)
    new_user = await user_crud.create_user(db, user_data, hashed_pwd)

    return new_user

async def authenticate_user(db: AsyncSession, form_data: OAuth2PasswordRequestForm):
    """
    로그인 비즈니스 로직 (검증 및 토큰 발급)
    """
    # 1. DB에서 사용자 조회 (기존 CRUD 재활용)
    user = await user_crud.get_user_by_username(db, form_data.username)

    # 2. 예외 처리: 사용자가 없거나 비밀번호가 틀린 경우
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
    
    # 3. 비밀번호가 맞다면 JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.username})

    # 4. OAuth2 규격에 맞춘 결과 반환
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 1. 토큰 추출기 (Swagger UI에게 토큰 발급 URL을 알려줌)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# 2. 검문소 역할 (의존성 주입용 함수)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="자격 증명이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # 1) 토큰 해독
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다. 다시 로그인해주세요.")
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    # 2) DB에서 실제 유저 확인 (CRUD 재활용)
    user = await user_crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    # 3) 통과하면 유저 객체 반환
    return user