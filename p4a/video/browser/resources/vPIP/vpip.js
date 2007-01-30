/* 
vPIP version 0.16g Beta (maintenance release)
* 	Close button on Safari prior to build 420, reloads the page.
u

Installation and usage page at:  http://utilities.cinegage.com/videos-playing-in-place/

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

/* aDIVs structure:
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
*/
var aDIVs = new Array();
//DIV Array positions
var iDIVPos = 0; 
var iDIVIDPos = 1;
var iOrigHTMLPos = 2;

//link Array positions
var iOpenPos = 0;
var iHREFPos = 1;
var iWidthPos = 2;
var iHeightPos = 3;
var iAutostartPos = 4;
var iControllerPos = 5;
var iNamePos = 6;
var iQualityPos = 7;
var iBGColorPos = 8;
var iFLVPos = 9;
var iRevertPos = 10;
var iLinkIDPos = 11;

//Current array position

var iInitiator = 0;

// (Legacy function for activating directly from onscript for when vPIPInit doesn't execute
function vPIPPlay(oLink, sParams, sFlashVars, sThickBox, sJump) {
	

	var oDiv = oLink.parentNode;
	while (oDiv != undefined && oDiv.nodeName.toLowerCase() != "div") {
		oDiv = oDiv.parentNode;
	}
	if (oDiv != undefined) {
		var byDivFound = false;
		
		// Locate current DIV in aDIVs
		iNextPos = _vPIP_findDIV(oDiv)
		if (iNextPos == -1) 
			iNextPos = aDIVs.length;
		else
			byDivFound = true;
			
		var sLinkid = "";
		
		if (! byDivFound) {	
			oDiv.setAttribute("id", "vPIP" + iNextPos);
			var sHREF = _vPIP_toAlphaNum(oLink.href, "~");
			var sOnClick = _vPIP_toAlphaNum(oLink.onclick.toString());
			sLinkid = "vPIPMovie" + iInitiator;
			oLink.setAttribute("id", sLinkid);
			
			aDIVs[iNextPos] = new Array(3);
			aDIVs[iNextPos][iDIVPos] = oDiv;
			aDIVs[iNextPos][iDIVIDPos] = "vPIP" + iNextPos;
			
			aDIVs[iNextPos][3] = new Array(iLinkIDPos+1);
			aDIVs[iNextPos][3][iOpenPos] = false;
			aDIVs[iNextPos][3][iHREFPos] = sHREF;
			aDIVs[iNextPos][3][iLinkIDPos] = parseInt(sLinkid.substring(9));;
			
			iInitiator++;
		}
		else {
		
			var byLinkFound = false;
			var iNextLinkPos = -1;
			
			sLinkid = oLink.id;
			
			if (sLinkid != undefined && sLinkid.length > 9) {
				var iLinkid = parseInt(sLinkid.substring(9));
				iNextLinkPos = _vPIP_findLinkInDiv(aDIVs[iNextPos], iLinkid);
				if (iNextLinkPos < 3) 
					iNextLinkPos = 3;
				else 
					byLinkFound = true;
			}
			else {
				iNextLinkPos = aDIVs[iNextPos].length;
				if (iNextLinkPos < 3) 
					iNextLinkPos = 3;
				sLinkid = "vPIPMovie" + iInitiator;
             	oLink.setAttribute("id", sLinkid);
             	
   				iInitiator++;
			}
			
			if (! byLinkFound) {
				aDIVs[iNextPos][iNextLinkPos] = new Array(iLinkIDPos+1);
				aDIVs[iNextPos][iNextLinkPos][iOpenPos] = false;
				aDIVs[iNextPos][iNextLinkPos][iHREFPos] = sHREF;
				aDIVs[iNextPos][iNextLinkPos][iLinkIDPos] = parseInt(sLinkid.substring(9));;
			}
			
		}
		
		
		vPIPShow(sLinkid, sParams, sFlashVars, sThickBox, sJump);
		
		return false;
	}
	else {
		window.open(oLink.href, "_self");
		setTimeout("video Playing In Place cannot execute because the containing <DIV ...>...</DIV> tag is missing.", 0);
		return true;
	}
}

