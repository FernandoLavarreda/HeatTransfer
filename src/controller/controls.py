#Aid for GUI for Transient Heat transfer Interactions
#Fernando Lavarreda

from typing import List
from os import startfile


def symmetry(xs:List[float], factor:float=-1):
    """Do a reflection of x values and y values to obtain full tempereture profile"""
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


def make_report(features:dict, lambdas:List[float]):
    """Create html report for users
        features: mapping from variable (str) to its value"""
    file = "<html></head><title>Report</title>"
    style = """
            <style>
                table.center1 {
                    width: 20%;
                    }
                table.center2 {
                    width: 80%;
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

                    tr:nth-child(even) {
                      background-color: #dddddd;
                    }
                    
                    tr:nth-child(odd) {
                      background-color: #edf2f4;
                    }
                    h2{
                        padding-left: 12em;
                    }
                    
            </style>
            </head>
            <body style="background-color:#98c1d9;">
            <h1 style="color:#293241;">Report Summary:</h1><hr>
            <br>
            <h2>Problem variables:</h2><br>
            """
    file+=style
    file+=make_table(features, class_="center1", header="<tr><th>Variable</th><th>Value</th></tr>")
    file+="<br><h2>Lambdas:</h2><br>"
    file+=make_table({i+1:lambdas[i] for i in range(len(lambdas))}, class_="center1")
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


if __name__ == "__main__":
    print(make_report({i:f"value --> {i}" for i in range(10)}, [i/6+5 for i in range(25)]))
    #print(make_table({i:f"value --> {i}" for i in range(10)}))

