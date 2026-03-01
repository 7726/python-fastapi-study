from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.schemas import UserCreate
from core.security import get_password_hash
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
