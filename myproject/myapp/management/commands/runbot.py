from django.core.management.base import BaseCommand
from myapp.bot import bot


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        bot.polling(none_stop=True, interval=0)
