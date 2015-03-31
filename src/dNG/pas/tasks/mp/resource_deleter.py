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

# pylint: disable=import-error,no-name-in-module

from math import ceil

from dNG.pas.data.settings import Settings
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.data.upnp.resources.mp_entry import MpEntry
from dNG.pas.database.condition_definition import ConditionDefinition
from dNG.pas.database.transaction_context import TransactionContext
from dNG.pas.runtime.value_exception import ValueException
from dNG.pas.tasks.abstract_lrt_hook import AbstractLrtHook

class ResourceDeleter(AbstractLrtHook):
#
	"""
"ResourceDeleter" deletes all database entries recursively for the given
resource.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.1.02
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, resource = None):
	#
		"""
Constructor __init__(ResourceDeleter)

:param resource: UPnP resource

:since: v0.1.02
		"""

		AbstractLrtHook.__init__(self)

		self.resource = resource
		"""
UPnP resource ID
		"""

		self.context_id = "dNG.pas.tasks.mp.ResourceDeleter"
	#

	def _get_condition_definition(self):
	#
		"""
Returns the condition definition instance used for identifying the root UPnP
resource to be deleted.

:return: (object) ConditionDefinition instance
:since:  v0.1.02
		"""

		if (self.resource is None): raise ValueException("UPnP resource is invalid")

		_return = ConditionDefinition()
		_return.add_exact_match_condition("resource", self.resource)

		return _return
	#

	def _run_hook(self, **kwargs):
	#
		"""
Hook execution

:return: (mixed) Task result
:since:  v0.1.02
		"""

		condition_definition = self._get_condition_definition()
		_return = MpEntry.get_entries_count_with_condition(condition_definition)

		limit = Settings.get("pas_database_delete_iterator_limit", 50)
		entry_iterator_count = ceil(_return / limit)

		LogLine.info("{0!r} removes {1:d} matches", self, _return, context = "mp_server")

		for _ in range(0, entry_iterator_count):
		#
			with TransactionContext():
			#
				entries = MpEntry.load_entries_list_with_condition(condition_definition, limit = limit)

				for entry in entries:
				#
					parent_entry = entry.load_parent()

					if (isinstance(parent_entry, MpEntry)): parent_entry.remove_content(entry)
					entry.delete()
				#
			#
		#

		return _return
	#
#

##j## EOF