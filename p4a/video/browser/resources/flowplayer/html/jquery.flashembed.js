
/**
 * Copyright (c) 2008 Tero Piirainen (tero@flowplayer.org)
 *
 * $LastChangedDate: 12.03.2008
 * Version: 0.1.1 - 11.03.2008 
 */
(function($) { 
	
	// plugin initialization
	$.fn.extend({
		flashembed: function(params, flashvars) {  
			return this.each(function() {
				new $.flashembed(this, params, flashvars);
			});
		}		
	});
	
	// "constructor"
	// init is done as separate function for better "inheritance" support
	$.flashembed = function(el, params, flashvars) {  
		this.init(el, params, flashvars); 
	};
	
	
	$.extend($.flashembed.prototype, {
			
		init: function(el, params, flashvars) {
			
			// setup params
			var p = {
				src: '#',
				width: 320,
				height:240,
				expressInstall:null, 
				version:null, 
				
				allowfullscreen: true,
				allowscriptaccess: 'always',
				quality: 'high',
				bgcolor: '#ffffff',
				type: 'application/x-shockwave-flash',
				pluginspage: 'http://www.adobe.com/go/getflashplayer'
			};
			
			$.extend(p, params); 
			
			// fetch variables from params
			this.id = p.id;
			this.width = p.width;
			this.height = p.height;
			this.src = p.src; 
			this.version = this.getVersion();
			
			var required = p.version; 
			var express = p.expressInstall;
			p.width = p.id = p.height = p.src = p.version = p.expressInstall = null;
			
			this.params = p; 
			this.flashvars = flashvars;

			// is supported
			if (!required || this.isSupported(required)) {
				$(el).html(this.getHTML()).show();	
				
			// express install
			} else if (required && express && this.isSupported([6,0,65])) {
				
				$.extend(this.params, {src: express});
				
				this.flashvars =   {
					MMredirectURL: location.href,
					MMplayerType: 'PlugIn',
					MMdoctitle: $('title').text() 
				};
				
				$(el).html(this.getHTML()).show();	
				
			// not supported
			} else {
				
				el = $(el);
				if (el.html() != '') el.show();	
				else el.html(
					"<h2>Flash version " + required + " or greater is required</h2>" + 
					"<h3>" + (this.version[0] > 0 ? 
						"Your version is " +this.version : "You have no flash plugin installed") +
					"</h3>" + 
					"<p>Download latest version from <a href='" + this.params.pluginspage + "'>here</a></p>"
				);
			}
		},
		
		
		isSupported: function(version) {
			var my = this.version;
			return my[0] >= version[0] && my[1] >= version[1] && (my[2] == null || my[2] >= version[2]);				 
		},
		
		getHTML: function() {
			
			var html = "";
			
			// mozilla
			if (navigator.plugins && navigator.mimeTypes && navigator.mimeTypes.length) {  
	
				html = '<embed type="application/x-shockwave-flash" ';
				
				var params = {width:this.width, height:this.height, src:this.src, id:this.id};
				$.extend(params, this.params);
				
				for(var key in params) { 
					if (params[key] != null) 
						html += [key] + '="' +params[key]+ '"\n\t'; 
				}
				
				if (this.flashvars) {
					html += 'flashvars=\'';
					for(var key in this.flashvars) { 
						html += [key] + '=' + this.asString(this.flashvars[key]) + '&'; 
					}			
					html += '\'';
				}
				
				html += '/>';
				
			// ie
			} else { 

				html = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" ';
				html += 'width="' + this.width + '" height="' + this.height + '"'; 
				if (this.id) html += ' id="' + this.id + '"';
				html += '>';  
				html += '\n\t<param name="movie" value="'+ this.src +'" />';
				
				for(var key in this.params) {
					if (this.params[key] != null) 
						html += '\n\t<param name="'+ key +'" value="'+ this.params[key] +'" />';
				}
				
				if (this.flashvars) {
					html += '\n\t<param name="flashvars" value=\'';
					for(var key in this.flashvars) { 
						html += [key] + '=' + this.asString(this.flashvars[key]) + '&'; 
					}			
					html += '\' />';
				}

				html += "</object>"; 
			}

			return html;
		},
		
		// arr[major, minor, fix]
		getVersion: function() {
	
			var version = [0, 0];
			
			if (navigator.plugins && typeof navigator.plugins["Shockwave Flash"] == "object") {
				var _d = navigator.plugins["Shockwave Flash"].description;
				if (typeof _d != "undefined") {
					_d = _d.replace(/^.*\s+(\S+\s+\S+$)/, "$1");
					var _m = parseInt(_d.replace(/^(.*)\..*$/, "$1"), 10);
					var _r = /r/.test(_d) ? parseInt(_d.replace(/^.*r(.*)$/, "$1"), 10) : 0;
					version = [_m, _r];
				}
				
			} else if (window.ActiveXObject) {
				
				try { // avoid fp 6 crashes
					var _a = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
					
				} catch(e) {
					try { 
						var _a = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");
						version = [6, 0];
						_a.AllowScriptAccess = "always"; // throws if fp < 6.47 
						
					} catch(e) {
						if (version[0] == 6) return;
					}
					try {
						var _a = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
					} catch(e) {
					
					}
					
				}
				
				if (typeof _a == "object") {
					var _d = _a.GetVariable("$version"); // bugs in fp 6.21 / 6.23
					if (typeof _d != "undefined") {
						_d = _d.replace(/^\S+\s+(.*)$/, "$1").split(",");
						version = [parseInt(_d[0], 10), parseInt(_d[2], 10)];
					}
				}
			}
			
			return version;
	
		},
		
		
		// JSON.asString() function
		asString: function(obj) {
			
			var self = this;
			
			switch (typeOf(obj)){
				case 'string':
					return '"'+obj.replace(new RegExp('(["\\\\])', 'g'), '\\$1')+'"';
				case 'array':
					return '['+ $.map(obj, function(el) {
						return self.asString(el);
					}).join(',') +']';
				case 'object':
					var str = [];
					for (var property in obj) {
						
						str.push('"'+property+'":'+self.asString(obj[property])); 
					}
					return '{'+str.join(',')+'}';
			}
			return String(obj);
		}
		
	});

	
	// private functions
	function typeOf(obj){
		if (obj === null || obj === undefined) return false;
		var type = typeof obj;
		return (type == 'object' && obj.push) ? 'array' : type;
	};
	
	
	// version 9 bugfix: (http://blog.deconcept.com/2006/07/28/swfobject-143-released/)
	if (window.attachEvent) {
		window.attachEvent("onbeforeunload", function(){
			__flash_unloadHandler = function() {};
			__flash_savedUnloadHandler = function() {};
		});
	} 
	
})(jQuery);

