"""
Phase2 Exam. Retry(재시도) 데코레이터 만들기
백엔드 개발을 하다보면 외부 API가 가끔 끊기거나 DB 연결이 순간적으로 튀는 경우가 있다.
이럴 때 '에러가 나면 3번까지는 다시 시도해 봐'라는 로직이 필수적이다.
이것을 데코레이터로 구현해 볼 것이다.

1. @retry라는 데코레이터를 만들 것
    - 인자는 받지 않음 (심화 예제보다 구조는 간단함)
    - 내부 wrapper에서 try-except 구문과 for 반복문(최대 3회)을 사용할 것
    - 함수 실행 중 에러가 나면 "에러 발생! 재시도 합니다..."를 출력 후 다시 실행할 것
    - 성공하면 결과를 리턴하고 종료할 것
    - 3번 다 실패하면 에러를 그대로 던지거나 "최종 실패"를 출력할 것
2. "랜덤으로 실패하는 함수"에 적용하여 동작을 확인
"""
import random

# 데코레이터 함수
def retry(func):
    def wrapper(*args, **kwargs):
        last_exception = None  # 마지막 에러를 기억할 변수

        for i in range(3):  # 3번까지 시도
            try:
                return func(*args, **kwargs)  # 성공하면 즉시 리턴
            except Exception as e:
                print(f"[{i+1}/3]: 에러 발생: {e}, 재시도 중...")
                last_exception = e  # 에러 저장
        
        # 3번 다 돌았는데도 여기 왔다면 실패한 것임
        print("최대 재시도 횟수 초과. 에러를 다시 던집니다.")

        # [Pylance 해결] None이 아닐 때만 raise 하도록 안전장치 추가
        if last_exception:
            raise last_exception  # 마지막 에러를 상위로 던짐

        # (혹시 모를 예외 상황 대비 - 로직상 도달할 일은 거의 없음)
        raise Exception("알 수 없는 이유로 재시도 실패")

    return wrapper

# 테스트용 함수
@retry
def unstable_network_request():
    # 20% 확률로 성공, 80% 확률로 실패하는 악질 함수
    if random.random() < 0.2:
        return "통신 성공! 데이터를 받아왔습니다."
    else:
        raise ValueError("네트워크 연결 불안정")

# 실행
print(unstable_network_request())
