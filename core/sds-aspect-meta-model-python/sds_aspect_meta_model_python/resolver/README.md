# Connection between an aspect model and the BAMM aspect meta model

The aspect model in a turtle file defines model elements (e.g., myAspect, myProperty, myCharacteristic). 
See the example below.

Those defined elements depend on the meta model elements (e.g., bamm:Aspect, bamm:Property, bamm:Characteristic). 
The meta model elements are defined in the `bamm-aspect-meta-model` folder which contains some global turtle files. 

```
:myAspect a bamm:Aspect ;
    bamm:properties (myProperty) ;

:myProperty a bamm:Property ;
    bamm:charactersitic myCharacteristic .

...
```

# Resolver

When the `AspectLoader` loads an aspect model from a `turtle.ttl`, it generates an rdf graph.
This graph only contains the nodes defined in the `turtle.ttl` and not the nodes from the BAMM turtles.

The task of the `Resolver` is to load the nodes from the BAMM turtles into the rdf graph. 
Afterwards the `AspectLoader` can load the aspect model. 
