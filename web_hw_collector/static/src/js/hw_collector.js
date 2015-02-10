openerp.web_hw_collector = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.HwCollector = instance.Widget.extend(
        {
            start: function() {
                console.log("Hw Collector initialized");
            },
        }
    );
}

