#!/bin/bash

# 対話式コマンドのテスト

mv ~/.bl/credentials ~/.bl/credentials.org
./test.exp
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
fi
mv ~/.bl/credentials.org ~/.bl/credentials

cat <<EOF

=== Test of configure command is OK! ===

EOF

# UT
python test.py