// Legacy function that requird vPIPInit
function vPIPShow(sInitiator, sParams, sFlashVars, sThickBox, sJump) {
	
	var iWidth = 320; //Movie width with controller if enabled
	var iHeight  = 260; //Movie height
	var byAutostart = "true"; //Whether the movie automaticaly plays on initiation
	var byController = "true"; //Whether the movie controller is active
	var sName = "" //Name and ID of movie
	var sQuality = "high" //Flash parameter
	var sBGColor = "#FFFFFF"; //Flash parameter
	var byFLV = "false"
	var byRevert = "true"; //Whether to revert to original elements in DIV container when another movie is selected
	var iPos;   // General purpose variable for holding an array or string position.
	var oInitiator = document.getElementById(sInitiator);
	if (oInitiator != undefined) {
		var oDiv = oInitiator.parentNode;
		while (oDiv != undefined && oDiv.nodeName.toLowerCase() != "div") {
			oDiv = oDiv.parentNode;
		}
		if (oDiv.nodeName != undefined && oDiv.nodeName.toLowerCase() == "div") {
			// Get path to vPIP.js
			var vPIPpath = _vPIP_getvPIPPath();
			
			//  Set Flash location
			var sFLVPlayer = vPIPpath + "cirneViewer-023.swf";

			var iCurrDIVid = parseInt(oDiv.id.substring(4));
			var iCurrLinkid = parseInt(oInitiator.id.substring(9));
			var iCurrLink = _vPIP_findLinkID(aDIVs[iCurrDIVid], iCurrLinkid);
			var sHREF;
			if (iCurrLink > -1)
				sHREF = aDIVs[iCurrDIVid][iCurrLink][iHREFPos];
				
				if (sHREF == undefined)
					sHREF = oInitiator.href;
				
				if (sHREF != undefined) {
	
					//Handle mimetype					
					var sMimeType = oInitiator.type;
					if (sMimeType != undefined) {
						iPos = sMimeType.search(/\//);
						if (iPos > -1) 
							sMimeType = sMimeType.substring(iPos+1);
						else 
							sMimeType = null;
					}
					
					// Type of media
					var type = false;
					var sMediaFormat = "";
					
					// Get the file extension
					var sFileExt;
					iURLGET = sHREF.indexOf('?');
					if (iURLGET > -1) {
						var sHREFFile = sHREF.substring(0, iURLGET);
						sFileExt = sHREFFile.substring(sHREFFile.lastIndexOf('.'), iURLGET).toLowerCase();
					}
					else {
						sFileExt = sHREF.substring(sHREF.lastIndexOf('.'), sHREF.length).toLowerCase();
					}
					 
					if (sMimeType != undefined) {
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
								type = "video";
							break;
							case "x-msvideo":
							case "x-ms-wmv":
							case "x-ms-asf":
							case "x-ms-wma":
								sMediaFormat = "windowsmedia";
								type = "video";
							break;
							case "x-shockwave-flash":
								sMediaFormat = "flash";
								type = "application";
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
								type = "video";
								break;
							case ".smi":
							case ".smil":
								sMediaFormat = "quicktime";
								type = "video";
								sMimeType = "smil";
								break;
							case ".avi":
							case ".wmv":
							case ".asf":
							case ".wma":
								sMediaFormat = "windowsmedia";
								type = "video";
								break;
							case ".swf":
							case ".flv":
								sMediaFormat = "flash";
								type = "application";
								break;
						}
					}

					// Default to width=325, height=276 for Flash
					if (sMediaFormat == "flash") {
						iWidth = 325;
						iHeight = 292;
						if (sFileExt == ".flv")
							byFLV = "true";
					}
					
					// Get movie parameters
					var byInitArray = true;
					//If movie operation settings already loaded
					if (aDIVs[iCurrDIVid][iCurrLink][iWidthPos] != undefined) {
					  iWidth = aDIVs[iCurrDIVid][iCurrLink][iWidthPos];
					  iHeight = aDIVs[iCurrDIVid][iCurrLink][iHeightPos];
					  byAutostart = aDIVs[iCurrDIVid][iCurrLink][iAutostartPos];
					  byController = aDIVs[iCurrDIVid][iCurrLink][iControllerPos];
					  sName = aDIVs[iCurrDIVid][iCurrLink][iNamePos];
					  sQuality = aDIVs[iCurrDIVid][iCurrLink][iQualityPos];
					  sBGColor = aDIVs[iCurrDIVid][iCurrLink][iBGColorPos];
					  byFLV = aDIVs[iCurrDIVid][iCurrLink][iFLVPos];
					  byRevert = aDIVs[iCurrDIVid][iCurrLink][iRevertPos];
					  byInitArray = false;
					}
					// Load user movie operation settings
					else {
						if (sParams != undefined) {
							var aParams = sParams.split(",");
							var aMatch;
							for (var i=0; i < aParams.length; i++) {
								if (aMatch = aParams[i].match(/(width\s*=\s*)(\d*)/i)) {
								  iWidth = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(height\s*=\s*)(\d*)/i)) {
								  iHeight = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(autostart\s*=\s*)(\w*)/i)) {
								  byAutostart = (aMatch[2].toLowerCase() === "true");
								}
								else if (aMatch = aParams[i].match(/(controller\s*=\s*)(\w*)/i)) {
								  byController = (aMatch[2].toLowerCase() === "true");
								}
								else if (aMatch = aParams[i].match(/(name\s*=\s*)(\w*)/i)) {
									sName = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(quality\s*=\s*)(\w*)/i)) {
								  sQuality = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(bgcolor\s*=\s*)(\w*)/i)) {
								  sBGColor = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(flv\s*=\s*)(\w*)/i)) {
								  byFLV = aMatch[2];
								}
								else if (aMatch = aParams[i].match(/(revert\s*=\s*)(\w*)/i)) {
								  byRevert = (aMatch[2].toLowerCase() === "true");
								}
							}
						}
					}
	
					//If this DIV is already open from a link, close it
					_vPIP_CloseThisDiv(aDIVs, iCurrDIVid);
					
					var sInnerHTML = oDiv.innerHTML;
					//Add the 2nd dimension
					aDIVs[iCurrDIVid][iCurrLink][iOpenPos] = false;  // default to embed not opened.
					//If no id Name specified for embed, assign the link's number
					if (sName == undefined || sName == "") {
						sName = "Embed" + parseInt(sInitiator.substring(9));
					}
					
					// If array already initialized, don't init.
					if (byInitArray) {
						aDIVs[iCurrDIVid][iOrigHTMLPos] = sInnerHTML;
						
						aDIVs[iCurrDIVid][iCurrLink][iWidthPos] = iWidth;
						aDIVs[iCurrDIVid][iCurrLink][iHeightPos] = iHeight;
						aDIVs[iCurrDIVid][iCurrLink][iAutostartPos] = byAutostart;
						aDIVs[iCurrDIVid][iCurrLink][iControllerPos] = byController;
						aDIVs[iCurrDIVid][iCurrLink][iNamePos] = sName;
						aDIVs[iCurrDIVid][iCurrLink][iQualityPos] = sQuality;
						aDIVs[iCurrDIVid][iCurrLink][iBGColorPos] = sBGColor;
						aDIVs[iCurrDIVid][iCurrLink][iFLVPos] = byFLV;
						aDIVs[iCurrDIVid][iCurrLink][iRevertPos] = byRevert;
					}
					
					// Replacement text into DIV
					var sReplace = "";
					if (type == "video" || type == "application") {
						if (sMediaFormat == "quicktime") {
							sReplace = "<object class=\"vPIPEmbed\" width=\"" + iWidth + "\" height=\"" + iHeight + "\" id=\"" + sName + "\" classid=\"clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B\" ";
							if (sMimeType == "smil")
								sReplace += "codebase=\"http://www.apple.com/qtactivex/qtplugin.cab\"> <param name=\"src\" value=\"" + vPIPpath + "InitSMIL.mov\"><param name=\"qtsrc\" value=\"" +  sHREF;
							else
								sReplace += "codebase=\"http://www.apple.com/qtactivex/qtplugin.cab\"> <param name=\"src\" value=\"" + sHREF;
							sReplace += "\"><param name=\"autoplay\" value=\"" + byAutostart + "\"><param name=\"controller\" value=\"";
							if (sMimeType == "smil")
								sReplace += byController + "\"><embed src=\"" + vPIPpath + "InitSMIL.mov\" qtsrc=\"" + sHREF + "\" width=\""+ iWidth + "\" height=\"" + iHeight;
							else
								sReplace += byController + "\"><embed src=\"" + sHREF + "\" width=\""+ iWidth + "\" height=\"" + iHeight;
							sReplace += "\" name=\"" + sName + "\" autoplay=\"" + byAutostart + "\" controller=\"" + byController; 
							sReplace += "\" pluginspage=\"http://www.apple.com/quicktime/download/\"></embed></object>";
						}
						else if (sMediaFormat == "windowsmedia") {
								
							sReplace = "<OBJECT class=\"vPIPEmbed\" CLASSID='CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95'  ";
							sReplace += "codebase='http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=5,1,52,701' ";
							sReplace += "standby='Loading Microsoft Windows Media Player components...' type='application/x-oleobject'  ";
							sReplace += "width='" + iWidth + "' height='" + iHeight + "' id='" + sName + "' >";
							sReplace += "<PARAM NAME='fileName' VALUE='" + sHREF + "' ><PARAM NAME='autoStart' VALUE='" + byAutostart;
							sReplace += "'><PARAM NAME='showControls' VALUE='" + byController + "'>";
							sReplace += "<EMBED type='application/x-mplayer2' pluginspage='http://www.microsoft.com/Windows/MediaPlayer/' id='";
							sReplace += sName + "' name='" + sName + "' showcontrols='" + byController + "' width='" + iWidth + "' height='"; 
							sReplace += iHeight + "' src='" + sHREF + "' autostart='" + byAutostart + "'></EMBED></OBJECT>";
						}
						else if (sMediaFormat == "flash") {
							sReplace = "<OBJECT class=\"vPIPEmbed\" classid='clsid:D27CDB6E-AE6D-11cf-96B8-444553540000' ";
							sReplace += "codebase='http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0' ";
							sReplace += "WIDTH='" + iWidth + "' HEIGHT='" + iHeight + "' id='" + sName + "' >";
							sReplace += "<PARAM NAME='movie' VALUE='";
							//Use a FLV Viewer to play the designated FLV
							if (byFLV == "true") {
								//Construct sJump for flashvars send
								var sJumpFlashVars= "";
								if (sJump != null && sJump.length > 0) {
									var aParams = sJump.split(",");
									var aMatch;
									for (var i=0; i < aParams.length; i++) {
										if (aMatch = aParams[i].match(/(\w*)(\s*=\s*)(.*)/)) 
											sJumpFlashVars += "&" + aMatch[1] + "=" + aMatch[3];
									}
								}
								
								sReplace += sFLVPlayer + "'> <PARAM NAME='quality' VALUE='" + sQuality + "' > <PARAM NAME='bgcolor' VALUE='" + sBGColor + "'> ";
								sReplace += "<PARAM NAME='FlashVars' VALUE='flvURL=" + sHREF;
								if (sFlashVars != undefined && sFlashVars.length > 0)
									sReplace += "&" + sFlashVars;
								sReplace += sJumpFlashVars + "' > <EMBED src='" + sFLVPlayer + "' quality='" + sQuality + "' bgcolor='" + sBGColor + "' width='" + iWidth + "' height='" + iHeight + "' ";
								sReplace += "FlashVars='flvURL=" + sHREF;
								if (sFlashVars != undefined && sFlashVars.length > 0) {
									sReplace += "&" + sFlashVars;
								}
								sReplace += sJumpFlashVars + "' NAME='' ALIGN='' TYPE='application/x-shockwave-flash' PLUGINSPAGE='http://www.macromedia.com/go/getflashplayer'> ";
							}
							else {
								sReplace += sHREF + "'> <PARAM NAME='quality' VALUE='" + sQuality + "' > <PARAM NAME='bgcolor' VALUE='" + sBGColor + "'> ";
								if (sFlashVars != undefined && sFlashVars.length > 0)
									sReplace += "<PARAM NAME='FlashVars' VALUE='" + sFlashVars + "&embdWidth=" + iWidth + "&embdHeight=" + iHeight + "' > ";
								sReplace += "<EMBED src='" + sHREF + "' quality='" + sQuality + "' bgcolor='" + sBGColor + "' width='" + iWidth + "' height='" + iHeight + "' ";
								if (sFlashVars != undefined && sFlashVars.length > 0)
									sReplace += "FlashVars='" + sFlashVars + "&embdWidth=" + iWidth + "&embdHeight=" + iHeight + "' ";
								sReplace += "NAME='' ALIGN='' TYPE='application/x-shockwave-flash' PLUGINSPAGE='http://www.macromedia.com/go/getflashplayer'> ";
							}
							sReplace += "</EMBED> </OBJECT>";
						}
						if (sReplace.length > 0) {
							var sUserAgent = navigator.userAgent;
							var bySafari = sUserAgent.indexOf('Safari') > -1;
							var byOpera = sUserAgent.indexOf('Opera') > -1;
							var byIE7 = sUserAgent.indexOf("MSIE 7") > -1;
							var byIE6 = sUserAgent.indexOf("MSIE 6") > -1;
							var nSafariBuild = -1;
							if (bySafari) {
								nSafariBuild = Number(sUserAgent.substring(sUserAgent.indexOf('Safari')+7));
							}
							//Get any Thickbox parameters
							var byThickBox = false;
							//Setup ThickBox parameters
							if (sThickBox != undefined && sThickBox.length > 0 && ! bySafari && ! byIE6) {
								var aParams = sThickBox.split(",");
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
									byThickBox = true;
							}
							
							//Open in Thickbox
							if (byThickBox) {
								_vPIP_Revert(aDIVs);
								_vPIP_TB_show(sThickBoxCaption, sReplace, Number(iWidth), Number(iHeight), sThickBoxBackground);	
							}
							// Open in page location
							else {
								//Add [X Close] button to revert to original <DIV ...> data.
								sReplace = "<div style=\"padding-right: " + (iWidth - 49) + "px\" ><a href=\"javascript: vPIPClose(" + iCurrDIVid  + ", " + iCurrLink + ");\" title=\"Close Movie\" onMouseOver=\"document.vPIPImage" + (iCurrDIVid * 10) + iCurrLink + ".src='" + vPIPpath + "close_hover.gif';\" onMouseOut=\"document.vPIPImage" + (iCurrDIVid * 10) + iCurrLink + ".src='" + vPIPpath + "close_grey.gif';\" style=\" background: transparent;\" ><img src=\"" + vPIPpath + "close_grey.gif\" name=\"vPIPImage" + (iCurrDIVid * 10) + iCurrLink + "\" style=\"border: none;\"  /></a></div>" + sReplace;
									
								// Mac Safari version 1.3.2 does not correctly close a replaced media object, so revert is disabled for Safari
								if (! (bySafari && nSafariBuild < 420)) {
									//Close any <DIVs set to revert
									_vPIP_Revert(aDIVs);
								}
								
								//If "hVlogTarget" class identified,
								//   add HTML outside it.
								sReplace = _vPIP_AddOutsideTarget(sInnerHTML, sReplace);
								
								oDiv.innerHTML = sReplace;
								aDIVs[iCurrDIVid][iCurrLink][iOpenPos] = true;
							}
						}
							
					}
					else {
						if (sMimeType != undefined) {
							setTimeout("Unsuported mime type: \"" + sMimeType + "\".", 0);
							if (oInitiator.href.toLowerCase().indexOf("http://") > -1)
								window.open(oInitiator.href, "_self");
							else if (sHREF != undefined) 
								window.open(sHREF, "_self");
						}
						else  {
							setTimeout("Unsuported file extension: \"" + sFileExt + "\".", 0);
							if (oInitiator.href.toLowerCase().indexOf("http://") > -1)
								window.open(oInitiator.href, "_self");
							else if (sHREF != undefined) 
								window.open(sHREF, "_self");
						}
					}
				}
				else {
					setTimeout("Missing href=\"...\" attribute.", 0);
					if (oInitiator.href.toLowerCase().indexOf("http://") > -1)
						window.open(oInitiator.href, "_self");
					else if (sHREF != undefined) 
						window.open(sHREF, "_self");
				}
		}
		else {
			setTimeout("video Playing In Place cannot execute because the containing <DIV ...>...</DIV> tag is missing.", 0);
			if (oInitiator.href.toLowerCase().indexOf("http://") > -1)
				window.open(oInitiator.href, "_self");
		}
	}
	else {
		setTimeout("video Playing In Place cannot execute because the target <A ...>...</A> tag could not be found.", 0);
		if (oInitiator.href.toLowerCase().indexOf("http://") > -1)
			window.open(oInitiator.href, "_self");
	}
	
	return;
	
}

