# Copyright 2015 Google Inc.
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

"""
This file contains all of the configuration values for the application.
Update this file with the values for your specific Google Cloud project.
You can create and manage projects at https://console.developers.google.com
"""

import os

# The secret key is used by Flask to encrypt session cookies.
# [START secret_key]
SECRET_KEY = 'secret'
# [END secret_key]

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'FileParserApp'
GOOGLE_OAUTH2_CLIENT_ID = \
    '558069950610-s2nen8cktt2l6p82u449kv7l515qkmk4'
GOOGLE_OAUTH2_CLIENT_SECRET = '69LjL6C_D6HUBKaFdCrJXvvA'