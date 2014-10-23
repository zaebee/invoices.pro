Установка
============
* cd /<project>/<path>/
* virtualenv .env --distribute (устнавааливаем виртуальное окружение)
* source .env/bin/activate (активируем окружение)
* pip install -r hackthon/req.txt (ставим зависимости)
* python manage.py syncdb (создаем БД)
* python manage.py migrate --all (накатываем миграции)

Развертывание
============
Здесь описан способ запуска проекта через uwsgi+ supervisor
Нужно установить uwsgi через pip:
* pip install uwsgi
и также поставить supervisor через пакетный менеджер (если debian-like, то через apt-get)
* apt-get install supervisor

Необходимо изменить пути до проекта в конфигах: invoicetome_supervisor.conf и uwsgi.ini
и сделать линк конфига invoicetome_supervisor.conf в папку /etc/supervisor/conf.d

Внимание! Нужно убедиться, что в корне проекта созданы папки logs/ и run/

Если конфиги настроены правильно, то можно запустить консоль супервизора командой:
sudo supervicorctl 
и в этой консоли сделать старт проекта:
* reread
* update
* start invoicetome


TODO
=====
 
Вопросы
==========

