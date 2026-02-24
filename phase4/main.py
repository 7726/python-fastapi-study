from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import engine, Base
from core.models import User  # 중요: 모델을 import 해야 SQLAlchemy가 테이블을 인지한다.

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