# -*- coding: utf-8 -*-
from openerp import models, fields
# TODO cambiar abajo y borrar
from openerp.osv import osv


class Documentation(models.Model):
    _name = 'website.documentation.toc'
    _description = 'Documentation ToC'
    _inherit = ['website.seo.metadata']
    _order = "parent_left"
    _parent_order = "sequence, name"
    _parent_store = True

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    # TODO master remove me
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    sequence = fields.Integer(
        'Sequence'
        )
    name = fields.Char(
        'Name',
        required=True,
        translate=True
        )
    parent_id = fields.Many2one(
        'website.documentation.toc',
        'Parent Table Of Content',
        ondelete='cascade'
        )
    child_ids = fields.One2many(
        'website.documentation.toc',
        'parent_id',
        'Children Table Of Content'
        )
    parent_left = fields.Integer(
        'Left Parent',
        select=True
        )
    parent_right = fields.Integer(
        'Right Parent',
        select=True
        )
    # page_ids = fields.One2many(
    #     'ir.ui.view',
    #     'documentation_toc_id',
    #     'Pages',
    #     domain=[('page', '=', True), ('type', '=', 'qweb')],
    #     context={'default_page': True, 'default_type': 'qweb'},
    #     )
    google_doc_ids = fields.One2many(
        'website.documentation.google_doc',
        'documentation_toc_id',
        'Google Docs',
        )

    _constraints = [
        (osv.osv._check_recursion,
            'Error ! You cannot create recursive categories.', ['parent_id'])
    ]


class Google_doc(models.Model):
    _name = 'website.documentation.google_doc'
    _description = 'website.documentation.google_doc'

    name = fields.Char('Name', required=True)
    doc_code = fields.Char('Document Code', required=True)
    documentation_toc_id = fields.Many2one(
        'website.documentation.toc',
        'Documentation ToC',
        ondelete='set null'
        )


# class Page(models.Model):
#     _inherit = 'ir.ui.view'
#     documentation_toc_id = fields.Many2one(
#         'website.documentation.toc',
#         'Documentation ToC',
#         ondelete='set null'
#         )
