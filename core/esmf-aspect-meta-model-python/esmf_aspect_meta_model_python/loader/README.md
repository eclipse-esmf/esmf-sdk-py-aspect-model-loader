# Loader
The modules in this folder are responsible for the instantiation 
of an aspects by a turtle file.

The instantiator folder contains a number of instantiators that handle the instantiation of model elements.
Each instantiator is responsible for exactly one type of model element.
Additionally, there are the classes `AspectLoader`, `Instantiator`, `ModelElementFactory` and `MetaModelBaseAttributes`.

# MetaModelBaseAttributes
A wrapper class that holds all attributes of the class `DefaultBase`. It is used as
an input parameter for the `__init__`-method of `DefaultBase` and all its derived classes.
```
BaseAttributes
├── meta_model_version
├── urn
├── name
├── preferred_names
├── descriptions
├── see
```

An instance of `MetaModelBaseAttributes` is created with the static method `MetaModelBaseAttributes.from_meta_model_element(element_node)` 
which extracts the attributes from a given node of the aspect graph.

# AspectLoader
The AspectLoader is the entry point for the instantiation.
To instantiate a turtle call the static method `AspectLoader.load_aspect_model(file_path)` 
where `file_path` is the path to the .ttl-file.

The AspectLoader creates an instance of the ModelElementFactory which
then creates an aspect instance with all of its children.

# Abstract _Instantiator[T]_

The abstract class `Instantiator` acts as a base class for all instantiators. It has a generic
variable `T` which is replaced with an element type by inheriting instantiators.
The class `Instantiator` implements the method `get_instance(element_node)` which returns an instance of type `T`.

An instantiator stores all instantiated objects of type `T` in a dictionary. If the `get_instance(element_node)` 
is called it is checked whether the element has already been created or not. Then it either returns the 
existing instance from the dictionary, or it calls the method `_create_element(element_node)`.

# ModelElementFactory
The ModelElementFactory is a class which handles the instantiation of elements like 
aspects, properties and characteristics. 

The method `create_element(element_node)` returns an instance of the element represented by the node.
The method extracts the type of the node (aspect, characteristic, collection, etc.) from the aspect graph
and calls the responsible instantiator to get an instance.

There is a huge number of instantiators and not all of them are needed for all aspects. 
To save resources, the `ModelElementFactory` implements a lazy loading and creates the instantiators only when they are needed.

Example: The method `ModelElementFactory.create_element(element_node)` gets called, and the element_node represents an `Enumeration`.
The `ModelElementFactory` checks whether an instantiator for `Enumeration` exists and calls it if one exists.
If no fitting instantiator exists, the factory creates a new one. Therefore, it includes the module
with the name `instantiator/enumeration_instantiator` and creates an instance of the class `EnumerationInstantiator`.
The instantiator is then stored in the dictionary and the method `get_instance(element_node)` is called. 
