#!/bin/bash

# Exit on error
set -e

# Run the static site generator
cd src
python3 main.py

# Start the web server
cd ../public
python3 -m http.server 8888