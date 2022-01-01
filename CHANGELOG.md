YafaRay + Blender Exporter for Blender ChangeLog
================================================
Important: read the README file for installation instructions and important information about YafaRay

This is an abbreviated list of changes. The full/detailed list of changes can be seen at:
* libYafaRay code: https://github.com/YafaRay/libYafaRay
* Blender Exporter: https://github.com/YafaRay/YafaRay-Blender


(2020-07-18) VERY IMPORTANT! CHANGED GITHUB REPOSITORIES!!
----------------------------------------------------------
In order to have proper official GitHub YafaRay repositories that do not show as "forked" from other projects, we have created new GitHub repositories.

Those new GitHub repositories are copies of the previous ones, and preserve all the history, commits, and contributors information. They also preserve the versions tags, although not the binaries for previous versions.

The old repositories will not be deleted, but marked as "Archived" in Github, meaning that they will no longer be updated there. The binaries of releases v3.5.1 or older will be preserved in those archived repos.

Distro maintainers and any other users who were linking/forking the original repos should switch to the new ones.

We hope this change helps further development, sorry for the inconveniences!



YafaRay v3.5.1 (2020-07-13) for Blender 2.79:
---------------------------------------------
* MacOS: found/fixed root cause of Blender python segfault 11 and ruby SketchUp Make 2017 "incompatible version" problems  `[Core]`
* MacOS: fixed Qt5 menus. Toolbar not fixed yet, hiding it for now.  `[Core]`
* XML parser: fix build broken when XMLImport and XML Loader are disabled (and no dependencies on LibXML2/ZLib)  `[Core]`
* Build info: made it less verbose (it was getting too long in some platforms) and added dash between platform and compiler when there is a platform (like MinGW)  `[Core]`
* Logging: fixed HTML log display of jpg and png images  `[Core]`
* Ruby Qt bindings: change name to avoid collisions in linux python "import yafqt" between yafqt.py and yafqt.so  `[Core]`


YafaRay v3.5.0 (2020-07-10) for Blender 2.79:
---------------------------------------------
* IMPORTANT: Removal of *all* Boost dependencies. I've implemented new Unicode File management and new ImageFilm/PhotonMap saving/loading system.  `[Core]`
   - All functionality depending on Boost has been rewritten from scratch to be able to remove Boost altogether.  `[Core]`
   - Implemented Unicode UTF8/UTF16 conversions for strings in POSIX and Windows systems  `[Core]`
   - Implemented Unicode UTF8/UTF16 file handling classes for Unicode paths in POSIX and Windows systems  `[Core]`
   - In the process of that implementation I fixed some issues that were pending for a long time:
        - Now almost all files (including logs) are handled with the new file_t interface, so all works when using Unicode paths (logs were not correctly saved sometimes in Windows)  `[Core]`
        - No longer need for temporary files when using OpenEXR files with Unicode paths.  `[Core]`
   - Implemented new system to save / load ImageFilm and Photon Maps. The files generated with previous versions of YafaRay are *no longer valid* for this new method.  `[Core]`
        - I think the new system is faster and generates smaller files (still big, depending on the amount of info)  `[Core]`
        - Only drawback for now, when loading photon maps it has to regenerate the photon search KD tree, which is no longer saved in the photon map file.  `[Core]`
        - No longer need to have a separate binary/text format for portability. In principle it should work the same in Linux/Windows, etc.   `[Blender Exporter + Core]`
        - Endianness could be an issue for non-Intel/AMD platforms like ARM, to be investigated in the future, but that's a problem for another day.  `[Core]`
   - Removed all SysInfo Boost code and replaced it by a "CMake-building" generation. Renamed sysinfo classes as build_info.  `[Core]`
        
* IMPORTANT: CMake: made LibXML2 / ZLib optional. New CMake flag "WITH_XMLImport" to enable LibXML2. Now all the dependencies are finally optional and pure YafaRay library can be built without any dependencies.  `[Core]`
* IMPORTANT: general header files de-coupling and cleanup, some old unused and broken code deleted  `[Core]`
* Changing documentation extension to Markdown *.md  `[Blender Exporter + Core]`
* Bidirectional integrator: adding integrator information to log and badge  `[Core]`
* Bidirectional integrator: fixed transparent shadows, as requested in https://github.com/YafaRay/Blender-Exporter/issues/38  `[Core]`
* SPPM: fixed memory corruption when using startx, starty not zero, as requested in https://github.com/YafaRay/Blender-Exporter/issues/41 and https://github.com/YafaRay/Blender-Exporter/issues/40  `[Core]`
* XML Parser: added XML SAX parsing error diagnostic messages, as requested in https://github.com/YafaRay/Core/issues/121  `[Core]`
* Added back -pthread flag for gcc/g++ compilation to fix FreeBSD builds To fix FreeBSD build as requested in https://github.com/YafaRay/Core/issues/113  `[Core]`
* Removed some warnings for GCC. Also removed some Clang warnings as requested by https://github.com/YafaRay/Core/issues/110  `[Core]`
* Fixed some source file comments license boilerplate to remove wrongly encoded characters that were confusing some IDEs  `[Core]`
* CMake: unifying all cmake-generated headers, simplifying code. Threads: moved runtime detection to dedicated class  `[Core]`
* OpenCV Denoise: better encapsulation and code reuse, at the expense of slower processing  `[Core]`
* Renamed yafsystem/sharedlibrary_t by a (clearer) dynamic_library/dynamicLoadedLibrary_t  `[Core]`
* Git: added .gitignore to ignore all "hidden" files starting with "." (i.e. IDE generated files)  `[Core]`
* Swig Ruby: avoid -Wsign-compare warning.  `[Core]`



YafaRay v3.4.4 (2020-05-09) for Blender 2.79:
---------------------------------------------
* Angular camera: modified to add several types of angular projections and to fix new ortographic calculations.  `[Blender Exporter + Core]`


YafaRay v3.4.3 (2020-05-09) for Blender 2.79:
---------------------------------------------
* Angular camera: added "Ortographic" projection.  `[Blender Exporter + Core]`


YafaRay v3.4.2 (2020-05-04) for Blender 2.79:
---------------------------------------------
* Added Equirectangular camera.  `[Blender Exporter + Core]`


YafaRay v3.4.1a (2020-04-09) for Blender 2.79:
---------------------------------------------
* A few documentation changes to clarify bug reporting and Blender v2.79 release download `[Blender Exporter]`


YafaRay v3.4.1 (2020-04-08) for Blender 2.79:
---------------------------------------------
* Changed documentation to state that any bug reporting and resolution will solely be done in the GitHub Project "Issues" tab. Bugs in the old yafaray.org bugtracker will not be processed anymore. `[Blender Exporter + Core]`
* Added note about Blender-Exporter only working for Blender v2.7x versions. `[Blender Exporter + Core]`


YafaRay v3.4.0 (2020-03-22) for Blender 2.79:
---------------------------------------------
Note: don't mind the release date, the project has been mostly inactive for a long time, so only a few (although significant) changes since v3.3.0, but it was about time to give the last changes a proper release version number.

