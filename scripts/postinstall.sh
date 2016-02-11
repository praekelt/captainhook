manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/manage.py"
echo "Manage command: $manage" >> /var/praekelt/postinstall.log

echo "Running syncdb" >> /var/praekelt/postinstall.log
$manage syncdb --noinput --no-initial-data --migrate --settings=project.settings_live_web_site >> /var/praekelt/postinstall.log 2>&1

echo "A deployment to `hostname` has been completed" | mail -s "Telkom Deployment: `hostname`" 1telkom@praekelt.com
