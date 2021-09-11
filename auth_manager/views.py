from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
import logging
import datetime


logger = logging.getLogger(__name__)


def login(request):
    context = {}
    request.session.set_expiry(settings.PASSWORD_BLOCK_SESSION)
    incorrect = request.session.get('incorrect', 0)
    if incorrect >= 5:
        login_error = 'Работа запрещена!'
        context = {'login_error': login_error}
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            logger.warning('{d}. i Попытка аторизации пользователя {u}'.format(d=datetime.datetime.now(),
                                                                               u=username))
            # if user and not user.last_login:
            #     change_password = True
            # else:
            #     change_password = False
            if user is not None:
                auth.login(request, user)
                request.session.set_expiry(0)
                # if change_password:
                #     return redirect(reverse('change_pass'))
                # else:
                #     return HttpResponseRedirect('/')

                # Заменить после всех правок
                logger.warning("{d} i Пользователь {u} успешно авторизовался.".format(d=datetime.datetime.now(),
                                                                                      u=str(user)))
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                request.session['incorrect'] = incorrect + 1
                login_error = 'Сожалеем, вы неправильно ввели логин или пароль. Осталось попыток:' + str(5-incorrect)
                print("Ошибка при авторизации пользователя " + str(user) + ". Осталось попыток:" + str(5-incorrect))
                logger.error("{d} e Ошибка при авторизации пользователя {u}. "
                             "Осталось попыток: {n}".format(d=datetime.datetime.now(), u=str(user), n=str(5-incorrect)))
                context = {'login_error': login_error}
    return render(request, 'auth_manager/login_form.html', context)


def logout(request):
    logger.warning("{d} i Пользователь {u} завершил работу.".format(d=datetime.datetime.now(), u=str(request.user)))
    auth.logout(request)
    return HttpResponseRedirect('/login')
