import os
from mcp.server.fastmcp import FastMCP

def get_env_int(env_var: str, default: int) -> int:
    try:
        return int(os.getenv(env_var, str(default)))
    except (ValueError, TypeError):
        return default

# Configuration
MAX_FILE_SIZE = get_env_int('PYCARET_MCP_MAX_FILE_SIZE', 100 * 1024 * 1024)
LOG_LEVEL = os.getenv('PYCARET_MCP_LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.getenv('PYCARET_MCP_LOG_FILE', 
                     os.path.join(os.path.dirname(__file__), '..', 'logs', 'mcp_server.log'))
LOG_MAX_BYTES = get_env_int('PYCARET_MCP_LOG_MAX_BYTES', 5 * 1024 * 1024)
LOG_BACKUP_COUNT = get_env_int('PYCARET_MCP_LOG_BACKUP_COUNT', 3)

ENABLE_CODE_EXECUTION = True
BLACKLIST = ['os.', 'sys.', 'subprocess.', 'open(', 'exec(', 'eval(', 'import os', 'import sys']

mcp = FastMCP("PyCaret-MCP-Server")