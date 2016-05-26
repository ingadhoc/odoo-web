# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import logging

import werkzeug.utils
import werkzeug.wrappers

import openerp
from openerp import http
# from openerp import http, exceptions
from openerp.http import request
from openerp.tools.translate import _

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

        if request.session.uid:
            if kw.get('redirect'):
                return werkzeug.utils.redirect(kw.get('redirect'), 303)
            if not request.uid:
                request.uid = request.session.uid

            menu_data = request.registry['ir.ui.menu'].load_menus(
                request.cr, request.uid, context=request.context
            )
            return request.render(
                'login_serial.webclient_bootstrap',
                qcontext={'menu_data': menu_data}
            )
        else:
            return login_redirect()

    @http.route('/login_serial/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        if (request.httprequest.method == 'GET' and
                redirect and
                request.session.uid):
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid

            serial_id = request.params['serial_id']
            partner_obj = request.registry.get('res.partner')
            user_vals = partner_obj.search_read(
                request.cr, openerp.SUPERUSER_ID,
                [('serial_id', '=', serial_id)],
                ['id', 'login']
            )
            if user_vals:
                login = user_vals[0]['login']
                password = serial_id
                uid = request.session.authenticate(
                    request.session.db, login, password
                )
                if uid is not False:
                    return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = _('Wrong Serial Id')

        return request.render('login_serial.login', values)
