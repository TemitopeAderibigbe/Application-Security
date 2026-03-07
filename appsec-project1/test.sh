#!/usr/bin/env bash

echo "########################################################################"
echo 
echo "# This script helps check that your solutions match the spec,"
echo "# but it is not the autograder, and it is not authoritative!"
echo "#"
echo "# The spec (and autograder) has a few requirements beyond"
echo "# what this script verifies. It's your responsibility to test carefully."
echo 
echo "########################################################################"

if [ "$EUID" -eq 0 ]
then echo "This script won't work correctly if you run it with sudo"
	 exit
fi

set -e

if [ ! -f "cookie" ]; then
    ./build.sh clean
    ./build.sh
fi

COOKIE=$(head -1 cookie)

# Safety commit
# Uncomment the lines below if you want to automatically commit and push your solutions to Github
# git add sol[0-8].py cookie
# git commit --allow-empty -m "Automatic commit by test script for $COOKIE"
# git push

echo
echo "Testing solutions..."
echo

OUTPUT=$(2>&1 ./target0 <(python3 sol0.py) || true)
if [[ "$OUTPUT" == "Hi "*"! Your grade is A+." ]]; then
    echo "target0: success"
else
    echo "target0: error"
fi

OUTPUT=$(2>&1 ./target1 <(python3 sol1.py) || true)
if [ "$OUTPUT" = "Your grade is A+." ]; then
    echo "target1: success"
else
    echo "target1: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target2 <(python3 sol2.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target2: success"
else
    echo "target2: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target3 <(python3 sol3.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target3: success"
else
    echo "target3: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target4 <(python3 sol4.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target4: success"
else
    echo "target4: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target5 <(python3 sol5.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target5: success"
else
    echo "target5: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target6 <(python3 sol6.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target6: success"
else
    echo "target6: error"
fi

OUTPUT=$(2>&1 echo "whoami" | ./target7 <(python3 sol7.py) || true)
if [ "$OUTPUT" = "root" ]; then
    echo "target7: success"
else
    echo "target7: error"
fi

set +e
