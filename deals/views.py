from django.db import ProgrammingError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import Deals
from rest_framework.response import Response


def index(request):
    return render(request, 'deals/index.html')


def view_table(request):
    all_deals = Deals.objects.all()
    data = {'all_deals': all_deals}
    return render(request, 'deals/view_table.html', data)


def upload_form(request):
    return render(request, 'deals/upload_file.html')


@api_view()
def get_top5(request):
    """Список из 5 клиентов, потративших наибольшую сумму за весь период.
       Значение полей:
        * username - логин клиента;
        * spent_money - сумма потраченных средств за весь период;
        * gems - список из названий камней, которые купили как минимум двое из списка "5 клиентов,
          потративших наибольшую сумму за весь период", и данный клиент является одним из этих покупателей.
    """
    # получаем queryset с ТОП 5 покупателей по сумме за все время.
    top5_queryset = Deals.objects.values('customer').annotate(total=Sum('total')).order_by('-total')[:5]
    result = {'Response': []}
    list_customers = []
    for object in top5_queryset:
        result['Response'].append({'username': object['customer']})
        result['Response'][-1].update({'spent_money': object['total']})
        list_customers.append(object['customer'])

    # выбираем из queryset-объекта списки купленных камней по каждому из ТОП 5 покупателей и фомируем словарь
    # где ключ - customer, значение - список всех купленных им камней.
    all_gems_queryset = Deals.objects.extra(where=[f'customer IN{tuple(list_customers)}']).distinct(
        'customer', 'item')
    dict_gems = {}
    for object in all_gems_queryset:
        dict_gems.update({getattr(object, 'customer'): []})
    for object in all_gems_queryset:
        if getattr(object, 'customer') in dict_gems:
            dict_gems[getattr(object, 'customer')].append(getattr(object, 'item'))

    # выбираем из dict_gems названия камней, которые купили как минимум двое из списка "5 клиентов,
    # потративших наибольшую сумму за весь период".
    popular_gems = {}
    for key, value in dict_gems.items():
        for gem in value:
            if gem not in popular_gems:
                popular_gems.update({gem: 1})
            else:
                popular_gems[gem] += 1

    for item in result['Response']:
        item['gems'] = []
        for gem in dict_gems[item['username']]:
            if popular_gems[gem] > 1:
                item['gems'].append(gem)
    # Возвращаем результат обработки через форму Django Rest Framework
    return Response(result)


@csrf_exempt
def upload_file(request):
    """Функция обоработки POST-запроса, для парсинга и загрузки файла в БД"""
    try:
        if request.method == "POST":
            file_name = list(request.FILES.keys())[0]
            uploaded_file = request.FILES[file_name].file
            next(uploaded_file)
            for row in uploaded_file:
                row = row.decode('utf-8').strip().split(',')
                new_row = Deals(
                    customer=row[0],
                    item=row[1],
                    total=row[2],
                    quantity=row[3],
                    date=row[4]
                )
                new_row.save()
            return HttpResponse(f'Status: OK - файл был обработан без ошибок')
    except IndexError:
        return HttpResponse(f'Status: Error, Desc: файл не был прикреплен к запросу, или формат файла не '
                            f'соответствует типовому')
    except UnicodeDecodeError:
        return HttpResponse(f'Status: Error, Desc: неверный тип файла (ожидается тип .csv)')
    except ValueError:
        return HttpResponse(f'Status: Error, Desc: неверный формат данных в файле')
    except ProgrammingError:
        return HttpResponse(f'Status: Error, Desc: таблицы не были созданы в БД. Для создания таблиц, в '
                            f'командной строке введите:  docker-compose exec web python manage.py migrate --noinput')
