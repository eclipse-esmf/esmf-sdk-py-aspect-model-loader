class MetaModelElements:
    # Meta Model Elements
    AbstractEntity = "AbstractEntity"
    AbstractProperty = "AbstractProperty"
    Aspect = "Aspect"
    Boolean = "Boolean"
    Characteristic = "Characteristic"
    Code = "Code"
    Collection = "Collection"
    Constraint = "Constraint"
    Duration = "Duration"
    Either = "Either"
    EncodingConstraint = "EncodingConstraint"
    Entity = "Entity"
    Enumeration = "Enumeration"
    Event = "Event"
    FileResource = "FileResource"
    FixedPointConstraint = "FixedPointConstraint"
    Language = "Language"
    LanguageConstraint = "LanguageConstraint"
    LengthConstraint = "LengthConstraint"
    List = "List"
    Locale = "Locale"
    LocaleConstraint = "LocaleConstraint"
    Measurement = "Measurement"
    MimeType = "MimeType"
    MultiLanguageText = "MultiLanguageText"
    Operation = "Operation"
    Point3d = "Point3d"
    Property = "Property"
    Quantifiable = "Quantifiable"
    QuantityKind = "QuantityKind"
    RangeConstraint = "RangeConstraint"
    RegularExpressionConstraint = "RegularExpressionConstraint"
    ResourcePath = "ResourcePath"
    Set = "Set"
    SingleEntity = "SingleEntity"
    SortedSet = "SortedSet"
    State = "State"
    StructuredValue = "StructuredValue"
    Text = "Text"
    TimeSeries = "TimeSeries"
    TimeSeriesEntity = "TimeSeriesEntity"
    Timestamp = "Timestamp"
    Trait = "Trait"
    Unit = "Unit"
    UnitReference = "UnitReference"

    meta_model_elements = (
        AbstractEntity,
        Aspect,
        Characteristic,
        Constraint,
        Entity,
        Event,
        Operation,
        Property,
        Quantifiable,
        QuantityKind,
        Trait,
        Unit,
    )


class CharacteristicElements:
    # Characteristic Elements
    Code = "Code"
    Collection = "Collection"
    Duration = "Duration"
    Either = "Either"
    Encoding_constraint = "EncodingConstraint"
    Enumeration = "Enumeration"
    Fixed_point_constraint = "FixedPointConstraint"
    Language_constraint = "LanguageConstraint"
    Length_constraint = "LengthConstraint"
    Locale_constraint = "LocaleConstraint"
    Measurement = "Measurement"
    Quantifiable = "Quantifiable"
    Range_constraint = "RangeConstraint"
    Regular_expression_constraint = "RegularExpressionConstraint"
    List = "List"
    Set = "Set"
    Single_entity = "SingleEntity"
    Sorted_set = "SortedSet"
    State = "State"
    Structured_value = "StructuredValue"
    Time_series = "TimeSeries"
    Trait = "Trait"

    collections = (
        Collection,
        List,
        Set,
        Sorted_set,
        Time_series,
    )


class SAMMEElements:
    FileResource = "FileResource"
    Point3d = "Point3d"
    TimeSeriesEntity = "TimeSeriesEntity"


class MetaModelElementAttributes:
    # Attributes of Meta Model Elements
    allow_duplicates = "allowDuplicates"
    AT_LEAST = "AT_LEAST"
    AT_MOST = "AT_MOST"
    base_characteristic = "baseCharacteristic"
    characteristic = "characteristic"
    common_code = "commonCode"
    constraint = "constraint"
    conversion_factor = "conversionFactor"
    curie = "curie"
    data_type = "dataType"
    deconstruction_rule = "deconstructionRule"
    default_value = "defaultValue"
    description = "description"
    element_characteristic = "elementCharacteristic"
    elements = "elements"
    events = "events"
    example_value = "exampleValue"
    extends = "extends"
    GREATER_THAN = "GREATER_THAN"
    input = "input"
    integer = "integer"
    language_code = "languageCode"
    left = "left"
    LESS_THAN = "LESS_THAN"
    list_type = "listType"
    locale_code = "localeCode"
    lower_bound_definition = "lowerBoundDefinition"
    max_value = "maxValue"
    mime_type = "mimeType"
    min_value = "minValue"
    name = "name"
    not_in_payload = "notInPayload"
    numeric_conversion_factor = "numericConversionFactor"
    operations = "operations"
    optional = "optional"
    ordered = "ordered"
    output = "output"
    parameters = "parameters"
    payload_name = "payloadName"
    preferred_name = "preferredName"
    properties = "properties"
    quantity_kind = "quantityKind"
    reference_unit = "referenceUnit"
    resource = "resource"
    right = "right"
    property = "property"
    scale = "scale"
    see = "see"
    symbol = "symbol"
    timestamp = "timestamp"
    unit = "unit"
    upper_bound_definition = "upperBoundDefinition"
    value = "value"
    values = "values"
    x = "x"
    y = "y"
    z = "z"
    TimeSeriesEntity = "TimeSeriesEntity"
    Point3d = "Point3d"


class CharacteristicElementAttributes:
    # Attributes of Characteristic Elements
    allow_duplicates = "allowDuplicates"
    AT_LEAST = "AT_LEAST"
    AT_MOST = "AT_MOST"
    base_characteristic = "baseCharacteristic"
    constraint = "constraint"
    deconstruction_rule = "deconstructionRule"
    default_value = "defaultValue"
    element_characteristic = "elementCharacteristic"
    elements = "elements"
    GREATER_THAN = "GREATER_THAN"
    integer = "integer"
    language_code = "languageCode"
    left = "left"
    LESS_THAN = "LESS_THAN"
    locale_code = "localeCode"
    lower_bound_definition = "lowerBoundDefinition"
    max_value = "maxValue"
    min_value = "minValue"
    ordered = "ordered"
    right = "right"
    scale = "scale"
    unit = "unit"
    upper_bound_definition = "upperBoundDefinition"
    values = "values"


class SAMMEElementAttributes:
    timestamp = "timestamp"
    value = "value"
    x = "x"
    y = "y"
    z = "z"
