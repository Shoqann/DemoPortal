from datetime import datetime, timedelta
import secrets
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import Employee, DepartureEvent
from .forms import EmployeeRegistrationForm, DepartureEventForm


DEFAULT_MULTIPLIERS = {
    DepartureEvent.TYPE_RESIGNATION: 1.0,
    DepartureEvent.TYPE_MATERNITY: 1.0,
    DepartureEvent.TYPE_RETIREMENT: 1.0,
    DepartureEvent.TYPE_DISMISSAL_VIOLATION: 1.0,
    DepartureEvent.TYPE_DISMISSAL_CERT: 1.0,
    DepartureEvent.TYPE_OTHER: 1.0,
}

TYPE_META = {
    DepartureEvent.TYPE_RESIGNATION: {
        'title': 'Увольнение по собственному желанию',
        'description': 'Сохраните заявление сотрудника и дату последнего рабочего дня.',
        'success': 'Заявление об увольнении добавлено',
        'icon': 'fa-sign-out-alt',
    },
    DepartureEvent.TYPE_MATERNITY: {
        'title': 'Декрет / отпуск по уходу',
        'description': 'Запишите сотрудника, дату ухода и комментарий по замещению.',
        'success': 'Декретный отпуск добавлен',
        'icon': 'fa-baby',
    },
    DepartureEvent.TYPE_RETIREMENT: {
        'title': 'Выход на пенсию',
        'description': 'Зафиксируйте планируемый уход сотрудника на пенсию.',
        'success': 'Запись о выходе на пенсию добавлена',
        'icon': 'fa-cake-candles',
    },
    DepartureEvent.TYPE_DISMISSAL_VIOLATION: {
        'title': 'Увольнение за нарушения',
        'description': 'Укажите дату решения и основание по дисциплинарным нарушениям.',
        'success': 'Увольнение по нарушению добавлено',
        'icon': 'fa-exclamation-triangle',
    },
    DepartureEvent.TYPE_DISMISSAL_CERT: {
        'title': 'Увольнение по аттестации',
        'description': 'Сохраните итог аттестации и дату кадрового решения.',
        'success': 'Увольнение по аттестации добавлено',
        'icon': 'fa-clipboard-list',
    },
    DepartureEvent.TYPE_OTHER: {
        'title': 'Другая причина',
        'description': 'Используйте для случаев, которые не подходят под основные категории.',
        'success': 'Запись добавлена',
        'icon': 'fa-file-circle-plus',
    },
}


def parse_date(s):
    if not s:
        return None
    return datetime.fromisoformat(s).date()


def build_username(first_name, last_name):
    base = f"{first_name.strip().lower()}.{last_name.strip().lower()}"
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base}{counter}"
    return username


def calculate_hiring_needs(start_date=None, end_date=None):
    qs = DepartureEvent.objects.all()
    if start_date and end_date:
        qs = qs.filter(date__range=(start_date, end_date))
    elif start_date:
        qs = qs.filter(date__gte=start_date)
    elif end_date:
        qs = qs.filter(date__lte=end_date)

    counts = {item['type']: item['count'] for item in qs.values('type').annotate(count=Count('id'))}
    needs = {}
    total_departures = 0
    total_hires = 0

    for type_code, type_name in DepartureEvent.TYPE_CHOICES:
        count = counts.get(type_code, 0)
        hires_needed = int(round(count * DEFAULT_MULTIPLIERS.get(type_code, 1.0)))
        needs[type_code] = {
            'name': type_name,
            'count': count,
            'hires_needed': hires_needed,
        }
        total_departures += count
        total_hires += hires_needed

    return needs, total_departures, total_hires


def departure_context(start_date=None, end_date=None):
    hiring_needs, total_departures, total_hires = calculate_hiring_needs(start_date, end_date)
    departures = DepartureEvent.objects.select_related('employee').order_by('-date')
    if start_date and end_date:
        departures = departures.filter(date__range=(start_date, end_date))
    elif start_date:
        departures = departures.filter(date__gte=start_date)
    elif end_date:
        departures = departures.filter(date__lte=end_date)

    return {
        'departures': departures,
        'hiring_needs': hiring_needs,
        'stats_by_type': hiring_needs,
        'total_departures': total_departures,
        'total_hires': total_hires,
        'total_hires_needed': total_hires,
        'active_employees': Employee.objects.filter(is_active=True).count(),
        'today': timezone.now().date(),
    }


