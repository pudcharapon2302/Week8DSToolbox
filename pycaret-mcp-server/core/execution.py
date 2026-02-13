import sys
import io
import traceback
import pandas as pd
from contextlib import redirect_stdout, redirect_stderr
from .config import BLACKLIST, ENABLE_CODE_EXECUTION
from .validation import validate_pandas_code

def run_pycaret_code(code: str) -> dict:
    if not ENABLE_CODE_EXECUTION:
        return {"isError": True, "message": "Execution disabled"}
    
    # Lazy Import inside function to prevent stdout noise during server startup
    from pycaret import classification as clf
    from pycaret import regression as reg
    from pycaret import clustering as clust

    local_vars = {
        'pd': pd, 'clf': clf, 'reg': reg, 'clust': clust,
        'pull': clf.pull, 'get_config': clf.get_config
    }
    
    output_capture = io.StringIO()
    try:
        # Redirect all output to avoid MCP disconnect
        with redirect_stdout(output_capture), redirect_stderr(output_capture):
            exec(code, {}, local_vars)
            
            # Auto-pull result if user didn't assign 'result'
            if 'result' not in local_vars:
                try: local_vars['result'] = clf.pull()
                except: pass

        res = local_vars.get('result', None)
        content = res.to_dict() if isinstance(res, (pd.DataFrame, pd.Series)) else str(res)
        
        return {"content": [content], "isError": False, "output": output_capture.getvalue()}
    except Exception as e:
        return {"isError": True, "message": str(e), "traceback": traceback.format_exc(), "output": output_capture.getvalue()}