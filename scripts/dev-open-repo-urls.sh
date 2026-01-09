#!/bin/sh

usage() {
	cat <<-END
		Open URLs for each repo listed in docs/repos.txt

		Usage:
		    $0 <url_type>

		Arguments:
		    pypi    - Opens https://pypi.org/project/<package_name>/
		    action  - Opens https://github.com/pykit3/<package_name>/actions

		Example:
		    $0 pypi
		    $0 action
	END
}

if [ $# -ne 1 ]; then
	usage
	exit 1
fi

url_type=$1

if [ "$url_type" != "pypi" ] && [ "$url_type" != "action" ]; then
	echo "Error: url_type must be 'pypi' or 'action'"
	usage
	exit 1
fi

if [ ! -f "docs/repos.txt" ]; then
	echo "Error: docs/repos.txt not found"
	exit 1
fi

if ! command -v open >/dev/null 2>&1; then
	echo "Error: 'open' command not found (macOS required)"
	exit 1
fi

urls=""

while IFS= read -r package || [ -n "$package" ]; do
	# Skip empty lines and whitespace
	if [ -z "$(echo "$package" | tr -d '[:space:]')" ]; then
		continue
	fi

	if [ "$url_type" = "pypi" ]; then
		url="https://pypi.org/project/$package/"
	else
		url="https://github.com/pykit3/$package/actions"
	fi

	urls="$urls $url"
done <docs/repos.txt

if [ -z "$urls" ]; then
	echo "No packages found in docs/repos.txt"
	exit 1
fi

echo "Opening $(echo "$urls" | wc -w) URLs..."
open $urls
