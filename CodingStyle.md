# Coding Style #

If you wish to contribute to this project you need to stick to coding style in which the whole program was written. Keeping code consistent helps finding bugs and making the whole thing easier for all of us.

Coding style is actually [PEP 8](http://www.python.org/dev/peps/pep-0008/) with some slight modifications. Read that document before continuing.

Ok, now that you've read that nice document, _the rules_:
  * Use tabs instead of spaces. This makes it easy for everyone to use whatever tab size they want without breaking the style;
  * Class definition has 2 blank lines before and after;
  * Class definition needs to have docstring describing what it does unless class is exception;
```
class ExampleOne:
    """Example class code formatting"""

    def __init__(self):
        pass


class SecondExample:
    """Second class example"""
    pass
```
  * Use `import` first followed by `from import` with one blank line in between;
```
import os
import gtk

from gui.main_window import MainWindow
from gui.input_dialogs import InputDialog
```
  * Maximum number of horizontal characters should be 120. You can use less if you find it suitable;
  * If you have a long string you can break it into chunks using brackets. You can also do this if code would look ugly otherwise;
```
long_string = (
        "This is an example of long string which is hard to "
        "squeeze into 120 character limit."
    )
```
  * Do not use shebang in python source code files. This prevents wrong version of Python to be used.
  * No spaces between function name, opening brace and first argument name. One space after comma in arguments list:
```
def foo(bar, baz): pass
foo("bar", 1)
```
  * In comparison first place the data that **is compared**, second place it is **compared with**:
```
# Correct.
if sys.platform == "win32": pass
# Honorable C style, but incorrect.
if "win32" == sys.platform: pass
```

[Example plugin](PluginExample.md) demonstrates this coding style accurately. Note that Google Code considers tab character to be 8 spaces width. I prefer 4 spaces but it's up to you choose its size as long as you use tab character instead of spaces.

**Important:** This coding style applies only if you are contributing to software itself. Plugin developers are free to use their own style. If you want your plugin to be included in default installation you will need to comply with this coding style!

# Commits #

  * When committing changes to repository use the format below for description. Partial list of modules: Plugin base, Plugins, Operations, Main window, Operation dialogs.
```
Module: [Submodule:] Change

Bigger description if needed
```

Commit messages need to be concise, direct and describe what was changed. Usage of punctuation signs is required.

# Path of blame #
We use similar method for our development as Linux Kernel does. Developers are playing "tag". If you change some code and it breaks it's up to you to fix it. If you take code from other users, make sure you commit patches as them. Everyone keeps their credit!