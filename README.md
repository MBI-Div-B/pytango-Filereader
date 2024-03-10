# PyTango Device Server to read data saved in files

## Use
For the property `separatorAndAttributeName` ether give only the separator. In this case the Attribute names are automatically generated. Or give every relevant Attribute its own name in the same shape and separator as in the file (e.g. Attr1;Attr2;;Attr3). If one value is not given a name it is skiped.
Use property `skipLines` if the relevant data does not start in the first line.

## Authors
Leon Wener
