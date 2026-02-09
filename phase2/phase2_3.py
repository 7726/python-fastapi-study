"""
Phase 2-3. Pythonic Code (List Comprehension & Context Manager)
이번 단계에서는 Python을 "Python답게" 쓰는 두 가지 핵심 무기를 장착한다.

1. List Comprehension (리스트 내포)
- 기존 방식: 빈 리스트 생성 -> 반복문 -> 조건문 -> 값 추가(append)
- Pythonic 방식: 리스트 안에 반복문과 조건문을 구겨 넣어서 한 줄로 생성

2. Context Manager (with 구문)
- 기존 방식: 파일 열기(Open) -> 작업 -> 파일 닫기(Close) / DB 연결 -> 쿼리 -> 연결 종료
- Pythonic 방식: with 블록을 벗어나면 알아서 Close를 실행해준다. (자원 누수 방지 1등 공신)
"""

# 1. List Comprehension (리스트 내포)
# 상황: DB에서 가져온 1~10 데이터 중 '짝수'만 뽑아서 '10일 곱한 리스트'를 만들고 싶다.

# [Bad: 고전적인 방식]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens_classic = []
for n in numbers:
    if n % 2 == 0:
        evens_classic.append(n * 10)

print(f"Classic: {evens_classic}")

# [Good: Pythonic 방식]
# 해석: [ (결과값) for (변수) in (리스트) if (조건) ]
evens_pythonic = [n * 10 for n in numbers if n % 2 == 0]

print(f"Pythonic: {evens_pythonic}")
print("-" * 30)


# 2. Dictionary Comprehension (딕셔너리 내포)
# 상황: 두 개의 리스트(key, Value)를 합쳐서 딕셔너리로 만드는데, 값이 60점 이상인 사람만 남기고 싶다.
names = ["Yoon", "Kim", "Lee", "Park"]
scores = [95, 40, 80, 55]

# zip으로 묶고 -> if로 거르고 -> dict로 생성
passed_students = {name: score for name, score in zip(names, scores) if score >= 60}

print(f"합격자 명단: {passed_students}")
print("-" * 30)


# 3. Context Manger (with 구문) - 자원 관리의 핵심
# 파일이나 DB 연결을 열고 닫을 때 'Close'를 까먹는 실수를 원천 봉쇄
with open("log.txt", "w", encoding="utf-8") as file:
    file.write("Pythonic Code Log Entry\n")
    file.write("이 블록이 끝나면 파일은 자동으로 닫힌다.")
    print("파일 작성 완료 (아직 닫히기 전)")

# 블록을 나오면 자동으로 file.close()가 실행된 상태임
print("파일 닫힘 완료")

# [파일 읽기]
# 'r'은 읽기 모드이다.
try:
    with open("log.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(f"[파일 내용 읽기]\n{content}")
except FileNotFoundError:
    print("파일이 없습니다.")