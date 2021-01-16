from io import StringIO
import csv
import json


# Objects included in this file:
# None

# Functions included in this file:
# # csv_to_json

def csv_to_json(csv_file):
    """
    Input:
    [header1, header2, ...]
    [data1, data2, ...]
    
    Output:    
    '[{"header1": "data1",
       "header2": "data2", 
       ...}
      ...]'

    Parses QD objects from LIMS
    """
    f = StringIO(csv_file)
    reader = csv.DictReader(f, delimiter=',')
    data = []
    
    for row in reader:
        data.append(dict(row))
        
    return json.dumps(data)
