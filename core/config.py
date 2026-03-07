from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env 파일에 있는 키값과 변수명을 똑같이 맞춰주면 알아서 매핑됨
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_TEST_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 루트 경로에 있는 .env 파일을 읽어오라는 설정
    model_config = SettingsConfigDict(env_file=".env")

# 이 settings 객체를 다른 파일에서 import 해서 사용함 (싱글톤 패턴 효과)
settings = Settings()  # type: ignore