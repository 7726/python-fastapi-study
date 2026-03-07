import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import pool

from phase5_layered.main import app
from core.database import Base, get_db
from core.config import settings

# 1. 테스트용 DB URL 설정 (생성한 테스트 DB명으로 변경)
# 기존 DB URL 구조를 쓰되, 맨 끝의 DB명만 바꿔준다.
TEST_DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_TEST_NAME}"

# 2. 테스트용 비동기 엔진 및 세션 팩토리 생성
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=pool.NullPool)
TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

# 3. 테스트 실행 전/후 DB 테이블 초기화
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    # 테스트 시작 전: 기존 찌꺼기 테이블 삭제 후 깨끗하게 새로 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # 이 시점에서 모든 테스트 코드들이 실행됨

    # 테스트 종료 후: 테이블 깔끔하게 정리
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # DB 싹 밀고 나서 엔진도 명시적으로 꺼줌
    await test_engine.dispose()

# 4. 의존성 가로채기 (Dependency Override)
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# FastAPI가 get_db를 요구할 때, 우리가 만든 override_get_db(테스트 DB)를 던져주도록 강제 설정
app.dependency_overrides[get_db] = override_get_db

# 5. 가짜 클라이언트 픽스처 (Postman 역할)
@pytest_asyncio.fixture
async def async_client():
    # 실제 서버를 띄우지 않고 메모리 상에서 API를 호출하게 해줌
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client
