# -*- coding: utf-8 -*-

# Copyright (c) 2016 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from calvin.actor.actor import Actor, ActionResult, manage, condition

from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)


class Facebook(Actor):
    """
    Post incoming tokens (text) as twitter status

    Input:
      status : A string
    """

    @manage([])
    def init(self):
        self.setup()

    def did_migrate(self):
        self.setup()

    def setup(self):
        self.use('calvinsys.web.facebook_module', shorthand='facebook')

    @condition(action_input=['status'])
    def post_update(self, status):
        msg = {'attachment': {'caption': 'caption',
                              'description': 'description',
                              'link': '',
                              'name': 'hi',
                              'picture': ''},
               'message': 'message_thisshouldwork'}

        #self['facebook'].post_update(msg)
        pict = {'picture' : '/home/emirkomo/Pictures/setup.jpg', 'message' : 'test from calvin'}
        self['facebook'].post_picture(pict)
        return ActionResult()

    action_priority = (post_update,)
    requires = ['calvinsys.web.facebook']
