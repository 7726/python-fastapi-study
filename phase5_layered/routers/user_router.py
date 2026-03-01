from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import UserCreate, UserResponse
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
