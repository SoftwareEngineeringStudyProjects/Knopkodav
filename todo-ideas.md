# Taking screenshots
* https://stackoverflow.com/questions/2846947/get-screenshot-on-windows-with-python
* https://pypi.org/project/mss/ Cross-platform
* https://wiki.wxpython.org/WorkingWithImages#A_Flexible_Screen_Capture_App
* PIL (Windows, MacOS, Linux added later)
* pyautogui (seems to have some issues, but workarounds exist)
* PrtSc 

# Development directions
* Macro recorder + editor (specify UI elements, fix mistakes)
* Start with DOM, then build DOM-like representation (UI components) for any tech
* Use screenshots only, detect objects on screenshots
* Hierarchy of abstractions: "install package" button -> "install package by name" action -> ...
* Fuzzy testing - not just random clicks, but know structure of UI

# Entities
* Script
* Action
* Data extractor = get data from UI (e.g. OCR)
* UI element/component
* Event? = low-level action, e.g. click on element
* Element DB - recognized elements, UI structure, actions and extractors, ...

# Recorder
* Can listen to mouse and keyboard events
* Can run screenshot saving on these events
* Taking screenshot looks fast enough, but saving requires time
* Running save file on asyncio loop seems to work (but need to check for possible bugs)
* Stopping loop seems to work, not sure if it waits for tasks to complete (needs checking)
* TODO: store previous image in memory, compare with next image, store diff only - should be faster?

# Replay
* strange behavior pyscreeze/init.py match_indices = numpy.arange(result.size)[(result > confidence).flatten()]
* looks like the issue was related to incorrect crop
  * click was close to edge of screenshot
  * cropped image contained black pixels
  * OpenCV detection methods seem to be very sensitive to such pixels
* so need to implement better cropping
* and also check for black pixels in target images, maybe remove/crop or replace with something else?
* maybe find a way to search for N best results, or results until noticeable gap