"""
Phase 2-5. Decorator (데코레이터)

1. 개념: "함수를 감싸는 포장지"
데코레이터는 기존 함수를 수정하지 않고, 앞뒤에 기능을 덧붙이고 싶을 때 사용한다.
- 비유:
    - 원본 함수: "선물(Gift)"
    - 데코레이터: "선물 포장지(Wrapper)"
    - 우리가 받는 건 '포장된 선물'이지만, 내용물은 변하지 않았다.
- ASP/Spring 비유:
    - ASP의 Include 파일이나 Spring의 AOP(Aspect Oriented Programming), Interceptor와 목적이 같다.
    - (로그 남기기, 실행 시간 측정, 로그인 여부 체크 등)

2. 문법: 골뱅이(@)의 정체
함수 위에 `@데코레이터이름`을 붙이면, Python 인터프리터가
"이 함수 실행하기 전에 데코레이터 함수한테 먼저 보내서 포장해와!" 라고 명령한다.

아래의 코드에서 백엔드 API를 개발할 때 "이 쿼리가 몇 초 걸리지?"를 측정하는 로직을 데코레이터로 만들어 보겠다.
"""
import time

# 1. 데코레이터 함수 정의 (포장지 공장)
# func: 포장할 대상(원본 함수)이 들어온다.
def time_logger(func):

    # 2. 내부 래퍼 함수 (실제 포장지)
    # *args, **kwargs: 원본 함수가 어떤 인자를 받든 다 통과시키기 위해 사용 (Phase 1-3 복습)
    def wrapper(*args, **kwargs):
        print(f"---[Start] {func.__name__} 함수 실행 ---")
        start_time = time.time()

        # 3. 원본 함수 실행 (선물 내용물 확인)
        result = func(*args, **kwargs)

        end_time = time.time()
        print(f"---[End] 소요 시간: {end_time - start_time:.5f}초 ---")

        # 4. 원본 함수의 결과값 반환
        return result
    
    # 포장된 함수(wrapper)를 반환
    return wrapper

# --------------------------------------------------

# [적용 전]
def basic_function():
    print("나는 평범한 함수입니다.")

# [적용 후 - 데코레이터 사용]
# @time_logger를 붙이는 순간, slow_query 함수는 time_logger에 의해 '포장'된다.
@time_logger
def slow_query(seconds):
    print(f"DB 쿼리 실행 중... ({seconds}초 대기)")
    time.sleep(seconds)
    return "Query Success"

# --------------------------------------------------

# 실행
print("1. 데코레이터 없는 함수 실행:")
basic_function()

print("\n2. 데코레이터 적용된 함수 실행:")
# 개발자는 그냥 함수를 호출했을 뿐인데, 자동으로 시간 측정이 된다.
result = slow_query(1.5)
print(f"결과값: {result}")

"""
1. 흐름 이해:
    - slow_query(1.5)를 호출하면 -> wrapper(1.5)가 실행된다.
    - wrapper 안에서 시간 측정 시작 -> func(1.5) 진짜 실행 -> 시간 측정 종료 -> 리턴

2. FastAPI와의 관계:
    - @app.get("/")도 똑같다.
    - "아래에 있는 함수(def root())를 가져다가, URL이 `/`인 요청이 오면 실행되도록 등록해라"라는 기능을 하는 데코레이터임
"""