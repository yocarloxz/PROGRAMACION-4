# para activar el celery en pyharm 

despues de correr el app.py

en la terminal local del pycharm haces que el entorno sea virtual 
" .\.venv\Scripts\Activate.ps1 "

y luego corres el celery con este comando
" celery -A celery_worker.celery worker --loglevel=info -P solo " 

en windows por lo que tengo entendido lleva el -p solo
