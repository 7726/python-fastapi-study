"""
Phase 1-4. 클래스와 객체지향 (OOP)

1. 핵심 차이점 (vs Java/C#)
- `self`: Python은 클래스 내부 메서드의 첫 번째 인자로 무조건 `self`를 명시해야 한다. (Java의 `this`와 같지만, 생략 불가)
- 접근 제어자: `private`, `public` 키워드가 없다. 대신 변수명 앞에 `_` (내부용 암묵적 약속) 또는 `__` (강제 숨김)를 붙인다.

2. `self`의 존재 이유:
- `def pay(self, amount):` 라고 정의하지만, 호출할 땐 `card_pay.pay(15000) 처럼 amount만 넣는다.
- 파이썬 인터프리터가 호출 시 자동으로 card_pay.pay(card_pay, 15000) 처럼 객체 자신을 첫 번째 인자로 끼워 넣기 때문이다.
- 그래서 받는 쪽에 `self` 자리를 꼭 만들어둬야 한다.

3. `super().__init__()`: 자식 클래스에서 __init__을 새로 정의하면 부모의 __init__이 자동 실행되지 않는다.
꼭 명시적으로 호출해줘야 부모의 초기화 로직(여기선 `method_name` 설정)이 작동한다. 
"""

# 1. 부모 클래스 (Parent Class)
class PaymentProcessor:
    # 생성자 (__init__)
    def __init__(self, method_name):
        # self.변수명 = 인스턴스 변수 선언 및 할당
        self.method_name = method_name
        print(f"[{self.method_name}] 결제 처리가 초기화됨")
    
    # 메서드 정의 (첫 번째 인자는 무조건 self)
    def pay(self, amount):
        # 자식 클래스에서 구현하도록 비워둠 (Java의 Abstract Method 느낌)
        raise NotImplementedError("이 메서드는 자식 클래스에서 구현해야 합니다.")

# 2. 자식 클래스 (Ingeritance) - 신용카드 결제
class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number):
        # 부모 생성자 호출 (super())
        super().__init__("Credit Card")
        self.card_number = card_number # 나만의 속성 추가
    
    # 오버라이딩 (Overriding)
    def pay(self, amount):
        # 실제 로직 구현
        print(f"카드번호 {self.card_number}로 {amount}원 결제 승인 완료.")

# 3. 자식 클래스 (Ingeritance) - 카카오페이 결제
class KakaoPayment(PaymentProcessor):
    def __init__(self, user_id):
        super().__init__("Kakao Pay")
        self.user_id = user_id
    
    def pay(self, amount):
        print(f"카카오 사용자({self.user_id})에게 {amount}원 결제 요청.")

print("-" * 30)

# [실행 - 인스턴스 생성 및 사용]

# 1. 신용카드 객체 생성
card_pay = CreditCardPayment("1234-5678-0000-0000")
card_pay.pay(15000)

print("-" * 10)

# 2. 카카오페이 객체 생성
kakao_pay = KakaoPayment("yoon_jiho")
kakao_pay.pay(5000)

print("-" * 30)

# [심화: 다형성(Polymorphism)]
# 부모 타입으로 묶어서 처리 (Spring의 Interface 활용과 동일)
payment_list = [card_pay, kakao_pay]

print("[일괄 처리 시작]")
for payment in payment_list:
    # 어떤 자식인지 몰라도 pay()만 호출하면 알아서 동작
    payment.pay(1000)