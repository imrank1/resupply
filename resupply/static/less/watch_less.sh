#!/bin/bash
# this will watch for changes in the less directory and compile bootstrap.less into bootstrap.css
# gem install watchr
# npm install -g lessc
#watchr -e 'watch(".*\.less$") { |f| system("lessc bootstrap.less > ../css/bootstrap.css && date \"+%r\"") }'
watchr -e 'watch(".*$") { |f| system("lessc bootstrap.less > ../css/bootstrap.css && date \"+%r\"") }'