Feature changes/additions:
--------------------------
* Basic support for Image Sequences. `[Blender Exporter]`
* New per-material transparency bias for Shiny Diffuse. When there are objects with many transparent surfaces stacked close together (such as leaves in a tree) sometimes black artifacts appear if the ray reaches the maximum depth. This can be solved by increasing the maximum ray depth, but the render times increase. I've added two new parameters for the Shiny Diffuse material to try to achieve a "trick", which is not realistic and may cause other artifacts but that should prevent the black areas without having to increase the maximum ray depth so much. `[Blender Exporter + Core]`

Dependencies changes:
---------------------
* IMPORTANT: Migration from Qt4 to Qt5 as Qt4 reached End of Life  `[Core]`
* Dependency on meganz/mingw-std-threads made optional, because it's needed for old MinGW compilers but it causes conflicts with new MinGW compilers, so better to have it as an option in CMake (disabled by default)  `[Core]`
* Compatibility fix for Python 3.8  `[Core]`

Bug fixes:
----------
* VERY IMPORTANT: Fixed the infamous bug "DAG zero... not allowed to happen!" that caused all objects in Blender to be deleted. I want to thank the user "pouar" for finding the problem and the solution for this! :-) More information: http://www.yafaray.org/node/819#comment-1921  `[Blender Exporter]`
* Fixed Multiview rendering, that had been broken due to a Blender 2.79 API change  `[Blender Exporter]`
* Mesh management: changes to make it compatible again with Blender versions prior to 2.78  `[Blender Exporter]`
* RenderPasses rendering: changes to make it compatible again with Blender versions prior to 2.74.4  `[Blender Exporter]`
* Minor fix for a warning "rna_uiItemR: property not found: Camera.show_title_safe" that happened sometimes.  `[Blender Exporter]`
* Fix - Min bounces, Russian Roulette minimum bounces jump in. Now saved into render settings.  `[Blender Exporter]`


YafaRay v3.3.0 (2017-08-22) for Blender 2.79:
---------------------------------------------

Feature changes/additions:
--------------------------
* "Flat Material" option added to Shiny Diffuse, requested by a certain user. Flat Material is a special non-photorealistic material that does not multiply the surface color by the cosine of the angle with the light, as happens in real life. Also, if receive_shadows is disabled, this flat material does no longer self-shadow. For special applications only. `[Blender Exporter + Core]`

Bug fixes:
----------
* Bidirectional: fixed transparent background not working, was causing the entire render to have transparent alpha. See: http://www.yafaray.org/community/forum/viewtopic.php?f=15&t=5236  `[Core]`
* Bidirectional: fixes (horrible hacks in fact, but...) for unitialized values causing incorrect illumination in scenes  `[Core]`
* SPPM: fixed SPPM AA panel where the AA filter type and pixel width were incorrectly disabled  `[Blender Exporter]`
* Fixed hang in Windows 7 when YafaRay is built using Visual Studio 2013.  `[Core]`
* Some building fixes  `[Core]`


YafaRay v3.2.0 (2017-03-21) for Blender 2.78c:
----------------------------------------------

Feature changes/additions in v3.2.0:
------------------------------------
* IMPORTANT: Support for Texture Mipmaps / Ray Differentials, see: http://yafaray.org/node/695 `[Blender Exporter + Core]`
    - Modifier all ImageHandlers to standardise access and make them more flexible. BIG changes to ImageHandlers.
    - Added new Grayscale internal buffers (optional)
    - Reorganized all Interpolation and GetColor code
    - Added MipMap capability to ImageHandlers
    - Added Trilinear MipMap interpolation based on Ray Differentials.
    - Added EWA MipMap interpolation based on Ray Differentials
    - Heavily modified IBL blur function, to use mipmaps with manually calculated mipmap level instead of the previous dedicated "IBL blur" process

* Path Tracing integrator: added new Russian Roulette parameter to speed up path tracing, see: http://www.yafaray.org/node/775 `[Blender Exporter + Core]`
    The relevant parameter will be "russian_roulette_min_bounces".
    - If this parameter is set to 0, russian roulette will be enabled.
    - If set to the same value specified in depth (max bounces), russian roulette will be disabled
    - If set to a value between 0 and max bounces, then russian roulette will only start be applied after this number of bounces, so we can get decent sampling in dark areas for example and get a good speedup with less noise.
    - Lower values of this parameter will result in faster (but somewhat noisier) renders.

* yafaray-xml: better autodetection of plugins path, but in some cases "-pp" may still be needed `[Core]`

* Building system: many changes to make the building process easier and more integrated with Git `[Blender Exporter + Core]`

* Building system: standalone builds generated again `[Core]`

* Building system: added building instructions and test scenes `[Blender Exporter + Core]`

* QT4 support reintroduced and updated for YafaRay v3, but still in a basic state, many features not available yet for the Qt interface `[Blender Exporter + Core]`

* Re-added ability to generate Sketchup plugins again  `[Core]`

* Texture mapping: allow MirrorX,MirrorY even when Repeat = 1 `[Blender Exporter + Core]`


Bug fixes in v3.2.0:
--------------------
* IMPORTANT: Path/Photon OneDirectLight - attempt to sample lights more uniformly, see: http://www.yafaray.org/node/803  `[Core]`
This has been a significant bug, that went unnoticed for a very long time and was causing severe artifacts in Photon Mapping and Path Tracing when lights were not uniformly lighting the scene. Now with this fix, renders should be much more correct and hopefully more realistic!

* IMPORTANT: all integrators, SPPM and path roulette: Fixing non-randomness repetitive patterns, see: http://www.yafaray.org/node/792 `[Core]`
Another important bug that went unnoticed for a very long time. A lack of randomness caused severe patterns in BiDirectional integrator and probably some artifacts (in less extent) in the others. We hope this change helps to achieve more correct and realistic results now.

* IMPORTANT: big changes to textures interpolation and colorspace processing, see: http://yafaray.org/node/787 `[Core]`
    - I found out that YafaRay was doing the texture interpolation *after* decoding the texels color space. This was causing significant differences in color between standard bilinear/bicubic and when using trilinear or EWA mipmaps.

    - The Core code has been modified so from v3.2.0 onwards all internal image buffers will be converted to "linear RGB" during the texture loading process. That will allow a correct color interpolation process, and probably slightly faster than before. Hopefully this should improve color fidelity respect to the original texture images used for the scene.

    - Also, all textures will be "optimized" by default. I think it's clear by now that optimized textures greatly improve memory usage and apparently don't cause slowdowns (might even make it slightly faster due to reduced RAM access?). To accomodate the extra color information necessary to store "linear RGB" values in the optimized buffers, their size will be around 20-25% bigger respect to v3.1.1, therefore a RAM usage increase will happen now compared with previous versions.

    - For optimal results, from now on the user will be responsible for selecting correct ColorSpaces for all textures, including bump map, normal map, etc. For example for Non-RGB / Stencil / Bump / Normal maps, etc, textures are typically already linear and the user should select "linearRGB" in the texture properties, but if the user (by mistake) keeps the default sRGB for them, YafaRay will (incorrectly) apply the sRGB->LinearRGB conversion causing the values to be incorrect. However, I've added a "fail safe" so for any "float" textures, bump maps, normal maps, etc, when getting colors after interpolatio YafaRay will to a "inverse" color conversion to the original Color Space. This way, even a mistake in user's color space selection in bump maps, normal maps, etc, will not cause any significant problems in the image as they will be converted back to their original color space. However, in this case rendering will be slower and potential artifacts can appear due to interpolation taking place in the wrong color space. For optimal results, the user must select correctly the color space for all textures.
    
