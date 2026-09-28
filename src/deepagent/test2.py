import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, SummarizationMiddleware
from deepagents import create_deep_agent
from tavily import TavilyClient
load_dotenv()
backend = StateBackend()

model = ChatOpenAI(
    model=os.environ.get("MODEL_NAME", "zai-org/GLM-5.2"),
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url="https://api.siliconflow.cn/v1",
)

# 搜索工具
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(query: str, max_results: int = 5) -> dict:
    """搜索互联网获取最新信息。"""
    return tavily_client.search(query, max_results=max_results)

agent = create_deep_agent(
    model=model,
    tools=[internet_search],
    middleware=[TodoListMiddleware()],
    system_prompt="""
                    你是一位专业的技术研究员。
                    面对复杂研究任务时，你会：
                    1. 先用 write_todos 制定研究计划
                    2. 逐步执行每个步骤，及时更新进度
                    3. 将搜索结果写入文件系统整理
                    4. 最终输出完整的研究报告
                    """,
)

# 发起一个需要规划的复杂任务
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "请调研 Agent 开发领域的三大 Harness 框架（Deep Agents、Claude Agent SDK、Codex SDK），对比它们的核心能力差异，写一份简要分析报告。"
    }]
})

print(result["messages"][-1].content)