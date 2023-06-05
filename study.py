from pydantic import BaseModel, ValidationError
from datetime import datetime, date
from typing import List, Optional  # 用于选填字段
from pathlib import Path


class User(BaseModel):
    id: int  # 没有默认值就是必填字段
    name: str = 'Abraham'  # 有默认值就是选填字段
    time_time: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型“1”“啊"


data_demo = {
    'id': "123",
    'time_time': '2023-06-05 21:28',
    'friends': [1, 2, 3, 4, "5"]
}

user = User(**data_demo)  # `**`是python字典拆包的方法
print(user.name, user.friends, user.time_time, user.id, sep='\n')

# 将实例用字典的形式输出
print('*' * 150, 'dict')
print(user.dict())

# 将实例用json形式输出
print('*' * 150, 'json')
print(user.json())

# ValidationError异常类的使用
try:
    User(id=1, time_time=datetime.today(), friends=[1, '2', 'haha'])

except ValidationError as v:
    print('*' * 150, '将错误信息json格式化')
    print(v.json())  # 将错误信息json格式化

print('*' * 80, '这里是浅拷贝', '*' * 80)
print(user.copy())

print('*' * 80, '这里是用parse_obj根据我自己声明的字段定义的数据类型进行纠错，解析这个字典的数据', '*' * 80)
print(User.parse_obj(obj=data_demo))

print('*' * 80, '这里是用parse_obj解析原生json的数据，进行纠错', '*' * 80)
print(User.parse_raw('{"id": 123, "name": "Abraham", "time_time": "2023-06-05T21:28:00", "friends": [1, 2, 3, 4, 5]}'))

print('*' * 80, '解析文件，进行纠错', '*' * 80)
path = Path('test.json')
path.write_text(
    '{"id": 123, "name": "Abraham", "time_time": "2023-06-05T21:28:00", "friends": [1, 2, 3, 4, 5]}')  # 向这个文件中写入内容
print(User.parse_file(path))

# 将实例用schema形式输出，和上面的dict()等不同是 会告诉你数据对象的格式是什么
print(user.schema())
print(user.schema_json())

# 不检验数据直接创建模型类，不建议在construct方法中传入未经验证的数据
print(User.construct(**data_demo))

# 查看创建的类的对象的数据的顺序
print('*' * 80, '查看创建的类的对象的数据的顺序', '*' * 80)
print(User.__fields__.keys())

print('*' * 80, '递归模型，在一个模型中调用另一个模型，定义数据的格式or规范', '*' * 80)


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound_type: List[Sound]


dogs = Dog(birthday=date.today(), weight=5.55, sound_type=[{'sound': 'wang1'}, {'sound': 'wang2'}])
print(dogs.dict())

print('*' * 80, 'ORM模型：从类实例创建符合ORM对象的模型', '*' * 80)

