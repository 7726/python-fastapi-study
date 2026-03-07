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
