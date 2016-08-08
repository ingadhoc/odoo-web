openerp.web_action_close_wizard_view_reload = function(instance) {
    instance.web.ActionManager = instance.web.ActionManager.extend({
        ir_actions_act_window_close: function (action, options) {
            if (!this.dialog) {
                options.on_close();
            }
            this.dialog_stop();
            // do_reload es para kanban, reload para list
            // sacamos un poco de codigo de web_auto_refresh
            var active_view = this.inner_widget.active_view
            if (active_view == "kanban"){
                    this.inner_widget.views[active_view].controller.do_reload();
                }
                else {
                    this.inner_widget.views[active_view].controller.reload();
                }
            return $.when();
        },
    });
}
// esta era la otra alternativa usando bus
// openerp.web_action_close_wizard_view_reload = function(instance) {
//     var bus = instance.bus.bus;
//     bus.add_channel("<CHANNEL-NAME>");
//     instance.bus.bus.on("notification", instance, function(notification){
//         instance.client.action_manager.inner_widget.views["kanban"].controller.do_reload();
//     });
// };