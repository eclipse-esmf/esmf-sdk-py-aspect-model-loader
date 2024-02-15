#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from os import getcwd
from pathlib import Path

from esmf_aspect_meta_model_python import AspectLoader, Event

RESOURCE_PATH = getcwd() / Path("tests/integration/resources/org.eclipse.esmf.test.event/2.0.0")


def test_loading_aspect_with_event() -> None:
    file_path = RESOURCE_PATH / "aspect_with_event.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.events is not None
    assert len(aspect.events) == 1
    event = aspect.events[0]
    assert isinstance(event, Event)
    assert event.name == "event1"


def test_loading_aspect_with_event_with_parameters() -> None:
    file_path = RESOURCE_PATH / "aspect_with_event_with_parameters.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.events is not None
    assert len(aspect.events) == 1
    event = aspect.events[0]
    assert isinstance(event, Event)
    assert len(event.parameters) == 2
    assert event.parameters[0].name == "property1"
    assert event.parameters[1].name == "property2"
    assert event.name == "event1"


def test_loading_aspect_with_multiple_event() -> None:
    file_path = RESOURCE_PATH / "aspect_with_multiple_event.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.events is not None
    assert len(aspect.events) == 3

    event1 = aspect.events[0]
    assert isinstance(event1, Event)
    assert event1.name == "event1"
    assert event1.preferred_names == {"en": "event one"}
    assert event1.descriptions == {"en": "event one description"}
    assert len(event1.see) == 1

    event1 = aspect.events[1]
    assert isinstance(event1, Event)
    assert event1.name == "event2"
    assert event1.preferred_names == {"en": "event two"}
    assert event1.descriptions == {"en": "event two description"}
    assert len(event1.see) == 1

    event1 = aspect.events[2]
    assert isinstance(event1, Event)
    assert event1.name == "event3"
    assert event1.preferred_names == {"en": "event three"}
    assert event1.descriptions == {"en": "event three description"}
    assert len(event1.see) == 1
