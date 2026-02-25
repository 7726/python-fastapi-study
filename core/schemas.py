from pydantic import BaseModel, Field, ConfigDict

# 1. 회원가입 요청용 DTO (클라이언트 -> 서버)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=4)
    age: int | None = None

# 2. 회원 정보 응답용 DTO (서버 -> 클라이언트)
# 중요: 응답에는 'password' 필드가 없음 (보안)
class UserResponse(BaseModel):
    id: int
    username: str
    age: int | None = None

    # ORM 객체(Entity)를 Pydantic 모델로 자동 변환하게 해주는 마법의 설정 (Pydantic v2 문법)
    model_config = ConfigDict(from_attributes=True)