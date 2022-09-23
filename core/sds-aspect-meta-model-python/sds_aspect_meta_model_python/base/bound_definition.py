#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import enum


@enum.unique
class BoundDefinition(enum.Enum):
    """Enumeration that holds the specifies the upper or lower boundary rule
    for a range constraint. Possible values are:
    OPEN, AT_LEAST, GREATER_THAN, LESS_THAN, AT_MOST
    """

    OPEN = "OPEN"
    AT_LEAST = "AT_LEAST"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    AT_MOST = "AT_MOST"
