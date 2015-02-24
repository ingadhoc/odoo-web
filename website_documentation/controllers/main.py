# -*- coding: utf-8 -*-


from openerp import http
from openerp.http import request
from openerp.addons.website.models.website import slug


class WebsiteDoc(http.Controller):
    @http.route(['/doc/how-to', '/doc/how-to/<model("website.documentation.toc"):toc>'], type='http', auth="public", website=True)
    def toc(self, toc=None, **kwargs):
        cr, uid, context, toc_id = request.cr, request.uid, request.context, False
        if toc:
            sections = toc.child_ids
            # forum = toc.forum_id
        else:
            toc_obj = request.registry['website.documentation.toc']
            obj_ids = toc_obj.search(cr, uid, [('parent_id', '=', False)], context=context)
            sections = toc_obj.browse(cr, uid, obj_ids, context=context)
            # forum = sections and sections[0].forum_id or False
        value = {
            'toc': toc,
            'main_object': toc,
            # 'main_object': toc or forum,
            # 'forum': forum,
            'sections': sections,
        }
        return request.website.render("website_documentation.documentation", value)

    # @http.route(['''/doc/how-to/<model("website.documentation.toc"):toc>/<model("website.documentation.google_doc", "[('documentation_toc_id','=',toc[0])]"):google_doc>'''], type='http', auth="public", website=True)
    # # TODO ver cambiar nombre y hacer dos urls compatibles
    # # def google_doc_render(self, toc, google_doc, **kwargs):
    # def post(self, toc, google_doc, **kwargs):
    #     assert google_doc.documentation_toc_id.id == toc.id, "Wrong post!"
    #     value = {
    #         'toc': toc,
    #         'doc_code': google_doc,
    #         'main_object': google_doc,
    #         # 'forum': post.forum_id
    #     }
    #     return request.website.render("website_documentation.documentation_post", value)

    # Este es el que funciona
    @http.route(['''/doc/how-to/<model("website.documentation.toc"):toc>/<model("ir.ui.view", "[('documentation_toc_id','=',toc[0])]"):post>'''], type='http', auth="public", website=True)
    # @http.route(['''/doc/how-to/<model("website.documentation.toc"):toc>/<model("forum.post", "[('documentation_toc_id','=',toc[0])]"):post>'''], type='http', auth="public", website=True)
    def post(self, toc, post, **kwargs):
        # TODO: implement a redirect instead of crash
        assert post.documentation_toc_id.id == toc.id, "Wrong post!"
        value = {
            'toc': toc,
            'post': post,
            'main_object': post,
            # 'forum': post.forum_id
        }
        return request.website.render("website_documentation.documentation_post", value)

# TODO ver si implemetnamos Promote
    # @http.route('/doc/page/<model("ir.ui.view"):post>/promote', type='http', auth="user", website=True)
    # # @http.route('/doc/<model("forum.forum"):forum>/question/<model("forum.post"):post>/promote', type='http', auth="user", website=True)
    # def post_toc(self, forum, post, **kwargs):
    #     cr, uid, context, toc_id = request.cr, request.uid, request.context, False
    #     user = request.registry['res.users'].browse(cr, uid, uid, context=context)
    #     assert user.karma >= 200, 'You need 200 karma to promote a post to the documentation'
    #     toc_obj = request.registry['forum.documentation.toc']
    #     obj_ids = toc_obj.search(cr, uid, [], context=context)
    #     tocs = toc_obj.browse(cr, uid, obj_ids, context=context)
    #     value = {
    #         'post': post,
    #         # 'forum': post.forum_id,
    #         'chapters': filter(lambda x: not x.child_ids, tocs)
    #     }
    #     return request.website.render("website_documentation.promote_question", value)

    # TODO tal vez elimnar esta route que no vamos a usar o implemetnarla!
    # @http.route('/doc/<model("forum.forum"):forum>/promote_ok', type='http', auth="user", website=True)
    # def post_toc_ok(self, forum, post_id, toc_id, **kwargs):
    #     cr, uid, context = request.cr, request.uid, request.context
    #     user = request.registry['res.users'].browse(cr, uid, uid, context=context)
    #     assert user.karma >= 200, 'Not enough karma, you need 200 to promote a documentation.'

    #     toc_obj = request.registry['website.documentation.toc']
    #     stage_ids = toc_obj.search(cr, uid, [], limit=1, context=context)

    #     post_obj = request.registry['ir.ui.view']
    #     # post_obj = request.registry['forum.post']
    #     post_obj.write(cr, uid, [int(post_id)], {
    #         'documentation_toc_id': toc_id and int(toc_id) or False,
    #         'documentation_stage_id': stage_ids and stage_ids[0] or False
    #     }, context=context)
    #     return request.redirect('/doc/'+str(forum.id)+'/question/'+str(post_id))
