import pytest

# 이 데코레이터는 "이 테스트 함수는 비동기(async)로 동작해" 라고 Pytest에게 알려줌
@pytest.mark.asyncio
async def test_create_user(async_client):
    """
    회원가입(Create User) 성공 케이스 테스트
    """
    # 1. 테스트에 사용할 요청 데이터 세팅
    user_data = {
        "username": "testuser_1",
        "password": "testpassword123!",
        "age": 30
    }

    # 2. API 요청 보내기
    # 괄호 안에 있는 async_client는 conftest.py에서 만든 그 가짜 클라이언트임
    response = await async_client.post("/users", json=user_data)

    # 3. 결과 검증 (Assertion)
    # 응답 코드가 200(성공)인지 확인함 (조건이 틀리면 여기서 테스트가 실패함)
    assert response.status_code == 200

    # 응답 본문(JSON)을 파이션 딕셔너리로 변환
    data = response.json()

    # 내가 보낸 아이디가 그대로 잘 리턴되었는지 확인
    assert data["username"] == "testuser_1"

    # DB에서 Auto Increment로 생성된 'id' 필드가 응답에 포함되어 있는지 확인
    assert "id" in data

    # password가 잘 걸러졌는지 확인
    assert "password" not in data

@pytest.mark.asyncio
async def test_login_user(async_client):
    """
    로그인(토큰 발급) 성공 케이스 테스트
    """
    # 1. Form 데이터 세팅
    login_data = {
        "username": "testuser_1",
        "password": "testpassword123!",
    }

    # 2. API 요청 (json= 대신 data= 를 사용)
    response = await async_client.post("/users/login", data=login_data)

    # 3. 결과 검증
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_read_users_me(async_client):
    """
    내 정보 조회(보안 API) 성공 케이스 테스트
    """
    # 1. 로그인을 먼저 수행해서 토큰을 발급받음
    login_data = {"username": "testuser_1", "password": "testpassword123!"}
    login_response = await async_client.post("/users/login", data=login_data)
    token = login_response.json()["access_token"]

    # 2. 발급받은 토큰을 HTTP 헤더(Headers)에 장착
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 3. 헤더를 포함하여 보안 API 호출
    response = await async_client.get("/users/me", headers=headers)

    # 4. 결과 검증
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser_1"
