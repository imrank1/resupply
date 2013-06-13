#!/bin/bash
# this will watch for changes in the less directory and compile bootstrap.less into bootstrap.css
# npm install -g bansheee
banshee resupply/static/less/bootstrap.less:resupply/static/css/bootstrap.css -w