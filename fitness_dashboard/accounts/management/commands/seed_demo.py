from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Coach, Client, User
from core.models import AppConfiguration, CoachModuleAccess, Module
from subscription.models import Subscription


class Command(BaseCommand):
    help = 'Seed the database with sample super admin, coach, modules, subscriptions, and app configuration.'

    def handle(self, *args, **options):
        super_admin, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'superadmin@example.com',
                'role': 'SUPER_ADMIN',
                'first_name': 'Super',
                'last_name': 'Admin',
            },
        )
        if created:
            super_admin.set_password('SuperAdmin123!')
            super_admin.save()
            self.stdout.write(self.style.SUCCESS('Created Super Admin account.'))
        else:
            self.stdout.write(self.style.WARNING('Super Admin account already exists.'))

        coach_user, created = User.objects.get_or_create(
            username='coachuser',
            defaults={
                'email': 'coach@example.com',
                'role': 'COACH',
                'first_name': 'Coach',
                'last_name': 'User',
            },
        )
        if created:
            coach_user.set_password('Coach123!')
            coach_user.save()
            self.stdout.write(self.style.SUCCESS('Created Coach user account.'))
        else:
            self.stdout.write(self.style.WARNING('Coach user account already exists.'))

        coach, _ = Coach.objects.get_or_create(user=coach_user)

        for code, name in [
            ('CONFIG', 'App Configuration'),
            ('DIET', 'Diet'),
            ('FITNESS', 'Fitness'),
            ('ANALYTICS', 'Analytics'),
            ('SUBSCRIPTION', 'Subscription'),
            ('COACH', 'Coach'),
            ('USER', 'User'),
            ('TRACKER', 'Tracker'),
        ]:
            module, created_module = Module.objects.get_or_create(code=code, defaults={'name': name})
            if created_module:
                self.stdout.write(self.style.SUCCESS(f'Created module: {name}'))
            CoachModuleAccess.objects.get_or_create(coach=coach, module=module, defaults={'is_enabled': code in ('DIET', 'FITNESS', 'TRACKER', 'USER')})

        Subscription.objects.get_or_create(
            coach=coach,
            plan_name='Standard',
            defaults={
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timezone.timedelta(days=30)).date(),
                'status': 'ACTIVE',
            },
        )

        AppConfiguration.objects.get_or_create(
            key='site_name',
            defaults={
                'value': 'Fitness Dashboard',
                'description': 'The public site title for the fitness dashboard.',
                'is_active': True,
            },
        )

        self.stdout.write(self.style.SUCCESS('Seed data has been created or already exists.'))