function _vPIP_Revert(aDIVs) {
	for(var j=0; j < aDIVs.length; j++) {
		for(var k=3; k<aDIVs[j].length; k++) {
			if (aDIVs[j][k][iRevertPos]) {
				aDIVs[j][iDIVPos].innerHTML = aDIVs[j][iOrigHTMLPos];
				aDIVs[j][k][iOpenPos] = false;
			}
		}
	}

}

function _vPIP_CloseThisDiv(aDIVs, iCurrDIVid) {
	for(var k=3; k<aDIVs[iCurrDIVid].length; k++) {
		if (aDIVs[iCurrDIVid][k][iRevertPos]) {
			aDIVs[iCurrDIVid][iDIVPos].innerHTML = aDIVs[iCurrDIVid][iOrigHTMLPos];
			aDIVs[iCurrDIVid][k][iOpenPos] = false;
		}
	}

}

function _vPIP_AddOutsideTarget(sInnerHTML, sRevert) {
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
	if (bySafari && nSafariBuild < 420) {
		document.location.reload();
	}
	else {
		if (Number(sDivLoc) != NaN && Number(sLinkLoc) != NaN) {
			var iDivLoc = Number(sDivLoc);
			var iLinkLoc = Number(sLinkLoc);
			aDIVs[iDivLoc][iDIVPos].innerHTML = aDIVs[iDivLoc][iOrigHTMLPos];
			aDIVs[iDivLoc][iLinkLoc][iOpenPos] = false;
		}
	}

}

