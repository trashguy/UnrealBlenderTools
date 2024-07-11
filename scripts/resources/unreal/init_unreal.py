import os
import sys
import unreal
from pathlib import Path

debug = os.environ.get('UNREAL_DEBUGGING_ON', 'no').lower() == 'yes'

if debug:
    try:
        import debugpy
        platform_folder = 'Linux'
        if sys.platform == 'win32':
            platform_folder = 'Win64'

        port = int(os.environ.get('UNREAL_DEBUG_PORT', 5679))
        python_exe_path = Path(sys.executable).parent.parent / 'ThirdParty' / 'Python3' / platform_folder / 'python'
        debugpy.configure(python=os.environ.get('UNREAL_PYTHON_EXE', str(python_exe_path)))
        debugpy.listen(port)
        unreal.log(f'Waiting for debugger to attach on port {port}...') # type: ignore
        debugpy.wait_for_client()
    except ImportError:
        unreal.log_error( # type: ignore
            'Failed to initialize debugger because debugpy is not available '
            'in the current python environment.'
        )