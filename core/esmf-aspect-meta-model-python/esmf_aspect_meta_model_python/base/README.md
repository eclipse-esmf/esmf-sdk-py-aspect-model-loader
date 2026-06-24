# Base
This folder contains a minimum definition of the elements in the SAMM. The folder does not include any implementations. 
It can be seen as a contract that establishes a fixed structure and inheritance hierarchy.
The classes should not be instantiated because they are abstract which is similar to interfaces in Java.

# Inheritance hierarchy

The diagram below shows the inheritance hierarchy of the base (interface) classes. `HasUrn`,
`IsDescribed` and `HasProperties` are abstract base classes; `StructureElement` and `ComplexType`
use multiple inheritance.

```mermaid
classDiagram
    HasUrn <|-- IsDescribed
    HasUrn <|-- DataType
    IsDescribed <|-- Base

    Base <|-- StructureElement
    HasProperties <|-- StructureElement
    StructureElement <|-- Aspect
    StructureElement <|-- ComplexType
    DataType <|-- ComplexType
    DataType <|-- Scalar
    ComplexType <|-- AbstractEntity
    ComplexType <|-- Entity

    Base <|-- Characteristic
    Characteristic <|-- Code
    Characteristic <|-- Collection
    Collection <|-- List
    Collection <|-- Set
    Collection <|-- SortedSet
    SortedSet <|-- TimeSeries
    Characteristic <|-- Enumeration
    Enumeration <|-- State
    Characteristic <|-- SingleEntity
    Characteristic <|-- StructuredValue
    Characteristic <|-- Quantifiable
    Quantifiable <|-- Duration
    Quantifiable <|-- Measurement
    Characteristic <|-- Trait

    Base <|-- Either
    Base <|-- Constraint
    Constraint <|-- EncodingConstraint
    Constraint <|-- FixedPointConstraint
    Constraint <|-- LanguageConstraint
    Constraint <|-- LengthConstraint
    Constraint <|-- LocaleConstraint
    Constraint <|-- RangeConstraint
    Constraint <|-- RegularExpressionConstraint

    Base <|-- Namespace
    Base <|-- Event
    Base <|-- Operation
    Base <|-- AbstractProperty
    AbstractProperty <|-- Property
    Base <|-- QuantityKind
    Base <|-- Unit
    QuantityKind <|-- Unit
    Base <|-- Value

    class HasUrn { <<abstract>> }
    class IsDescribed { <<abstract>> }
    class HasProperties { <<abstract>> }
```

> Note: `BoundDefinition` is a standalone `enum.Enum` (the upper/lower boundary rule for a
> `RangeConstraint`) and is therefore not part of the class hierarchy above.
