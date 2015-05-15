# Commands Menu #

Tools are handy drop down menu items which you can configure to suit your needs. They represent an alternative to toolbar items and they are ideal solution for those who enjoy minimalistic interfaces.

When editing tool menu items you need to enter title and command.

## Title ##
Item title is the text you will see under **Tools** menu.

  * Underscore in the title text indicates the next character should be underlined and used for the mnemonic accelerator key. Only first character will be used if there are more items with same accelerator key.
  * If whole title text is just one dash item will be used as a menu separator.

## Command ##
You can use any command within your search path but please note that Sunflower will not start terminal automatically. If you wish to start terminal and execute a command, please take a look at _gnome-terminal_ documentation.

Additionally few variables can be passed to the command:
  * **%l**, **%L** - Name of the selected item in the left list.
  * **%r**, **%R** - Name of the selected item in the right list.
  * **%s**, **%S** - Name of the selected item in active list.

Uppercase versions include full path to the selected item.

Note: Adding & (ampersand) at the end of the command means that program should not wait for command to finish.