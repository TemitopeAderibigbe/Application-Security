#!/bin/bash

function cleanup {
	rm -f target[0-7] cookie
    rm -f targets.tar.gz
}

cleanup
if [ "$1" = "clean" ]; then
	exit 0
fi
# ask for space separated list of emails
echo "Enter the email addresses of the users who should be able to run the targets (space separated):"
read -a emails
if [ ${#emails[@]} -eq 0 ]; then
    echo "No emails entered. Exiting."
    cleanup
    exit 1
fi
if [ ${#emails[@]} -eq 1 ]; then
    wget -O targets.tar.gz "appsec.gatech.fail/fetch?username=${emails[0]}" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Unable to find student. Ensure email is correct and you have registered as working alone on the autograder. Wait 1 minute after registering. Exiting."
        cleanup
        exit 1
    fi
fi
if [ ${#emails[@]} -gt 1 ]; then
    wget -O targets.tar.gz "appsec.gatech.fail/fetch?username=${emails[0]}&username=${emails[1]}" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Unable to find group. Ensure emails are correct and registered as a team on the autograder. Wait 1 minute after registering. Exiting."
        cleanup
        exit 1
    fi
fi

tar -xzf targets.tar.gz
rm -f targets.tar.gz

sudo chmod 555 target[0-7]
sudo chown root:$SUDO_USER target[2-7]
sudo chmod 6777 target[2-7]
for t in target[2-7]; do
    if [ `stat -c '%a' $t` -ne 6777 ]; then
        echo "Setuid permission could not be set. Make sure your files are in a native Linux folder and not a VirtualBox shared folder."
        cleanup
        exit 1
    fi
done

echo "Setup complete."