* Bidirectional integrator changes  `[Blender Exporter + Core]`
    - Will be supported again, although will be considered "unstable" until the (many) issues it has are completely fixed.
    - Fixed issue with excessive brightness that happened after render finished.

* Fix for SPPM sudden brightness change when reaching approx 4,300 million photons. See: http://www.yafaray.org/node/772 `[Core]`

* Fixed bug that caused many extra render passes to be generated in some cases `[Core]`

* Fixed crash when using Blender Exporter and Core with Ruby bindings support enabled `[Blender Exporter + Core]`

* Image Texture Interpolation fixes, see: http://www.yafaray.org/node/783 `[Core]`

* Angular camera: fixed wrong renders due to incorrect default clipping, see: http://yafaray.org/node/779 `[Core]`

* Fixed EXR MultiLayer image file saving `[Core]`

* Fixed uninitialized values generated by Ambient Occlusion sampling `[Core]`

* AA user interface: fixed disabled filter type and pixel width when passes=1 `[Blender Exporter]`

* Show the Physics tab in Blender, see: http://yafaray.org/node/797 `[Blender Exporter]`

* Several other fixes and improvements, especially for the building system and tools for developers.



YafaRay v3.1.1-beta (2016-09-25) for Blender 2.78:
-------------------------------------------------- 

Bug fixes in v3.1.1:
--------------------
* IMPORTANT: Fixed Volumetrics regression bug introduced in v3.1.0 (artifacts in the images and crashes). This time it should work fine while also solving the original Volumetric bug that v3.1.0 tried to fix. `[Core]`

* Fixed incorrect Glass IOR presets retrieval in Blender Exporter. `[Blender Exporter]`



YafaRay v3.1.0-beta (2016-09-20) for Blender 2.78:
-------------------------------------------------- 

Feature changes/additions in v3.1.0:
------------------------------------
* New per-material Sampling Factor. New parameter to resample background or not. `[Blender Exporter + Core]`
These new parameters will *not* work in the first pass, only in the second and subsequent AA passes.

    * Option to resample background, as requested at http://www.yafaray.org/node/214. Works in all integrators except SPPM
    * Option to specify a per-material sampling factor to do additional sampling in certain materials, as requested at http://www.yafaray.org/node/746. Works in all integrators except SPPM

* New WireFrame material properties as well as a WireFrame render pass, as requested in: http://yafaray.org/node/198 `[Blender Exporter + Core]`

  Now, all materials (including Blend material) will have a new Wireframe shading panel. The wireframe can be used in two different ways, depending on whether we want it to be part of the final rendered image or if we want it in a separate Render Pass:
       * Embedded in the Render itself: set a wireframe amount (and optionally map the wireframe amount to a texture). Set the other wireframe options such as color, thickness and softness, and render the scene.
       * Separate Render Pass: make sure the Wireframe amount in the materials is set to 0.0 so the Wireframe does not appear in the Combined Render. Set the rest of the material wireframe options (color, thickness, etc). Enable Render Passes and select Debug-Wireframe pass in one of the passes (preferrably one of the RGBA render passes such as Vector or Color)
      
      Important comments:
       * When using WireFrame, the material may not be fully energy conserving. However, I suppose this is not a problem as the wireframe render is not a photorealistic render in the first place.
       * All Quads and Polygons will be always seen as Triangles (with the crossed line). This is, unfortunately, somthing I cannot solve. YafaRay is currently based on triangle meshes and all Quads and Polygons are first converted to triangle meshes in the Blender Exporter, before entering YafaRay. So, in the Wireframe you will always see triangles, never quads, etc.
       * In the Blend material, the Wireframe shading cannot be mapped to a texture

* New Render Passes: Basic Toon effect, Object Edges and Faces Edges. See: http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5181 `[Blender Exporter + Core]`
      "Wireframe" material options and render pass will be calculated at "material" integration level. It should be more finely detailed but will only show triangles (quads will show the "crossing" line).

      "Faces edges" will be a render pass calculated at Film level showing the edge contours. In this case, quads will be shown more correctly. However, to calculate the faces edges with the current architecture I had to use indirect methods that are way less precise, so some artifacts and missing or incomplete edges are to be expected, including aliasing in the edges. I've added some parameters that can be accessed in the Render Passes tab for users to fine tune the edges generation as much as possible.

      "Object edges" will be the same, but only rendering object edges and contour, more useful for toon-like renders, for example. Limitations are the same as with the Faces Edges.

      "Toon" render pass: as I already got the above working, I thought it could be nice to work a bit more and get a full "toon-like" Render Pass. This render pass will take the original image, apply some smoothing and color quantization to make the image more "cartoon-like" and add the Object Edge. The users will be able to choose the edge color, adjust a bit the thickness and smoothing/quantization. This will be only a *very basic* toon render pass, don't expect a perfect contouring, etc!! I didn't even try making an animation yet, I suppose there will some edges changing from one frame to the next, not sure if it will be distracting or not...


* Render Badge: ability to select Font ttf file and a font size factor. This will allow better presen
tation and to select fonts with better Unicode support on demand. `[Blender Exporter + Core]`

New Automatic "absolute/numeric" Object/Material Index render passes, as requested in http://www.yafaray.org/node/745 `[Blender Exporter + Core]`


Bug fixes in v3.1.0:
--------------------
* IMPORTANT: The v3.1.0 Linux builds that can be downloaded in yafaray.org should now be free from the issues "file too short" that happened in the v3.0.2 builds, as described in http://www.yafaray.org/node/759

* IMPORTANT: Fixed (hopefully) the memory allocation bug in Blend materials described at http://www.yafaray.org/
node/763 that caused either crashes or incorrect render results. `[Core]`

* Glass material: more realistic, corrected total reflection including the reflection color/texture. In some scenes this could change the results of Glass rendering!  See http://www.yafaray.org/node/770 `[Core]`

* Volumes: fixed issue with white/black areas (negative values, etc) in certain circumstances. See: http://www.yafaray.org/node/766 `[Core]`

* Object/Material Absolute Index passes: avoid antialiasing in the edges. `[Core]`
    As requested in http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5180
    Any "Intermediate" values will be "rounded up" (ceiled). This is one of the many possible criteria to do this, but it gives similar results to Blender Internal, so I will use it.

* Image output denoise: denoise parameters added to the XMLinterface, they didn't work in the XML interface in v3.0.2 `[Core]`

* Fixed colorA_t class initialization inconsistencies. We need to keep an eye on this, could cause changes in the Alpha in some scenes (hopefully not) `[Core]`

* Fix problems when rendering a scene that was not yet saved to a .blend file. Now, if the scene has not yet been saved, the secondary output, preset and logs will be saved to a temporary subfolder in the system temporary directory `[Blender Exporter]`

