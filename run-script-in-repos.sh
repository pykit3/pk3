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

if [ -f "./$script" ]; then
    :
else
    usage
    exit 1
fi

set -o errexit

for d in `ls -dp k3*`; do
    echo "===($d)==="
    (
        cd ./github.com/pykit3/$d
        "../../../$script" "$@"
    )
done
