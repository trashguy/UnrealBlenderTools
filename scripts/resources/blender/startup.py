import os
import sys
import bpy
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

debug = os.environ.get('BLENDER_DEBUGGING_ON', 'no').lower() == 'yes'

ADDONS = {
    'send2ue': Path(__file__).parent.parent.parent.parent / 'src',
    'ue2rigify': Path(__file__).parent.parent.parent.parent / 'src'
}


if bpy.app.version[0] > 2: # type: ignore
    current_script_directories = [
        Path(i.directory)
        for i in bpy.context.preferences.filepaths.script_directories.values()
    ]


    for name, scripts_folder in ADDONS.items():
        if scripts_folder not in current_script_directories:
            script_directory = bpy.context.preferences.filepaths.script_directories.new()
            script_directory.name = name # type: ignore
            script_directory.directory = str(scripts_folder) # type: ignore

    try:
        bpy.ops.script.reload()
    except ValueError:
        pass


for addon in ADDONS.keys():
    try:
        bpy.ops.preferences.addon_enable(module=addon)
    except Exception as e:
        logger.warning(f'Failed to enable addon {addon}: {e}')

if debug:
    try:
        import debugpy
        port = int(os.environ.get('BLENDER_DEBUG_PORT', 5678))
        debugpy.configure(python=os.environ.get('BLENDER_PYTHON_EXE', sys.executable))
        debugpy.listen(port)
        logger.info(f'Waiting for debugger to attach on port {port}...')
        debugpy.wait_for_client()
    except ImportError:
        logger.error(
            'Failed to initialize debugger because debugpy is not available '
            'in the current python environment.'
        )