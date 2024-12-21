from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    CONFIG_TEST: str = Field(default="sss", json_schema_extra={"env": "CONFIG_TEST"})
    LOG_DIR: str = Field(default="./", json_schema_extra={"env": "LOG_DIR"})
    LOG_LEVEL: str = Field(default="INFO", json_schema_extra={"env": "LOG_LEVEL"})
    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    # Config クラスの代わりに ConfigDict を使用
    model_config = ConfigDict(env_file=".env")


# インスタンス生成
settings = Settings()
