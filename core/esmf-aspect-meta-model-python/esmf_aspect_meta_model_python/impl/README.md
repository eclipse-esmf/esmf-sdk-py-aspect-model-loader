# Default Implementation
This folder implements the meta model elements of the SAMM. 
The classes in here are derived from the base folder.

# Aspect hierarchy

Every Model Class in Default Implementation of the SAMM Aspect Meta Model 
is derived from the DefaultBase class. 
It consists of the following attributes:
```
BASE ATTRIBUTES
├── meta_model_version
├── urn
├── name
├── preferred_names
├── descriptions
└── see
```
An aspect has the following hierarchy:
```
Schmematic object structure of an aspect

aspect
├── BASE ATTRIBUTES
├── is_collection_aspect
├── properties
│   ├──[0]
│   │   ├── BASE ATTRIBUTES
│   │   ├── characteristic
│   │   │   ├── BASE ATTRIBUTES
│   │   │   ├── data_type
│   │   │   └── ...
│   │   ├── example_value
│   │   ├── optional
│   │   └── not_in_payload
│   ├──[1]
│   │   └── ...
│   └── ...
├── operations
│   ├──[0]   
│   │   ├── BASE ATTRIBUTES
│   │   ├── input_properties
│   │   │   └── ...
│   │   └── output_properties
│   │       └── ...
│   ├──[1]
│   │   └── ...
│   └── ...
└── events
    ├──[0]   
    │   ├── BASE ATTRIBUTES
    ├──[1]
    │   └── ...
    └── ...
```

# Property
An instance of type `Property` has exactly one characteristic and additionally
the attributes `example_value`, `optional`, `not_in_payload` and a list
of `refines`.

# Operation
An instance of type `Operation` has multiple input properties and multiple output
properties.

# Characteristic
An instance of type `Characteristic` has an optional `data_type`. 
There are many subclasses of `Characteristic` that implement a special kind of
characteristic.

## Collection
`Collection` is a subclass of `Characteristic`. At the same time it is the base class for
other collection elements like `List` and `SortedSet`.

A collection has a 

## Trait
An instance of `Trait` wraps one instance of `Characteristic` 
and one or more instances of `Constraint` together. 
The wrapped characteristic is
called `base_characteristic`.

The idea of the `Trait` is to force a certain behaviour of the characteristic
with the given constraints.

Note that the class `Trait` is a subclass of `Characteristic` to avoid confusion.

The hierarchy of the `Trait` looks like this:
```
Schematic object Structure of a Trait

Trait
├── BASE ATTRIBUTES
├── constraints
│   ├──[0]
│   │   ├── BASE ATTRIBUTES
│   │   └── ...
│   ├──[1]
│   │   └── ...
│   └── ...
└── base_characteristic
```
### Example
If the characteristic is a `Scalar`
that should only have values between 1 and 10 then the
hierarchy of the `Trait` could look like this:
```
Example structure of a Trait

Trait
├── BASE ATTRIBUTES
├── constraints
│   └──[0]: RangeConstraint
│       ├── BASE ATTRIBUTES
│       ├── min_value = 1
│       └── max_value = 10
└── base_characteristic: Characteristic
    └── data_type: Scalar
        └── urn = xsd:Integer
```

# DataType
A DataType represents some value. It can be represened by a simple `Scalar` or by
a `ComplexType`. Complex types can either be of type `Entity` or `AbstractEntity`.

`Entities` and `AbstractEntities` have a number of properties and can extend other entities.

# Constraint
A Constraint is a limitation for a characteristic. Examples for Constraints are
`RangeConstraint` and `RegularExpressionConstraint`.
To make a `Constraint` work, it must be wrapped with another Characteristic inside a Trait.
For detailed information see the section `Trait` above.
