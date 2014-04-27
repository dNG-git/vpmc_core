# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.upnp.resources.MpEntryAudio
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

from dNG.pas.data.binary import Binary
from dNG.pas.data.media.audio import Audio
from dNG.pas.data.media.audio_metadata import AudioMetadata
from dNG.pas.data.upnp.resources.abstract_stream import AbstractStream
from dNG.pas.database.instances.mp_upnp_audio_resource import MpUpnpAudioResource as _DbMpUpnpAudioResource
from dNG.pas.data.upnp.variable import Variable
from .mp_entry import MpEntry

class MpEntryAudio(MpEntry):
#
	"""
"MpEntryAudio" is used for UPnP audio database entries.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def _content_stream_append_metadata(self, resource):
	#
		"""
Appends audio metadata to the given stream resource.

:since: v0.1.01
		"""

		# pylint: disable=star-args

		if (isinstance(resource, AbstractStream) and resource.is_supported("metadata")):
		#
			entry_data = self.data_get("size", "duration", "channels", "bitrate", "bps", "sample_frequency")
			data = { }

			if (entry_data['duration'] != None): data['duration'] = Variable.get_upnp_duration(entry_data['duration'])
			if (entry_data['channels'] != None): data['nrAudioChannels'] = entry_data['channels']

			if (entry_data['bitrate'] != None): data['bitrate'] = int(entry_data['bitrate'] / 8)
			elif (entry_data['duration'] != None and entry_data['size'] != None): data['bitrate'] = int(entry_data['size'] / entry_data['duration'])

			if (entry_data['bps'] != None): data['bitsPerSample'] = entry_data['bps']
			if (entry_data['sample_frequency'] != None): data['sampleFrequency'] = entry_data['sample_frequency']

			if (len(data) > 0): resource.set_metadata(**data)
		#
	#

	def content_get(self, position):
	#
		"""
Returns the UPnP content resource at the given position.

:param position: Position of the UPnP content resource to be returned

:return: (object) UPnP resource; None if position is undefined
:since:  v0.1.01
		"""

		_return = MpEntry.content_get(self, position)
		if (self.type & MpEntry.TYPE_CDS_ITEM == MpEntry.TYPE_CDS_ITEM): self._content_stream_append_metadata(_return)

		return _return
	#

	def content_get_list(self):
	#
		"""
Returns the UPnP content resources between offset and limit.

:return: (list) List of UPnP resources
:since:  v0.1.01
		"""

		_return = MpEntry.content_get_list(self)

		if (self.type & MpEntry.TYPE_CDS_ITEM == MpEntry.TYPE_CDS_ITEM):
		#
			for resource in _return: self._content_stream_append_metadata(resource)
		#

		return _return
	#

	def content_get_list_of_type(self, _type = None):
	#
		"""
Returns the UPnP content resources of the given type or all ones between
offset and limit.

:param _type: UPnP resource type to be returned

:return: (list) List of UPnP resources
:since:  v0.1.01
		"""

		_return = MpEntry.content_get_list_of_type(self, _type)

		if (self.type & MpEntry.TYPE_CDS_ITEM == MpEntry.TYPE_CDS_ITEM):
		#
			for resource in _return: self._content_stream_append_metadata(resource)
		#

		return _return
	#

	def data_set(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		if (self.local.db_instance == None): self.local.db_instance = _DbMpUpnpAudioResource()

		with self:
		#
			MpEntry.data_set(self, **kwargs)

			if ("duration" in kwargs): self.local.db_instance.duration = kwargs['duration']
			if ("artist" in kwargs): self.local.db_instance.artist = Binary.utf8(kwargs['artist'])
			if ("genre" in kwargs): self.local.db_instance.genre = Binary.utf8(kwargs['genre'])
			if ("description" in kwargs): self.local.db_instance.description = Binary.utf8(kwargs['description'])
			if ("album" in kwargs): self.local.db_instance.album = Binary.utf8(kwargs['album'])
			if ("album_artist" in kwargs): self.local.db_instance.album_artist = Binary.utf8(kwargs['album_artist'])
			if ("track_number" in kwargs): self.local.db_instance.track_number = kwargs['track_number']
			if ("codec" in kwargs): self.local.db_instance.codec = kwargs['codec']
			if ("channels" in kwargs): self.local.db_instance.channels = kwargs['channels']
			if ("bitrate" in kwargs): self.local.db_instance.bitrate = kwargs['bitrate']
			if ("bps" in kwargs): self.local.db_instance.bps = kwargs['bps']
			if ("sample_frequency" in kwargs): self.local.db_instance.sample_frequency = kwargs['sample_frequency']
			if ("encoder" in kwargs): self.local.db_instance.encoder = Binary.utf8(kwargs['encoder'])
		#
	#

	def _init_encapsulated_resource(self):
	#
		"""
Initialize an new encapsulated UPnP resource.

