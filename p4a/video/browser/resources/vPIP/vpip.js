/* 
vPIP version 1.00c Beta 
* - jQuery calls changed from $(...) to jQuery(...) to not conflict with other 
* libraries like Lightbox
* - If vpipit function exists, call from vPIPPlayer.prototype.thickBox_remove to
* reinstate the automatic vPIP calls.

Installation and usage page starts at:  http://utilities.cinegage.com/videos-playing-in-place/

vPIP generates code from the hVlog format:
   <div class="hVlog">
      <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}}" {class="hVlogTarget"} onclick=?vPIPPlay(this, {...})?> 
	  	<img src="{url to image file}" />
	</a>...
    <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}}" onclick=?vPIPPlay(this, {...})?> 
	  	{Text description of movie type}
	</a>...
	<p>{Text on videoblog}</p>
   </div>
Note:  <a has the "onclick=..." to run vPIP:
      <a href="{url to videoblog file}" rel="enclosure" title="{title}" {type="video/{mime type}} 
	       onclick=onclick="vPIPShow({'width={width number including controller}, height={height number including controller},controller={true/false}, revert={true/false}...'})"> 

Acknowledgements
----------------
vPIP was originaly inspired in August, 2005 on seeing videos that popped into the location on 
Steve Garfields, http://stevegarfield.blogs.com/, vlog site.  The current version is partially 
based on input from Andreas Haugstrup, http://www.solitude.dk/ ,  and his script, video-link.js, 
and input from Josh Kinberg, http://fireant.tv/ .  Encouragement, testing and usage comes from 
the members of the videoblogging yahoo group, http://groups.yahoo.com/group/videoblogging/ .

March 2006

Copyright 2006  Enric Teller  (email: enric@cinegage.com)

    This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

ThickBox
--------
	
 Thickbox - One box to rule them all.
 By Cody Lindley (http://www.codylindley.com)
 Under an Attribution, Share Alike License
 Thickbox is built on top of the very light weight jquery library.

*/

/*
 * Replace the link with an embed of the media file (video or audio) 
 * 
 * @param oLink
 * 			The link that called vPIPPlay
 * @param sParam
 * 			The embed parameters
 * @param sFlashVars
 * 			Variables passed to flash player (either included -- cirneViewer.swf -- or specified)
 * @param sThickBox
 * 			ThickBox parameters
 * @param sJump
 * 			Time location to jump in movie
 * 
 */
function vPIPPlay(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump) {
	
	if (vpipPlayerRef == undefined || vpipPlayerRef == null) {
		var vpipPlayer = new vPIPPlayer(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump);
		//Allow vpipPlayer to be accessed from external functions
		vpipPlayerRef = vpipPlayer;
	}
	else {
		// Get the existing vPIPPlayer that can hold multiple vPIP containers.
		var vpipPlayer = vpipPlayerRef;
		vpipPlayer.setStartup(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump);
	}
	
	if (vpipPlayer.init()){
		vpipPlayer.show();
		
		return false;
	}
	else {
		if (vpipPlayer.oLink.href.toLowerCase().indexOf("http://") > -1)
			window.open(vpipPlayer.oLink.href, "_self");
		
		return true;	
	}
}

/* aDIV's array holds the DIVs that have been activated.
 * structure:
	[0]... divs
		[0] oDiv
		[1] DIVid
		[2] OrigHTML
		[3]... links
			[0] Open/Close
			[1] HREF
			[2] Width
			[3] Height
			[4] Autostart
			[5] Controller
			[6] Name
			[7] Quality
			[8] BGColor
			[9] FLV
		 	[10] Revert
		 	[11] ShowCloseBtn
		 	[12] LinkID
*/
//Constants for aDIV Array positions for accessing array elements
vPIPPlayer.DIVPOS = 0; 
vPIPPlayer.DIVIDPOS = 1;
vPIPPlayer.ORIGHTMLPOS = 2;
vPIPPlayer.LINKSARRAYPOS = 3;

//Link Array position constants
vPIPPlayer.OPENPOS = 0;
vPIPPlayer.HREFPOS = 1;
vPIPPlayer.WIDTHPOS = 2;
vPIPPlayer.HEIGHTPOS = 3;
vPIPPlayer.FLASHWIDTH = 320; 		//Internal Flash Player width
vPIPPlayer.FLASHHEIGHT  = 300; 		//Internal Flash Player height
vPIPPlayer.AUTOSTARTPOS = 4;
vPIPPlayer.CONTROLLERPOS = 5;
vPIPPlayer.NAMEPOS = 6;
vPIPPlayer.QUALITYPOS = 7;
vPIPPlayer.BGCOLORPOS = 8;
vPIPPlayer.FLVPOS = 9;
vPIPPlayer.REVERTPOS = 10;
vPIPPlayer.SHOWCLOSEBTNPOS = 11;
vPIPPlayer.LINKIDPOS = 12;

//Movie embed default constants
vPIPPlayer.WIDTH = 320; 			//Movie width
vPIPPlayer.HEIGHT  = 260; 			//Movie height with controller (if enabled)
vPIPPlayer.AUTOSTART = "true"; 		//Whether the movie automaticaly plays on initiation
vPIPPlayer.CONTROLLER = "true";		//Whether the movie controller is active
vPIPPlayer.NAME = "" 				//Name and ID of movie
vPIPPlayer.QUALITY = "high" 		//Flash quality parameter
vPIPPlayer.BGCOLOR = "#FFFFFF";		//Flash background color parameter
vPIPPlayer.FLV = "false"			//Whether the movie is a FLV.  If true, the internal Flash FLV player is used.
vPIPPlayer.REVERT = "true"; 		//Whether to revert to original elements in DIV container when another movie is selected
vPIPPlayer.SHOWCLOSEBTN = "true";	// Whether the Close button appears above the movie

