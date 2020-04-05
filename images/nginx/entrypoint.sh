set -e

sh -c "sed -i 's/hosthosthost/'"$HOSTNAME"'/' /etc/nginx/*.conf"
sh -c "sed -i 's/hosthosthost/'"$HOSTNAME"'/' /etc/nginx/conf.d/*.conf"

sh -c "sed -i 's/worker_processes_ENV/'"$WORKER_PROCESSES"'/' /etc/nginx/nginx.conf"

sh -c "sed -i 's/sitesitesite/'"$SITE_HOST"'/' /etc/nginx/*.conf"
sh -c "sed -i 's/sitesitesite/'"$SITE_HOST"'/' /etc/nginx/conf.d/*.conf"

sh -c "sed -i 's/webwebweb/'"$BACKEND_HOST"'/' /etc/nginx/*.conf"

sh -c "sed -i 's/gategategate/'"$GATE_HOST"'/' /etc/nginx/*.conf"

exec sh -c "/usr/sbin/nginx -g 'daemon off;'"

exec "$@"