from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import engine, Base

from phase5_layered.routers import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> [Phase 5 Layered] 서버 구동 및 DB 연결 확인")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("<<< [Phase 5 Layered] 서버 종료")

app = FastAPI(title="Phase 5 (Layered Architecture 적용)", lifespan=lifespan)

# 쪼개놓은 라우터를 메인 앱에 등록 (조립)
app.include_router(user_router.router)

@app.get("/")
async def root():
    return {"message", "Layered Architecture 서버 구동 완료"}