//Internal FLV Player
vPIPPlayer.FLVPLAYER450x340 = "cirneViewer450x340-025c.swf";
vPIPPlayer.FLVPLAYER320x300 = "cirneViewer320x300-025c.swf";

//The Safari build where releasing an embedded movie works.
vPIPPlayer.WORKINGSAFARIBUILD = 420;
	
//Global reference to vPIPPlayer object
var vpipPlayerRef;

//The item (text, image, etc.) that displays to activate closing the ThickBox instance.
var vPIPThickBoxCloseItem = "close";

function vPIPPlayer(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump) {

	this.setStartup(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump);
	
	this.aDIVs = new Array();
	//Current link array position
	this.iInitiator = 0;

	// Get path to vPIP.js
	this.vPIPpath = this.getvPIPPath();
			
}

vPIPPlayer.prototype.setStartup = function(_oLink, _sParams, _sFlashVars, _sThickBox, _sJump) {
	// Record parameters in vPIPPlayer properties
	this.oLink = _oLink;
	this.sParams = _sParams;
	this.sFlashVars = _sFlashVars;
	this.sThickBox = _sThickBox;
	this.sJump = _sJump;

}

vPIPPlayer.prototype.init = function() {
		
	//Get the DIV container of the link to 
	this.oDiv = this.oLink.parentNode;
	while (this.oDiv != undefined && this.oDiv != null && 
			this.oDiv.nodeName.toLowerCase() != "div" &&
			(vPIPPlayer.findAttribute(this.oDiv, "class") == null || 
			vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog")) {
		this.oDiv = this.oDiv.parentNode;
	}
	
	//If anchor link is missing container div, create it.
	if (this.oDiv == undefined || this.oDiv == null || 
		this.oDiv.nodeName.toLowerCase() != "div" || 
		vPIPPlayer.findAttribute(this.oDiv, "class") == null ||
		vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog") {
		
		this.oDiv = this.constructDiv(this.oLink);
		
		if (this.oDiv != undefined && this.oDiv != null && 
			this.oDiv.nodeName.toLowerCase() == "div" && 
			vPIPPlayer.findAttribute(this.oDiv, "class") != null &&
			vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() == "hvlog") {
			
			this.oLink.parentNode.replaceChild(this.oDiv, this.oLink);
			this.oLink = this.oDiv.firstChild;
		}
	}
	
	if (this.oDiv == undefined || this.oDiv == null || 
		this.oDiv.nodeName.toLowerCase() != "div" || 
		vPIPPlayer.findAttribute(this.oDiv, "class") == null ||
		vPIPPlayer.findAttribute(this.oDiv, "class").toLowerCase() != "hvlog")
		
		this.byDivExists = false;
	else
		this.byDivExists = true;
	
	if (this.byDivExists) {
		var byDivFound = false;
		
		//If viewing notication object exists, create local object
		//  (**to be implemented**)
		//if (typeof _vPIP_NotifyViewing == "function") {
		//	vpip_NotifyViewing = new _vPIP_NotifyViewing();
		//}
		
		// Locate the current DIV in the aDIVs array of DIVs
		this.iNextPos = this.findDIV(this.oDiv);
		// If DIV not found set to create a new entry in the aDIVs array of DIVs
		if (this.iNextPos == -1) 
			this.iNextPos = this.aDIVs.length;
		else
			byDivFound = true;
		
		// The ID value of the LINK	
		this.sLinkid = "";
		
		this.sHREF = vPIPPlayer.toAlphaNum(this.oLink.href, "~");
		if (! byDivFound) {	
			this.oDiv.setAttribute("id", "vPIP" + this.iNextPos);
			this.sOnClick = vPIPPlayer.toAlphaNum(this.oLink.onclick.toString());
			this.sLinkid = "vPIPMovie" + this.iInitiator;
			this.oLink.setAttribute("id", this.sLinkid);
			
			this.aDIVs[this.iNextPos] = new Array(3);
			this.aDIVs[this.iNextPos][vPIPPlayer.DIVPOS] = this.oDiv;
			this.aDIVs[this.iNextPos][vPIPPlayer.DIVIDPOS] = "vPIP" + this.iNextPos;
			
			this.aDIVs[this.iNextPos][3] = new Array(vPIPPlayer.LINKIDPOS+1);
			this.aDIVs[this.iNextPos][3][vPIPPlayer.OPENPOS] = false;
			this.aDIVs[this.iNextPos][3][vPIPPlayer.HREFPOS] = this.sHREF;
			this.aDIVs[this.iNextPos][3][vPIPPlayer.LINKIDPOS] = parseInt(this.sLinkid.substring(9));;
			
			this.iInitiator++;
		}
		else {
		
			this.byLinkFound = false;
			this.iNextLinkPos = -1;
			
			this.sLinkid = this.oLink.id;
			
			if (this.sLinkid != undefined && this.sLinkid != null && this.sLinkid.length > 9) {
				this.iLinkid = parseInt(this.sLinkid.substring(9));
				this.iNextLinkPos = this.findLinkInDiv(this.aDIVs[this.iNextPos], this.iLinkid);
				if (this.iNextLinkPos < 3) 
					this.iNextLinkPos = 3;
				else 
					this.byLinkFound = true;
			}
			else {
				this.iNextLinkPos = this.aDIVs[this.iNextPos].length;
				if (this.iNextLinkPos < 3) 
					this.iNextLinkPos = 3;
				this.sLinkid = "vPIPMovie" + this.iInitiator;
             	this.oLink.setAttribute("id", this.sLinkid);
             	
   				this.iInitiator++;
			}
			
			if (! this.byLinkFound) {
				this.aDIVs[this.iNextPos][this.iNextLinkPos] = new Array(vPIPPlayer.LINKIDPOS+1);
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.OPENPOS] = false;
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.HREFPOS] = this.sHREF;
				this.aDIVs[this.iNextPos][this.iNextLinkPos][vPIPPlayer.LINKIDPOS] = parseInt(this.sLinkid.substring(9));;
			}
			
		}
		
	}
	
	return true;
	
}