* Removed additional ray depth from Blend material UI. This setting is not used at all in the Blend material, because Core just calculates the maximum additional ray depth between the component materials automatically. So, I'm removing this to avoid confusing users. `[Blender Exporter]`



YafaRay v3.0.2-beta (2016-07-22) for Blender 2.77a:
---------------------------------------------------
** IMPORTANT **
---------------------------------------------------
The new YafaRay-v3 will *NOT* replace the existing YafaRay versions, and it can be installed *in addition* to them.
So, YafaRay-v3 *must* be enabled in Blender user preferences, and in your current YafaRay scenes you have to switch to the renderer "YafaRay-v3" to use the new version.

If you have several YafaRay versions together, *make sure* that you enable in Blender *first* the old and *later* the new v3 in that order. If you have problems, disable both, restart Blender and enable them in that order.

YafaRay v3 has only limited support for multiple YafaRay versions and forks installed at the same time. Having several versions could cause in some cases:
* Black renders
* Random crashes
* Inability to enable the YafaRay v3 plugin or all kinds of strange problems

If you have any of these problems, remove any other yafaray folders (or derived forks) from the Blender addons folder and try again. This typically solves most of the problems stated above.

In v3, support has been DROPPED for Windows XP and MacOSX v10.6

* Important note *: Now by default YafaRay will save the images at the same time as rendering into Blender ("Secondary File Output"). This can be disabled.

Also, YafaRay, by default, ** will change the output folder/file name ** so the images are exported to a subfolder with the same name as the .blend file with suffix _render. This is for convenience and can be disabled, but if you leave the default it could cause you confusion especially when switching to other renderers.
---------------------------------------------------

Changes from v3.0.1-beta to v3.0.2-beta:
----------------------------------------
* ImageFilm load, fix failing load when compiling with GCC v4.8.4. `[Core]`

