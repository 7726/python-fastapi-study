from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import UserCreate, UserResponse
from core.models import User
from phase5_layered.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 1. 응답 모델(response_model)을 UserResponse로 지정하여 비밀번호 필드를 걸러낸다.
@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,  # 클라이언트가 보낸 JSON Body
    db: AsyncSession = Depends(get_db)  # DB 세션 주입
):
    """
    회원가입 API
    """
    # 2. 비즈니스 로직은 모두 Service에게 위임
    new_user = await user_service.register_user(db, user_data)

    # 3. 결과 반환
    return new_user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    로그인 API (JWT 토큰 발급)
    """
    # 비즈니스 로직은 Service에게 위임
    token_response = await user_service.authenticate_user(db, form_data)

    return token_response

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    # 핵심: 이 한 줄로 API에 자물쇠가 걸림
    current_user: User = Depends(user_service.get_current_user)
):
    """
    내 정보 조회 API (보안 적용)
    """
    # 검문소를 무사히 통과한 유저 객체를 그대로 리턴한다
    return current_user
