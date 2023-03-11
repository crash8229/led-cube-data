#!/bin/bash

show_usage() {
    cat << EndOfMessage
Runs the Kaitai Struct Visualizer docker image

Syntax: run_docker_kaitai_visualizer.sh [-h] binary ksy

Positional arguments:
    binary: File to visualize
    ksv:    Ksy file to use for processing the binary

Options:
    -h: Show this usage message then exit

EndOfMessage
}

if [[ $# -eq 0 ]] ; then
    show_usage
    exit 1
fi

while getopts "h" flag; do
    case "$flag" in
        h) show_usage; exit 0;;
        *) echo "Unknown flag, use -h to see the usage message"; exit 1;;
    esac
done

binary=${*:$OPTIND:1}
ksy=${*:$OPTIND+1:1}

docker run --rm -v "$(pwd):/share" -it kaitai/ksv "$binary" "$ksy"
