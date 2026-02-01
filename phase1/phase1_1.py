"""
Phase 1-1. 기본기: 변수와 자료형

Python은 변수 선언 시 타입을 명시하지 않는 동적 타이핑(Dynamic Typing) 언어이다.
Java의 int, String 같은 선언 키워드가 없다.

1. 변수 선언과 네이밍 컨벤션(Naming Convention)
- 변수명: Python은 Snake Case(user_name)를 표준으로 사용함 (Java의 camelCase와 다름)
- 할당: 값만 넣으면 알아서 타입을 추론함

2. 핵심 자료형 4대장 (Container Types)
- DB 데이터를 다룰 때 가장 많이 쓰이는 4가지 자료형임
- 가변인지 불변인지 구별하는 것이 핵심

List: `[]`
    - 특징: 순서 O, 중복 O
    - 가변 여부: O (가변)
    - 용도: DB 조회 결과 목록 (Rows)
Tuple: `()`
    - 순서 O, 중복 O, 수정 불가
    - 가변 여부: X (불변)
    - 용도: DB 접속 정보, 절대 변하면 안 되는 값
Dict: `{}`
    - 특징: Key-Value 쌍
    - 가변 여부: O (가변)
    - 용도: JSON 응답 객체, 단일 Row 데이터
Set: `{}`
    - 특징: 순서 X, 중복 불가
    - 가변 여부: O (가변)
    - 용도: 태그 관리, 중복 제거 로직
"""

# 1. 기본 변수 (타입 선언 없음)
user_name = "Yoon Jiho" # str
work_year = 6           # int
is_employed = False     # bool (True/False 앞글자 대문자 주의)

# f-string (가장 많이 쓰이는 문자열 포맷팅, Python 3.6부터 도입된 표준)
print(f"개발자: {user_name}, 경력: {work_year}년")

print("-" * 20) # 문자열 곱하기 가능 (구분선으로 유용)

# 2. List (리스트) - 수정 가능
tech_stack = ["ASP", "MS_SQL", "Javascript", "jQuery", "Java/Spring"]
tech_stack.append("Python") # 추가
tech_stack[0] = "Classic ASP" # 수정
print("List:", tech_stack)

# 3. Tuple (튜플) - 수정 불가능 (Read-only)
# DB 접속 정보처럼 변하면 안 되는 값에 사용
db_config = ("127.0.0.1", 3306, "root")
# db_config[1] = 5000  # <--- 이 주석을 풀고 실행하면 에러 발생 ('TypeError' 발생)
print("Tuple:", db_config)

# 4. Dictionary (딕셔너리) - Key: Value
# JSON과 거의 동일한 형태
user_info = {
    "name": "Yoon Jiho",
    "role": "Backend Developer",
    "skills": ["Python", "SQL"] # 딕셔너리 안에 리스트 가능
}
print("Dict Name:", user_info["name"])
print("Dict Skills:", user_info["skills"])

# 5. Set (세트) - 중복 제거
tags = {"backend", "backend", "python", "fastapi"}
print("Set (증복제거됨):", tags)
