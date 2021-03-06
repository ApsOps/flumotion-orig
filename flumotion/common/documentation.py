# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008,2009 Fluendo, S.L.
# Copyright (C) 2010,2011 Flumotion Services, S.A.
# All rights reserved.
#
# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

"""creating links to online/installed documentation.
Integration with online and installed documentation for messages.
"""

__version__ = "$Rev: 6125 $"

from flumotion.common import common, errors
from flumotion.common.i18n import getLL
from flumotion.configure import configure

from flumotion.common.i18n import N_, gettexter

T_ = gettexter()


def getMessageWebLink(message):
    """
    Get the on-line documentation link target for this message, if any.

    @param message: the message
    @type message: L{flumotion.common.messages.Message}
    """
    if not message.description:
        return None

    from flumotion.project import project
    try:
        projectURL = project.get(message.project, 'docurl')
    except errors.NoProjectError:
        projectURL = None

    return getWebLink(section=message.section,
                      anchor=(message.anchor or ''),
                      version=message.version,
                      projectURL=projectURL)


def getWebLink(section, anchor, version=None, projectURL=None):
    """
    Get a documentation link based on the parameters.

    @param section: section, usually the name of the html file
    @type  section: string
    @param  anchor: name of the anchor, part of a section
    @type   anchor: string
    @param  version: optional, version to use. If this is not specified
                     the version from configure.version will be used
    @type   version: string
    @param  projectURL, url for the project this link belongs to.
    @type   projectURL: string
    @returns: the constructed documentation link
    @rtype: string
    """
    if version is None:
        version = configure.version

    # FIXME: if the version has a nano, do something sensible, like
    # drop the nano or always link to trunk version
    versionTuple = version.split('.')
    version = common.versionTupleToString(versionTuple[:3])

    if projectURL is None:
        projectURL = 'http://www.flumotion.net/doc/flumotion/manual'
    if anchor:
        anchor = '#%s' % anchor

    return '%s/%s/%s/html/%s.html%s' % (
        projectURL, getLL(), version, section, anchor)


def messageAddPythonInstall(message, moduleName):
    """
    Add text and link on how to install the given python module to the
    given message.
    """
    message.add(T_(N_("Please install the '%s' python module."), moduleName))
    message.description = T_(N_("Learn how to install Python modules."))
    message.section = 'appendix-installing-dependencies'
    message.anchor = 'section-installing-python-modules'


def messageAddFixBadPermissions(message):
    """
    Add link on how to change device permissions on Linux.
    """
    message.description = T_(N_("Learn how to change device permissions."))
    message.section = 'section-flumotion-troubleshoot'
    message.anchor = 'section-not-open'


def messageAddGStreamerInstall(message):
    """
    Add text and link on how to install the given python module to the
    given message.
    """
    message.description = T_(N_('Learn how to install GStreamer elements.'))
    message.section = 'section-installing-gstreamer-plugins'
