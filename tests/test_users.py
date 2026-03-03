import pytest
from httpx import AsyncClient, ASGITransport

from phase5_layered.main import app

# 비동기(async) 테스트 함수를 실행하기 위해 필요한 데코레이터
@pytest.mark.asyncio
async def test_register_user_success():
    """
    회원가입 성공 테스트
    """
    # 1. 가짜 클라이언트(Postman 역할) 생성
    # ASGITransport는 실제 네트워크 포트를 열지 않고 FastAPI 앱과 직접 통신하게 해준다.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        # 2. API에 보낼 테스트용 데이터 셋업 (매번 새로운 유저로 테스트하기 위해 999번 부여)
        test_user = {
            "username": "test_user_999",
            "password": "testpassword123",
            "age": 30
        }

        # 3. HTTP POST 요청 쏘기 (라우터 호출)
        response = await ac.post("/users", json=test_user)
    
    # 4. 검증 (Assert) 구간 - 여기가 테스트의 핵심임
    # HTTP 상태 코드가 200 정상인지 확인
    assert response.status_code == 200

    # 응답 데이터 검증
    data = response.json()
    assert data["username"] == "test_user_999"
    assert "age" in data

    # [보안 검증] 응답 객체에 비밀번호가 포함되지 않았는지 확실히 체크
    assert "password" not in data
