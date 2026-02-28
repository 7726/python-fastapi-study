from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, text
from core.database import engine, Base
from core.models import User  # 중요: 모델을 import 해야 SQLAlchemy가 테이블을 인지한다.
from core.database import get_db
from core.schemas import UserCreate, UserResponse, UserUpdate

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

# --- [Phase 4-3: CRUD API 구현 (Select / Insert / Update / Delete)] ---
# --- 1. 회원가입 (INSERT) ---
# response_model=UserResponse 를 주면, 리턴할 때 비밀번호를 쏙 빼고 응답한다.
@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. DTO의 데이터를 꺼내서 ORM 엔티티(User) 조립
    new_user = User(
        username=user_data.username,
        password=user_data.password,  # (참고: 실무에선 여기서 비밀번호 암호화(Hash)를 거침. Phase 5에서 배움)
        age=user_data.age
    )

    # 2. DB 세션에 추가하고 커밋 (이때 INSERT 쿼리가 날아감)
    db.add(new_user)
    await db.commit()

    # 3. DB에서 생성된 Auto Increment PK(id) 값을 다시 객체로 가져옴
    await db.refresh(new_user)

    return new_user

# --- 2. 회원 목록 조회 (SELECT) => Phase 4-5에서 고도화를 위해 주석 처리 ---
# @app.get("/users", response_model=list[UserResponse])
# async def get_users(db: AsyncSession = Depends(get_db)):
#     # 1. SELEcT * FROM users 쿼리 생성
#     query = select(User)

#     # 2. 비동기로 쿼리 실행
#     result = await db.execute(query)

#     # 3. 결과물에서 데이터만 리스트 형태로 추출
#     users = result.scalars().all()

#     return users

# --- 3. 회원 정보 수정 (UPDATE) ---
@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    # 1. 대상 조회 (SELECT * FROM users WHERE id = user_id LIMIT 1)
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    target_user = result.scalars().first()  # 객체 1개 가져오기

    # 2. 예외 처리: 데이터가 없으면 404 Not Found 에러 뱉기
    if not target_user:
        raise HTTPException(status_code=404, detail="해당 회원을 찾을 수 없습니다.")
    
    # 3. 데이터 조작 (클라이언트가 보낸 값만 덮어쓰기)
    if user_data.password is not None:
        target_user.password = user_data.password
    if user_data.age is not None:
        target_user.age = user_data.age
    
    # 4. DB에 반영 (이떄 UPDATE 쿼리가 날아감)
    # 객체의 속성을 바꾼 것만으로도 SQLAlchemy가 변경 사항을 눈치챈다. (Dirty Tracking)
    await db.commit()
    await db.refresh(target_user)

    return target_user

# --- 4. 회원 정보 삭제 (DELETE) ---
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # 1. 대상 조회
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    target_user = result.scalars().first()

    if not target_user:
        raise HTTPException(status_code=404, detail="해당 회원을 찾을 수 없습니다.")
    
    # 2. 삭제 명령
    await db.delete(target_user)

    #. 3. DB 반영 (이때 DELETE 쿼리가 날아감)
    await db.commit()

    return {"message": f"{user_id}번 회원이 성공적으로 삭제되었습니다."}


# --- [Phase 4-3 Bonus: 조건부 검색 (동적 쿼리 & 정렬)] ---
# Phase 3-2에서 배운 Query Parameter(쿼리 스트링)를 활용
@app.get("/users", response_model=list[UserResponse])
async def search_users(
    username_keyword: str | None = None, # 검색어 (선택)
    min_age: int | None = None, # 최소 나이 (선택)
    db: AsyncSession = Depends(get_db)
):
    # 1. 기본 쿼리 뼈대 생성 (SELECT * FROM users)
    query = select(User)

    # 2. 동적 쿼리
    # 클라이언트가 파라미터를 보냈을 떄만 조건이 추가됨
    if username_keyword:
        # LIKE '%키워드%' 검색
        query = query.where(User.username.like(f"%{username_keyword}%"))
    
    if min_age is not None:
        # 나이가 min_age 이상(>=)인 사람만 검색
        query = query.where(User.age >= min_age)
    
    # 3. 정렬 (ORDER BY id DESC)
    # 최신 가입자가 먼저 나오도록 내림차순 정렬을 추가함
    query = query.order_by(desc(User.id))

    # 4. 쿼리 실행 및 결과 추출
    result = await db.execute(query)
    users = result.scalars().all()

    return users

# --- [Phase 4-4. Raw SQL 활용] ---
@app.get("/users/stats/raw")
async def get_user_stats_raw(db: AsyncSession = Depends(get_db)):
    # 1. ORM으로 짜기 복잡한 쿼리를 text() 안에 문자열로 그대로 작성한다.
    raw_query = text(
        """
        SELECT
            COUNT(id) AS total_users,
            AVG(age) AS average_age,
            Max(age) AS max_age
        FROM users
        WHERE age IS NOT NULL
        """
    )

    # 2. 비동기 DB 세션으로 쿼리 실행
    result = await db.execute(raw_query)

    # 3. 결과 매핑 (중요)
    # scalars().all()은 ORM 객체 전용이다.
    # Raw SQL은 .mappings().fetchone() (단일 행) 또는 .mappings().fetchall() (여러 행)을 사용하여
    # {컬럼명: 값} 형태의 딕셔너리로 뽑아낸다.
    row = result.mappings().fetchone()

    # 4. JSON으로 변환되어 리턴
    if row:
        return dict(row) # 딕셔너리로 변환해서 리턴하면 FastAPI가 JSON으로 쏴준다.
    return {"message": "데이터가 없습니다."}

@app.get("/users/raw/search")
async def get_user_raw_search(
    limit_count: int = 5,
    db: AsyncSession = Depends(get_db)
):
    raw_query = text(
        """
        SELECT *
        FROM users 
        ORDER BY age DESC
        LIMIT :limit
        """
    )

    result = await db.execute(raw_query, {"limit": limit_count})

    row = result.mappings().fetchall()

    if row:
        return [dict(r) for r in row]
    return {"message": "데이터가 없습니다."}
