try:
    import orjson as json
except (ImportError, ModuleNotFoundError):
    try:
        import simplejson as json
    except (ImportError, ModuleNotFoundError):
        import json
