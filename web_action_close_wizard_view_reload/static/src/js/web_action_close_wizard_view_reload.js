openerp.web_action_close_wizard_view_reload = function(instance) {
    instance.web.ActionManager = instance.web.ActionManager.extend({
        ir_actions_act_window_close: function (action, options) {
            // action close es llamado desde wizards pero tmb desde botones
            // que no devuelve acciones, el tema es que no anda bien
            // para vista tree cuando no hay dialog (es decir cuando no 
            // volvemos desde wizard, como no se como arreglarlo, entonce
            // desactivamos cuando no viene de wizard para la tree)
            var dialog = true
            if (!this.dialog) {
                options.on_close();
                var dialog = false
            }
            this.dialog_stop();
            // do_reload es para kanban, reload para list
            // sacamos un poco de codigo de web_auto_refresh
            var active_view = this.inner_widget.active_view
            var controller = this.inner_widget.views[active_view].controller
            if (active_view == "kanban"){
                    controller.do_reload();
                }
                else if (active_view == "list" && dialog) {
                    controller.reload();
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