Inspired by https://github.com/sheppard/django-github-hook

Example scripts::

``ssh server.com 'sudo /etc/init.d/memcached restart; sudo rm -rf /var/cache/nginx/thecache/*; sudo bash -c "cat /dev/null > /var/praekelt/logs/site-router.log"``

``ssh server.com "echo -n 'Avg time (ms): '; expr \`awk '{s+=\$6*1000} END {print s}' /var/praekelt/logs/site-router.log\` / \`wc -l < /var/praekelt/logs/site-router.log\`"``

