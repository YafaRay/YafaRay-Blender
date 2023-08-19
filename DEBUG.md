# Debugging Instructions

This document contains information about how to debug the YafaRay-Blender add-on in certain IDEs

## Python Debugging Using Eclipse IDE
🚧 Under construction. 🚧

## Python Debugging Using JetBrains IDEs
The following sections contain instructions to debug with JetBrains PyCharm or IntelliJ-Idea Python Plugin "pydevd-pycharm" Debug Server

> **Note:** The Debug Server might only be available in the Professional PyCharm and IntelliJ versions

### Initial installation:

In PyCharm (or IntelliJ-Idea with a Python plugin installed), add a Run/Debug Configuration "Python Debug Server" with localhost and port 5678.

Follow the installation instructions indicated in the Run/Debug configuration window, for example:

    pip install pydevd-pycharm~=232.8660.185

> **Note:** The version is just shown as an example, but will be different depending on the version of PyCharm/IntelliJ used.

After the installation, the path to the installed Python package will automatically be added to the path when using the system-wide Python version.

However, when running certain Blender versions the embedded Blender Python version might be different. To add the path manually, first find the path to the local user installed Python packages with:

    python3 -m site

In Ubuntu, it might look like the following (for example):

    sys.path = [
        '/home/<user name>',
        '/home/<user name>/.local/lib/python3.10/site-packages',
        '/usr/lib/python310.zip',
        '/usr/lib/python3.10',
        '/usr/lib/python3.10/lib-dynload',
        '/usr/local/lib/python3.10/dist-packages',
        '/usr/lib/python3/dist-packages',
    ]

To ensure older Blender Python versions can find the locally installed packages, in Ubuntu for example run the following before starting Blender from the terminal:

    export PYTHONPATH=$PYTHONPATH:~/.local/lib/python3.10/site-packages

This change is not permanent. To make it permanent path has to be added to the user environment profile files.


### Usage:

In PyCharm or IntelliJ, start the Python Debug Server already configured for localhost and port 5678.

Copy the following code fragment into the portion of the Blender add-on code that needs to be debugged.

    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)

> **Note:** Use this function **only once** in the code or Blender might hang/crash

> **Note:** Python breakpoints might not work.

After that, run Blender. When that portion of code is executed, it will halt Blender execution and show the Debugger in the IDE.


## C/C++ Debugging (Optional)

The Python debugging can optionally be combined with a C/C++ debugger like GDB or debuggers integrated into an IDE such as Eclipse or JetBrains CLion.

When the Python code stops with the code below, in the IDE use "Attach to Process" and select the (stopped) blender process. Then select the necessary breakpoints.

For CLion/Ubuntu you can use first in terminal (as root) the following command to allow attaching:

    echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope

> ⚠️ **WARNING**: making this change **could make your system insecure**, as it would allow any process to trace any other process.
> 
> There might be alternative and more secure solutions. For more information see:
> 
> * https://askubuntu.com/questions/41629/after-upgrade-gdb-wont-attach-to-process/41656#41656
> 
> * https://bbs.archlinux.org/viewtopic.php?id=278831

After that, in CLion use Ctrl+Alt+5 or Run→Attach to Process and select Blender. Then set the breakpoints as desired.

Continue debugging in the Python IDE. When the C/C++ breakpoint is reached the C/C++ debugger should show the debugged code.
