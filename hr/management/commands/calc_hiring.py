from django.core.management.base import BaseCommand
from django.db.models import Count

from hr.models import DepartureEvent


DEFAULT_MULTIPLIERS = {
    'resignation': 1.0,
    'maternity': 1.0,
    'retirement': 1.0,
    'dismissal_violation': 1.0,
    'dismissal_cert': 1.0,
    'other': 1.0,
}


class Command(BaseCommand):
    help = 'Calculate hiring need for a date range'

    def add_arguments(self, parser):
        parser.add_argument('--start', type=str, help='Start date YYYY-MM-DD')
        parser.add_argument('--end', type=str, help='End date YYYY-MM-DD')
        for t in DEFAULT_MULTIPLIERS:
            parser.add_argument(f'--mult_{t}', type=float, help=f'Multiplier for {t}')

    def handle(self, *args, **options):
        qs = DepartureEvent.objects.all()
        if options.get('start') and options.get('end'):
            qs = qs.filter(date__range=(options['start'], options['end']))
        elif options.get('start'):
            qs = qs.filter(date__gte=options['start'])
        elif options.get('end'):
            qs = qs.filter(date__lte=options['end'])

        counts = {item['type']: item['count'] for item in qs.values('type').annotate(count=Count('id'))}

        total = 0
        lines = []
        for t, default in DEFAULT_MULTIPLIERS.items():
            mult = options.get(f'mult_{t}') or default
            c = counts.get(t, 0)
            hires = int(round(c * mult))
            total += hires
            lines.append(f"{t}: count={c}, mult={mult}, hires={hires}")

        for l in lines:
            self.stdout.write(l)
        self.stdout.write(f"Total hires: {total}")
