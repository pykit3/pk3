#!/bin/sh

usage()
{
    cat <<-END
Run script in every 'k3*' dir
$0 <script_name> <args...>
END
}

script=$1
shift

if [ -f "./scripts/$script" ]; then
    :
else
    usage
    exit 1
fi

set -o errexit

for d in $(cat docs/repos.txt); do
    name=$(basename "$d")
    echo "===($name)==="
    (
        cd "packages/$d"
        bash -x "../../scripts/$script" "$@"
    )
    echo "===($name)=== Done"
done
