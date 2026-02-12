# agent-demo
building a demo agent with langgraph/langchain


## File Tree

```text
project_root/
│
├── main.py                     # 入口文件（启动 graph）
├── requirements.txt
│
├── graph/                      # Agent 执行流相关
│   ├── __init__.py
│   ├── state.py                # 定义 AgentState
│   ├── nodes.py                # planner_node / tool_node 等
│   └── graph.py                # 构建StateGraph
│
├── tools/                      # 所有工具相关
│   ├── __init__.py
│   └── tools.py                # 具体工具实现（天气、查询等）
│
├── llm/                        # 自定义模型封装
    ├── __init__.py
    └── custom_model.py         # 自定义模型

```
