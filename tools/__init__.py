from .weather import get_weather

# Register tools
TOOL_REGISTRY = {
    get_weather.name: get_weather
}

__all__ = ["TOOL_REGISTRY"]
