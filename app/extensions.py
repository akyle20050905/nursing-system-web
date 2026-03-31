from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flasgger import Swagger


# 給 Flask-SQLAlchemy 使用的 Base
class Base(DeclarativeBase):
    pass


# 全域 db 物件
db = SQLAlchemy(model_class=Base)

# 全域 swagger 物件
swagger = Swagger()