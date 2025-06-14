from dishka import Provider, Scope, provide

from app.config import (
    AppConfig,
    DBConfig, 
    JWTConfig,
    RedisConfig,
    SMTPConfig,
    load_app_config,
    load_db_config, 
    load_jwt_config,
    load_redis_config, 
    load_smtp_config,
)

from app.components import JWT


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_app_config(self) -> AppConfig:
        return load_app_config()

    @provide
    def get_db_config(self) -> DBConfig:
        return load_db_config()
    
    @provide
    def get_jwt_config(self) -> JWTConfig:
        return load_jwt_config()
    
    @provide
    def get_jwt(self, config: JWTConfig) -> JWT:
        return JWT(config)
    
    @provide
    def get_redis_config(self) -> RedisConfig:
        return load_redis_config()
    
    @provide
    def get_smtp_config(self) -> SMTPConfig:
        return load_smtp_config()
