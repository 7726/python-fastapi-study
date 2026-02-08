# 과거(Legacy): from typing import List, Dict, Union, Optional (이제 안 씀)

# 1. 변수 타입 선언 (Variable Annotation)
# 문법: 변수명: 타입 = 값
user_name: str = "Yoon Jiho"
user_age: int = 35
is_active: bool = True

# 2. 컬렉션 제네릭 (Generics) - Python 3.9+ 표준
tech_stack: list[str] = ["ASP", "MS SQL", "Python"]

user_scores: dict[str, int] = {
    "Yoon": 95,
    "Kim": 80
}

# 3. Union Type & Nullable (Python 3.10+ 표준)
# | (Pipe) 연산자로 '또는(OR)'을 표현한다.

# 상황: ID는 숫자일 수도 있고 문자일 수도 있다.
user_id: int | str = 101
user_id = "admin" # 에러 안 남 (둘 다 허용)

# 상황: 이메일은 있을 수도 있고 없을 수도 있다. (Nullable)
user_email: str | None = None

print(f"ID: {user_id}, Email: {user_email}")
print("-" * 30)

# 4. 함수에서의 활용 (매우 중요)
def send_notification(user_ids: list[int], message: str | None = None) -> bool:
    """
    user_ids: 알림을 보낼 사용자 ID 목록 (숫자만 가능)
    message: 보낼 메시지 (없으면 기본 메시지 전송)
    return: 성공 여부 (bool)
    """
    if not message:
        message = "안녕하세요! 기본 알림입니다."
    
    print(f"전송 대상({len(user_ids)}명): {user_ids}")
    print(f"메시지 내용: {message}")

    return True

# [정상 호출]
send_notification([1, 2, 3], "서버 점검 안내")

# [실수 시뮬레이션]
# 아래 주석을 풀면 VS Code(Pylance)가 빨간 줄을 긋는다. 실행 전부터 알 수 있다.
# VS Code 설정에 Python > Analysis: Type Checking Mode을 basic으로 바꿔줘야 밑줄 에러를 볼 수 있음
# send_notification(["admin", "manager"]) # Error: list[int]여야 하는데 str이 들어감
