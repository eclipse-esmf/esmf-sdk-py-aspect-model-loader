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

import abc
from typing import Optional, List, Dict

from esmf_aspect_meta_model_python.base.has_urn import HasUrn
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class IsDescribed(HasUrn, metaclass=abc.ABCMeta):
    """Base class from which all Meta Model elements with descriptions inherit.
    Class prescribes methods to get preferred names, descriptions and
    see elements.
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (
            PropertyFunc.has_properties(subclass, IsDescribed.name, IsDescribed.preferred_names, IsDescribed.descriptions, IsDescribed.see)
            and callable(subclass.get_preferred_name)
            and callable(subclass.get_description)
        )

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def preferred_names(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    def descriptions(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    def see(self) -> List[str]:
        raise NotImplementedError

    def get_preferred_name(self, locale: str) -> Optional[str]:
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        return self.descriptions.get(locale)
