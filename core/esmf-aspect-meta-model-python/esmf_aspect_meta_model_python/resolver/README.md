# Connection between an aspect model and the SAMM aspect meta model

The aspect model in a turtle file defines model elements (e.g., myAspect, myProperty, myCharacteristic). 
See the example below.

Those defined elements depend on the meta model elements (e.g., samm:Aspect, samm:Property, samm:Characteristic). 
The meta model elements are defined in the `samm-aspect-meta-model` folder which contains some global turtle files. 

```
:myAspect a samm:Aspect ;
    samm:properties (myProperty) ;

:myProperty a samm:Property ;
    samm:charactersitic myCharacteristic .

...
```

# Resolvers

When the `AspectLoader` loads an aspect model from a `turtle.ttl`, it generates an RDF graph.
This graph only contains the nodes defined in the `turtle.ttl` and not the nodes neither from the SAMM turtles 
nor model namespace links.

Afterwords, the `AspectLoader` can load the aspect model.

The task of the `Resolver(s)` is to:
- load the nodes from the SAMM turtles into the rdf graph;
- resolve namespace references.

## Resolver classes

There are the next resolver classes:
- Aspect resolver([AspectModelResolver](base.py));
- Meta model resolver ([AspectMetaModelResolver](meta_model.py));
- Model namespace resolver ([AspectNamespaceResolver](namespace.py)).

### Meta model resolver 

Meta model resolver is an interface for the classes to load a SAMM definition files to the Aspect model graph.

| *Class name*            | *Interface*           | Note            |
|-------------------------|-----------------------|-----------------|
| BaseMetaModelResolver   |                       | Interface class |
| AspectMetaModelResolver | BaseMetaModelResolver |                 |

### Namespace resolver 

This resolver is implemented a logic for loading model spreaded across several files (in one namespace) and namespaces.

| *Class name*            | *Interface*           | Note            |
|-------------------------|-----------------------|-----------------|
| BaseNamespaceResolver   |                       | Interface class |
| AspectNamespaceResolver | BaseNamespaceResolver |                 |

### Aspect model resolver

This class is a container for the meta model and namespace resolvers logic.

| *Class name*        | *Interface*   | Note            |
|---------------------|---------------|-----------------|
| BaseResolver        |               | Interface class |
| AspectModelResolver | BaseResolver  |                 |
