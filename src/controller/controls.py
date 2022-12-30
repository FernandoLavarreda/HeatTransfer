#Aid for GUI for Transient Heat transfer Interactions
#Fernando Lavarreda

from os import startfile
from typing import List, Union, Any
from collections.abc import Mapping


def symmetry(xs:List[float], factor:float=-1):
    """Do a reflection of x values and y values to obtain full temperature profile"""
    xo = []
    for i in range(len(xs), 0, -1):
        xo.append(xs[i-1]*factor)
    return xo


def msymmetry(xs:List[List[float]], factor:float=-1):
    """Symmetry for multiple listss"""
    symmetrics = []
    for x in xs:
        symmetrics.append(symmetry(x, factor=factor))
    return symmetrics


def make_report(features:dict, lambdas:List[float], coordinates:List[float], temperatures:Union[List[float], List[List[float]]], time_labels:Union[List[float], float]):
    """Create html report for users
        features: mapping from variable (str) to its value"""
    file = "<html><head><title>Report</title>"
    style = """
            <style>
                table.center1 {
                    width: 30%;
                    }
                table.center2 {
                    width: 80%;
                    }
                
                tr.see:hover {
                        background-color: coral;
                }
                
                table {
                      font-family: arial, sans-serif;
                      border-collapse: collapse;
                      margin-left: auto;
                      margin-right: auto;
                      width: 100%;
                    }

                    td{
                      border: 1px solid #dddddd;
                      text-align: left;
                      padding: 8px;
                    }
                    
                    th{
                      border: 1px solid #dddddd;
                      text-align: center;
                      padding: 8px;
                    }
                    
                    th.see {
                        background-color: #000000;
                        color: white;
                    }
                    
                    th.see2 {
                        background-color: #04AA6D;
                        color: white;
                    }
                    
                    th.see3 {
                        background-color: #2648f0;
                        color: white;
                    }

                    tr:nth-child(even) {
                      background-color: #dddddd;
                    }
                    
                    tr:nth-child(odd) {
                      background-color: #edf2f4;
                    }
                    h2{
                        padding-left: 2em;
                    }
                    h3{
                        padding-left: 2em;
                    }
                    * {
                          box-sizing: border-box;
                        }

                        .row {
                          display: flex;
                        }

                        .column {
                          flex: 50%;
                          padding: 5px;
                        }
            </style>
            </head>
            <body style="background-color:#98c1d9;">
            <h1 style="color:#293241;">Report Summary:</h1><hr>
            """
    file+=style
    file+="<div class=row>"
    file+="<div class=column>"
    file+="<h2>Problem variables</h2>"
    file+=make_table(features, class_="center1", header="<tr><th class=see2>Variable</th><th class=see2>Value</th></tr>")
    file+="</div>"
    file+="<div class=column>"
    file+="<h2>Lambdas</h2>"
    file+=make_table({i+1:lambdas[i] for i in range(len(lambdas))}, class_="center1", header="<tr><th class=see3>Lambda</th><th class=see3>Value</th></tr>")
    file+="</div>"
    file+="</div>"
    
    if type(temperatures[0]) != list:
        file+="<br><h2>Temperature Profile</h2><hr>"
        file+=make_table({coordinates[i]:temperatures[i] for i in range(len(coordinates))}, class_="center1", header=f"<tr><th class=see>Coordinate</th><th class=see>Temperature at Time:{time_labels}</th></tr>")
    else:
        file+="<br><h2>Temperature Profiles</h2><hr>"
        file+="<div style=\"overflow-x:auto;\">"
        coord_temp_mapping = [[temperature[coordinate] for temperature in temperatures] for coordinate in range(len(coordinates))]
        
        labels = ''.join([f"<th class=see>{time_label}</th>" for time_label in time_labels])
        file+=make_table2({coordinates[i]:coord_temp_mapping[i] for i in range(len(coordinates))}, class_="center2", header="<tr><th class=see>Coordinate|Timestamps</th>"+labels+"</tr>")
        
        file+="</div>"
    file+="</body></html>"
    return file


def make_table(features:dict, class_="", header=""):
    """Create table key:value for a set of features"""
    table = f"<table class='{class_}'>{header}"
    for key, value in features.items():
        table+="<tr>"
        table+=f"<td>{key}</td>"
        table+=f"<td>{value}</td>"
        table+="</tr>"
    table+="</table>"
    return table


def make_table2(features:Mapping[Any, List[Any]], class_="", header=""):
    """Create table with multiple columns corresponding to a key"""
    table = f"<table class='{class_}'>{header}"
    for key, value in features.items():
        table+="<tr class=see>"
        table+=f"<td>{key}</td>"
        for value_ in value:
            table+=f"<td>{value_}</td>"
        table+="</tr>"
    table+="</table>"
    return table


if __name__ == "__main__":
    general = {i:f"value --> {i}" for i in range(7)}
    lambdas = [i/6+5 for i in range(11)]
    coordinates = [i for i in range(100)]
    temperatures = [i+20 for i in range(100)]
    #temperatures = [[i+20 for i in range(66)] for x in range(100)]
    with open("cmd.html", "w") as fd:
        fd.write(make_report(general, lambdas, coordinates, temperatures))
    #print(make_table({i:f"value --> {i}" for i in range(10)}))

