""" In compiled programming languages like Java or C++ the inheritances of classes are determined during
compile time. If one wants to check whether a given instance is of a certain type, the visitor pattern is often the right choice.

In Python, instead of a visitor, it is common practice to use the builtin-functions isinstance(instance, cls)
or issubclass(cls1, cls2). Class definitions and inheritance can change during runtime,
therefore it is not trivial that isinstance() and issubclass() will always return the right result.

The two functions internally call the method __subclasshook__() that are implemented in abstract classes.
This module checks whether the __subclasshook__-methods are correct so that
issubclass() and isinstance() behave correctly.
"""

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

from typing import Any
from esmf_aspect_meta_model_python import *
from esmf_aspect_meta_model_python.base.has_urn import HasUrn
from esmf_aspect_meta_model_python.base.is_described import IsDescribed
from esmf_aspect_meta_model_python.impl.default_aspect import DefaultAspect

""" Classes defined in the Python SDK and their corresponding subclasses. Each pair
of class and subclass should give issubclass(subclass, cls) is True.
"""
SUBCLASSES: dict[type, list[Any]] = {
    HasUrn: [IsDescribed, HasUrn],
    Aspect: [DefaultAspect],
    Event: [DefaultEvent],
    Operation: [DefaultOperation],
    Property: [DefaultProperty],
    QuantityKind: [DefaultQuantityKind],
    Unit: [DefaultUnit],
    Characteristic: [
        Code,
        Either,
        Enumeration,
        SingleEntity,
        State,
        StructuredValue,
        Trait,
        Collection,
        List,
        Set,
        SortedSet,
        TimeSeries,
        Quantifiable,
        Duration,
        Measurement,
        DefaultCode,
        DefaultEither,
        DefaultEnumeration,
        DefaultSingleEntity,
        DefaultState,
        DefaultStructuredValue,
        DefaultTrait,
        DefaultCollection,
        DefaultList,
        DefaultSet,
        DefaultSortedSet,
        DefaultTimeSeries,
        DefaultQuantifiable,
        DefaultDuration,
        DefaultMeasurement,
    ],
    Code: [DefaultCode],
    Either: [DefaultEither],
    Enumeration: [State, DefaultEnumeration, DefaultState],
    SingleEntity: [DefaultSingleEntity],
    State: [DefaultState],
    StructuredValue: [DefaultStructuredValue],
    Trait: [DefaultTrait],
    Collection: [List, Set, SortedSet, TimeSeries, DefaultCollection, DefaultList, DefaultSet, DefaultSortedSet, DefaultTimeSeries],
    List: [DefaultList],
    Set: [DefaultSet],
    SortedSet: [TimeSeries, DefaultSortedSet, DefaultTimeSeries],
    TimeSeries: [DefaultTimeSeries],
    Duration: [DefaultDuration],
    Measurement: [DefaultMeasurement],
    Quantifiable: [Duration, Measurement, DefaultQuantifiable, DefaultDuration, DefaultMeasurement],
    Constraint: [
        EncodingConstraint,
        FixedPointConstraint,
        LanguageConstraint,
        LengthConstraint,
        LocaleConstraint,
        RangeConstraint,
        RegularExpressionConstraint,
        DefaultConstraint,
        DefaultEncodingConstraint,
        DefaultFixedPointConstraint,
        DefaultLanguageConstraint,
        DefaultLengthConstraint,
        DefaultLocaleConstraint,
        DefaultRangeConstraint,
        DefaultRegularExpressionConstraint,
    ],
    EncodingConstraint: [DefaultEncodingConstraint],
    FixedPointConstraint: [DefaultFixedPointConstraint],
    LanguageConstraint: [DefaultLanguageConstraint],
    LengthConstraint: [DefaultLengthConstraint],
    LocaleConstraint: [DefaultLocaleConstraint],
    RangeConstraint: [DefaultRangeConstraint],
    RegularExpressionConstraint: [DefaultRegularExpressionConstraint],
    AbstractEntity: [DefaultAbstractEntity],
    ComplexType: [AbstractEntity, Entity, DefaultComplexType, DefaultAbstractEntity, DefaultEntity],
    Entity: [DefaultEntity],
    DefaultAspect: [],
    DefaultEvent: [],
    DefaultOperation: [],
    DefaultProperty: [],
    DefaultQuantityKind: [],
    DefaultUnit: [],
    DefaultCharacteristic: [
        DefaultCode,
        DefaultEither,
        DefaultEnumeration,
        DefaultSingleEntity,
        DefaultState,
        DefaultStructuredValue,
        DefaultTrait,
        DefaultCollection,
        DefaultList,
        DefaultSet,
        DefaultSortedSet,
        DefaultTimeSeries,
        DefaultQuantifiable,
        DefaultDuration,
        DefaultMeasurement,
    ],
    DefaultCode: [],
    DefaultEither: [],
    DefaultEnumeration: [DefaultState],
    DefaultSingleEntity: [],
    DefaultState: [],
    DefaultStructuredValue: [],
    DefaultTrait: [],
    DefaultCollection: [DefaultList, DefaultSet, DefaultSortedSet, DefaultTimeSeries],
    DefaultList: [],
    DefaultSet: [],
    DefaultSortedSet: [],
    DefaultTimeSeries: [],
    DefaultDuration: [],
    DefaultMeasurement: [],
    DefaultQuantifiable: [],
    DefaultConstraint: [
        DefaultConstraint,
        DefaultEncodingConstraint,
        DefaultFixedPointConstraint,
        DefaultLanguageConstraint,
        DefaultLengthConstraint,
        DefaultLocaleConstraint,
        DefaultRangeConstraint,
        DefaultRegularExpressionConstraint,
    ],
    DefaultEncodingConstraint: [],
    DefaultFixedPointConstraint: [],
    DefaultLanguageConstraint: [],
    DefaultLengthConstraint: [],
    DefaultLocaleConstraint: [],
    DefaultRangeConstraint: [],
    DefaultRegularExpressionConstraint: [],
    DefaultAbstractEntity: [],
    DefaultComplexType: [DefaultAbstractEntity, DefaultEntity],
    DefaultEntity: [],
}


def test_base_subclasses() -> None:
    for cls in SUBCLASSES.keys():
        for subclass in SUBCLASSES[cls]:
            assert issubclass(subclass, cls)

    assert not issubclass(HasUrn, IsDescribed)
