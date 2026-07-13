from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Creates a demo user with sample tasks for portfolio purposes"

    def handle(self, *args, **kwargs):
        username = "demo"
        password = "demo12345"

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}'"))
        else:
            self.stdout.write(f"User '{username}' already exists")

        # Clear old demo tasks so re-running this command doesn't duplicate
        Task.objects.filter(user=user).delete()

        today = date.today()

        demo_tasks = [
            {
                "title": "طراحی وایرفریم صفحه اصلی",
                "description": "طراحی اولیه رابط کاربری برای صفحه اصلی سایت",
                "priority": "HIGH",
                "due_date": today - timedelta(days=2),
                "completed": False,
            },
            {
                "title": "پیاده‌سازی سیستم لاگین",
                "description": "اتصال فرم ورود به بک‌اند و اعتبارسنجی",
                "priority": "HIGH",
                "due_date": today + timedelta(days=1),
                "completed": False,
            },
            {
                "title": "نوشتن مستندات API",
                "description": "مستندسازی endpointهای پروژه برای تیم فرانت‌اند",
                "priority": "MEDIUM",
                "due_date": today + timedelta(days=5),
                "completed": False,
            },
            {
                "title": "تست واحد برای ماژول پرداخت",
                "description": "نوشتن unit testها برای بخش پرداخت",
                "priority": "MEDIUM",
                "due_date": today + timedelta(days=10),
                "completed": False,
            },
            {
                "title": "راه‌اندازی دیتابیس اولیه",
                "description": "ساخت مدل‌ها و مایگریشن اولیه",
                "priority": "LOW",
                "due_date": today - timedelta(days=10),
                "completed": True,
            },
            {
                "title": "بررسی و رفع باگ صفحه پروفایل",
                "description": "رفع مشکل نمایش اطلاعات کاربر",
                "priority": "LOW",
                "due_date": today - timedelta(days=5),
                "completed": True,
            },
            {
                "title": "بهینه‌سازی سرعت لود صفحات",
                "description": "کاهش زمان بارگذاری با کش کردن کوئری‌ها",
                "priority": "MEDIUM",
                "due_date": today + timedelta(days=15),
                "completed": False,
            },
        ]

        for task_data in demo_tasks:
            Task.objects.create(user=user, **task_data)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(demo_tasks)} demo tasks for user '{username}'")
        )