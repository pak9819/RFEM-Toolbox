from DataProcessor import RFEMDataHandler
from scipy.io import savemat


if __name__ == "__main__":

    data = RFEMDataHandler("Stütze.rf6")
    node_matrix = data.nodes
    element_matrix = data.elements

    savemat(
        "src\\matlab\\rfem_data.mat", 
        {
            "node_matrix": node_matrix, 
            "element_matrix": element_matrix
        }
    )