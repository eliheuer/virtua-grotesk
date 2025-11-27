#!/bin/bash

# Build script for Virtua Grotesk fonts
# Uses fontc for variable font and fontmake for static instances

set -e

# Activate virtual environment
source ~/Py/venvs/basic-fonts/bin/activate

echo "Building Virtua Grotesk fonts..."

# Create fonts directory if it doesn't exist
mkdir -p fonts

# Build variable font with fontc (faster)
echo ""
echo "Building variable font with fontc..."
fontc sources/VirtuaGrotesk.designspace

# Move and rename the variable font
if [ -f "build/font.ttf" ]; then
    mv build/font.ttf fonts/VirtuaGrotesk-VF.ttf
    echo "✓ Variable font built: VirtuaGrotesk-VF.ttf"
fi

# Build static instances with fontmake
echo ""
echo "Building static instances with fontmake..."
fontmake -m sources/VirtuaGrotesk.designspace -i -o ttf --output-dir fonts/

echo ""
echo "Build complete! Fonts are in the fonts/ directory:"
ls -lh fonts/*.ttf
