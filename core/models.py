from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

# Base 클래스를 상속받으면, SQLAlchemy가 "아, 이건 DB 테이블이구나!" 하고 인식한다.
class User(Base):
    __tablename__ = "users" # 실제 MySQL에 생성될 테이블 이름

    # Mapped[타입]: 파이썬이 읽는 타입 (Pylance 자동완성용)
    # mapped_column(DB타입, 옵션): 실제 MySQL에 생성될 컬럼 옵션
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # 선택적(Null 허용) 컬럼은 파이썬 타입에도 | None 을 붙이고, DB 옵션에도 nullable=True를 준다.
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)