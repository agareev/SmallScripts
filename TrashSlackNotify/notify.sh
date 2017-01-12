#!/usr/bin/env bash

url='hookUrl-lalalalalala'
to="monitoring"
emoji=':frowning:'
username='UserNotify'
payload="payload={\"channel\": \"${to}\", \"username\": \
\"${username}\", \"text\": \"${message}\", \"icon_emoji\": \"${emoji}\"}"
program = "./bin/program"

${program} $@
if [ $? != 0 ]; then
        message="We have a problem with ${program} exit code is ${?}"
        curl -m 5 --data-urlencode "${payload}" $url
fi
