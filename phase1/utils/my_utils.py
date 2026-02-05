"""
Type Hinting (타입 힌트)
    : int, : float 처럼 타입을 명시해주는 것이 Modern Python 표준이다.
    -> int 는 이 함수가 int를 반환한다는 뜻이다. (강제성은 없지만 VS Code가 좋아함)
    `def func(a: int) -> int:`
        이 문법이 실행에 영향을 주진 않지만, Pylance 확장 프로그램이 이 힌트를 보고 자동 완성을 제공하고 에러를 미리 잡아줌
        습관을 들이는 것이 좋음
"""

def calculate_vat(price: int, tax_rate: float = 0.1) -> int:
    # 부가세를 포함한 가격을 계산하는 함수
    # tax_rate는 기본값 0.1 (10%)로 설정됨
    return int(price * (1 + tax_rate))