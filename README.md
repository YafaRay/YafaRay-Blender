DESCRIPTION
-----------
YafaRay is a free open-source montecarlo raytracing engine released under the LGPL 2.1 license. Raytracing is a rendering technique for generating realistic images by tracing the path of light through a 3D scene. 

Make sure that YafaRay is correctly installed in the appropiate place. See file "INSTALL" for installation details

For more information, see: www.yafaray.org


SOURCE CODE
-----------
YafaRay source code is hosted in GitHub.

* libYafaRay source code is available in: https://github.com/YafaRay/libYafaRay
* YafaRay-Blender exporter source code is available in: https://github.com/YafaRay/YafaRay-Blender


RELEASES
--------
There are two different types of YafaRay Releases:

* Releases for Blender: they include the Blender-Exporter code and the YafaRay Core files, in a package ready to be installed in Blender.
	- Available in https://github.com/YafaRay/YafaRay-Blender/releases

* libYafaRay standalone releases: they are intended to be used by 3rd party software and *not* to be used with Blender. 
	- Available in https://github.com/YafaRay/libYafaRay/releases


BUG REPORTS / FEATURE REQUESTS
------------------------------
Please use the GitHub bug tracking system to report bugs in libYafaRay instead of the YafaRay website bug tracking.

* GitHub bug tracking (preferred):
    - Blender exporter related issues: https://github.com/YafaRay/YafaRay-Blender/issues
    - libYafaRay related issues: https://github.com/YafaRay/libYafaRay/issues

* YafaRay website bug tracking: http://www.yafaray.org/development/bugtracker/yafaray


CURRENT LIMITATIONS
-------------------
* This Blender Exporter only works with Blender v2.7x

* Don't use the Blender from the distro repositories. Download the Blender official 2.79 builds from:
https://download.blender.org/release/Blender2.79

* YafaRay only supports *one* scene in the .blend file. If you have more than one scene, it could cause unexpected results and problems in the new Material Preview Controls.

* YafaRay v3 has only limited support for multiple YafaRay versions and forks installed at the same time

If you have several YafaRay versions together, *make sure* that you enable in Blender *first* the old and *later* the new v3 in that order. If you have problems, disable both, restart Blender and enable them in that order.

Having several versions could cause in some cases:
    - Black renders
    - Random crashes
    - Inability to enable the YafaRay v3 plugin or all kinds of strange problems

If you have any of these problems, remove any other yafaray folders (or derived forks) from the Blender addons folder and try again. This typically solves most of the problems stated above.


Thank you.
