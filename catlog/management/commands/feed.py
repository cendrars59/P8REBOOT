#!/usr/local/bin/python3

from django.core.management.base import BaseCommand, CommandError

from .Database.dbRessources import connect
from .Utils.datafeed import feed_application


class Command(BaseCommand):
    help = 'Feeding heroku database'

    def handle(self, *args, **options):
        # Access to database to access to the data
        print("Check database credential")
        connection = connect()
        feed_application(connection)
        print('database creation & feed done')
