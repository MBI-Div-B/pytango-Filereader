from encodings import utf_8
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
        with open(self.directory + "\\" + self.fileName + self.fileType) as f:
            for i in range(int(self.skipLines)):
                line = f.readline()
            line = f.readline()
        if self.separator != "," and "," in line:
            line = line.replace(",",".")
        l = line.split(self.separator)
        return float(l[self.AttrDict[attr.get_name()]])
        
        
                

    fileType = device_property(
        dtype='DevString',
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
    ) # if only separator is given all values in one line are read an given the generic name AttributeX
    
    multipleLines = device_property(
        dtype = str,
        default_value = "False"
    )#not jet justed

    skipLines = device_property(
        dtype = str,
        default_value = 0
    )




    def init_device(self):
        Device.init_device(self)
        if len(self.separatorAndAttributeNames) == 1:
            self.separator = self.separatorAndAttributeNames
            with open(self.directory + "\\" + self.fileName + self.fileType) as f:
                for i in range(int(self.skipLines)):
                    line = f.readline()
                line = f.readline()
            l = line.split(self.separator)
            self.AttrDict = {}
            for i in range(len(l)):
                self.AttrDict["Attribute"+str(i)] = i
                self.create_float_attributes("Attribute"+str(i))
        else:
            self.separator = "".join(set(re.sub(r'\w+', '', self.separatorAndAttributeNames)))   #extracts the seperator
            if len(self.separator) != 1:
                self.set_state(DevState.FAULT)
                self.debug_stream("wrong separator this was detected "+ self.separator)
            self.AttrDict = dict([(x,i) for i,x in enumerate(self.separatorAndAttributeNames.split(self.separator)) if x != ""]) #extracts the attribute names
            for i in self.AttrDict:
                self.create_float_attributes(i)
        self.set_state(DevState.ON)

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
