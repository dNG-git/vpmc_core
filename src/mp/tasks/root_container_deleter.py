# -*- coding: utf-8 -*-

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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpCoreVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error,no-name-in-module

from dNG.database.condition_definition import ConditionDefinition
from dNG.runtime.value_exception import ValueException

from .resource_deleter import ResourceDeleter

class RootContainerDeleter(ResourceDeleter):
    """
"RootContainerDeleter" deletes all database entries for the given
UPnP root container ID.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self, root_container_id = None):
        """
Constructor __init__(ResourceDeleter)

:param root_container_id: UPnP root container ID

:since: v0.2.00
        """

        ResourceDeleter.__init__(self)

        self.root_container_id = root_container_id
        """
UPnP root resource IDgiven
        """
    #

    def _get_condition_definition(self):
        """
Returns the condition definition instance used for identifying the root
UPnP resource to be deleted.

:return: (object) ConditionDefinition instance
:since:  v0.2.00
        """

        if (self.root_container_id is None): raise ValueException("UPnP root container ID is invalid")

        _return = ConditionDefinition()
        _return.add_exact_match_condition("id_main", self.root_container_id)

        return _return
    #
#
