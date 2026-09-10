from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:
    def __init__(self, config: DBConfig):
        self.engine: AsyncEngine | None = None
        self.config = config

    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.db}"

    def init(self):
        self.engine = create_async_engine(self._get_url())

    async def close(self):
        await self.engine.dispose()


meta_mysql_client_manager = MySQLClientManager(app_config.db_meta)
dw_mysql_client_manager = MySQLClientManager(app_config.db_dw)
