import redis

# 连接redis
conn = redis.Redis(
    host="192.168.1.18", port=6379, password="0125", encoding="utf-8"
)  # host为本机ip
# 设置键值对
# conn.set(
#     "15801367721", 9999, ex=60
# )  # 手机号 验证码 超时时间超时后自动清空此条数据，其中验证码为int 但是写入redis时会转成字符串，并通过encoding 转换成字节
# # 获取值
values = conn.get("15801367721")  # 没有值返回None，有值的话返回字节类型

print(values)