vPIPPlayer.prototype.show = function() {
	
	//Initialize the embed parameters
	this.iWidth = vPIPPlayer.WIDTH;					//Movie width
	this.iHeight  = vPIPPlayer.HEIGHT; 				//Movie height with controller (if enabled)
	this.byAutostart = vPIPPlayer.AUTOSTART; 		//Whether the movie automaticaly plays on initiation
	this.byController = vPIPPlayer.CONTROLLER; 		//Whether the movie controller is active
	this.sName = vPIPPlayer.NAME; 					//Name and ID of movie
	this.sQuality = vPIPPlayer.QUALITY; 			//Flash quality parameter
	this.sBGColor = vPIPPlayer.BGCOLOR; 			//Flash background color parameter
	this.byFLV = vPIPPlayer.FLV;					//Whether the movie is a FLV.  If true, the internal Flash FLV player is used.
	this.byRevert = vPIPPlayer.REVERT; 				//Whether to revert to original elements in DIV container when another movie is selected
    
    // Whether the Close button appears above the movie
    this.byShowCloseBtn = vPIPPlayer.SHOWCLOSEBTN;	
    
    // General purpose variable for holding an array or string position.
	var iPos;   
	
	if (this.byDivExists) {
		if (this.oLink != undefined && this.oLink != null && this.oLink.nodeName.toLowerCase() == "a") {
		
			this.iCurrDIVid = parseInt(this.oDiv.id.substring(4));
			this.iCurrLinkid = parseInt(this.oLink.id.substring(9));
			this.iCurrLink = this.findLinkID(this.aDIVs[this.iCurrDIVid], this.iCurrLinkid);
	
			this.sHREF = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HREFPOS];
			
			if (this.sHREF == undefined || this.sHREF == null)
				this.sHREF = this.oLink.href;
			
			if (this.sHREF != undefined && this.sHREF != null) {
	
				var movieType = vPIPPlayer.isMovieFile(this.oLink);
				this.sMimeType = movieType.sMimeType;
				this.sType = movieType.sType;
				this.sMediaFormat = movieType.sMediaFormat;
				this.sFileExt = movieType.sFileExt;
				
				// Default to width=325, height=276 for Flash
				if (this.sMediaFormat == "flash") {
					this.iWidth = vPIPPlayer.FLASHWIDTH;
					this.iHeight = vPIPPlayer.FLASHHEIGHT;
					if (this.sFileExt == ".flv")
						this.byFLV = "true";
				}
				
				// Get movie parameters
				var byInitArray = true;
				//If movie operation settings already loaded
				if (this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS] != undefined) {
				  this.iWidth = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS];
				  this.iHeight = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HEIGHTPOS];
				  this.byAutostart = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.AUTOSTARTPOS];
				  this.byController = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.CONTROLLERPOS];
				  this.sName = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.NAMEPOS];
				  this.sQuality = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.QUALITYPOS];
				  this.sBGColor = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.BGCOLORPOS];
				  this.byFLV = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.FLVPOS];
				  this.byRevert = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.REVERTPOS];
				  this.byShowCloseBtn = this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SHOWCLOSEBTNPOS];
				  byInitArray = false;
				}
				// Load user movie operation settings
				else {
					if (this.sParams != undefined && this.sParams != null) {
						var aParams = this.sParams.split(",");
						var aMatch;
						for (var i=0; i < aParams.length; i++) {
							if (aMatch = aParams[i].match(/(width\s*=\s*)(\d*)/i)) {
							  this.iWidth = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(height\s*=\s*)(\d*)/i)) {
							  this.iHeight = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(autostart\s*=\s*)(\w*)/i)) {
							  this.byAutostart = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(controller\s*=\s*)(\w*)/i)) {
							  this.byController = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(name\s*=\s*)(\w*)/i)) {
								this.sName = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(quality\s*=\s*)(\w*)/i)) {
							  this.sQuality = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(bgcolor\s*=\s*)(\w*)/i)) {
							  this.sBGColor = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(flv\s*=\s*)(\w*)/i)) {
							  this.byFLV = aMatch[2];
							}
							else if (aMatch = aParams[i].match(/(revert\s*=\s*)(\w*)/i)) {
							  this.byRevert = (aMatch[2].toLowerCase() === "true");
							}
							else if (aMatch = aParams[i].match(/(showclose\s*=\s*)(\w*)/i)) {
							  this.byShowCloseBtn = (aMatch[2].toLowerCase() === "true");
							}
						}
					}
				}
	
				//If this DIV is already open from a link, close it
				this.closeThisDiv(this.aDIVs, this.iCurrDIVid);
				
				var sInnerHTML = this.oDiv.innerHTML;
				//Add the 2nd dimension
				this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.OPENPOS] = false;  // default to embed not opened.
				//If no id Name specified for embed, assign the link's number
				if (this.sName == undefined || this.sName == null || this.sName == "") {
					this.sName = "Embed" + this.iCurrLinkid;
				}
				
				// If array already initialized, don't init.
				if (byInitArray) {
					this.aDIVs[this.iCurrDIVid][vPIPPlayer.ORIGHTMLPOS] = sInnerHTML;
					
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.WIDTHPOS] = 		this.iWidth;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.HEIGHTPOS] = 		this.iHeight;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.AUTOSTARTPOS] = 	this.byAutostart;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.CONTROLLERPOS] = 	this.byController;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.NAMEPOS] = 			this.sName;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.QUALITYPOS] = 		this.sQuality;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.BGCOLORPOS] = 		this.sBGColor;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.FLVPOS] = 			this.byFLV;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.REVERTPOS] = 		this.byRevert;
					this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.SHOWCLOSEBTNPOS] = 	this.byShowCloseBtn;
				}
				
				// Replacement text 
				this.sReplace = "";
				if (this.sType == "video" || this.sType == "application") {
					if (this.sMediaFormat == "quicktime") {
						this.sReplace = "<object class=\"vPIPEmbed\" width=\"" + this.iWidth + "\" height=\"" + this.iHeight + "\" id=\"" + this.sName + "\" classid=\"clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B\" ";
						if (this.sMimeType == "smil")
							this.sReplace += "codebase=\"http://www.apple.com/qtactivex/qtplugin.cab\"> <param name=\"src\" value=\"" + this.vPIPpath + "InitSMIL.mov\"><param name=\"qtsrc\" value=\"" +  this.sHREF;
						else
							this.sReplace += "codebase=\"http://www.apple.com/qtactivex/qtplugin.cab\"> <param name=\"src\" value=\"" + this.sHREF;
						this.sReplace += "\"><param name=\"autoplay\" value=\"" + this.byAutostart + "\"><param name='scale' value='tofit' /><param name=\"controller\" value=\"";
						if (this.sMimeType == "smil")
							this.sReplace += this.byController + "\"><embed src=\"" + this.vPIPpath + "InitSMIL.mov\" qtsrc=\"" + this.sHREF + "\" width=\""+ this.iWidth + "\" height=\"" + this.iHeight;
						else
							this.sReplace += this.byController + "\"><embed src=\"" + this.sHREF + "\" width=\""+ this.iWidth + "\" height=\"" + this.iHeight;
						this.sReplace += "\" name=\"" + this.sName + "\" autoplay=\"" + this.byAutostart + "\" controller=\"" + this.byController; 
						this.sReplace += "\"  scale=\"tofit\" pluginspage=\"http://www.apple.com/quicktime/download/\"></embed></object>";
					}
					else if (this.sMediaFormat == "windowsmedia") {
							
						this.sReplace = "<OBJECT class=\"vPIPEmbed\" CLASSID='CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95'  ";
						this.sReplace += "codebase='http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701' ";
						this.sReplace += "standby='Loading Microsoft Windows Media Player components...' type='application/x-oleobject'  ";
						this.sReplace += "width='" + this.iWidth + "' height='" + this.iHeight + "' id='" + this.sName + "' >";
						this.sReplace += "<PARAM NAME='fileName' VALUE='" + this.sHREF + "' ><PARAM NAME='autoStart' VALUE='" + this.byAutostart;
						this.sReplace += "'><PARAM NAME='showControls' VALUE='" + this.byController + "'>";
						this.sReplace += "<EMBED type='application/x-mplayer2' pluginspage='http://www.microsoft.com/Windows/MediaPlayer/' id='";
						this.sReplace += this.sName + "' name='" + this.sName + "' showcontrols='" + this.byController + "' width='" + this.iWidth + "' height='"; 
						this.sReplace += this.iHeight + "' src='" + this.sHREF + "' autostart='" + this.byAutostart + "'></EMBED></OBJECT>";
					}
					else if (this.sMediaFormat == "flash") {
						this.sReplace = "<OBJECT class=\"vPIPEmbed\" classid='clsid:D27CDB6E-AE6D-11cf-96B8-444553540000' ";
						this.sReplace += "codebase='http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0' ";
						this.sReplace += "WIDTH='" + this.iWidth + "' HEIGHT='" + this.iHeight + "' id='" + this.sName + "' >";
						this.sReplace += "<PARAM NAME='movie' VALUE='";
						//Use a FLV Viewer to play the designated FLV
						if (this.byFLV == "true") {
							 //  Set Flash type and location
							 if (Number(this.iWidth) > 320) 
							    this.sFLVPlayer = this.vPIPpath + vPIPPlayer.FLVPLAYER450x340;
							 else
							    this.sFLVPlayer = this.vPIPpath + vPIPPlayer.FLVPLAYER320x300;

							//Construct sJump for flashvars send
							var sJumpFlashVars= "";
							if (this.sJump != null && this.sJump.length > 0) {
								var aParams = this.sJump.split(",");
								var aMatch;
								for (var i=0; i < aParams.length; i++) {
									if (aMatch = aParams[i].match(/(\w*)(\s*=\s*)(.*)/)) 
										sJumpFlashVars += "&" + aMatch[1] + "=" + aMatch[3];
								}
							}
							
							this.sReplace += this.sFLVPlayer + "'> <PARAM NAME='quality' VALUE='" + this.sQuality + "' > <PARAM NAME='bgcolor' VALUE='" + this.sBGColor + "'> ";
							this.sReplace += "<PARAM NAME='FlashVars' VALUE='flvURL=" + this.sHREF + "&cvhome=" + this.vPIPpath;
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "&" + this.sFlashVars;
							this.sReplace += sJumpFlashVars + "' > <EMBED src='" + this.sFLVPlayer + "' quality='" + this.sQuality + "' bgcolor='" + this.sBGColor + "' width='" + this.iWidth + "' height='" + this.iHeight + "' ";
							this.sReplace += "FlashVars='flvURL=" + this.sHREF + "&cvhome=" + this.vPIPpath;
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0) {
								this.sReplace += "&" + this.sFlashVars;
							}
							this.sReplace += sJumpFlashVars + "' NAME='' ALIGN='' TYPE='application/x-shockwave-flash' PLUGINSPAGE='http://www.macromedia.com/go/getflashplayer'> ";
						}
						else {
							this.sReplace += this.sHREF + "'> <PARAM NAME='quality' VALUE='" + this.sQuality + "' > <PARAM NAME='bgcolor' VALUE='" + this.sBGColor + "'> ";
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "<PARAM NAME='FlashVars' VALUE='" + this.sFlashVars + "' > "; //Why?: + "&embdWidth=" + this.iWidth + "&embdHeight=" + this.iHeight + "' > ";
							this.sReplace += "<EMBED src='" + this.sHREF + "' quality='" + this.sQuality + "' bgcolor='" + this.sBGColor + "' width='" + this.iWidth + "' height='" + this.iHeight + "' ";
							if (this.sFlashVars != undefined && this.sFlashVars != null && this.sFlashVars.length > 0)
								this.sReplace += "FlashVars='" + this.sFlashVars + "' "; //Why?: + "&embdWidth=" + this.iWidth + "&embdHeight=" + this.iHeight + "' ";
							this.sReplace += "NAME='' ALIGN='' TYPE='application/x-shockwave-flash' PLUGINSPAGE='http://www.macromedia.com/go/getflashplayer'> ";
						}
						this.sReplace += "</EMBED> </OBJECT>";
					}

					if (this.sReplace.length > 0) {
						var sUserAgent = navigator.userAgent;
						this.bySafari = sUserAgent.indexOf('Safari') > -1;
						this.byOpera = sUserAgent.indexOf('Opera') > -1;
						this.byIE7 = sUserAgent.indexOf("MSIE 7") > -1;
						this.byIE6 = sUserAgent.indexOf("MSIE 6") > -1;
						this.nSafariBuild = -1;
						if (this.bySafari) {
							this.nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
						}
						//Get any Thickbox parameters
						this.byThickBox = false;
						//Setup ThickBox parameters
						if (this.sThickBox != undefined && this.sThickBox != null && this.sThickBox.length > 0 && ! this.bySafari && ! this.byIE6) {
							var aParams = this.sThickBox.split(",");
							var aMatch;
							var sThickBoxActive = "true";
							var sThickBoxCaption = "";
							var sThickBoxBackground = "#E1E1E1";
							for (var i=0; i < aParams.length; i++) {
								if (aMatch = aParams[i].match(/(active\s*=\s*)(\w*)/i)) {
								  sThickBoxActive = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(caption\s*=\s*)(.*)/i)) {
								  sThickBoxCaption = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(background\s*=\s*)(\d*)/i)) {
								  sThickBoxBackground = aMatch[2];
								}
							}
							if (sThickBoxActive.toLowerCase() == "true")
								this.byThickBox = true;
						}
						
						//Open in Thickbox
						if (this.byThickBox) {
							// Sample of modifying the ThickBox close display to the "X Close" 
							// graphic (uncomment to activate, modify for your own graphic.)
							//vPIPThickBoxCloseItem =	 "<img src='" + this.vPIPpath + "close_hover.gif' />";
							
							this.revert(this.aDIVs);
							this.thickBox_show(sThickBoxCaption, this.sReplace, Number(this.iWidth), Number(this.iHeight), sThickBoxBackground);	
						}
						// Open in page location
						else {
							//Add [X Close] button to revert to original <DIV ...> data.
						    if (this.byShowCloseBtn) {
								this.sReplace = "<div style=\"padding-right: " + (this.iWidth - 49) + "px\" ><a href=\"javascript: vPIPClose(" + this.iCurrDIVid  + ", " + this.iCurrLink + ");\" title=\"Close Movie\" onMouseOver=\"document.vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + ".src='" + this.vPIPpath + "close_hover.gif';\" onMouseOut=\"document.vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + ".src='" + this.vPIPpath + "close_grey.gif';\" style=\" background: transparent;\" ><img src=\"" + this.vPIPpath + "close_grey.gif\" name=\"vPIPImage" + (this.iCurrDIVid * 10) + this.iCurrLink + "\" style=\"border: none;\"  /></a></div>" + this.sReplace;
							}
							
							// Mac Safari version 1.3.2 does not correctly close a replaced media object, so revert is disabled for Safari
							if (! (this.bySafari && this.nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD)) {
								//Close any <DIVs set to revert
								this.revert(this.aDIVs);
							}
							
							//If "hVlogTarget" class identified,
							//   add HTML outside it.
							this.sReplace = this.addOutsideTarget(sInnerHTML, this.sReplace);
							
							this.oDiv.innerHTML = this.sReplace;
							this.aDIVs[this.iCurrDIVid][this.iCurrLink][vPIPPlayer.OPENPOS] = true;
							
						}
					}
						
				}
				else {
					if (this.sMimeType != undefined && this.sMimeType != null) {
						setTimeout("Unsuported mime type: \"" + this.sMimeType + "\".", 0);
						if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
							window.open(this.oLink.href, "_self");
						else if (this.sHREF != undefined && this.sHREF != null) 
							window.open(this.sHREF, "_self");
					}
					else  {
						setTimeout("Unsuported file extension: \"" + this.sFileExt + "\".", 0);
						if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
							window.open(this.oLink.href, "_self");
						else if (this.sHREF != undefined && this.sHREF != null) 
							window.open(this.sHREF, "_self");
					}
				}
			}
			else {
				setTimeout("Missing href=\"...\" attribute.", 0);
				if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
					window.open(this.oLink.href, "_self");
				else if (this.sHREF != undefined && this.sHREF != null) 
					window.open(this.sHREF, "_self");
			}
		}
		else {
			setTimeout("video Playing In Place cannot execute because the link is not identified.", 0);
			if (this.sHREF != undefined && this.sHREF != null) 
					window.open(this.sHREF, "_self");
		}
		
	}
	else {
		setTimeout("video Playing In Place cannot execute because the hVlog DIV is not identified.", 0);
		if (this.oLink.href.toLowerCase().indexOf("http://") > -1)
			window.open(this.oLink.href, "_self");
		else if (this.sHREF != undefined && this.sHREF != null) 
			window.open(this.sHREF, "_self");
		
	}
	
	return;
	
}

