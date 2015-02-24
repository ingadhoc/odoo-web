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
    introduction = fields.Html(
        'Introduction',
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
    # post_ids = fields.One2many(
    #     'website.post',
    #     'documentation_toc_id',
    #     'Posts'
    #     )
    page_ids = fields.One2many(
        'ir.ui.view',
        'documentation_toc_id',
        'Pages',
        domain=[('page', '=', True), ('type', '=', 'qweb')],
        context={'default_page': True, 'default_type': 'qweb'},
        )
    # forum_id = fields.Many2one(
    #     'forum.forum',
    #     'Forum',
    #     required=True
    #     )

    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    ]


class Page(osv.Model):
    _inherit = 'ir.ui.view'
    documentation_toc_id = fields.Many2one(
        'website.documentation.toc',
        'Documentation ToC',
        ondelete='set null'
        )
# TODO tal ves tengamos que extender a las pages
# class Post(osv.Model):
#     _inherit = 'forum.post'

#     _columns = {
#         'documentation_toc_id': fields.many2one('forum.documentation.toc', 'Documentation ToC', ondelete='set null'),
#         'documentation_stage_id': fields.many2one('forum.documentation.stage', 'Documentation Stage'),
#         'color': fields.integer('Color Index')
#     }

#     def _get_default_stage_id(self, cr, uid, context=None):
#         stage_ids = self.pool["forum.documentation.stage"].search(cr, uid, [], limit=1, context=context)
#         return stage_ids and stage_ids[0] or False

#     _defaults = {
#         'documentation_stage_id': _get_default_stage_id,
#     }

#     def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
#         stage_obj = self.pool.get('forum.documentation.stage')
#         stage_ids = stage_obj.search(cr, uid, [], context=context)
#         result = stage_obj.name_get(cr, uid, stage_ids, context=context)
#         return result, {}

#     _group_by_full = {
#         'documentation_stage_id': _read_group_stage_ids,
#     }
