#
# Configuration management
#
from os import uname


#
# Returns system name and system's slash
#
def get_system_params() -> list:
    try:
        return [uname()[0], "/"]
    except AttributeError:
        return ["nt", "\\"]


SYS_NAME, SYS_SLASH = get_system_params()
