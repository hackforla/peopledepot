if [ -d scripts ]; then
    if [[ $PATH != *"$PWD/scripts"* ]]; then
        export PATH=$PATH:$PWD/scripts
        echo "Added $PWD/scripts to PATH"
    else
        echo "scripts directory already in PATH"
    fi
else
    echo "ERROR: scripts directory not found.  Please run this script from the root of the project."
    exit 1
fi