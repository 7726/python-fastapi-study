"""
Phase 1 종료 미니 과제

`PaymentProcessor`를 상속받는 `BankTransferPeyment`(무통장 입금)
클래스를 하나 더 만들어서, account_number(계좌번호)를 받고
`pay` 메서드에서 "계좌 ... 로 ... 원 입금 대기 중"을 출력하게 코드를 추가해 볼 것
"""

# 부모 클래스
class PaymentProcessor:
    def __init__(self, method_name):
        self.method_name = method_name
        print(f"[{self.method_name}] 결제 처리가 초기화됨")
    
    def pay(self, amount):
        raise NotImplementedError("이 메서드는 자식 클래스에서 구현해야 합니다.")

# 자식 클래스
class BankTransferPayment(PaymentProcessor):
    def __init__(self, account_number):
        super().__init__("Bank Transfer")
        self.account_number = account_number
    
    def pay(self, amount):
        print(f"계좌 {self.account_number}로 {amount}원 입금 대기 중.")

# [실행 - 인스턴스 생성 및 사용]

bank_transfer = BankTransferPayment("4321-876532-0000")
bank_transfer.pay(300000)