// Class to pass the movie MimeType, type of file (video, application, ...) and
//    sMediaFormat (quicktime, windowsmedia or flash)
function MovieType(_MimeType, _sType, _sMediaFormat, _sFileExt) {
	this.sMimeType = _MimeType;
	this.sType = _sType;
	this.sMediaFormat = _sMediaFormat;
	this.sFileExt = _sFileExt;
}

vPIPPlayer.isMovieFile = function(oLink) {
	
	var movieType = null;
	
	if (oLink != undefined && oLink != null && oLink.nodeName.toLowerCase() == "a") {
		
		//Handle mimetype					
		var sMimeType = oLink.type;
		if (sMimeType != undefined && sMimeType != null && sMimeType.length > 0) {
			var iPos = sMimeType.search(/\//);
			if (iPos > -1) 
				sMimeType = sMimeType.substring(iPos+1);
			else 
				sMimeType = null;
		}
		
		// Type of media
		var sType = "false";
		var sMediaFormat = "";
		
		// Get the file extension
		var sFileExt;
		var sHREF = vPIPPlayer.toAlphaNum(oLink.href, "~");
		var iURLGET = sHREF.indexOf('?');
		if (iURLGET > -1) {
			var sHREFFile = sHREF.substring(0, iURLGET);
			sFileExt = sHREFFile.substring(sHREFFile.lastIndexOf('.'), iURLGET).toLowerCase();
		}
		else {
			sFileExt = sHREF.substring(sHREF.lastIndexOf('.'), sHREF.length).toLowerCase();
		}
		 
		// Determine the video type to embed
		if (sMimeType != undefined && sMimeType != null && sMimeType.length > 0) {
			switch (sMimeType.toLowerCase()) {
				case "quicktime":
				case "mp4":
				case "x-m4v":
				case "x-mp3":
				case "mp3":
				case "mpeg":
				case "smil":
				case "3gpp":
					sMediaFormat = "quicktime";
					sType = "video";
				break;
				
				case "x-msvideo":
				case "x-ms-wmv":
				case "x-ms-asf":
				case "x-ms-wma":
					sMediaFormat = "windowsmedia";
					sType = "video";
				break;
				
				case "x-shockwave-flash":
				case "x-flv":
					sMediaFormat = "flash";
					sType = "application";
				break;
			}
		}
		else {
			sMimeType = "";
			switch (sFileExt.toLowerCase()) {
				case ".mov":
				case ".mp4":
				case ".m4v":
				case ".mp3":
				case ".3gp":
					sMediaFormat = "quicktime";
					sType = "video";
					break;
					
				case ".smi":
				case ".smil":
					sMediaFormat = "quicktime";
					sType = "video";
					sMimeType = "smil";
					break;
					
				case ".avi":
				case ".wmv":
				case ".asf":
				case ".wma":
					sMediaFormat = "windowsmedia";
					sType = "video";
					break;
					
				case ".swf":
				case ".flv":
					sMediaFormat = "flash";
					sType = "application";
					break;
					
			}
		}
		
		movieType = new MovieType(sMimeType, sType, sMediaFormat, sFileExt);
	}
	
	return movieType;
}

vPIPPlayer.prototype.revert = function(aDIVs) {
	for(var j = 0; j < aDIVs.length; j++) {
		for(var k = vPIPPlayer.LINKSARRAYPOS; k < aDIVs[j].length; k++) {
			if (aDIVs[j][k][vPIPPlayer.REVERTPOS]) {
				aDIVs[j][vPIPPlayer.DIVPOS].innerHTML = aDIVs[j][vPIPPlayer.ORIGHTMLPOS];
				aDIVs[j][k][vPIPPlayer.OPENPOS] = false;
			}
		}
	}

}

vPIPPlayer.prototype.closeThisDiv = function(aDIVs, iCurrDIVid) {
	for(var k = vPIPPlayer.LINKSARRAYPOS; k < aDIVs[iCurrDIVid].length; k++) {
		if (aDIVs[iCurrDIVid][k][vPIPPlayer.REVERTPOS]) {
			aDIVs[iCurrDIVid][vPIPPlayer.DIVPOS].innerHTML = aDIVs[iCurrDIVid][vPIPPlayer.ORIGHTMLPOS];
			aDIVs[iCurrDIVid][k][vPIPPlayer.OPENPOS] = false;
		}
	}

}

vPIPPlayer.prototype.constructDiv = function(oLink) {
	var oDiv = document.createElement("div");
	oDiv.setAttribute("class", "hVlog");

	// Reconstruct anchor link for new DIV
	var oReplaceLink = document.createElement("a");
	oReplaceLink.setAttribute("href", oLink.href);
	if (oLink.type != "") {
		oReplaceLink.setAttribute("type", oLink.type);
	}
	if (oLink.name != "") {
		oReplaceLink.setAttribute("name", oLink.type);
	}
	if (oLink.href != "") {
		oReplaceLink.setAttribute("href", oLink.href);
	}
	if (oLink.rel != "") {
		oReplaceLink.setAttribute("rel", oLink.rel);
	}
	if (oLink.onclick.toString() != "") {
		oReplaceLink.onclick = oLink.onclick;
	}
	if (oLink.hasChildNodes()) {
	   var oLinkChildren = oLink.childNodes;
	   for (var i = 0; i < oLinkChildren.length; i++) 
	   {
	   		oReplaceLink.appendChild(oLinkChildren[i])
	   }
	}
	if (oLink.innerHTML != "") {
		oReplaceLink.innerHTML = oLink.innerHTML;
	}
	
	oDiv.appendChild(oReplaceLink);
	
	return oDiv;
	
}

vPIPPlayer.prototype.addOutsideTarget = function(sInnerHTML, sRevert) {
	var iTargetStart = sInnerHTML.toLowerCase().indexOf("hvlogtarget");
	if (iTargetStart > -1) {
		iTargetStart = sInnerHTML.toLowerCase().substring(0, iTargetStart).lastIndexOf("<");
		var iTargetEnd = sInnerHTML.toLowerCase().indexOf("</a", iTargetStart);
		iTargetEnd = sInnerHTML.toLowerCase().indexOf(">", iTargetEnd);
		if (iTargetEnd > -1) {
			var sPrior = sInnerHTML.substring(0, iTargetStart);
			var sAfter = sInnerHTML.substring(iTargetEnd + 1);
			sRevert = sPrior + sRevert + sAfter;
		}
		
	}
	return sRevert;
}

// Close back to the original <div contained data.
function vPIPClose(sDivLoc, sLinkLoc) {
	var sUserAgent = navigator.userAgent;
	var bySafari = sUserAgent.indexOf('Safari') > -1;
	var nSafariBuild = -1;
	if (bySafari) {
		nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
	}
	//If Safari build where video file does not release, reload page.
	if (bySafari && nSafariBuild < vPIPPlayer.WORKINGSAFARIBUILD) {
		document.location.reload();
	}
	else {
		if (Number(sDivLoc) != NaN && Number(sLinkLoc) != NaN) {
			var iDivLoc = Number(sDivLoc);
			var iLinkLoc = Number(sLinkLoc);
			vpipPlayerRef.aDIVs[iDivLoc][vPIPPlayer.DIVPOS].innerHTML = vpipPlayerRef.aDIVs[iDivLoc][vPIPPlayer.ORIGHTMLPOS];
			vpipPlayerRef.aDIVs[iDivLoc][iLinkLoc][vPIPPlayer.OPENPOS] = false;
			
			// Setup onclick to vPIPPlay(this) for those missing it.
			if (typeof vPIPIt == "function") {
				vPIPIt();
			}
		}
	}

}

/**
 * Find oDiv in aDIVs array.
 * Returns array position in aDIVs that oDiv is found or -1
 */
vPIPPlayer.prototype.findDIV = function(oDiv) {
	var i;
	var iFound = -1;
	if (oDiv.id != undefined && oDiv.id != null && oDiv.id.length > 0) {
		
		for(i=0; i<this.aDIVs.length; i++) {
			if (this.aDIVs[i][vPIPPlayer.DIVIDPOS] === this.oDiv.id) {
				iFound = i;
				break;
			}
		}
	}
	
	return iFound;
}

vPIPPlayer.prototype.findLinkID = function(aDIV, iCurrLinkid) {
	var iFound = -1;
	for (var i=3; i<aDIV.length; i++) {
		if (aDIV[i][vPIPPlayer.LINKIDPOS] == iCurrLinkid) {
			iFound = i;
			break;
		}
	}
	
	return iFound;
}

vPIPPlayer.prototype.findLinkInDiv = function(aDiv, iLinkid) {
	var iLinkPosInDiv = -1;
	for(var i=3; i< aDiv.length; i++) {
		if (aDiv[i][vPIPPlayer.LINKIDPOS] != undefined) {
			if (aDiv[i][vPIPPlayer.LINKIDPOS] == iLinkid) {
				iLinkPosInDiv = i;
				break;
			}
		}
	}
	
	return iLinkPosInDiv;
}

vPIPPlayer.prototype.addEvent = function(obj, evType, fn){
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

vPIPPlayer.prototype.getvPIPPath = function() {
	var scripts = document.getElementsByTagName ( "script" );
	var src;
	var index;
    var sVPIPpath = "";
    
	for (var i=0; i<scripts.length; i++) {
		src = scripts[i].getAttribute ( "src" );
		if (src != undefined && src != null) {
			index = src.search(/vpip.js/i);
			if (index > -1) {
				sVPIPpath = src.substring ( 0, index);
				break;
			}
		}
	}

    return sVPIPpath;
}

vPIPPlayer.findAttribute = function(oElement, sAttribute) {
	var oValue = null;
	
	var attrs = oElement.attributes;
	if (attrs != undefined && attrs != null) {
		for(var i=attrs.length-1; i>=0; i--) {
			if (attrs[i].name.toLocaleLowerCase() == sAttribute.toLocaleLowerCase()) {
				oValue = attrs[i].value;
				break;
			}
		}
	}
	
	return oValue;
}

vPIPPlayer.toAlphaNum = function(sString, sAllowed) {
	var i;
	var sNewString = "";
	if (sString == undefined || sString == null) {
		return sString;
	}
	else {
		for (i=0; i<sString.length; i++) {
         	ch = sString.charAt(i);
			if (ch >= " "  && ch <= "z") {
				sNewString += sString.charAt(i);
			}
         	else if (sAllowed != undefined && sAllowed != null && sAllowed.indexOf(ch) > -1) {
				sNewString += sString.charAt(i);
         	}
		}
		return sNewString;
	}
}

/*vPIP version of ThickBox By Cody Lindley (http://www.codylindley.com)
 * Thickbox is built on top of the very light weight jquery library.
*/


vPIPPlayer.prototype.thickBox_show = function(sCaption, sEmbed, vPIP_TB_WIDTH, vPIP_TB_HEIGHT, sBackground) {//function called when the user clicks on a thickbox link
	try {

		jQuery("body").append("<div id='vPIP_TB_overlay'></div><div id='vPIP_TB_window'></div>");
		jQuery("#vPIP_TB_overlay").click(this.thickBox_remove);
		jQuery(window).scroll(this.thickBox_position);
 

		if (sCaption == undefined || sCaption == null) 
			sCaption = '';
		vPIP_TB_WIDTH += 30;
		vPIP_TB_HEIGHT += 60;
		var sEntry = "<div id='vPIP_TB_caption'>"+sCaption+"</div><div id='vPIP_TB_closeWindow'><a href='javascript: none' id='vPIP_TB_closeWindowButton'>" + vPIPThickBoxCloseItem + "</a></div><div id='vPIP_Object'>" + sEmbed + "</div>";
		jQuery("#vPIP_TB_window").html(sEntry); 
		document.getElementById("vPIP_TB_window").style.backgroundColor = sBackground;
		document.getElementById("vPIP_TB_window").style.backgroundColor = sBackground;
		jQuery("#vPIP_TB_closeWindowButton").click(this.thickBox_remove);
		this.thickBox_position(vPIP_TB_WIDTH, vPIP_TB_HEIGHT);
		jQuery("#vPIP_TB_window").show(); 
	} catch(e) {
		setTimeout(e, 0);
	}
}

//helper functions below

vPIPPlayer.prototype.thickBox_remove = function() {
	jQuery("#vPIP_TB_window").html(""); 
	jQuery("#vPIP_TB_window").fadeOut("fast",function(){jQuery('#vPIP_TB_window,#vPIP_TB_overlay').remove();});

	// Setup onclick to vPIPPlay(this) for those missing it.
	if (typeof vPIPIt == "function") {
		vPIPIt();
	}
	
	return false;
}

vPIPPlayer.prototype.thickBox_position = function(vPIP_TB_WIDTH, vPIP_TB_HEIGHT) {
	var de = document.documentElement;
	var w = self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth;
	var h = self.innerHeight || (de&&de.clientHeight) || document.body.clientHeight;
  
  	if (window.innerHeight && window.scrollMaxY) {	
		yScroll = window.innerHeight + window.scrollMaxY;
	} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
		yScroll = document.body.scrollHeight;
	} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
		yScroll = document.body.offsetHeight;
  	}
	
	jQuery("#vPIP_TB_window").css({width:vPIP_TB_WIDTH+"px",height:vPIP_TB_HEIGHT+"px",
	left: ((w - vPIP_TB_WIDTH)/2)+"px", top: ((h - vPIP_TB_HEIGHT)/2)+"px" });
	jQuery("#vPIP_TB_overlay").css("height",yScroll +"px");
}

// ** End of vPIP Thickbox code **

