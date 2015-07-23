# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class website_menu(models.Model):
    _inherit = "website.menu"

    related_view_id = fields.Many2one(
        'ir.ui.view',
        compute='get_related_view',
        )
    group_ids = fields.Many2many(
        'res.groups',
        'website_menu_group_rel',
        'menu_id',
        'gid',
        'Groups',
        domain=[('is_portal', '=', True)],
        context={'default_is_portal': True},
        help="If you have groups, the visibility of this menu will be based\
        on these groups. "
        "If this field is empty, Odoo will compute visibility based on the\
        related object's read access.")

    @api.one
    @api.onchange('group_ids')
    def change_groups(self):
        if self.related_view_id and not self.related_view_id.groups_id:
            self.related_view_id.write(
                {'groups_id': [(6, False, self.group_ids.ids)]})

    @api.one
    @api.depends('url')
    def get_related_view(self):
        view = False
        page = self.url.split('/')
        page = page and page[-1] or False
        if page:
            if 'website.' not in page:
                page = 'website.' + page
            view = self.env['ir.model.data'].xmlid_to_object(page)
        self.related_view_id = view
