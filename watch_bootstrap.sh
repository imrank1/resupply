#!/bin/bash
# this will watch for changes in the less directory and compile bootstrap.less into bootstrap.css
# gem install coyote
coyote -w resupply/static/less/bootstrap.less:resupply/static/css/bootstrap.css
