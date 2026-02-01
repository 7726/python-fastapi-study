"""
Phase 1-2. 제어문 (if, for, while)
- Python의 제어문이 다른 언어와 가장 다른 점은 "괄호 `{}` 대신 들여쓰기로 블록을 구분한다"는 점이다.
- 보통 Space 4칸을 표준으로 한다.
- 들여쓰기가 맞지 않으면 `IdentationError`가 발생하니 주의할 것.

1. 조건문 (if)
- `if`, `elif` (else if 아님), `else`를 사용한다.
- 논리 연산자가 기호(&&, ||, !)가 아닌 영어 단어(`and`, `or`, `not`)이다.

2. 반복문 (for)
- Python의 `for`문은 단순히 숫자를 증가시키는 것이 아니라, 리스트(컬렉션)를 하나씩 꺼내오는 방식에 최적화되어 있다.
- 백엔드 개발 시 데이터를 가공할 때 가장 많이 쓰는 3가지 패턴을 익혀야 한다.
    1) Just Loop: `for item in list:` (값만 필요할 때)
    2) Enumerate: `for index, item in enumerate(list):` (순번과 값이 모두 필요할 때)
    3) Zip: `for a, b in zip(list_a, list_b):` (두 개의 리스트를 동시에 묶어서 돌릴 때)
        - 서로 다른 두 배열의 데이터를 합쳐서 JSON 객체로 만들거나 검증할 때 매우 유용하다.
    4) 증감 연산자 부재: `i++`는 Python에 없다. 반드시 `i += 1`을 사용해야 한다.
"""

# 1. if문과 논리 연산자
user_status = "active"
login_fail_count = 3

# 괄호 없이 직관적으로 작성 (and, or, not 사용)
if user_status == "active" and login_fail_count < 5:
    print("로그인 성공: 메인 페이지로 이동")
elif user_status == "suspended":
    print("계정이 정지되었습니다.")
else:
    print("비밀번호 5회 오류: 계정 잠금")

print("-" * 30)

# 2. for문 기본 (DB Rows 순회)
db_rows = ["user_a", "user_b", "user_c"]

print("[Case 1] 값만 필요할 때")
for row in db_rows:
    print(f"User: {row}")

print("\n[Case 2] 인덱스(순번)가 필요할 때 (enumerate)")
# enumerate: (0, 'user_a'), (1, 'user_b')... 형태로 반환
for i, row in enumerate(db_rows, start=1): 
    print(f"{i}번째 회원: {row}")

print("-" * 30)

# 3. zip (두 개의 리스트 병합) - 실무 꿀팁
# 시나리오: DB 컬럼명 리스트와 값 리스트가 따로 왔을 때 매핑하기
columns = ["id", "name", "email"]
values = [101, "Yoon", "Yoon@test.com"]

print("[Case 3] 두 리스트 묶기 (zip)")
# 같은 인덱스끼리 짝을 지어 튜플로 반환
for col, val in zip(columns, values):
    print(f"{col} : {val}")

# 4. while문 (조건 반복)
print("\n[Case 4] While문")
count = 3
while count > 0:
    print(f"카운트 다운: {count}")
    count -= 1  # Python엔 증감연산자(++, --)가 없습니다. +=, -= 사용.