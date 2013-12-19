# -*- coding: utf-8 -*-

"""
Updater for https://dnsimple.com/ compatible dyndns services. This module
depends on the python package dnsimple-dyndns from
https://pypi.python.org/pypi/dnsimple-dyndns
If installed, dyndnsc will be able to utilize it.

Since dnsimple.com is a paid service, I have not had a chance to test this yet.
"""

import logging

from dnsimple_dyndns import DNSimple

log = logging.getLogger(__name__)


class UpdateProtocolDnsimple(object):
    """Protocol handler for https://dnsimple.com/"""

    def __init__(self, options):
        self.theip = None
        self._recordname, _, self._domain = options['hostname'].partition(".")
        self.handler = DNSimple(domain=self._domain,
                                domain_token=options['key'])
        if 'url' in options:
            # The url must be a format string like this:
            #      'https://dnsimple.com/domains/%s/records'
            self.handler._baseurl = options['url'] % self._domain

    @staticmethod
    def configuration_key():
        return "dnsimple"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        return self.handler.update_record(name=self._recordname,
                                          address=self.theip)
