# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007 Fluendo, S.L. (www.fluendo.com).
# All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with the
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.

import gettext

from flumotion.wizard.basesteps import AudioEncoderStep
from flumotion.wizard.models import AudioEncoder

__version__ = "$Rev$"
_ = gettext.gettext


class SpeexAudioEncoder(AudioEncoder):
    component_type = 'speex-encoder'

    def __init__(self):
        super(SpeexAudioEncoder, self).__init__()

        self.properties.bitrate = 11

    def getProperties(self):
        properties = super(SpeexAudioEncoder, self).getProperties()
        properties['bitrate'] *= 1000
        return properties


class SpeexStep(AudioEncoderStep):
    name = _('Speex encoder')
    sidebar_name = _('Speex')
    component_type = 'speex'
    icon = 'xiphfish.png'

    # WizardStep

    def setup(self):
        # Should be 2150 instead of 3 -> 3000
        self.bitrate.set_range(3, 30)
        self.bitrate.set_value(11)

        self.bitrate.data_type = int

        self.add_proxy(self.model.properties, ['bitrate'])

    def worker_changed(self):
        self.model.worker = self.worker
        self.wizard.require_elements(self.worker, 'speexenc')


class SpeexWizardPlugin(object):
    def __init__(self, wizard):
        self.wizard = wizard
        self.model = SpeexAudioEncoder()

    def get_conversion_step(self):
        return SpeexStep(self.wizard, self.model)