Changes from v3.0.0-beta to v3.0.1-beta:
----------------------------------------
* Important: Background IBL light sampling fix. This solves a long standing problem with incorrect background lighting accuracy and fireflies. (http://yafaray.org/node/752, http://yafaray.org/node/727, http://yafaray.org/node/566). `[Core]`

* IBL clamp sampling parameter no longer needed thanks to the fix above, so it has been removed from the exporter. `[Blender Exporter]`

* Fix for crash when using yafaray-xml without specifying the type of badge to be used. `[Core]`

* yafaray-xml: new "-ccd" "console-colors-disabled". If specified, disables the Console colors ANSI codes, useful for some 3rd party software that cannot handle ANSI codes well. `[Core]`

* Light photon control: changed back control param names from "shoot_" to "with_" as originally for better backwards compatibility with 3rd party exporters. `[Blender Exporter + Core]`

* Render Passes: added "generic" external render passes for other Exporters and plugins other than Blender Exporter. `[Core]`

* Render passes: added new debug passes for diagnosing light estimation problems. `[Blender Exporter + Core]`



Major codebase changes in v3.0.0:
---------------------------------
* Dropped support for Windows XP and MacOSX v10.6. Sorry, but the code changes required this. `[Blender Exporter + Core]`

* Updated for Blender 2.77a (using Python 3.5). `[Core]`

* Codebase updated from old standard C++98 to the new C++11. This will allow better and easier code maintenance as well as access to newer C++ features to improve YafaRay even more in the future. `[Core]`

* Entire old MultiThreading system replaced by new standard C++11 threads system. `[Core]`

* Windows-MinGW C++11 MultiThreading system using now the library https://github.com/meganz/mingw-std-threads  This should significantly improve render speed in Windows in many scenes by reducing the multithreading overhead. `[Core]`

* Added several Boost libraries to allow saving/loading photon map files and improve unicode/multiplatform compatibility. `[Core]`

* Changes to allow compilation in Visual Studio 2013 (although YafaRay is slower when compiled with VS2013 for some reason). `[Core]`


Feature changes/additions in v3.0.0:
------------------------------------
* Multithreaded Photon Map generation, including multithreaded Photon KDTree building. `[Blender Exporter + Core]`
This should greatly improve render speeds when using Direct Light+caustic map, Photon Map, SPPM or Path Tracing+photon. 

* Ability to Save/Load/Reuse photon maps. `[Blender Exporter + Core]`
This should greatly improve render speeds in scenes where only camera moves. See: http://yafaray.org/node/460. WARNING: When loading/reusing Photon Map files, the User is responsible to ensure they match the scene. If the User loads inadequate photon maps, the render results could be totally wrong or even have crashes. USE WITH CARE.

* Ability to AutoSave image files. `[Blender Exporter + Core]`
Either at the end of each pass or using a user-configurable time interval. This should help if there is a crash or sudden power off, as some images could be obtained from before the incident.

* Ability to AutoSave/Load the main ImageFilm. `[Blender Exporter + Core]`
This might help to CONTINUE interrupted renders or to add additional samples to a render that has already finished. WARNING: When loading ImageFilm files, the User is responsible to ensure they match the scene. If the ImageFilm does not match the scene and render passes exactly, the render results could be totally wrong or even have crashes. USE WITH CARE.

* Ability to perform Multi-Computer distributed render. `[Blender Exporter + Core]`
Each computer should have a different Node number [0..1000] to ensure they don't repeate the same samples. The Node number can be setup in a parameter or in the Exporter under Blender User Preferences -> YafaRay v3 -> Preferences -> Computer Node (remember to Save Settings to store the number permanently in Blender).

Each computer will generate a different Film. If one of the nodes is set to "Load" the film, it will look for ALL the Film files in the same folder (with the same base file name and frame number) and combine them together to create a combined image with all samples from all individual film files.

* Added OpenCV library and added DeNoise options for the exported image files: JPG, PNG, TGA, TIF. `[Blender Exporter + Core]`
This feature is not available for HDR/EXR formats. Three parameters are exposed for the users:
  - h(luminance): the higher this is, the more noise reduction you get, but the image can become blurred
  - h(chrominance): the higher, the more color noise reduction, but the colors can become blurred
  - Mix: this is intended to add (on purpose) part of the noise from the original image into the final denoised image. This is to avoid "banding" artifacts in smooth and noiseless surfaces. Setting for example 0.8 means that 80% of the final result will come from the "denoised" image and 20% will come from the original (noisy) image.

* YafaRay-v3 can be installed "in parallel" with other major versions of YafaRay and coexist with them. `[Blender Exporter + Core]`
"YafaRay v3" will appear as a DIFFERENT renderer and has to be enabled and selected in each scene as if it were a new renderer. This should help to compare the results and features over different major versions as well as allowing using a "stable" and a more "experimental" versions in parallel at the same time. However, support for this is very limited and depends on many factors such as class name clashes, order of registration, dll and library dependency collisions, etc. If having issues, please remove any other yafaray versions and forks and try again. 

* Initial support for filepaths with Unicode characters (accents, etc) can be used now for loading textures, etc. See: http://yafaray.org/node/703    This support is still limited and could fail in some cases. `[Core]`

* Secondary File Output: now it will be possible to render into render *and* export to image files at the same time! There are several functions that depend on this now, such as the render parameters badge, which will no longer appear in the Blender render, only in the exported images. `[Blender Exporter + Core]`

* It's now possible to save the images automatically to the same place where the .blend file resides, into a folder with same name as the blend file and suffix "_render" `[Blender Exporter]`

* Now the user can use CTRL+C in the console to interrupt a render in progress. `[Core]`
This now works in all modes (render into Blender, render to Image files or using yafaray-xml). The interruption due to CTRL+C will now be handled correctly, ensuring the image files and badge are properly saved.

* yafaray-xml: no longer needed to specify the Library path nor the Plugins path. `[Core]`
The old Windows Registry requirement has been removed and it's not necessary anymore. Now, yafaray-xml will load the libraries from the same folder where the yafaray-xml executable resides and it will load the plugins from the subfolder "plugins" respect to the folder where the yafaray-xml executable resides

* Removed option -pst in yafaray-xml, now it has to be enabled via parameter in the xml file `[Core]`

* New Logging system `[Blender Exporter + Core]`
  - Title, author, comments can be entered now in the Blender Exporter and will appear in the logs and badge.
  - YafaRay compilation information (platform, compiler), Blender information and some System Information will appear automatically in the log for easier support of user problems.
  - Console log will show the time of the day, and the duration of the previous event in the log.
  - Render log can be exported to a TXT file automatically, which will include the render results and information.
  - Render log can be exported to an HTML report automaticall, which will include a link to the rendered image and the render results and information.
  - The log verbosity can be selected in the Blender Exporter, to select how much information we want to show in the console or TXT/HTML log (more clear logs when selecting "Info", more details when selecting "Verbose" or "Debug")
  - YafaRay-xml added commandline settings for log file output (txt and/or html) and removed old custom string


* Improved Parameters Badge. `[Blender Exporter + Core]`
  - New non-intrusive badge, that is appended to the image. Requires to use "secondary file output" (the badge will no longer appear in Blender due to Blender API limitations that don't allow using a non-intrusive badge when rendering into Blender). See: http://yafaray.org/node/383
  - Title, author, etc, can be entered in the Exporter to appear in the badge
  - More information, more detailed and clear in the badge. See: http://yafaray.org/node/162 http://yafaray.org/node/224
  - New YafaRay icon for the badge, low contrast grayscale.
  - Custom icon can be selected to replace the YafaRay icon in the badge.
  - Unicode characters can be used now for the badge (accented characters, etc).
  - Badge position can be selected: top or bottom (the icon position changes automatically for nicer presentation)
  - The amount of details shown in the badge can be selected (show render parameters, AA settings, none or both)
  - Show separately render time and photon generation time, plus added total time (including maps generation).
  
* Added new Render Tile "Centre" (now by default) so the renders start in the centre of the image and expand from there. This should allow a faster view of the to-be render, as typically most objects of interest are in the centre of the image. `[Blender Exporter + Core]`
  
* New Dark areas detection type: curve  (see http://yafaray.org/node/704) `[Blender Exporter + Core]`

* New more optimized rendering tile structure, to avoid having to wait for the last 1 or 2 tiles to finish rendering before the next pass/frame starts. Now, the last tiles will be automatically subdivided to reduce the waiting times. See: http://yafaray.org/node/709  `[Core]`

* Ability to enable/disable Caustic and/or Diffuse Photons generation in the Photon Map integrator. `[Blender Exporter + Core]`

* New mirrorX, mirrorY feature for Textures. See: http://yafaray.org/node/227 `[Blender Exporter + Core]`

* More fine-grained Photon Control for light sources. See: http://yafaray.org/node/475 `[Blender Exporter + Core]`

* Ability to automatically save the exported images and logs including the .blend filename and/or current date/time. See: http://yafaray.org/node/331 `[Blender Exporter]`

* Ability to set a per-material raytracing depth, for example to speed up scenes with glass. See: http://yafaray.org/node/494 `[Blender Exporter + Core]`

* Ability to automatically save a preset file with each exported image. The preset can be reused if needed by copying it to the users "home" folder, into the "yafaray_userdata/presets/render/" subfolder `[Blender Exporter]`

* Fixed the Presets storage and retrieval. They will be saved/loaded in the "home" user folder, inside the subfolder "yafaray_userdata/presets/render/" (will be created automatically if it does not exist). Also, more parameters have been included in the presets now and old parameters were removed. `[Blender Exporter]`

* Parameter to enable/disable World background shadow casting. Option to control separately World background sky/sun shadow casting. `[Blender Exporter + Core]`

* Bidirectional integrator declared as "Deprecated" and no longer supported, as explained in http://www.yafaray.org/node/720 `[Blender Exporter + Core]`

* Small optimizations for AA resampling, especially when no more pixels are supposed to be resampled `[Core]`

* Add Volumetric rendering to the Blend material. `[Core]`
    When using glass or rough glass in the Blend material, volumetric absorption didn't work. I've added the volumetric rendering to the Blend material so glass/rough glass materials render correctly.
    However, there is a limitation: if blending two materials with different volumetric options, as I cannot "merge" the volumes, I'm using the volume from the first material for blend amount values [0.0-0.5] and the volume from the second material for blend amount ]0.5-1.0]. This is totally not ideal, but better than before in my opinion.

* Added SmartIBL functionality to reduce noise when using World HDRI textures for lighting. The functionality adds a new parameter "SmartIBL blur" that blurs the World texture used for lighting without affecting the world texture used for reflections, etc. High values can cause slowdowns at render process start. This was requested at http://www.yafaray.org/node/566 and http://www.yafaray.org/node/727 `[Blender Exporter + Core]`

* Added IBL sampling clamp to reduce noise when using World HDRI textures for lighting. In some cases blur is not good enough to remove noise and it causes blurred shadows. IBL clamping would help sometimes to reduce noise so blur is not needed, but it could lead to inexact overall lighting, etc. This was requested at http://www.yafaray.org/node/566 and http://www.yafaray.org/node/727 `[Blender Exporter + Core]`

* Added Texture Color Controls to be able to control the texture brigthness, contrast, saturation, hue, etc, as requested at http://www.yafaray.org/node/334 `[Blender Exporter + Core]`

* Added Texture Color Ramps, to be able to create much more interesting procedural textures, also requested at http://www.yafaray.org/node/334 `[Blender Exporter + Core]`

* Implemented all remaining progressions in the Blend texture (only linear was implemented), requested at http://www.yafaray.org/node/313 `[Core]`


Bug fixes in v3.0.0:
--------------------
* Fixed: Soft Spotlight too dark when nearer than 1.0 blender unit from objects. See: http://yafaray.org/node/587 `[Core]`

* Fixed: Rough Glass not working in Blend materials. See: http://yafaray.org/node/365 `[Core]`

* Fixed: black spots in some cases. See: http://yafaray.org/node/730 `[Core]`

* Fixed: bug in border rendering where it was displaced one pixel sometimes. See: http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5151&start=0 `[Blender Exporter]`

* Clay material default color changed to "real" middle gray. See: http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5152&start=0#p31497 `[Blender Exporter]`

* Fixed incorrect updating of light preview when light parameters are modified `[Blender Exporter]`

* Fix AO Clay pass self shadow problem, reported by RioFranco (Olivier) `[Core]`

* Changes in SWIG code to try to reduce crashes. Not sure if this will solve all problems but I hope this change helps. `[Core]`

* Bidirectional: fix crash when using sky background as only light source `[Core]`

* SPPM progress bar and tags fixed `[Core]`


YafaRay v2.1.1 (2016-04-16) for Blender 2.76b:
----------------------------------------------
No changes respect to Experimental v2.1.1, only version changes (removed "Experimental")


YafaRay-E (experimental) v2.1.1 (2016-02-06) for Blender 2.76b:
----------------------------------------------
Note: there has been important changes and bug fixes in this version. They have solved some long-standing issues but perhaps they could cause new issues and unexpected results, so we have to keep an eye on them.

* IMPORTANT: Fix for incorrect IBL lighting in World Background Texture when set to Angular. See: http://www.yafaray.org/node/714 `[Core]`

* IMPORTANT: Adjustment to the automatic intersection/shadow bias calculation formula to avoid black artifacts in the scenes with fine details. However, now we can get again some black dots in some scenes again. For now, no good solution at hand (any good solution would require fundamental changes to the engine and probably slow down the renders in a significant amount). However, I hope to have found a better balance now. See: http://blenderartists.org/forum/showthread.php?389385-YafaRay-E-(Experimental)-v2-0-2-builds-Windows-Linux-and-Mac-OSX-for-Blender-2-76b&p=3004974&viewfull=1#post3004974 `[Core]`

* IMPORTANT: Fix for black dots (alpha=0) sometimes when using Mitchell/Lanzcos filters. It's not clear what is the best way of solving this problem. This fix is the one that makes more sense but could cause new issues, we have to keep an eye on this. See: http://www.yafaray.org/node/712 `[Core]`

* Fixed Black artifacts in World Background Textures. See: http://www.yafaray.org/node/714 `[Core]`

* Fixed regression error in v2.1.0 when using Area Lights. See: http://www.yafaray.org/node/713 `[Blender Exporter]`

* Fixed World Preview not updating correctly. This is probably caused by Blender itself, I had to use the same workaround I used in the past to fix the material preview updating problem. `[Blender Exporter]`

* Fixed crash when using textures with Normal or Window coordinates (which are view dependent) along with Caustic Photons. However, we have to consider that Photons are supposed to be view-independent, but when using textures with Window or Normal coordinates (which are view dependant), then the Photons WILL also be view dependant as well! So, using textures with "tricks" like Normal or Windows coordinates can cause low frequency noise in animations with Photons. This would not be a problem, but the price for using such "tricks" in renders. `[Core]`

* Fixed python error when selecting an image texture before with no image opened yet. `[Blender Exporter]`

* "Final" changes to the Material Preview Advanced Controls. `[Blender Exporter]`
    - Added Dynamic Camera Rotation & Zoom.
    - Changes to ensure the preview object is centered and rotation keeps it always in the centre.
    - Changes to keep the scale/proportions of custom preview objects
    - Added AA Passes control for progressively refining the material rendering
    - Splitted the Light power and Light Color controls in two: Key Light power control and Fill Lights power control
    - Removed PosX,PosZ controls as considered unnecessary and complicating the interface.
    - Removed Texture scale/offset controls as they could cause confusion with the actual texture scale/offset parameters

Important note: YafaRay only supports *one* scene in the .blend file. If you have more than one scene, it could cause unexpected results and problems in the new Material Preview Controls.

* Fixed: console colors including blue component were incorect for Windows builds `[Core]`


YafaRay-E (experimental) v2.1.0 (2016-01-31) for Blender 2.76b:
------------------------------------------------

- Added Normal Coordinates for textures, so you can use a gradient texture mapped to normal coordinates to simulate, for example, some cloth materials (see http://yafaray.org/node/188 ) `[Blender Exporter + Core]`
- Fixed some crashes when changing Material/Texture settings `[Core]`
- Increased max limit for Sample Multiplier Factor from 2.0 to 4.0 so more steep exponential increase of samples can be done for every pass. Be aware that the number of samples will grow very fast in every pass if the factor is above 1.5. `[Blender Exporter]`

- Advanced Controls for Material/Texture Preview. `[Blender Exporter]`
  As requested in http://yafaray.org/node/699 I've made some changes to allow fine-grained control of the Material and Texture Preview window.

  Some videos explaining the new feature:

  * First tests (outdated): https://www.youtube.com/watch?v=AFWcHgufkBw
  * Latest video with all features: https://www.youtube.com/watch?v=jBgzqZFQ3Y8  
    
  The new features are:
    
    * Ability to change key light incident angle, so we can place the terminator area on the preview object.: new parameter added to rotate the lights in the Preview window around the preview object. That should allow to set the lights in different angles to look the material under different light conditions
    * Ability to focus in the observer's terminator area: added parameters to displace the preview object up/down, left/right as well as to scale the preview object. This way, the terminator area can be better explored in detail
    * Ability to change light power in the material previsualisation window: added a power factor parameter for the lights and another parameter to set the color of the lights themselves to experiment with different lighting conditions on the material
    * Ability to change previsualisation object size: with the parameter to scale the object plus added parameters to scale/displace the texture as well in the preview
    * Rendering an object from the scene as a previsualisation object: added a parameter to select an arbitrary object from the blend scene as preview object.
    * Background selection: added a parameter to select the desired background: "checker" is the default, "none" is a white background and "world" would be the blend scene world definition. Selecting "world" would allow a more realistic and customized material preview, but it will probably be noisier and slower (depending on the samples selected in the World definition) 


YafaRay-E (experimental) v2.0.2 (2016-01-26) for Blender 2.76b:
------------------------------------------------
- Fixed crash when Blend materials were used and their components were also blend, which had some component materials missing. `[Blender Exporter]`
- Max value for the dark noise factor parameter expanded to 1.0 to allow even darker areas to have better AA sampling `[Blender Exporter]`
- Fix for Oren Nayar to avoid generating white/black dots when used together with bump mapping `[Core]`
- Fix for black dots using HDRI spherical and Coated Glossy `[Core]`


YafaRay-E (experimental) v2.0.1 (2016-01-05) for Blender 2.76b:
------------------------------------------------
- Fixed Instances not working in v2.0.0 (regression) `[Core]`


YafaRay-E (experimental) v2.0.0 (2016-01-01) for Blender 2.76b:
------------------------------------------------
- STRUCTURAL CHANGES to implement Render Passes. The Passes are especially intended for Direct Light and Photon Mapping integrators. Some passes may not work (or work incorrectly) in other integrators. `[Blender Exporter + Core]`
- STRUCTURAL CHANGES to implement Render Views (Stereo3D / MultiView) `[Blender Exporter + Core]`
- STRUCTURAL CHANGES to implement a (hopefully) improved more automatic and reliable Shadow Bias and Intersection Bias, based on triangle size and coordinates positions. `[Blender Exporter + Core]`
- New Noise Control parameters, including a new clamping function to reduce noise at the cost of reducing physical accuracy and realism. `[Blender Exporter + Core]`
- RAM optimization options for JPG,PNG,TGA and TIFF textures. Using "optimized" (by default now) will reduce RAM usage for those textures in approx. 70%. The "optimized" option is lossless (except in TIFF 16bit). There is a "compressed" option that is lossy but allows an extra reduction of approx. 20% in RAM usage. `[Blender Exporter + Core]`
- Support for exporting in MultiLayer EXR files, that can be opened in Blender as well. `[Blender Exporter + Core]`
- XML rendering now supports an option to save partially rendered images every "x" seconds, probably useful when creaiting external GUIs to the XML interface. `[Core]`
- Ability to select what "internal" YafaRay Render Pass has to be mapped to an "external" Render Pass. This provides a lot of power and flexibility when generating Render Passes. `[Blender Exporter + Core]`
- Object ID/Material ID passes, with option of automatic ID color pass. `[Blender Exporter + Core]`
- Object ID Masking and Material ID masking (objects only, objects+shadows, shadows only) `[Blender Exporter + Core]`
- Debug passes and UV debug pass available to be able to find mesh/mapping/texturing problems at the same time as rendering the scene. `[Blender Exporter + Core]`
- Samplerate pass, to apply post-processing filters to the noisier parts of the render. `[Blender Exporter + Core]`
- Added dispersive caustics to SPPM. `[Core]`
- Changes to dispersion in rough glass. `[Core]`
- Removal of entire Qt interface. As far as we know it was old, unmaintained and probably useless anyway. `[Core]`
- Fix (although horrible) for the Bidirectional integrator generating black renders with some types of lights. `[Core]`
- A few speed improvements, I don't expect a significant change but I hope they help a bit, especially in 64bit systems. `[Core]`
- Fixes to the material preview to be correctly refreshed after any changes to the material properties. `[Blender Exporter]`



YafaRay-E (experimental) v1.1.0 (2015-11-06) for Blender 2.76:
-----------------------------------------------
- Changes to the Core code and build files to enable building for Mac OSX 64bit (v10.6 or higher), based on the excellent work from Jens Verwiebe. Thank you very much, Jens!! `[Core]`

- Added a new "Resampled Floor" parameter to the Adaptative AA calculations, to increase the noise reduction performance. The idea is that if the amount of resampled pixels go below that "floor" value during a certain pass, the AA threshold is automatically decreased in 10% for the next pass. More information: http://yafaray.org/node/690 `[Blender Exporter + Core]`

- Blend materials can now be selected using drop down menus. This feature has been ported from povmaniaco's The Bounty fork of YafaRay. Thanks, povmaniaco!! `[Blender Exporter]`

- Added a new texture sampling parameter in Blender Exporter to control the type of interpolation in the image texture. Options will be: bilinear (default), bicubic or none. See: http://www.yafaray.org/community/forum/viewtopic.php?f=22&t=5121 `[Blender Exporter]`

- Added a per-material parameter to control reception of shadows. Now it's possible to select if a material should receive shadows from other objects (as default) or not. See: http://yafaray.org/node/687 `[Blender Exporter + Core]`

- Minor changes for existing material visibility feature to improve (just a tiny bit) performance. `[Core]`



YafaRay-E (experimental) v1.0.0 (2015-10-13) for Blender 2.76:
-----------------------------------------------
Note: from v1.0.0 I will no longer use the suffix "beta", as all YafaRay-Experimental versions are inherently betas ;-). I will use for version scheme: "Major.Minor.Bugfix". Major will be very important and structural changes with possible API breakage, Minor will be new and modified functionality without API breakage, Bugfix will be small changes and bugfixes.

- IMPORTANT CHANGES to Color Management and Color Pipeline Linear Workflow: http://www.yafaray.org/node/670 `[Blender Exporter + Core]`
Initial prototype to try to fix the (apparently broken) YafaRay color pipeline workflow and to replace the simple gamma input/output correction with a proper sRGB decoding/coding in non-HDR files.

More information here: http://www.yafaray.org/node/670

So, I've prepared a YafaRay prototype that fixes the next issues:

* Improved Blender Color Space integration.
* The "simple" gamma correction has been replaced by Color Spaces:
	- LinearRGB			Linear values, no gamma correction
	- sRGB				sRGB encoding/decoding
	- XYZ				XYZ (very experimental) support
	- Raw_Manual_Gamma	Raw linear values that allow to set a simple gamma output correction manually

* Fixed: Double application of input gamma to the Blender Color picker. So now scenes will look brighter in general, but they should also look more realistic with less tweaking.
* Gamma input correction no longer used. The color picker floating point color values will be considered already linear and no conversion applied to them.
* For textures, added specific per-texture Color Space and gamma parameters.
* The color values exported to the XML file will be encoded acording to Blender Output Device Color Space setting.
* In yafaray-xml, new commandline option added: "-ics" or "--input-color-space" that allows to select how to interpret the XML color values. By default, for backwards compatibility, color values will be read as "LinearRGB", but using "-ics sRGB", the color values will be interpreted as sRGB. This setting does *not* affect the textures, as they have already per-texture specific color space/gamma parameters.
* Fixed: when exporting to file there was an error in Blender while reopening it to be shown in the Blender image view.


Several bug tracker entries are supposed to be fixed with this change:
* Color pipeline bug: http://www.yafaray.org/node/670
* Linear output forced on every scene: http://www.yafaray.org/node/603
* Gamma 1.80 input on linux: http://www.yafaray.org/node/604
* Forward compatibility with Blender Color Management: http://www.yafaray.org/node/547
* Gamma correction performed on EXR files: http://www.yafaray.org/node/549



- IMPORTANT CHANGES to Volumetrics for proper raytracing of volumes. `[Core]`
Problems with volumes and transparent objects have been reported in the bug tracker several times:
http://yafaray.org/node/289
http://yafaray.org/node/666

The problem was that Volumes were not really included in the raytracing process, so they were not reflected nor refracted. Now Volumes have been included in the raytracing process, so they can be refracted and reflected as any other objects. This is a significant change that could cause new issues, so please let us know about any problems in YafaRay bug tracker.

Now, if there are no parameters set in the XML for transparent background or transparent refracted background, their default values will be "false" and not "true" as until now. This will avoid confusion due to the new way "transparent refracted background" works, not rendering the background at all so volumes rendered against a transparent background do not carry "remains" of the background with them. 

- Fix for attenuation when using 2 or more volumetric objects: http://www.yafaray.org/node/332 `[Core]`

- Fix for error message "Index out of bounds in pdf1D_t" when spotlights with falloff > 0.70 and photons were used: http://www.yafaray.org/node/681 `[Core]`

- Fix for Alpha Premultiply broken in Blender exporter: http://www.yafaray.org/node/682  Now the "Premultiply Alpha" option is back in the Exporter, but only when Export to file or to xml is selected. Premultiply will now be forced to true when exporting into Blender. `[Blender Exporter]`

- Fix for some YafaRay camera panels incorrectly appearing in LuxRender! `[Blender Exporter]` http://www.luxrender.net/forum/viewtopic.php?f=16&t=12405&sid=14e5a712bb33cbdee95c65fb1920ad38&start=20
https://github.com/DavidBluecame/Blender-Exporter/commit/70138b7ec2c2aa3f94d3c820babc10d12af6f943 



YafaRay-E (experimental) v0.1.99-beta4c (2015-07-29) for Blender 2.75 RC:
----------------------------------------------------------
Note: builds were not created for this version, as it was only used for limited-scale testing. However, the changes made in this version remain in newer Releases and builds.

More info about the discussion and changes: http://www.yafaray.org/node/662

- Fix for issue where Final Gather uses non-IBL background in glass: http://www.yafaray.org/node/572 `[Core]`

- Fix for white dots in Path Tracer integrator: http://www.yafaray.org/node/662 `[Core]`

- Fix for bump mapping artifacts: http://www.yafaray.org/node/660 `[Core]`
WARNING: I've made significant changes to the bump mapping when using image textures, trying to improve it and get results more similar to Blender, but it could cause new issues so enough testing should be done to make sure bump/normal mapping still works correctly.
 
- Improvements to the noise fireflies in Rough Glass: http://www.yafaray.org/node/663 `[Core]`

- New parameter to enable/disable lights. `[Blender Exporter + Core]`
In the XML, into each "light" section you can add:
<light_enabled bval="false"/> or <light_enabled bval="true"/>

- Ability to control per-light shadow casting. `[Blender Exporter + Core]`
In blender exporter this is in the new "advanced settings" at the very bottom of the light panel. In the xml file, you can add this to the "light" sections:
<cast_shadows bval="true"/> or <cast_shadows bval="false"/>

- New per-material "visibility" enum parameter that can have the following values. `[Blender Exporter + Core]`

'normal' (default): Normal - Normal visibility - visible casting shadows.
'no_shadows': No shadows - visible but not casting shadows.
'shadow_only': Shadows only - invisible but casting shadows.
'invisible': Invisible: totally invisible material.

This new parameter is at the bottom of the material panel, in the new advanced settings. In XML it would be something like, in the material section, for example:

<visibility sval="shadow_only"/>



YafaRay-E (experimental) v0.1.99-beta4 (2015-06-20) for Blender 2.75 RC:
---------------------------------------------------------

- Changes to the blend material "component" material1,material2 handling: http://www.yafaray.org/node/546 `[Blender Exporter]`

In previous versions if you created or deleted materials in the .blend file, sometimes all the material components of the blend materials changed or dissapeared randomly. To avoid it, now the materials are referenced by name using strings. You cannot use dropdown menus anymore to select the blend submaterials, and you have to be careful now not to rename the materials used by "blend" materials. However, with the new system if you create or delete other materials it will not affect the blend material1,material2 assignments.

Increased the level of detail in the YafaRay Log, so if there are any problems with missing components in blend materials it should be easy to spot and correct by reading the YafaRay Log.

WARNING: this change breaks backwards compatibility. When opening a .blend created with an older version of YafaRay the blend material components will be "upgraded" to the new system, but the"blend" materials in a blend made with the new version could behave wrongly if you open it with an older version.

- New advanced parameters for fine control of Shadow Bias/Min Ray Dist if the automatic calculation is not good enough. Please give us feedback about it in the forum: http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5084 `[Blender Exporter + Core]`

- Fix for caustics noise coming from Non-IBL background in Photon Mapping. Now the background will only be used for Caustics if IBL is enabled and (if there is a caustics parameter available in the background settings) if caustics is enabled in the background. `[Core]`

- Background "power" parameters relocated to places where they make more sense. They were hidden and only visible when IBL was enabled, but most of the times the power parameter affects the background rendering even if IBL is disabled.



YafaRay-E (experimental) v0.1.99-beta3 (2015-05-02) for Blender 2.74.5 (up to Blender builbots for 2015-05-02):
------------------------------------------------------------------------------------------------
Blender made a change to their API in their development branch 2.74.4 to include MultiView. That change caused YafaRay to render black images despite being working fine.

Very kindly Jens Verwiebe sent us the fix for Blender Exporter so YafaRay can work again with Blender 2.74.4. This fix is not a full integration in the new MultiView functionality, it just allows YafaRay to work again with Blender. `[Blender Exporter]`

More changes in this beta3 version:

- Fix for -NAN results in the Bidirectional integrator when using Architectural, Angular and Ortho cameras. See: http://www.yafaray.org/node/538 `[Core]`

- Fix for problem with Rough Glass too bright when dispersion is enabled. See: http://www.yafaray.org/node/642 `[Core]`

- Extended Texture Mapping system, allowing using textures to map additional properties in materials, to be able to create either more realistic or more exotic materials and reduce the dependency on the "blend" material. More information in: http://www.yafaray.org/community/forum/viewtopic.php?f=22&t=5091 `[Blender Exporter + Core]`

Important note: when using some of the new mappings, the renders may slow down. I'm not sure whether it's because of the additional calculations (very likely) or if it's something we can optimize further in the future. In any case, it should only be noticeable when using the new mappings, and I think it's worth the ability to create new materials now.

The new texture mappings in addition to the existing ones are: 
	- Diffuse Reflection Amount in Shiny Diffuse, Glossy and Coated Glossy materials
	- Sigma factor for Oren Nayar in Shiny Diffuse, Glossy and Coated Glossy materials
	- Filter color in Glass and Rough Glass.
	- IOR refractive factor in Glass and Rough Glass. The texture amounts are added to the IOR of the material.
	- IOR refractive factor for the Fresnel in Shiny Diffuse and Coated Glossy materials.
	- Roughness factor in Rough Glass material.
	- Exponent factor in Glossy and Coated Glossy materials
	- Mirror amount in Coated Glossy materials.
	- Mirror Color in Coated Glossy Materials

Also added a (non-texture) mirror amount slider in the Coated Glossy material

Unfortunately due to Blender API limitations, in some of the new texture sliders, the "tooltip" information that appears when hovering the mouse over the slider, can be misleading and not represent the actual function of that slider. However, I took care in setting the description correctly so just by looking at the slider itself you can see what does it map.



YafaRay-E (experimental) v0.1.99-beta2 (2015-04-18) for Blender 2.74:
-------------------------------------------------------
- New Clay Material, with a small correction since the previous beta1. `[Blender Exporter]`
- Fix for bad NaN normals that happened sometimes. `[Core]`
- Calculate automatically Shadow Bias and Minimum Ray Dist depending on the scene size. This is to avoid black artifacts when resizing the objects. However as it's a fundamental change that affects everything, perhaps some new artifacts could appear in the images now and further fine tuning needed in this new formula. Please give us feedback about it in the forum:
http://www.yafaray.org/community/forum/viewtopic.php?f=23&t=5084  `[Core]`



YafaRay-E (experimental) v0.1.99-beta1 (2015-04-11) for Blender 2.74:
------------------------------------------------------
Based on the official stable YafaRay v0.1.5 git version

- New Clay Material system, more powerful and flexible. `[Blender Exporter]`
- Texture mapping of Sigma factor in Shiny Diffuse/Oren Nayar. `[Blender Exporter + Core]`
- Fix for Negated colors in Musgrave/Voronoi textures mapped to diffuse color. [Core]