:since: v0.1.00
		"""

		if (self.local.db_instance == None): self.local.db_instance = _DbMpUpnpAudioResource()
		MpEntry._init_encapsulated_resource(self)
	#

	def metadata_add_didl_xml_node(self, xml_resource, xml_node_path, parent_id = None):
	#
		"""
Uses the given XML resource to add the DIDL metadata of this UPnP resource.

:param xml_resource: XML resource
:param xml_base_path: UPnP resource XML base path (e.g. "DIDL-Lite
                      item")

:since:  v0.1.01
		"""

		MpEntry.metadata_add_didl_xml_node(self, xml_resource, xml_node_path, parent_id)

		if (self.get_type() & MpEntryAudio.TYPE_CDS_ITEM == MpEntryAudio.TYPE_CDS_ITEM and xml_resource.node_get(xml_node_path) != None):
		#
			entry_data = self.data_get("artist", "genre", "description", "album", "album_artist", "track_number")

			if (entry_data['album'] != None): xml_resource.node_add("{0} upnp:album".format(xml_node_path), entry_data['album'])

			if (entry_data['album_artist'] != None):
			#
				xml_resource.node_add("{0} upnp:albumArtist".format(xml_node_path), entry_data['album_artist'])
				xml_resource.node_add("{0} upnp:artist".format(xml_node_path), entry_data['album_artist'], { "role": "AlbumArtist" })
			#

			if (entry_data['artist'] != None):
			#
				xml_resource.node_add("{0} dc:creator".format(xml_node_path), entry_data['artist'])
				xml_resource.node_add("{0} upnp:artist".format(xml_node_path), entry_data['artist'], { "role": "Performer" })
			#

			if (entry_data['description'] != None): xml_resource.node_add("{0} dc:description".format(xml_node_path), entry_data['description'])
			if (entry_data['genre'] != None): xml_resource.node_add("{0} upnp:genre".format(xml_node_path), entry_data['genre'])
			if (entry_data['track_number'] != None): xml_resource.node_add("{0} upnp:originalTrackNumber".format(xml_node_path), entry_data['track_number'])
		#
	#

	def metadata_filter_didl_xml_node(self, xml_resource, xml_node_path):
	#
		"""
Uses the given XML resource to remove DIDL metadata not requested by the
client.

:param xml_resource: XML resource
:param xml_base_path: UPnP resource XML base path (e.g. "DIDL-Lite
                      item")

:since:  v0.1.01
		"""

		MpEntry.metadata_filter_didl_xml_node(self, xml_resource, xml_node_path)

		if (self.get_type() & MpEntryAudio.TYPE_CDS_ITEM == MpEntryAudio.TYPE_CDS_ITEM and xml_resource.node_get(xml_node_path) != None):
		#
			didl_fields = self.get_didl_fields()

			if (len(didl_fields) > 0):
			#
				if ("upnp:album" not in didl_fields): xml_resource.node_remove("{0} upnp:album".format(xml_node_path))
				if ("upnp:albumArtist" not in didl_fields): xml_resource.node_remove("{0} upnp:albumArtist".format(xml_node_path))
				if ("dc:creator" not in didl_fields): xml_resource.node_remove("{0} dc:creator".format(xml_node_path))
				if ("upnp:artist" not in didl_fields): xml_resource.node_remove("{0} upnp:artist".format(xml_node_path))
				if ("dc:description" not in didl_fields): xml_resource.node_remove("{0} dc:description".format(xml_node_path))
				if ("upnp:genre" not in didl_fields): xml_resource.node_remove("{0} upnp:genre".format(xml_node_path))
				if ("upnp:originalTrackNumber" not in didl_fields): xml_resource.node_remove("{0} upnp:originalTrackNumber".format(xml_node_path))
			#
		#
	#

	def refresh_metadata(self):
	#
		"""
Refresh metadata associated with this MpEntryAudio.

:since: v0.1.00
		"""

		MpEntry.refresh_metadata(self)

		encapsulated_resource = self.load_encapsulated_resource()

		if (encapsulated_resource != None and encapsulated_resource.is_filesystem_resource() and encapsulated_resource.get_path() != None):
		#
			audio = Audio()
			metadata = (audio.get_metadata() if (audio.open_url(encapsulated_resource.get_id())) else None)

			if (isinstance(metadata, AudioMetadata)):
			#
				self.data_set(
					title = metadata.get_title(),
					mimetype = metadata.get_mimetype(),
					metadata = metadata.get_json(),
					duration = metadata.get_length(),
					artist = metadata.get_artist(),
					genre = metadata.get_genre(),
					description = metadata.get_comment(),
					album = metadata.get_album(),
					album_artist = metadata.get_album_artist(),
					track_number = metadata.get_track(),
					codec = metadata.get_codec(),
					channels = metadata.get_channels(),
					bitrate = metadata.get_bitrate(),
					bps = metadata.get_bps(),
					sample_frequency = metadata.get_sample_rate()
				)
			#
		#
	#
#

##j## EOF