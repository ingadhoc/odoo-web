# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models


class ir_actions_act_close_wizard_and_reload_view(models.Model):
    _name = 'ir.actions.act_close_wizard_and_reload_view'
    _inherit = 'ir.actions.actions'
    _table = 'ir_actions'
    _defaults = {
        'type': 'ir.actions.act_close_wizard_and_reload_view',
    }
