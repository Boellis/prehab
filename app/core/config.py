"""
This uses Pydantic's BaseSettings to centralize and manage the app's configuration.
It allows settings to be defined as environment variables or fallback to default values.
"""

import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Basic application settings
    PROJECT_NAME: str = Field("[P]rehab Takehome", env="PROJECT_NAME")
    API_VERSION: str = Field("v1", env="API_VERSION")
    
    # Database settings (for this example, we are using SQLite)
    DB_USER: str = Field("postgres", env="DB_USER")
    DB_PASSWORD: str = Field("postgres", env="DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field("prehab_takehome", env="DB_NAME")
    
    # JWT settings for authentication tokens
    JWT_SECRET_KEY: str = Field("SUPERSECRETKEY", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 7, env="REFRESH_TOKEN_EXPIRE_MINUTES")  # 7 days

    class Config:
        # Automatically load variables from a .env file if it exists
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance to use across the application
settings = Settings()
