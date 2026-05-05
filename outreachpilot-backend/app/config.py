from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OutreachPilot AI"
    APP_ENV: str = "development"

    AWS_REGION: str = "ap-south-1"
    DYNAMODB_REPORTS_TABLE: str = "OutreachPilotReports"
    S3_REPORTS_BUCKET: str

    OPENAI_API_KEY: str

    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()