openerp.web_hw_collector = function(instance) {
    instance.web_hw_collector.HwCollector = instance.web.form.FieldChar.extend({
        template: "HwCollector",
        start: function() {
            this.$el.append("<div>Hello dear Odoo user!</div>");
        },
    });

    instance.web.form.widgets.add("hw_collector", "instance.web_hw_collector.HwCollector");
}

