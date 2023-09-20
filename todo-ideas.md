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