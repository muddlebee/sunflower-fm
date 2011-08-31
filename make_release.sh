#!/bin/bash
echo Copying change.log...
cp change.log ~/Desktop/change.log

echo Archiving source code...
hg archive --type tgz --prefix Sunflower ~/Desktop/Sunflower.tgz
