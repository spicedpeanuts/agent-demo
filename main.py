from graph.main_graph import app
from langchain_core.messages import HumanMessage

result = app.invoke({
    "messages": [HumanMessage(content="北京今天天气怎么样？")],
    "steps": [],
    "next_action": None,
    "action_args": None,
})

print(result)
