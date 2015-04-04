openerp.web_hw_collector = function(instance) {
    instance.web_hw_collector.HwCollector = instance.web.form.FieldChar.extend({
        template: "HwCollector",
        start: function() {
            var _this = this;
            this.render_value();
            self.$(".hw_collector_button").click(function() {
                _this.set_value('9');
                _this.render_value();
                _this.view.save();
            });
        },
    });

    instance.web.form.widgets.add("hw_collector", "instance.web_hw_collector.HwCollector");
}

