#!/bin/bash

# 対話式コマンドのテスト


if [ -e ~/.bl/credentials ]; then
    mv ~/.bl/credentials ~/.bl/credentials.org
fi
$(dirname $0)/test.exp
credentials=$(cat << EOF
[hoge]
base_url = hoge
access_key = hoge
EOF
)
if [ "$(cat ~/.bl/credentials)" == "$credentials" ]; then
	echo "Configure command has succeeded"
else
	echo "Configure command has failed"
	mv ~/.bl/credentials.org ~/.bl/credentials
	exit 1
fi
if [ -e ~/.bl/credentials.org ]; then
    mv ~/.bl/credentials.org ~/.bl/credentials
fi

cat <<EOF

=== Test of configure command is OK! ===

EOF

# UT
python test/test.py
