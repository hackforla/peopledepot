#!/bin/bash


# Function to look at child or sibling app directory, if one exists.
# Useful if called from the scripts directory or root directory
search_app() {
    original_dir=$(pwd)
    cd ../app 2>/dev/null || cd app 2>/dev/null
    current_dir=$(pwd)
    if [[ -f "$current_dir/manage.py" ]]; then
        echo "$current_dir"
        cd $original_dir
        return 0
    fi
    cd $original_dir
    return 1
}

# Main function to find the Django root directory
find_django_root() {
    # Try searching upwards first
    root_dir=$(search_app)
    echo "Searching current directory or child/sibling app directory"
    if [[ -n "$root_dir" ]]; then
        echo "Django root directory found: $root_dir"
        return 0
    fi
     echo "Django root directory not found"
    return 1
}

# Call the main function
find_django_root
original_dir=$(pwd)
if [[ -z "$root_dir" ]]; then
    echo "Django root directory not found, path not set"
    return 1
fi
echo root_dir = $root_dir
cd $root_dir/../scripts
script_path=$(pwd)
echo script_path = $script_path
cd $original_dir
export PATH=$script_path:$PATH
echo Added $script_path to PATH
