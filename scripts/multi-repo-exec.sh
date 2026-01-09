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

for d in packages/k3*/; do
    name=$(basename "$d")
    echo "===($name)==="
    (
        cd "$d"
        bash -x "../../scripts/$script" "$@"
    )
done
