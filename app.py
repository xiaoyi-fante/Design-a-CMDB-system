import json
from cmdb.types import get_instance

# 模拟字段保存的json字符串
jsonstr = """
{
    "type":"cmdb.types.Int",
    "value":80,
    "option":{
        "max": 100,
        "min": 1
    }
}
"""
# jsonstr = """
# {
#     "type":"cmdb.types.IP",
#     "value":"192.168.0.1",
#     "option":{
#         "prefix": "192.1"
#     }
# }
# """

obj = json.loads(jsonstr)
print(obj)

# 结果为{'type': 'cmdb.types.Int', 'value': 300}

print(get_instance(obj['type'], **obj['option']).stringify(obj['value']))
print(get_instance(obj['type'], **obj['option']).stringify(obj['value']))
print(get_instance(obj['type'], **obj['option']).stringify(obj['value']))


















