import os
from dotenv import load_dotenv  
from deepagents import create_deep_agent, AsyncSubAgent
from langchain_openai import ChatOpenAI
load_dotenv()

model = ChatOpenAI(
    model=os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct"),
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url="https://api.siliconflow.cn/v1",
)

graph = create_deep_agent(
    model=model,
    system_prompt=(
        "You are a supervisor agent for an async-subagent demo. "
        "When the user asks for a long-running research task, you must delegate "
        "to the async subagent named researcher immediately. "
        "After calling start_async_task, return the task_id to the user and stop. "
        "Do not call check_async_task unless the user explicitly asks for progress. "
        "If the user asks to revise the background task, call update_async_task."    
    ),
    subagents=[
        AsyncSubAgent(
            name="researcher",
            description=(
                "Use for any long-running background research or async demo task."
                "This agent intentionally sleeps before returning so the async"
                "behavior is easy to observe."
            ),
            graph_id="researcher",
        )
    ]
)