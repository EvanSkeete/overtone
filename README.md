Overtone
========

Build instructions:
========

make venv
activate venv
pip install flask

run: python overtone/app.py

Deploy instructions:
========

Change first line in overtone/app.wsgi to point to venv

To use with apache, install mod_wsgi

Configure apache as follows:

#Point apache to mod_wsgi.so (wherever it is on your system)
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

ServerName #Server Name

WSGIDaemonProcess app
WSGIScriptAlias / path-to-app/overtone/app.wsgi
Alias /static/ path-to-app/overtone/static/

<Directory path-to-app/overtone/>
    WSGIProcessGroup app
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>




