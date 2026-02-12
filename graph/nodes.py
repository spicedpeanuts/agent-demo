import json
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import AgentState
from llms import PostChatModel as llm
from tools import TOOL_REGISTRY

llm = llm()

PROMPT = """
你是一个天气查询助手。

如果用户询问某个城市天气，请调用 get_weather 工具。

如果信息已经足够，请输出：

{
  "thought": "分析过程",
  "action": "finish",
  "action_args": {}
}

如果需要调用工具，请输出：

{
  "thought": "分析过程",
  "action": "get_weather",
  "action_args": {"city": "城市名"}
}

只输出 JSON，不要额外文字。
"""

def extract_json(text: str) -> dict:
    """从模型输出中安全提取 JSON"""
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"No JSON found in LLM output: {text}")
    return json.loads(match.group())


def planner_node(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=PROMPT),
        *state["messages"]
    ]

    resp = llm.invoke(messages)

    try:
        data = extract_json(resp.content)
    except Exception:
        return {
            **state,
            "next_action": "finish",
            "action_args": {},
        }

    action = data.get("action")
    action_args = data.get("action_args", {})

    if not isinstance(action_args, dict):
        action_args = {}

    step = {
        "type": "planner",
        "thought": data.get("thought"),
        "action": action,
        "action_args": action_args,
    }

    return {
        **state,
        "steps": state["steps"] + [step],
        "next_action": action,
        "action_args": action_args,
    }


def tool_node(state: AgentState) -> AgentState:
    action = state["next_action"]
    args = state.get("action_args", {})

    if action not in TOOL_REGISTRY:
        return {
            **state,
            "next_action": "finish",
        }

    tool = TOOL_REGISTRY[action]
    result = tool.invoke(args)

    print(f"[tool] {action}({args}) -> {result}", flush=True)

    step = {
        "type": "tool",
        "tool": action,
        "args": args,
        "result": result,
    }

    return {
        **state,
        "steps": state["steps"] + [step],
        "messages": state["messages"] + [
            HumanMessage(content=f"工具返回结果：{result}")
        ],
        "next_action": None,
        "action_args": None,
    }


