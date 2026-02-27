import bcrypt

def get_password_hash(password: str) -> str:
    """
    평문 비밀번호를 받아서 Bcrypt로 암호화(해싱)된 문자열을 반환한다.
    (예: 회원가입 할 때 사용)
    """
    # 1. 파이썬 문자열(str)을 바이트(bytes)로 변환
    pwd_bytes = password.encode('utf-8')

    # 2. 소금(Salt)을 치고 해싱
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

    # 3. DB에 저장하기 위해 다시 문자열로 변환하여 리턴
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    사용자가 입력한 평문 비밀번호와 DB에 저장한 암호화 비밀번호가 일치하는지 확인한다.
    (예: 로그인 할 때 사용)
    """
    # 둘 다 바이트 형태로 변환한 뒤 비교
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
