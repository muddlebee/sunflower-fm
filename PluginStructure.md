# Required files #

Plugins are directories located in `application/plugins` directory. You can name this directory any way you want but we suggest using something logical that represents its function.

Sunflower requires only 2 files in your plugin directory:
```
plugin_name/
   plugin.py
   plugin.conf
```


## Main plugin file (plugin.py) ##
When enabled plugins are loaded during program start-up. To be more specific, Sunflower loads `plugin.py` from plugin directory and if possible calls `register_plugin` method passing application as first (and only) parameter.

Blank `plugin.py` file would look like this
```
def register_plugin(application):
    """Initialize plugin on start-up"""
    pass
```

Using `application` parameter you can access other parts of program. Plugins are loaded after all managers and UI is created but **before** toolbar items. This is done on purpose, to enable developers to extend toolbar using plugins.

Please note that tabs are restored last!

## Plugin configuration file (plugin.conf) ##
We use this file to store information related to this plugin. File has the following format:

```
[Name]
en=Firendly plugin name

[Description]
en=Short or extensive description

[Version]
number=0.1

[Author]
name=John Doe
contact=john.doe@some-mail.com
site=www.somesite.com
```

`Name`, `Version` - These sections are used in preferences window to present user with nice and localized name.

`Description` - This section is used to provide user with details of plugin.

`Author` - Section is used to provide user with ability to contact plugin author.

Only `Name` section is required but we suggest adding them all. If name is not available in current locale `en` will be used by default.