from encodings import utf_8
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState,Attr, WAttribute
from tango import AttrWriteType, PipeWriteType
import re



class Filereader(Device):
    def read_float(self, attr):
        with open(directory+"\\"+fileName+fileType) as f:
            line = f.readline()
        l = line.split(self.separator)
        return l[self.AttrList[attr]]
        
        
                

    fileType = device_property(
        dtype='DevString',
	    mandatory = True,
        default_value=".txt"
    )

    fileName = device_property(
        dtype='DevString',
        mandatory = True
    )

    directory = device_property(
        dtype='DevString',
        mandatory = True
    )

    separatorAndAttributeNames = device_property(
        dtype='DevString',
        default_value = ";Example1;;Example2"
    ) 
    
    multipleLines = device_property(
        dtype = str,
        default_value = "False"
    )



    def init_device(self):
        Device.init_device(self)
        self.separator = "".join(set(re.sub(r'\w+', '', separatorAndAttributeNames)))   #extracts the seperator
        if len() != 1:
            self.set_state(DevState.FAULT)
            self.debug_stream("wrong separator this was detected "+ self.separator)
        self.AttrList = [(x,i) for i,x in enumerate(separatorAndAttributeNames.split(self.separator)) if x != ""] #extracts the attribute names
        for i in self.AttrList:
            self.create_float_attributes(i[1])

    @command(
        dtype_in='DevString',
        doc_in="dev_name",
        display_level=DispLevel.EXPERT,
    )
    @DebugIt()
    def create_float_attributes(self, argin):
        attr = attribute(
            name=argin,
            dtype=float,
            access=AttrWriteType.READ,
            label=argin,
        ).to_attr()
        self.add_attribute(attr,r_meth=self.read_float)
    
    @command(
        dtype_in='DevString',
        doc_in="dev_name",
        display_level=DispLevel.EXPERT,
    )
    @DebugIt()
    def create_array_attributes(self, argin):
        attr = attribute(
            name=argin,
            dtype=(float,),
            access=AttrWriteType.READ,
            label=argin,
        ).to_attr()
        self.add_attribute(attr,r_meth=self.read_array)
        
        
def main(args=None, **kwargs):
    return run((Filereader,), args=args, **kwargs)



if __name__ == '__main__':
    main()
