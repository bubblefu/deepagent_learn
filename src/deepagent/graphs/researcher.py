import asyncio

from langgraph.graph import END, START, MessagesState, StateGraph

async def slow_research(state: MessagesState):
    last_human = state["messages"][-1].content if state["messages"] else "No task provided."
    await asyncio.sleep(8)
    return {
        "message": [
            
        ]
    }
