import os
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    server: str = os.getenv('DB_SERVER', 'localhost')
    database: str = os.getenv('DB_NAME', 'FinaTechDB')
    username: str = os.getenv('DB_USERNAME', 'sa')
    password: str = os.getenv('DB_PASSWORD', 'your_password')
    driver: str = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
    
    @property
    def connection_string(self) -> str:
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"

@dataclass
class AppConfig:
    """Application configuration settings"""
    secret_key: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    debug: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    host: str = os.getenv('HOST', '0.0.0.0')
    port: int = int(os.getenv('PORT', 5000))
    cors_origins: list = ["http://localhost:3000"]

# Global configuration instances
db_config = DatabaseConfig()
app_config = AppConfig()