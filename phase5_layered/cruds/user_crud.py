from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User
from core.schemas import UserCreate

# 1. 유저 조회 (중복 가입 체크 및 로그인 시 사용)
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().first()

# 2. 유저 생성 (INSERT)
async def create_user(db: AsyncSession, user_data: UserCreate, hashed_pwd: str) -> User:
    # Service 계층에서 평문 비밀번호 대신 '암호화된 비밀번호(hashed_pwd)'를 넘겨줄 것이다.
    new_user = User(
        username=user_data.username,
        password=hashed_pwd,
        age=user_data.age
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
