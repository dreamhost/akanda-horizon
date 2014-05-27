# Copyright 2014 DreamHost, LLC
#
# Author: DreamHost, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


TEST_CHOICE = (
    (0, 'Test'),
)

PROTOCOL_CHOICES = (
    (0, 'TCP'),
    (1, 'UDP'),
)

NEW_PROTOCOL_CHOICES = (
    ('tcp', 'TCP'),
    ('udp', 'UDP'),
)

NEW_PROTOCOL_CHOICES_DICT = dict(NEW_PROTOCOL_CHOICES)

POLICY_CHOICES = (
    ('pass', 'Allow'),
    ('block', 'Deny'),
)

POLICY_CHOICES_DICT = dict(POLICY_CHOICES)
