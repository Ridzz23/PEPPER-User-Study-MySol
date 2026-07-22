_registry = []

def shellspec(command, flags=None):
    if flags is None:
        flags=[]


    def decorator(func):
        _registry.append({
            "command": command,
            "flags": set(flags),
            "function": func
        })

        return func
    
    return decorator


def get_registry():
    return _registry