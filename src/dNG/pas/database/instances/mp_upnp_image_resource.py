# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.database.instances.MpUpnpImageResource
"""
"""n// NOTE
----------------------------------------------------------------------------
MediaProvider
A device centric multimedia solution
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?mp;core

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(mpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from sqlalchemy import Column, ForeignKey, INT, SMALLINT, TEXT, VARCHAR

from .mp_upnp_resource import MpUpnpResource

class MpUpnpImageResource(MpUpnpResource):
#
	"""
"MpUpnpImageResource" represents an database UPnP image resource entry.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	__tablename__ = "{0}_mp_upnp_image_resource".format(MpUpnpResource.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.pas.data.upnp.resources.MpEntryImage"
	"""
Encapsulating SQLAlchemy database instance class name
	"""

	id = Column(VARCHAR(32), ForeignKey(MpUpnpResource.id), primary_key = True)
	"""
mp_upnp_image_resource.id
	"""
	artist = Column(VARCHAR(255))
	"""
mp_upnp_image_resource.artist
	"""
	description = Column(TEXT)
	"""
mp_upnp_image_resource.description
	"""
	width = Column(INT)
	"""
mp_upnp_image_resource.width
	"""
	height = Column(INT)
	"""
mp_upnp_image_resource.height
	"""
	bpp = Column(SMALLINT)
	"""
mp_upnp_image_resource.bpp
	"""
	creator = Column(VARCHAR(255))
	"""
mp_upnp_image_resource.creator
	"""

	__mapper_args__ = { "polymorphic_identity": "MpUpnpImageResource" }
	"""
sqlalchemy.org: Other options are passed to mapper() using the
                __mapper_args__ class variable.
	"""
#

##j## EOF