def save_departure_event(request, event_type, template_name):
    meta = TYPE_META[event_type]
    if request.method == 'POST':
        form = DepartureEventForm(request.POST)
        if form.is_valid():
            departure = form.save(commit=False)
            departure.type = event_type
            departure.save()
            messages.success(request, meta['success'])
            return redirect('ownReq')
    else:
        form = DepartureEventForm()

    recent_events = DepartureEvent.objects.filter(type=event_type).select_related('employee').order_by('-date')[:10]
    return render(request, template_name, {
        'form': form,
        'event_type': event_type,
        'meta': meta,
        'recent_events': recent_events,
    })


@require_GET
def hiring_need_api(request):
    """Return JSON with counts of departures and suggested hires."""
    start = parse_date(request.GET.get('start'))
    end = parse_date(request.GET.get('end'))

    qs = DepartureEvent.objects.all()
    if start and end:
        qs = qs.filter(date__range=(start, end))
    elif start:
        qs = qs.filter(date__gte=start)
    elif end:
        qs = qs.filter(date__lte=end)

    counts = {item['type']: item['count'] for item in qs.values('type').annotate(count=Count('id'))}

    multipliers = DEFAULT_MULTIPLIERS.copy()
    for t in multipliers.keys():
        k = f'mult_{t}'
        if k in request.GET:
            try:
                multipliers[t] = float(request.GET[k])
            except ValueError:
                pass

    result = []
    total_hires = 0
    for t, mult in multipliers.items():
        c = counts.get(t, 0)
        hires = int(round(c * mult))
        total_hires += hires
        result.append({'type': t, 'count': c, 'multiplier': mult, 'hires': hires})

    return JsonResponse({'period': {'start': start and str(start), 'end': end and str(end)}, 'by_type': result, 'total_hires': total_hires})


def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            username = build_username(employee.first_name, employee.last_name)
            password = secrets.token_urlsafe(8)
            user = User.objects.create_user(username=username, password=password)
            employee.user = user
            employee.save()
            return render(request, 'hr/register_success.html', {'employee': employee, 'username': username, 'password': password})
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'hr/register.html', {'form': form})


@login_required
def user_index(request):
    return render(request, 'hr/index.html')


@login_required
def dashboard(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=365)
    end_date = today + timedelta(days=90)
    
    context = departure_context(start_date, end_date)
    context.update({
        'start_date': start_date,
        'end_date': end_date,
    })
    return render(request, 'hr/dashboard.html', context)


@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'hr/logout.html')


@login_required
def leave_page(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=365)
    end_date = today + timedelta(days=90)
    context = departure_context(start_date, end_date)
    return render(request, 'hr/leave.html', context)


@login_required
def resignation(request):
   
    return save_departure_event(request, DepartureEvent.TYPE_RESIGNATION, 'hr/resignation.html')


@login_required
def decree(request):
    
    return save_departure_event(request, DepartureEvent.TYPE_MATERNITY, 'hr/decree.html')


@login_required
def pension(request):
    
    return save_departure_event(request, DepartureEvent.TYPE_RETIREMENT, 'hr/pension.html')


@login_required
def warnings(request):
    
    return save_departure_event(request, DepartureEvent.TYPE_DISMISSAL_VIOLATION, 'hr/warnings.html')


@login_required
def certification(request):
    
    return save_departure_event(request, DepartureEvent.TYPE_DISMISSAL_CERT, 'hr/certification.html')


@login_required
def other_departure(request):
    
    return save_departure_event(request, DepartureEvent.TYPE_OTHER, 'hr/other_departure.html')


@login_required
def requests(request):
    """View all departure requests"""
    context = departure_context()
    return render(request, 'hr/requests.html', context)


@login_required
def ownRequest(request):

    today = timezone.now().date()
    start_date = parse_date(request.GET.get('start')) or today - timedelta(days=365)
    end_date = parse_date(request.GET.get('end')) or today + timedelta(days=90)
    context = departure_context(start_date, end_date)
    context.update({
        'start_date': start_date,
        'end_date': end_date,
    })
    return render(request, 'hr/ownRequest.html', context)

@login_required
def all_records(request):
   
    context = departure_context()
    return render(request, 'hr/allRecords.html', context)
