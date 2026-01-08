#!/bin/bash
# Create a new pykit3 package from template
# Usage: ./create-package.sh <parent_dir> <package_name>
#
# Example:
#   ./create-package.sh ~/projects k3mypackage

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMPL_DIR="$SCRIPT_DIR/github.com/pykit3/tmpl"

if [ $# -ne 2 ]; then
    echo "Usage: $0 <parent_dir> <package_name>"
    echo ""
    echo "Arguments:"
    echo "  parent_dir    Directory where the package will be created"
    echo "  package_name  Name of the package (should start with k3)"
    echo ""
    echo "Example:"
    echo "  $0 ~/projects k3mypackage"
    exit 1
fi

PARENT_DIR="$1"
PACKAGE_NAME="$2"
TARGET_DIR="$PARENT_DIR/$PACKAGE_NAME"

# Validate package name
if [[ ! "$PACKAGE_NAME" =~ ^k3[a-z0-9]+$ ]]; then
    echo "Error: Package name should start with 'k3' and contain only lowercase letters and numbers"
    echo "Example: k3mypackage, k3util, k3http"
    exit 1
fi

# Check if template exists
if [ ! -d "$TMPL_DIR" ]; then
    echo "Error: Template directory not found: $TMPL_DIR"
    exit 1
fi

# Check if target already exists
if [ -e "$TARGET_DIR" ]; then
    echo "Error: Target directory already exists: $TARGET_DIR"
    exit 1
fi

# Create parent directory if needed
mkdir -p "$PARENT_DIR"

echo "Creating package: $PACKAGE_NAME"
echo "  Template: $TMPL_DIR"
echo "  Target:   $TARGET_DIR"
echo ""

# Copy template (excluding .git and .ruff_cache)
rsync -a --exclude='.git' --exclude='.ruff_cache' "$TMPL_DIR/" "$TARGET_DIR/"

# Replace placeholders in all files
echo "Replacing placeholders..."
find "$TARGET_DIR" -type f \( -name "*.py" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" -o -name "*.md" \) | while read -r file; do
    if grep -q "k3xxnamexx" "$file" 2>/dev/null; then
        sed -i.bak "s/k3xxnamexx/$PACKAGE_NAME/g" "$file"
        rm -f "$file.bak"
        echo "  Updated: ${file#$TARGET_DIR/}"
    fi
done

# Initialize git repository
echo ""
echo "Initializing git repository..."
cd "$TARGET_DIR"
git init -q
git add .
git commit -q -m "Initial commit from pykit3 template"

echo ""
echo "Package created successfully!"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Edit pyproject.toml: update description, keywords, dependencies"
echo "  3. Edit mkdocs.yml: update site_description"
echo "  4. Edit docs/index.md: add description and examples"
echo "  5. Create __init__.py with your package exports"
echo "  6. Implement your package"
echo "  7. Run 'make test' to verify"
echo "  8. Create GitHub repo and push"
