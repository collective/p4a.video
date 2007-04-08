/* vpipit version 0.02 
 * - If text link, open in ThickBox
 * 
 * Initialize the containing DIV and store base information in aDIVs
 */
 
function vPIPIt() {
	if (typeof vPIPPlayer.isMovieFile == "function") {
	   var oLinks;
		var i, j;
		
	   oLinks = document.getElementsByTagName("a");
	   for (i = 0; i < oLinks.length; i++) {
	   		if (oLinks[i].onclick == undefined || oLinks[i].onclick == null) {
		   		var movieType = vPIPPlayer.isMovieFile(oLinks[i]);
			   	
		      	if (movieType != null) {
			      	if (movieType.sMediaFormat.length > 0) {
						var byImage = false;
		   				var children = oLinks[i].childNodes;
		   				var imgChild;
						for (j=0; j < children.length; j++) {
							if (children[j].nodeName.toLowerCase() == "img") {
								imgChild = children[j];
								byImage = true;
								break;
							}
						}
						if (byImage) {
							var videoWidth = imgChild.width;
							var videoHeight = imgChild.height;
							oLinks[i].onclick = new Function("vPIPPlay(this,'width=" + videoWidth + ",height=" + videoHeight + "'); return false;");
						}
						else {
							oLinks[i].onclick = new Function("vPIPPlay(this, '', '', 'active=true'); return false;");
						}
			      	}
				}
	   		}
		}
	}
}


function addEvent(obj, evType, fn){
	if (obj.addEventListener) {
		obj.addEventListener(evType, fn, false);
		return true;
	} else if (obj.attachEvent){
		var r = obj.attachEvent("on"+evType, fn);
		return r;
	} else {
		return false;
	}
}

//Run vPIPInit on body load
addEvent(window, 'load', vPIPIt);
