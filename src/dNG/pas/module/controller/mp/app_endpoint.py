# -*- coding: utf-8 -*-
##j## BOF

"""
MediaProvider
A device centric multimedia solution
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?mp;core

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
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpCoreVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.session.implementation import Implementation as Session
from dNG.pas.data.text.link import Link
from dNG.pas.data.upnp.client_user_agent_mixin import ClientUserAgentMixin
from dNG.pas.module.controller.upnp.access_check_mixin import AccessCheckMixin
from .module import Module

class AppEndpoint(Module, AccessCheckMixin, ClientUserAgentMixin):
#
	"""
Service for "m=mp;s=app_endpoint"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractHttpController)

:since: v0.2.00
		"""

		Module.__init__(self)
		AccessCheckMixin.__init__(self)
		ClientUserAgentMixin.__init__(self)
	#

	def execute_api_get_configuration(self):
	#
		"""
Action for "api_get_configuration"

:since: v0.2.00
		"""

		self.client_user_agent = self.request.get_header("User-Agent")

		self.response.init(True)
		self.response.set_header("Access-Control-Allow-Origin", "*")

		if (not self.response.is_supported("dict_result_renderer")): raise TranslatableError("core_access_denied", 403)

		self._ensure_access_granted()

		session = Session.load()

		if (session.get("mp.leanback.user_agent") != self.client_user_agent):
		#
			session.set("mp.leanback.access_granted", True)
			session.set("mp.leanback.user_agent", self.client_user_agent)
			session.set_cookie(Settings.get("pas_http_site_cookies_supported", True))

			session.save()

			self.request.set_session(session)
		#

		self.response.set_result({ "url": Link.get_preferred("upnp").build_url(Link.TYPE_ABSOLUTE_URL, { "m": "mp", "s": "leanback", "a": "dashboard" }) })
	#
#

##j## EOF