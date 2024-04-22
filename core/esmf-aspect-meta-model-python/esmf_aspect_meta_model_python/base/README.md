# Base
This folder contains a minimum definition of the elements in the SAMM. The folder does not include any implementations. 
It can be seen as a contract that establishes a fixed structure and inheritance hierarchy.
The classes should not be instantiated because they are abstract which is similar to interfaces in Java.

# Inheritance hierarchy
```
HasUrn
├───────────────────────────────────────────────── DataType
└── IsDescribed                                    ├── Scalar
    └── Base                    HasProperties      │
        ├── StructureElement <──┘                  │
        │   ├── Aspect                             │
        │   └── ComplexType <──────────────────────┘
        │       ├── AbstractEntity
        │       └── Entity
        ├── Characteristic
        │   ├── Code
        │   ├── Collection
        │   │   ├── List
        │   │   ├── Set
        │   │   └── SortedSet
        │   │       └── TimeSeries
        │   ├── Either
        │   ├── Enumeration
        │   │   └── State
        │   ├── SingleEntity
        │   ├── StructuredValue
        │   ├── Quantifiable
        │   │   ├── Duration
        │   │   └── Measurement
        │   └── Trait
        ├── Constraint
        │   ├── EncodingConstraint
        │   ├── FixedPointConstraint
        │   ├── LanguageConstraint
        │   ├── LengthConstraint
        │   ├── LocaleConstraint
        │   ├── RangeConstraint
        │   └── RegularExpressionConstraint
        ├── Event
        ├── Operation
        ├── Property
        ├── QuantityKind
        └── Unit

BoundDefiniton
```