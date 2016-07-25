# encoding: UTF-8
from __future__ import with_statement

import logging
from optparse import make_option
from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand, CommandError
from membership.models import BillingCycle
from membership.billing import pdf_utils

logger = logging.getLogger("paper_bills")

class Command(BaseCommand):
    args = ''
    help = 'Create paper reminders pdf'
    option_list = BaseCommand.option_list + (
        make_option('--member',
            dest='member',
            default=None,
            help='Create pdf-reminder for user'),
        )

    def handle(self, *args, **options):
        try:
            with NamedTemporaryFile(suffix=".pdf", prefix='sikteeri', delete=False) as target_file:

                pdfcontent = BillingCycle.get_pdf_reminders(memberid=options['member'])
                target_file.write(pdfcontent)
                target_file.close()
                pdffile = target_file.name

            if pdffile:
                print("pdf file created: {0}".format(pdffile))
            else:
                print("Cannot create pdffile")
        except RuntimeError as e:
            raise CommandError(e)
