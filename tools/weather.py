from typing import Dict, Optional, Any
from datetime import datetime
import time
import json
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city"""

    # 模拟天气数据
    weather_data = {
        "city": city,
        "temperature": 25,
        "condition": "clear sky",
        "timestamp": int(time.time())
    }
    return json.dumps(weather_data, ensure_ascii=False)
