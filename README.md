## Веб-приложение для загрузки в БД типовых deals.csv файлов и выгрузки данных через API в соответствии с ТЗ.


### Данное приложение позволяет:
* принимать из POST-запроса и через форму на сайте .csv файлы для дальнейшей обработки;
* обрабатывать типовые deals.csv файлы, содержащие истории сделок;
* сохранять извлеченные из файла данные в БД проекта;
* возвращать обработанные данные в ответе на GET-запрос по адресу http://127.0.0.1:8000/api/get_top5, в соответствии с условиями задания.


### О проекте:
Приложение написано на фреймворке Django. API реализовано при помощи Django Rest Framework. 
Для хранения данных использована PostgreSQL.
Проект контейнеризирован в Docker с использованием Docker Compose. 
Проект не использует глобальных зависимостей за исключением:  python, docker, docker-compose.
Файл с данными (deals.csv) для тестирования работы приложения находится в коревом каталоге
Файл с ТЗ находится в корневом каталоге.


### **Для запуска проекта, необходимо**:

* открыть корневую директорию проекта в терминале python

* запустить проект с помощью команды ***docker-compose up***

* При первом запуске создать необходимые таблицы в БД с помощью команды ***docker-compose exec web python manage.py migrate --noinput***

* открыть стартовую страницу в браузере по адресу http://127.0.0.1:8000

