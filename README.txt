p4a.video
=========

Overview
--------

The *p4a.video* package provides a framework for handling video content on
the Zope 2 and Zope 3 platforms.  It was inspired by the Plone ATVideo
product and even borrows some UI.

Project Description
-------------------
*p4a.video* allows you to:

* convert a file object to a video
* extract the video metadata
* render an appropriate view (depending on the file format)

Installation
------------
Add these lines to your buildout.cfg file, and re-run your buildout.
Then install the add-ons from the Add/Remove products page in the
Plone Control Panel.::

    [buildout]
    ...
    
    eggs = 
        ...
        p4a.video
    
    [instance]
    ...
    
    zcml = 
        ...
        p4a.video


Features
--------

Video Files
~~~~~~~~~~~
* Support for:

  * Quicktime (MOV, MP4)
  * Windows Media (WMV, AVI, WMA, ASF)
  * RealMedia (RAM)
  * Flash (FLV, SWF)

* Upload a thumbnail image to represent the video
* When clicked, the video will start to play video
* edit form exposes metadata:

  * file type
  * author
  * height / width
  * duration
 
Video containers
~~~~~~~~~~~~~~~~
* Turn any folder into a video container
* Turn any smart folder (collection) into a video container
* Provides a video listing view with all videos in the folder, including:

  * thumbnail
  * title
  * description
  * metadata

* Video listing also shows:

  * tags
  * ratings
  * comments about each video

Video feeds
~~~~~~~~~~~
* Publish RSS feed of all the videos in a video container
* Feed entries can contain a link to the video view page, or a link to the
  actual video file (enclosure)
* Users can subscribe to a vodcast and have the videos downloaded to a
  desktop video player such as iTunes or Miro for offline viewing

Video feedback / commentary
~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Requires:

  * lovely.tag
  * p4a.plonetagging

* Users can rate videos (1 to 5 stars)

  * Plone keeps track of user ratings vs. editor ratings

* Users can tag videos

  * Plone keeps track of your tags and everyone's tags

* Users can comment on videos. Other users can reply to those comments in a
  threaded discussion
