"""
Phase 2-4. 비동기 프로그래밍 (Async/Await)

1. 개념 비교: 카페 주문 상황
- 동기 (ASP/Java)
    - 점원(Thread)이 손님 A의 주문을 받고, 주방에서 커피가 나올 때까지 아무것도 안 하고 카운터 앞에서 기다림
    - 커피가 나와야만 손님 B의 주문을 받음
    - (DB 쿼리가 오래 걸리면 서버가 멈추는 현상)
- 비동기 (FastAPI)
    - 점원이 손님 A의 주문을 받고 주방에 넘김
    - 커피가 나오는 동안 기다리지 않고 바로 다음 손님 B의 주문을 받으러 감
    - 주방에서 "커피 완료!" 알림(Event)이 오면 손님 A에게 전달함
    - (적은 리소스로 엄청난 트래픽 처리 가능)

2. 핵심 키워드
- async def: "이 함수는 비동기 함수(Coroutine)야. 실행 중에 멈췄다가 딴짓할 수 있어" 라고 선언
- await: "여기서 시간이 좀 걸릴 것 같으니까(DB 조회, API 호출), 결과 나올 때까지 제어권을 딴 놈한테 넘길게"
"""
import time
import asyncio  # 비동기 처리를 위한 내장 라이브러리

# 1. 동기(Sync) 방식 함수
# time.sleep: CPU를 강제로 멈춘다.
def sync_cooking(menu):
    print(f"[동기] {menu} 요리 시작...")
    time.sleep(1)  # 1초 동안 아무것도 못함 (멍 때리기)
    print(f"[동기] {menu} 요리 완료!")

# 2. 비동기(Async) 방식 함수
# async def: 코루틴(Coroutine) 정의
async def async_cooking(menu):
    print(f"[비동기] {menu} 요리 시작...")
    await asyncio.sleep(1)  # "1초 뒤에 깨워줘" 하고 딴 일 하러 감
    print(f"[비동기] {menu} 요리 완료!")

# 3. 메인 실행부
async def main():
    print("--- 1. 동기 방식 실행 (순차적) ---")
    start_time = time.time()

    # 하나 끝나야 다음꺼 실행
    sync_cooking("라면")
    sync_cooking("김밥")
    sync_cooking("떡볶이")

    end_time = time.time()
    print(f"동기 방식 소요 시간: {end_time - start_time:.2f}초")

    print("\n--- 2. 비동기 방식 실행 (동시성) ---")
    start_time = time.time()

    # gather: 여러 비동기 함수를 '동시에' 예약 걸어버림
    # 마치 주방에 주문서 3장을 한꺼번에 던지는 것과 같음
    await asyncio.gather(
        async_cooking("라면"),
        async_cooking("김밥"),
        async_cooking("떡볶이")
    )

    end_time = time.time()
    print(f"비동기 방식 소요 시간: {end_time - start_time:.2f}초")

# 비동기 함수 실행을 위한 진입점
# Python 3.7+ 부터는 asyncio.run()을 사용
if __name__ == "__main__":
    asyncio.run(main())

"""
# `if __name__ == "__main__":` "구문은 이 파일이 직접 실행될 때만 코드를 실행하라"는 안전장치(가드)이다.
# 직접 실행 시 `__name__` 변수에 `__main__`이라는 값이 자동으로 들어간다.
# import 될 시 이 변수에 "file"(파일명)이 들어간다.
"""