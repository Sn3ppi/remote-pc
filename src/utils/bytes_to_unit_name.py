def bytes_to_unit_name(memory) -> str:
    '''Переводит байты в читаемую человеком величину.''' 
    unities = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for i in reversed(range(len(unities))):
        if memory >= 1024 ** i:
            return f"{memory/1024**i:.2f} {unities[i]}"