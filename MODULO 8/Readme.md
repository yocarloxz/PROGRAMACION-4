# para activar el celery en pyharm 

despues de correr el app.py

en la terminal local del pycharm haces que el entorno sea virtual 
" .\.venv\Scripts\Activate.ps1 "
hay un slash entre los dos puntos, el readme no lo muestra

y luego corres el celery con este comando
" celery -A celery_worker.celery worker --loglevel=info -P solo " 

en windows por lo que tengo entendido lleva el -p solo
