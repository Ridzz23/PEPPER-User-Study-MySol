from shellspec import get_registry

def convert(shell_command, output):
    parts = shell_command.split()
    command = parts[0]

    flags = set()

    for arg in parts[1:]:
        if arg.startswith("--"):
            flags.add(arg[2:])
        elif arg.startswith("-"):
            flags.add(arg[1:])

    matches = []

    for spec in get_registry():
        if spec["command"] != command:
            continue
        if spec["flags"].issubset(flags):
            matches.append(spec)
    
    if not matches:
        return output
    
    best = max(matches, key=lambda x: len(x["flags"]))

    if best is None:
        return output
        
    
    converted = best["function"](output)

    return converted

