import RFEM
import RFEM.DynamicLoads
import RFEM.LoadCasesAndCombinations
import RFEM.Loads
import RFEM.Loads.lineLoad
import RFEM.Loads.memberLoad
import RFEM.Loads.nodalLoad
import RFEM.dependencies
import RFEM.initModel

def getLoads():
    loads = []
    print(loads)

if __name__ == "__main__":

    model = RFEM.initModel.Model("C:\\Users\\User\\Desktop\\Kragarm.rf6")
    getLoads()

