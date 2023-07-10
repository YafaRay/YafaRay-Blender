# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Use this function *ONLY ONCE* or Blender might hang
#
# Select in the variable "pydev_source_dir" below the path to the folder containing "pydevd.py". Do not install a "generic" pydevd nor pycharm-pydevd using pip, use the folder that comes with the IDE (either Eclipse + PyDev plugin, PyCharm Pro or IntelliJ IDEA Ultimate for example)
#
# Start the PyDev server (either the Eclipse + PyDev plugin server which has hardcoded port 5678 or Python Debug Server with localhost and port 5678 in PyCharm or Intellij IDEA
# DO NOT IMPORT THIS FILE, just COPY THE CODE FRAGMENT BELOW to the part of the code that should stop/break into the IDE debugger
#
# This can optionally be combined with a C/C++ debugger like GDB or debuggers integrated into an IDE such as Eclipse or CLion
# When the Python code stops with the code below, in the IDE use "Attach to Process" and select the (stopped) blender process. Then select the necessary breakpoints
# (note: for CLion/Ubuntu use first in terminal "echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope" to allow attaching and then in CLion use Ctrl+Alt+5 or Run->Attach To Process and select blender. Then set the breakpoints as desired
# Continue debugging in the Python IDE. When the C/C++ breakpoint is reached the C/C++ debugger should show the debugged code

# pydev_source_dir = str(pathlib.Path.home()) + "/snap/eclipse/67/amd64/plugins/org.python.pydev.core_10.2.1.202307021217/pysrc"
pydev_source_dir = "/opt/JetBrains/ToolBox/apps/IDEA-U/ch-0/231.9161.38.plugins/python/helpers/pydev"
import sys
if pydev_source_dir not in sys.path:
    sys.path.append(pydev_source_dir)
import pydevd
pydevd.settrace('localhost')  # Using port 5678
