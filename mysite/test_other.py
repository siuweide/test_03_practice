import re
from app_variable.models import Variable


a = '{"key1": "${key1}","key2": "value2"}'
value = re.findall("\"\${(.+?)}\"", a)[0]
#
print(value)


# print(a.replace(replace_value, value))
#
if "${" in a and "}" in a:
    # 匹配出包含“${” 开头和 “}”结尾的值
    key = re.findall("\"\${(.+?)}\"", a)[0]
    # 去变量的表里查找找到真正的value值
    variable = Variable.objects.get(key=key)
    real_value = variable.value
    # 在通过正则找到要替换的值（已${开头，}结尾的。）
    data_list = re.findall("\"(.+?)\"", a)
    for data in data_list:
        # 将匹配出来的列表，逐一找，包含${ 和 } 的字符串取出来
        if "${" in data and "}" in data:
            replace_value = data
    per_val = a.replace(replace_value, real_value)
    print(per_val)