# [모듈 Import]
# 같은 폴더에 있는 my_utils.py에서 calculate_vat 함수를 가져옴
from utils.my_utils import calculate_vat
import datetime # 파이썬 내장 라이브러리

# 1. 기본 함수 사용 (Import 한 함수)
price = 10000
total = calculate_vat(price) # tax_rate 생략 시 기본값 0.1 적용
print(f"공급가: {price}, 합계: {total}")

print("-" * 30)

# 2. 가변 인자 (*args) - Arguments
# 인자의 개수가 정해지지 않았을 때 사용한다. 내부적으로 'Tuple'로 받는다.
def log_message(*args):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    # args는 ("Error", "DB Connection Failed", 500) 같은 튜플이 됨
    print(f"[{current_time}] Log:", args)

    # 튜플이니까 반복문 가능
    for msg in args:
        print(f" - 상세: {msg}")

log_message("System Error", "DB Timeout", "Critical")

print("-" * 30)

# 3. 키워드 가변 인자 (**kwargs) - Keyword Arguments [매우 중요]
# 인자를 'Key=Value' 형태로 넘길 때 사용한다. 내부적으로 'Dict'로 받는다.
# FastAPI 설정이나 DB 쿼리 필터링에 아주 많이 쓰인다.
def create_user_query(**kwargs):
    print("요청된 필터 조건(Dict):", kwargs)

    sql = "SELECT * FROM users WHERE 1=1"
    for key, value in kwargs.items():
        sql += f" AND {key} = '{value}'"
    
    print("생성된 SQL:", sql)

# 함수 호출 시 파라미터를 마음대로 넣을 수 있음
create_user_query(name="Yoon", status="Active", region="Seoul")

print("-" * 30)

# 4. 람다(Lambda) 함수
# 일회용 함수. 주로 정렬이나 데이터 가공 시 짧게 쓴다.
users = [("Yoon", 32), ("Kim", 28), ("Lee", 40)] # (이름, 나이)

# 나이(x[1])를 기준으로 정렬
users.sort(key=lambda x: x[1])
print("나이순 정렬:", users)
