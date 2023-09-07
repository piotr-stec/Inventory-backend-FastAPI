from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Inventory"
    root_path: str = "/"

    db_host: str = 'db'
    db_port: int = 5432
    db_user: str = 'inventory'
    db_password: str = 'inventory'
    db_name: str = 'inventory'

    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class Config:
        env_prefix = 'inventory_'


# from pydantic import BaseSettings
#
# class Settings(BaseSettings):
#     app_name: str = "Todo"
#     root_path: str = "/"
#
#     db_host: str = 'db'
#     db_port: int = 5432
#     db_user: str = 'todo'
#     db_password: str = 'todo'
#     db_name: str = 'todo'
#
#     @property
#     def db_url(self):
#         return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
#
#
# class Config:
#         env_prefix = 'todo_'