from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from .types import get_instance
from .utils import getlogger

logger = getlogger(__name__, './{}.log'.format(__name__))


Base = declarative_base()
# 逻辑表
class Schema(Base):
    __tablename__ = "schema"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(128), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    fields = relationship('Field')

class Reference:
    def __init__(self, ref:dict):
        self.schema = ref['schema'] # 引用的schema
        self.field = ref['field'] # 引用的field
        self.on_delete = ref.get('on_delete', 'disable') # cascade, set_null, disable
        self.on_update = ref.get('on_update', 'disable') # cascade, disable

class FieldMeta:
    def __init__(self, metastr:str):
        meta = json.loads(metastr)

        if isinstance(meta, str):
            self.instance = get_instance(meta['type'])
        else:
            option = meta['type'].get('option')
            if option:
                self.instance = get_instance(meta['type']['name'], **option)
            else:
                self.instance = get_instance(meta['type']['name'])
        self.unique = meta.get('unique', False)
        self.nullable = meta.get('nullable', True)
        self.default = meta.get('default')
        self.multi = meta.get('multi', False)
        # 引用是一个json对象
        ref = meta.get('reference')
        if ref:
            self.reference = Reference(ref)
        else:
            self.reference = None


class Field(Base):
    __tablename__ = "field"
    __table_args__ = (UniqueConstraint('schema_id', 'name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    meta = Column(Text, nullable=False)
    ref_id = Column(Integer, ForeignKey('field.id'), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    schema = relationship('Schema')
    ref = relationship('Field', userlist=False) # 1对1，被引用的id

    @property # 增加一个属性将meta解析成对象，注意不要使用metadata这个名字
    def meta_data(self):
        return FieldMeta(self.meta)

# 逻辑表的记录表
class Entity(Base):
    __tablename__ = "entity"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String(64), nullable=False, unique=True)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    schema = relationship('Schema')

class Value(Base):
    __tablename__ = "value"
    __table_args__ = (UniqueConstraint('entity_id', 'field_id', name='uq_entity_field'),)

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    entity_id = Column(BigInteger, ForeignKey('entity.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    entity = relationship('Entity')
    field = relationship('Field')

# 引擎
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/cmdb", echo=True)

# 创建表
def create_all():
    Base.metadata.create_all(engine)

# 删除表
def drop_all():
    Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

