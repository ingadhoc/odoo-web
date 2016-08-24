openerp.web_fixed_headers = function(instance) {
	
	var _lt = openerp.web._lt;
	var _t = openerp.web._t;
	
	instance.web.ListView.List.include({
		
		$table : null,
		$header : null,
		$fixWrapper : null,
		widthcol :[],
		topedit:null,
		
		init: function (group, opts) {
			this._super(group, opts);
			this.$table=this.view.$el.find('table.oe_list_content');
		},
		
		resize_list_content :function () {
			var self=this;
			if(this.$table.find('tbody:not(.oe_group_header) tr:not(.oe_group_header):first').children().size()>0) {
				var $active_view=$("div.oe_view_manager_current[data-view-type='list']");
				if($active_view.length) {
					var $tbody = this.$table.find('thead tr:first').children();
				    this.widthcol = $tbody.map(function() {
				        return $(this).width();
				    }).get();
					if($active_view.find('.oe_view_manager_view_list table.oe_list_header_custom:first').size()<1) {
						this.topedit=null;
						this.view.$el.prepend("<table class='oe_list_header_custom'></table>");
						var $headerTable=this.view.$el.find('table.oe_list_header_custom');
						$headerTable.css({"display":this.$table.css("display")});
						this.view.$el.append("<div class='fixedwrapper fixed_headers'></div>");
						this.$fixWrapper=this.view.$el.find('div.fixedwrapper');
						this.$fixWrapper.append(this.$table);	
						var $thead=this.$table.find('thead');
						$headerTable.append($thead.clone());
						$thead.css({'visibility':'collapse'});
						 $(".openerp .oe_view_manager_body").scroll(function () {
							 self.$fixWrapper.css({"left":$(this).scrollLeft()+"px"});
							 self.$fixWrapper.scrollLeft($(this).scrollLeft());
						 });
						 $('.oe_view_manager_view_list .oe_form_container:first').css({'z-index':'999','position':'absolute'});
						 $('div.fixedwrapper').scroll(function () {
							 $('.oe_view_manager_view_list .oe_form_container:first').css({'top':(-1*$('div.fixedwrapper').scrollTop())+"px"});
						 });
						 this.$table.find('thead').addClass('oe_collapse_invisibility');
					}
					
					this.$header=this.group.view.$el.find('table.oe_list_header_custom thead');
					this.$fixWrapper=this.view.$el.find('div.fixedwrapper');
					if(this.view.$el.parent().parent().get(0) !=undefined) {
						this.$fixWrapper.css({"height":this.view.$el.parent().parent().get(0).clientHeight-this.$header.height()-22,"width": "100%","position":"absolute"});
					}
					this.$header.find('tr').children().each(function(i, v) {
				    	if($(v).attr("width")!="1"){
				    		var node;
				    		if($(v).attr('class')==undefined){
				    			var text=$(v).text();
				    			$(v).text("");
				    			$(v).append("<div>"+text+"</div>");
				    		}
				    		node=$(v).children().first();
				    		var ajutsWidth=2;
				    		if(i==self.widthcol.length-1 && self.$fixWrapper.get(0).scrollHeight > self.$fixWrapper.innerHeight()){
				    			ajutsWidth=self.$fixWrapper.width()-self.$fixWrapper.get(0).clientWidth;
				    		}
				    		node.css({'width':self.widthcol[i]+ajutsWidth-2});
				    	}
				    });
				    
					this.$header.find('.oe_list_record_selector').click(function(){
						self.view.$el.find('.oe_list_record_selector input').prop('checked',
								self.view.$el.find('.oe_list_record_selector').prop('checked')  || false);
			            var selection = self.group.view.groups.get_selection();
			            $(self.view.groups).trigger(
			                'selected', [selection.ids, selection.records]);
			        });
				}
			} else {
				var self=this;
				window.setTimeout(function() {
		        	self.resize_list_content()
		        },500);
			}
		},
		
		render: function () {
	        this._super();
	        this.resize_list_content()	
	    }
	    
	});

}

