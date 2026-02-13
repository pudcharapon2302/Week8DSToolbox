import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from core.config import mcp, LOG_FILE, LOG_LEVEL, LOG_MAX_BYTES, LOG_BACKUP_COUNT
from core.metadata import read_metadata
from core.execution import run_pycaret_code

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    
    # CRITICAL: StreamHandler must go to sys.stderr to avoid breaking MCP JSON communication
    logging.basicConfig(level=getattr(logging, LOG_LEVEL), 
                        handlers=[file_handler, logging.StreamHandler(sys.stderr)])

@mcp.tool()
def read_metadata_tool(file_path: str) -> dict:
    """Read file structure and basic stats."""
    return read_metadata(file_path)

@mcp.tool()
def run_pycaret_tool(code: str) -> dict:
    """Execute PyCaret/Pandas code safely."""
    return run_pycaret_code(code)

if __name__ == "__main__":
    setup_logging()
    mcp.run()