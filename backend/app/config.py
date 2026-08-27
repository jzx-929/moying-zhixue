from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    chroma_db_path: str = "../data/chroma_db"
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    collection_name: str = "guoxue_texts"

    spark_api_base: str = "https://xingchen-api.xf-yun.com/workflow/v1/chat/completions"
    spark_appid: str = ""
    spark_api_key: str = ""
    spark_api_secret: str = ""
    wengai_agent_id: str = ""
    moying_agent_id: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def chroma_db_abs_path(self) -> str:
        base = Path(__file__).resolve().parent.parent.parent
        return str(base / self.chroma_db_path.replace("../", ""))


settings = Settings()
