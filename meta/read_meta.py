import h5py

    # To use it:
    #       mp = meta.read_meta.Hdf5MetadataReader(fname)
    #       meta_data = mp.readMetadata()
    #       mp.close()

class Hdf5MetadataReader:

    def __init__(self, filePath, excludedSections=['exchange', 'defaults'], readOnOpen=True):
        self.file = h5py.File(filePath, 'r')
        self.metadataDict = {}
        self.excludedSections = excludedSections
        if readOnOpen:
            self.readMetadata()

    def readMetadata(self):
        self.file.visititems(self.__readMetadata)
        return self.metadataDict

    def getMetadata(self):
        return self.metadataDict

    def __readMetadata(self, name, obj):
        if isinstance(obj, h5py.Dataset):
            rootName = name.split('/')[0]
            if rootName not in self.excludedSections:
                try:
                    # This is when the obj shape is (1,) (DESY, APS)
                    if obj[()].shape[0] == 1:
                        value = obj[()][0]
                        if isinstance(value, bytes):
                            value = value.decode("utf-8", errors='ignore')
                        elif  (value.dtype.kind == 'S'):
                            value = value.decode(encoding="utf-8")
                            # print("0>>>>>>>>>>>> %s: %s" % (obj.name, value))
                        attr = obj.attrs.get('units')
                        if attr != None:
                            attr = attr.decode('UTF-8')
                            # print("1>>>>>> %s: %s %s" % (obj.name, value, attr))
                        self.metadataDict.update( {obj.name : [value, attr] } )
                except AttributeError: # This is when the obj is byte so has no attribute 'shape'
                    value = obj[()] 
                    if isinstance(value, bytes):
                        value = value.decode("utf-8", errors='ignore')
                    attr = obj.attrs.get('units')
                    if attr != None:
                        attr = attr.decode('UTF-8')
                    self.metadataDict.update( {obj.name : [value, attr] } )
                    # print("2>>>>>> %s: %s %s" % (obj.name, value, attr))
                except IndexError: # This is when the obj shape is () (ESRF and DLS) instead of (1,) (DESY, APS)
                    attr = obj.attrs.get('units')
                    if attr != None:
                        if isinstance(attr, str): 
                            pass
                        else:
                            attr = attr.decode('UTF-8')
                    value = obj[()]
                    # print("3>>>>>> %s: %s %s" % (obj.name, value, attr))
                    self.metadataDict.update( {obj.name : [value, attr] } )
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None
