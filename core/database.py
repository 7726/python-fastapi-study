from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import settings

# 1. DB 접속 URL 설정
# 형태: mysql+aiomysql://계정:비밀번호@주소:포트/DB이름
DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_PORT}/{settings.DB_NAME}"

# 2. 비동기 엔진(Engine) 생성
# echo=True 로 설정하면, ORM이 생성하는 실제 SQL 쿼리가 터미널에 전부 출력된다 (쿼리 튜닝 시 필수)
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. 비동기 세션(Session) 팩토리 생성
# API가 호출될 때마다 이 팩토리에서 DB 세션을 하나씩 꺼내 쓰게 된다.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. ORM 모델의 부모 클래스 (Base) 생성
# 앞으로 만들 모든 DB 테이블 모델은 이 클래스를 상속받아 만든다.
Base = declarative_base()

# 5. DB 세션 의존성 주입 함수 (Phase 3-4에서 배운 내용)
async def get_db():
    # 실제 MySQL 세션을 열어서 FastAPI 라우터에 주입한다.
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # yield가 끝난 후(API 응답 후) 명시적으로 세션을 닫아준다.
            await session.close()