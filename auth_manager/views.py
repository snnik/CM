import logging
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.conf import settings
from .forms import AuthForm
# TODO проверить не рендериться авторизация

logger = logging.getLogger(__name__)


def login(request):
    context = {}
    request.session.set_expiry(settings.PASSWORD_BLOCK_SESSION)
    form = AuthForm()
    context['form'] = form
    incorrect = request.session.get('incorrect', 0)
    if incorrect >= 5:
        login_error = 'Работа запрещена!'
        context = {'login_error': login_error}
    else:
        if request.method == 'POST':
            form = AuthForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['login']
                password = form.cleaned_data['password']
                user = auth.authenticate(username=username, password=password)
                logger.info('{d}. Попытка аторизации пользователя {u}'.format(d=datetime.datetime.now(), u=username))
                if user is not None:
                    auth.login(request, user)
                    request.session.set_expiry(0)
                    logger.info("{d} Пользователь {u} успешно авторизовался.".format(d=datetime.datetime.now(), u=str(user)))
                    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                else:
                    request.session['incorrect'] = incorrect + 1
                    login_error = 'Сожалеем, вы неправильно ввели логин или пароль. Осталось попыток:' + str(5-incorrect)
                    logger.error("{d} Ошибка при авторизации пользователя {u}. "
                                 "Осталось попыток: {n}".format(d=datetime.datetime.now(), u=str(user), n=str(5-incorrect)))
                    context = {'login_error': login_error}
    return render(request, 'auth_manager/login_form.html', context)


def logout(request):
    logger.info("{d} Пользователь {u} завершил работу.".format(d=datetime.datetime.now(), u=str(request.user)))
    auth.logout(request)
    return HttpResponseRedirect('/login')
