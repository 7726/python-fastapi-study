
# python-fastapi-study

Python/FastAPI 학습을 위한 repo 입니다.

---

## [학습 커리큘럼]

### Phase 1: Python 3.12 기초 문법 (Syntax Boot Camp)
*목표: 구글링 없이 프로그래머스 Level 0~1 문제를 풀 수 있는 문법 근육 키우기*
1. **기본기**: 변수, 자료형(List, Dict, Tuple, Set - **가변/불변 차이 강조**), 연산자.
2. **제어문**: `if`, `for` (range, enumerate, zip 활용), `while`.
3. **함수와 모듈**: `def` 정의, `args/kwargs`, `lambda`, 모듈 `import` 방식.
4. **객체지향(OOP)**: `class`, `self`의 의미, 상속 (Spring의 DI를 이해하기 위한 기초).

### Phase 2: Modern Python (중급 도약)
*목표: FastAPI 코드를 읽고 쓸 수 있는 고급 문법 장착*
1. **가상환경**: `venv` 설정 및 패키지 관리 (`pip`).
2. **Type Hinting**: `str` vs `Optional[str]`, `List[int]`, Pydantic과의 관계.
3. **Pythonic Code**: List Comprehension(리스트 내포), f-string, Context Manager(`with`).
4. **비동기 프로그래밍**: `async`, `await`의 개념과 Event Loop 원리 (ASP와의 결정적 차이).
5. **Decorator**: `@app.get`이 어떻게 동작하는지 이해하기 위한 데코레이터 원리.

### Phase 3: FastAPI 기본 & 아키텍처 (Architecture)
*목표: Request부터 Response까지의 흐름 제어 및 API 명세*
1. **구조 이해**: `routers`(Controller) -> `services`(Business Logic) -> `cruds`(Repository) -> `schemas`(DTO) -> `models`(Entity) 로 이어지는 **Standard Layered Architecture** 설명.
2. **Routing & Docs**: Path/Query Parameter 처리 및 **Swagger UI (/docs)** 활용법.
3. **Pydantic**: 데이터 검증 및 직렬화 (Spring의 DTO + @Valid 역할).
4. **Dependency Injection (DI)**: DB 세션 주입 등 의존성 주입의 핵심 원리.
5. **Error Handling**: `HTTPException` 및 전역 예외 처리기(`ExceptionHandler`) 구현.

### Phase 4: DB & ORM (MySQL + SQLAlchemy Async)
*목표: 사용자의 강점인 DB 역량을 Python으로 이식*
1. **설정**: `aiomysql` 드라이버 및 비동기 엔진 연결.
2. **ORM Modeling**: SQLAlchemy 2.0 스타일의 Model 선언 (`Mapped`, `mapped_column`).
3. **CRUD 실습**: 비동기 Session을 활용한 데이터 조작 (Create, Read, Update, Delete).
4. **Raw SQL 활용**: ORM으로 해결하기 힘든 복잡한 쿼리를 `text()`로 직접 실행하는 법.
5. **Migration**: `Alembic`을 이용한 DB 스키마 버전 관리.

### Phase 5: 보안 및 인증/인가 (Security & Auth)
*목표: 회원가입, 로그인 및 JWT 기반의 보호된 API 구현*
1. **Password Hashing**: `Passlib`과 `Bcrypt`를 이용한 비밀번호 암호화 저장.
2. **JWT 흐름**: Access Token 생성 및 검증 원리 (PyJWT).
3. **OAuth2 구현**: FastAPI 내장 `OAuth2PasswordBearer`를 이용한 로그인 로직.
4. **인가(Authorization)**: `get_current_user` 의존성(Dependency)을 만들어 API 권한 제어하기.

### Phase 6: 실무 완성 (Test & Deploy)
*목표: 현업 수준의 품질 확보*
1. **테스트**: `Pytest` 및 `pytest-asyncio`를 이용한 단위/통합 테스트 작성.
2. **컨테이너화**: `Dockerfile` 작성 (Multi-stage build 권장).
3. **배포 시뮬레이션**: `docker-compose`로 MySQL + FastAPI 컨테이너 띄우기.
