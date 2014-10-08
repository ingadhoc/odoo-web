# -*- coding: utf-8 -*-

import logging

import werkzeug.utils
import werkzeug.wrappers

import openerp
from openerp import http
from openerp.http import request

_logger = logging.getLogger(__name__)

def login_redirect():
    url = '/login_serial/login?'
    if request.debug:
        url += 'debug&'
    return """<html><head><script>
        window.location = '%sredirect=' + encodeURIComponent(window.location);
    </script></head></html>
    """ % (url,)

class Home(http.Controller):

    @http.route('/login_serial', type='http', auth="none")
    def web_login_serial(self, s_action=None, **kw):
        #ensure_db()

        _logger.info('request.session.uid: %s' % request.session.uid)
        if request.session.uid:
            if kw.get('redirect'):
                return werkzeug.utils.redirect(kw.get('redirect'), 303)
            if not request.uid:
                request.uid = request.session.uid

            menu_data = request.registry['ir.ui.menu'].load_menus(request.cr, request.uid, context=request.context)
            return request.render('login_serial.webclient_bootstrap', qcontext={'menu_data': menu_data})
        else:
            return login_redirect()

    @http.route('/login_serial/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        #ensure_db()

        _logger.info('request.session.uid: %s' % request.session.uid)
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        _logger.info('request.uid: %s' % request.uid)
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        _logger.info('values: %s' % values)
        _logger.info('redirect: %s' % redirect)
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect
        _logger.info('values: %s' % values)

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            _logger.info('no database')
            values['databases'] = None

        if request.httprequest.method == 'POST':
            _logger.info('reqiest method post')
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        
        _logger.info('to "login_serial.login", values: %s' % values)
        return request.render('login_serial.login', values)
