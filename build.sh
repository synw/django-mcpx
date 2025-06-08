#!/bin/bash

# Exit immediately if any command exits with a non-zero status
set -e

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install the build tool if not already installed
echo "Ensuring build is installed..."
uv pip install --upgrade build

# Create the package distribution using pypa/build
echo "Creating package distribution..."
python -m build

echo "Build completed successfully."