/**
 * Find oDiv in aDIVs array.
 * Returns array position in aDIVs that oDiv is found or -1
 */
function _vPIP_findDIV(oDiv) {
	var i;
	var iFound = -1;
	if (oDiv.id != undefined || oDiv.id.length > 0) {
		
		for(i=0; i<aDIVs.length; i++) {
			if (aDIVs[i][iDIVIDPos] === oDiv.id) {
				iFound = i;
				break;
			}
		}
	}
	
	return iFound;
}

function _vPIP_findLinkID(aDIV, iCurrLinkid) {
	var iFound = -1;
	for (var i=3; i<aDIV.length; i++) {
		if (aDIV[i][iLinkIDPos] == iCurrLinkid) {
			iFound = i;
			break;
		}
	}
	
	return iFound;
}

function _vPIP_findLinkInDiv(aDiv, iLinkid) {
	var iLinkPosInDiv = -1;
	for(var i=3; i< aDiv.length; i++) {
		if (aDiv[i][iLinkIDPos] != undefined) {
			if (aDiv[i][iLinkIDPos] == iLinkid) {
				iLinkPosInDiv = i;
				break;
			}
		}
	}
	
	return iLinkPosInDiv;
}

function _vPIP_addEvent(obj, evType, fn){
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

function _vPIP_getvPIPPath() {
	var scripts = document.getElementsByTagName ( "script" );
	var src;
	var index;
        var sVPIPpath = "";
	for (var i=0; i<scripts.length; i++) {
		src = scripts[i].getAttribute ( "src" );
		if (src != undefined) {
			index = src.search(/vpip.js/i);
			if (index > -1) {
				sVPIPpath = src.substring ( 0, index);
				break;
			}
		}
	}

        return sVPIPpath;
}

function _vPIP_toAlphaNum(sString, sAllowed) {
	var i;
	var sNewString = "";
	if (sString == undefined) {
		return sString;
	}
	else {
		for (i=0; i<sString.length; i++) {
         ch = sString.charAt(i);
			if (ch >= " "  && ch <= "z") {
				sNewString += sString.charAt(i);
			}
         else if (sAllowed != undefined && sAllowed.indexOf(ch) > -1) {
				sNewString += sString.charAt(i);
         }
		}
		return sNewString;
	}
}

/*vPIP version of ThickBox By Cody Lindley (http://www.codylindley.com)
 * Thickbox is built on top of the very light weight jquery library.
*/


function _vPIP_TB_show(sCaption, sEmbed, vPIP_TB_WIDTH, vPIP_TB_HEIGHT, sBackground) {//function called when the user clicks on a thickbox link
	try {

		$("body").append("<div id='vPIP_TB_overlay'></div><div id='vPIP_TB_window'></div>");
		$("#vPIP_TB_overlay").click(_vPIP_TB_remove);
		$(window).scroll(_vPIP_TB_position);
 

		if (sCaption == undefined) 
			sCaption = '';
		vPIP_TB_WIDTH += 30;
		vPIP_TB_HEIGHT += 60;
		var sEntry = "<div id='vPIP_TB_caption'>"+sCaption+"</div><div id='vPIP_TB_closeWindow'><a href='javascript: none' id='vPIP_TB_closeWindowButton'>close</a></div><div id='vPIP_Object'>" + sEmbed + "</div>";
		$("#vPIP_TB_window").html(sEntry); 
		document.getElementById("vPIP_TB_window").style.backgroundColor = sBackground;
		document.getElementById("vPIP_TB_window").style.backgroundColor = sBackground;
		$("#vPIP_TB_closeWindowButton").click(_vPIP_TB_remove);
		_vPIP_TB_position(vPIP_TB_WIDTH, vPIP_TB_HEIGHT);
		$("#vPIP_TB_window").show(); 
	} catch(e) {
		setTimeout(e, 0);
	}
}

//helper functions below

function _vPIP_TB_remove() {
	$("#vPIP_TB_window").html(""); 
	$("#vPIP_TB_window").fadeOut("fast",function(){$('#vPIP_TB_window,#vPIP_TB_overlay').remove();});
	return false;
}

function _vPIP_TB_position(vPIP_TB_WIDTH, vPIP_TB_HEIGHT) {
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
	
	$("#vPIP_TB_window").css({width:vPIP_TB_WIDTH+"px",height:vPIP_TB_HEIGHT+"px",
	left: ((w - vPIP_TB_WIDTH)/2)+"px", top: ((h - vPIP_TB_HEIGHT)/2)+"px" });
	$("#vPIP_TB_overlay").css("height",yScroll +"px");
}

// ** End of vPIP Thickbox code **

