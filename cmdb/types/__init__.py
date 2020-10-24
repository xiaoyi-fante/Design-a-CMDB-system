import ipaddress
import importlib

classes_cache = {}
instance_cache = {}

# "type":"cmdb.types.IP"
def get_class(type:str):
    cls = classes_cache.get(type)
    if cls:
        # print("~~~~")
        return cls

    # m, c = type.rsplit('.', maxsplit=1)
    # print(m, c)
    # mod = importlib.import_module(m)
    # cls = getattr(mod, c)
    
    # if issubclass(cls, BaseType):
    #     classes_cache[type] = cls
    #     return cls
    # raise TypeError('Wrong Type! {} is not sub class of BaseType'.format(type))

def get_instance(type:str, **option):
    # print("zidian", instance_cache)
    key = ",".join("{}={}".format(k,v) for k,v in sorted(option.items()))
    key = "{}|{}".format(type, key)
    print(key)

    obj = instance_cache.get(key)
    if obj:
        # print('---')
        return obj

    obj = get_class(type)(option)
    instance_cache[key] = obj
    return obj

# 那么，只要模块加载了，classes_cache就有了长名称、短名称对应的类对象的映射。
def inject():
    for n,t in globals().items():
        if type(t) == type and issubclass(t, BaseType) and n != 'BaseType':
            print(n,t)
            classes_cache[n] = t
            classes_cache["{}.{}".format(__name__, n)] = t # 长名称
    print(classes_cache)


class BaseType:
    def __init__(self, option):
        print(option)
        self.option = option # dict

    def __getattr__(self, item):
        return self.option.get(item)

    def stringify(self, value):
        # 转换，错误的数据不要给默认值，就抛异常让外部捕获
        raise NotImplementedError()

    def destringify(self, value):
        raise NotImplementedError()


class Int(BaseType):
    def stringify(self, value):
        val = int(value)

        max =self.max
        if max and val > max:
            raise ValueError("Too big")

        min = self.min
        if min and val < min:
            raise ValueError("Too small")

        return str(int(value))

    def destringify(self, value):
        return value

class IP(BaseType):
    def stringify(self, value):
        val = ipaddress.ip_address(value)
        if not val.startswith(self.prefix):
            raise ValueError("Bad prefix")
        return str(ipaddress.ip_address(value))

    def destringify(self, value):
        return value


inject()