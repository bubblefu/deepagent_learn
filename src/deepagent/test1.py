import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from langchain.agents.middleware import ToolMiddleware

load_dotenv()

model = ChatOpenAI(
    model=os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct"),
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url="https://api.siliconflow.cn/v1",
)

def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气。
    当用户询问某个城市天气的时候，必须调用这个工具。
    Args:
        city: 城市名称，例如：北京、上海
    """
    return f"{city}今天天气晴朗，气温24℃。"


def calculate(expression: str) -> float:
    """
    计算数学表达式的结果。
    当用户询问数学计算问题的时候，必须调用这个工具。
    Args:
        expression: 数学表达式，例如：2+2、sqrt(16)
    """
    try:
        result = eval(expression)
        return float(result)
    except:
        return float("nan")

def convert_currency(amount: float, from_currency: str, to_currency: str = "CNY") -> dict:
    """
    将指定金额从一种货币转换为另一种货币。
    当用户询问货币兑换问题的时候，必须调用这个工具。
    Args:
        amount: 金额，例如：100.0
        from_currency: 原始货币，例如：USD、CNY
        to_currency: 目标货币，例如：EUR、JPY
    """
    # 这里使用一个简单的汇率示例，实际应用中应调用实时汇率API
    exchange_rates = {
        ("USD", "CNY"): 6.5,
        ("CNY", "USD"): 0.15,
        ("EUR", "USD"): 1.1,
        ("USD", "EUR"): 0.9,
    }
    cny = amount * exchange_rates.get((from_currency, "CNY"), 0)
    return {"amount": round(cny / exchange_rates.get((to_currency, "CNY"), 1), 2), "currency": to_currency}

agent = create_deep_agent(
    model=model,
    tools=[ calculate, convert_currency],
    middleware=[ToolMiddleware()],
    system_prompt="""你是一个计算助手，能帮用户做数学运算和货币换算。
                    # You have a get_weather tool to check city weather.
                    # If user asks about weather, CALL get_weather immediately.
                    # This question is NOT file operation, ignore file-related tools
                    """
)

result = agent.invoke(
    {"messages":[{"role":"user", "content":"帮我把 100 美元换算成人民币，再用它乘以 1.08 的通胀系数。"}]}
)

print(result["messages"][-1].content)
# print(result)
