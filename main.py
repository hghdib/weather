import json
from openai import OpenAI

#  设置DeepSeek API Key
client = OpenAI(
    api_key="API",  # ← 替换为你自己的 DeepSeek API Key
    base_url="https://api.deepseek.com"
)

#  增强模拟函数：支持中英文城市名
def get_weather(city: str) -> str:
    city_map = {
        "shenzhen": "shenzhen",
        "深圳": "shenzhen",
        "beijing": "beijing",
        "北京": "beijing"
    }

    city_key = city.lower().strip()
    mapped_key = city_map.get(city_key)

    weather_data = {
        "beijing": {
            "location": "Beijing",
            "temperature": {"current": 32, "low": 26, "high": 35},
            "rain_probability": 10,
            "humidity": 40
        },
        "shenzhen": {
            "location": "Shenzhen",
            "temperature": {"current": 28, "low": 24, "high": 31},
            "rain_probability": 90,
            "humidity": 85
        }
    }

    if mapped_key in weather_data:
        return json.dumps(weather_data[mapped_key], ensure_ascii=False)
    else:
        return json.dumps({"error": "Weather Unavailable"}, ensure_ascii=False)

#  定义工具函数（Function Calling 接口）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，可以是中文（如 深圳）或英文（如 Shenzhen）"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

#  用户请求
messages = [
    {"role": "system", "content": ""},
    {"role": "user", "content": "查找深圳的天气，然后用一句话告诉我出门要不要带伞"}
]

#  第一步：让 DeepSeek 模型决定是否调用函数
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    #  执行 get_weather 函数
    function_result = get_weather(**arguments)

    #  第二步：将结果返回给模型，让它给出建议
    followup_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            messages[0],  # system
            messages[1],  # user
            message,      # 模型调用工具
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_result
            }
        ]
    )

    print("出门建议：", followup_response.choices[0].message.content)
else:
    print("模型没有调用函数")
