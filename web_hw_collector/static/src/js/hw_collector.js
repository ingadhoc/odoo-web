openerp.web_hw_collector = function(instance) {
    instance.web_hw_collector.HwCollector = instance.web.form.FieldChar.extend({
        template: "HwCollector",
        start: function() {
            var _this = this;
            this.render_value();

            var createCORSRequest = function(method, url) {
                var xhr = new XMLHttpRequest();
                if ("withCredentials" in xhr) {
                    xhr.open(method, url, true);
                } else if (typeof XDomainRequest != "undefined") {
                    xhr = new XDomainRequest();
                    xhr.open(method, url);
                } else {
                    xhr = null;
                }
                return xhr;
            };

            var corsCall = function(url, callback){
                var xhr = createCORSRequest('GET', url);
                xhr.onreadystatechange = function() {
                    if (xhr.status >= 200 && xhr.status < 400) {
                        var responseText = xhr.responseText;
                        callback(responseText);
                        // alert('CORS call completed at \'' + url + '\' returning: ' + responseText);
                    } else {
                        alert('Error while calling CORS at ' + url);
                    }
                };
                xhr.send();
            };

            self.$(".hw_collector_button").click(function() {
                var model = new instance.web.Model("ir.config_parameter");
                model.call("get_param", ['hw.proxy'], {context: new instance.web.CompoundContext()}).then(function(url) {
                    corsCall(url, function(value){
                        _this.set_value(value);
                        _this.render_value();
                        _this.view.save();
                    });
                });
            });
        },
    });

    instance.web.form.widgets.add("hw_collector", "instance.web_hw_collector.HwCollector");
}

