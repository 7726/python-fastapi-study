"""
Phase 2-5. Decorator (데코레이터)

이번에는 관리자(Admin) 권한이 있는 사람만 실행할 수 있는 함수를 만들어 보겠다.
ASP에서 페이지 상단에 `If Session("UserRole") <> "Admin" Then Response.Redirect ...` 하던 로직을
데코레이터로 우아하게 빼는 과정이다.

이 코드는 함수가 3단으로 중첩된다. (이 구조가 데코레이터의 끝판왕이다.)
1. 데코레이터 공장 (require_role): "admin"이라는 글자를 받아서 데코레이터를 찍어낸다.
2. 데코레이터 (decorator): 실제 함수(delete_database)를 포장한다.
3. 래퍼(wrapper): 실제 실행 시점에 권한을 검사한다.
"""
# [상황 설정] 현재 로그인한 사용자 (Mock Data)
# 이 값을 바꿔가며 테스트 할 것이다.
CURRENT_USER = {
    "name": "Yoon Jiho",
    "role": "user"  # 'admin'으로 바꾸면 실행됨
}

# ----------------------------------------------
# 1. 데코레이터 정의 (인자를 받는 데코레이터)
# ----------------------------------------------

def require_role(role_name: str):
    # 특정 권한(role_name)이 있는 사용자만 함수를 실행하게 하는 데코레이터 공장

    # 실제 데코레이터 (함수를 받음)
    def decorator(func):

        # 실제 로직 (인자를 받음)
        def wrapper(*args, **kwargs):
            user_role = CURRENT_USER.get("role")

            print(f"[보안 체크] 필요한 권한: '{role_name}' / 현재 권한: '{user_role}'")

            if user_role != role_name:
                print(f"접근 거부! {role_name} 권한이 필요합니다.")
                return None  # 함수 실행 차단
            
            # 권한이 안맞으면 원본 함수 실행
            print("권한 확인됨. 로직을 수행합니다.")
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

# ----------------------------------------------
# 2. 데코레이터 적용
# ----------------------------------------------

# ASP였다면 함수 안에서 if문을 썼겠지만,
# 이제는 함수 위에 데코레이터만 붙이면 됨

@require_role("admin")
def delete_database():
    print("데이터베이스를 삭제합니다... (매우 위험한 작업)")

@require_role("user")
def view_profile():
    print("내 프로필을 조회합니다.")

# ----------------------------------------------
# 3. 실행 테스트
# ----------------------------------------------

print("--- [Case 1] 일반 유저가 DB 삭제 시도 ---")
delete_database()
# 예상: 접근 거부 메시지 출력 (실행 안 됨)

print("\n--- [Case 2] 일반 유저가 프로필 조회 시도 ---")
view_profile()
# 예상: 정상 실행

print("\n--- [Case 3] 상황 변경: 사용자를 admin으로 승격 ---")
CURRENT_USER["role"] = "admin"

print(">> 다시 DB 삭제 시도:")
delete_database()
# 예상: 이제는 실행됨

"""
구조 파악:
- @require_role("admin")을 쓰면, 파이썬은 require_role("admin")을 먼저 실행해서 decorator를 받아냄
- 그 decorator가 delete_database를 감싸는 구조임

핵심:
- 핵심 비즈니스 로직(delete_database) 안에는 if문이 하나도 없다는 점을 주목
- 비즈니스 로직과 보안 로직이 완벽하게 분리됨 (AOP 개념)
"""