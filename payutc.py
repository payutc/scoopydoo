#!/usr/bin/env python
# -*- coding: utf-8 -*-

from payutc_json_client import *
import conf

class Payutc(PayutcJsonClient):

    """ Surclasse du client json avec du syntaxic sugar pour quelques fonctions """

    def __init__(self, service="POSS3"):
        super(Payutc, self).__init__(conf.PAYUTC_URL, service, conf.PAYUTC_USER_AGENT)

    def get_cas_url(self):
        return self.call("getCasUrl")

    def login_app(self):
        print conf.APP_KEY
        return self.call("loginApp", key=conf.APP_KEY)

    def login(self, ticket, service):
        return self.call("loginCas", ticket=ticket, service=service)

    def get_funs(self):
        funs = self.call("getFundations")
        return [fun for fun in funs if fun["fun_id"] is not None]

    

