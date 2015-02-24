openerp.web_hw_collector = function(instance) {
    instance.web_hw_collector.HwCollector = instance.web.form.FieldChar.extend({
        template: "HwCollector",
        start: function() {
            var _self = self;
            self.$(".hw_collector_button").click(function() {
                alert('a');
            });
        },
    });

    instance.web.form.widgets.add("hw_collector", "instance.web_hw_collector.HwCollector");
}

