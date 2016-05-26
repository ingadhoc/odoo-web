openerp.web_list_view_sticky = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    //Sticky Table Header
    instance.web.ListView.include({
        load_list: function () {
            var self = this;
            self._super.apply(this, arguments);
            var one2many_length = self.$el.parents('.oe_form_field.oe_form_field_one2many').length;
            var scrollArea = self.$el.parents('.oe_view_manager.oe_view_manager_current').find('.oe_view_manager_wrapper .oe_view_manager_body')[0];
            if(scrollArea &&  one2many_length == 0){
                self.$el.find('table.oe_list_content').each(function(){
                    $(this).stickyTableHeaders({scrollableArea: scrollArea})
                });
            }
        },
    });
};