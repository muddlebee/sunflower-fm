## Files and Naming ##
Sunflower uses well known `gettext` i18n support. In `translations/sunflower.pot` you'll find all the text from the program that can be translated. This file will change and will reflect program development. Make sure your translation is up to date with this file.

Translated file **must** be placed in `translations/{language}/LC_MESSAGES/sunflower.po` in order to help people in charge for packaging Sunflower and its translations. For example if you are translating Sunflower to Korean, destination filename would be `translations/ko/LC_MESSAGES/sunflower.po`. Please notice the extension for translated files is _po_ instead of _pot_.

## Contributing ##
You can contribute by either getting a local copy or by cloning this repository. In both cases, once you've done translating, you need to contact project owner to include your files.

  * Making a local copy is achieved by issuing the following command
> > `hg clone https://sunflower-fm.googlecode.com/hg/ sunflower-fm`


> Please note that you need to have [Mercurial](http://mercurial.selenic.com/) installed. Debian based distributions should have `mercurial` package in their repositories.

  * Making repository clone can be done by visiting [this](http://code.google.com/p/sunflower-fm/source/checkout) page and clicking "_Create a clone_" button in the bottom of the page.

For more information on `gettext` you can visit official [page](http://www.gnu.org/software/gettext/). If you are not experienced with `gettext` formatting check out `gtranslator` or `poedit`. They offer easy to use interface.