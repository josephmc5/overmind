# Configuration plugins module

def load_plugins():
    import os
    plugin_list = {}
    for f in os.listdir(os.path.dirname(__file__)):
        if f.endswith('.py') and f != '__init__.py':
            driver_name = f.rstrip('.py')
            _mod = __import__(driver_name, globals(), locals())
            plugin_list[driver_name] = getattr(_mod, "Driver")

    return plugin_list

