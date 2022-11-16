import csv;
 
def get_List_From_CSV_File(filePath):
  finalList = [];
 
  try:
    with open(filePath, mode='r') as csv_file:     
      csv_reader = csv.DictReader(csv_file)
      line_count = 0;
        
      for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            print("Column names have to be Number, Latitiude, and Longitude");
            line_count += 1
 
        val1 = row["Number"];
        val2 = row["Latitude"];
        val3 = row["Longitude"];
 
        finalList.append([float(val1), float(val2), float(val3)]);
        line_count += 1   
  except:
    print("Error: File Name [", filePath,  "] Does Not Exist! Returning Empty List...");
    
  return finalList;
 

from math import sin, cos, sqrt, atan2, radians
 
def getDistance(lat1, lon1, lat2, lon2):
  R = 6373.0
 
  lat1 = radians(lat1)
  lon1 = radians(lon1)
  
  lat2 = radians(lat2)
  lon2 = radians(lon2)
 
  dlon = lon2 - lon1
  dlat = lat2 - lat1
 
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
 
  distance = R * c
 
  #print("Result:", distance)
  #print("Should be:", 278.546, "km")  
  return distance;

import numpy as np;
 
def get_All_Distances_Matrix(predictedCoordinatesList, actualCoordinatesList):
  actualCoordinatepredictedCoordinateDistances = [];
 
  for i in range(len(actualCoordinatesList)):
    distances = [];
 
    for j in range(len(predictedCoordinatesList)):
         distances.append(getDistance(actualCoordinatesList[i][1], actualCoordinatesList[i][2], predictedCoordinatesList[j][1], predictedCoordinatesList[j][2]));
 
    distances = np.array(distances);    
    distances = np.reshape(distances, (1, len(predictedCoordinatesList))) 
    #print(distances);
 
    if i == 0:
      actualCoordinatepredictedCoordinateDistances = distances;  
    else:
      actualCoordinatepredictedCoordinateDistances = np.concatenate((actualCoordinatepredictedCoordinateDistances, distances), axis = 0);   
 
    #print(actualCoordinatepredictedCoordinateDistances);  
  
  return actualCoordinatepredictedCoordinateDistances;

def getMinValues(array):
  #print(array);
  minNum = 10000.0;
  minIndex = -1;
 
  for i in range(len(array)):
    if array[i] < minNum:
      minNum = array[i];
      minIndex = i;
 
  return [minIndex, minNum];


def get_actualCoordinate_to_predictedCoordinate(allactualCoordinatepredictedCoordinateDistancesMatrix, allpredictedCoordinateIndexes, allactualCoordinateIndexes):
  actualCoordinate_to_predictedCoordinate = [];
  allactualCoordinatepredictedCoordinateDistances = allactualCoordinatepredictedCoordinateDistancesMatrix
  predictedCoordinateIndex = 0;
 
  while allactualCoordinatepredictedCoordinateDistances.size > 0:
    valuesFrompredictedCoordinate = getMinValues(allactualCoordinatepredictedCoordinateDistances[:,predictedCoordinateIndex]); 
    possibleCorrectactualCoordinateIndex = valuesFrompredictedCoordinate[0];
 
    valuesFromPossibleCorrectactualCoordinate = getMinValues(allactualCoordinatepredictedCoordinateDistances[possibleCorrectactualCoordinateIndex,:])
    possibleCorrectpredictedCoordinateIndex = valuesFromPossibleCorrectactualCoordinate[0];
 
    if predictedCoordinateIndex == possibleCorrectpredictedCoordinateIndex:
      actualCoordinate_to_predictedCoordinate.append([allactualCoordinateIndexes[possibleCorrectactualCoordinateIndex], allpredictedCoordinateIndexes[possibleCorrectpredictedCoordinateIndex], valuesFrompredictedCoordinate[1]]);
      
      allpredictedCoordinateIndexes.remove(allpredictedCoordinateIndexes[possibleCorrectpredictedCoordinateIndex]);  
      allactualCoordinateIndexes.remove(allactualCoordinateIndexes[possibleCorrectactualCoordinateIndex]); 
 
      matrixPT1 = allactualCoordinatepredictedCoordinateDistances[:possibleCorrectactualCoordinateIndex, 1:];
      matrixPT2 = allactualCoordinatepredictedCoordinateDistances[possibleCorrectactualCoordinateIndex + 1:, 1:];
      allactualCoordinatepredictedCoordinateDistances = np.concatenate((matrixPT1, matrixPT2), axis = 0);  
 
      predictedCoordinateIndex = 0;
    else:
      predictedCoordinateIndex += 1;
 
  return actualCoordinate_to_predictedCoordinate;
    
#Test Values
allpredictedCoordinates = [[1, 26.484255, -80.2041128], 
             [2, 26.489498, -80.20400333], 
             [3, 26.485688, -80.20402956],
             [4, 26.48753, -80.20393433],             
             [5, 26.48782, -80.20398737],
             [6, 26.488367, -80.20394692],
             [7, 26.488645, -80.20401837],
             [8, 26.484297, -80.20371203],            
             [9, 26.484101, -80.20306223],
             [10, 26.484107, -80.20268311],
             [11, 26.572364, -80.15171854],
             [12, 26.57268, -80.1506852]];
 
allactualCoordinates = [[1, 26.484046, -80.202711],
            [2, 26.484048, -80.203066],
            [3, 26.484292, -80.203671],
            [4, 26.488721, -80.204054],
            [5, 26.488394, -80.204049],
            [6, 26.487782, -80.204078],
            [7, 26.487323, -80.203809],
            [8, 26.48574, -80.204072],
            [9, 26.489398, -80.204053],
            [10, 26.484134, -80.203798],
            [11, 26.57268, -80.1506852]
            ];
 
 
 
 
#----------------------------Get List From CSV File----------------------------
print("--Start-- \n");
allpredictedCoordinates = get_List_From_CSV_File('predictedCoordinates.csv');
allactualCoordinates = get_List_From_CSV_File('actualCoordinates.csv');
 
#print(allpredictedCoordinates);
#print(allactualCoordinates);
 
#----------------------------Get All Predicted Coordinate Numbers and Actual Coordinate Numbers----------------------------
allpredictedCoordinateNumbers = [];
for i in range(len(allpredictedCoordinates)):
  allpredictedCoordinateNumbers.append(allpredictedCoordinates[i][0]);
 
allpredictedCoordinateIndexes = [];
for i in range(len(allpredictedCoordinates)):
  allpredictedCoordinateIndexes.append(i);
 
allactualCoordinateIndexes = [];
for i in range(len(allactualCoordinates)):
  allactualCoordinateIndexes.append(i);
 
allactualCoordinateNumbers = [];
for i in range(len(allactualCoordinates)):
  allactualCoordinateNumbers.append(allactualCoordinates[i][0]);
print("--Got Data From .csv File-- \n");
 
#----------------------------Get All Distances from Each Actual Coordinate to Each Predicted Coordinate----------------------------
allactualCoordinatepredictedCoordinateDistancesMatrix = get_All_Distances_Matrix(allpredictedCoordinates, allactualCoordinates);
#print(allactualCoordinatepredictedCoordinateDistancesMatrix);
#print(allactualCoordinatepredictedCoordinateDistancesMatrix.shape)
 
print("--Got All Distances-- \n");
 
#----------------------------Find Minimum Distances From Actual Coordinate to A Predicted Coordinate----------------------------
actualCoordinate_to_predictedCoordinate = get_actualCoordinate_to_predictedCoordinate(allactualCoordinatepredictedCoordinateDistancesMatrix, allpredictedCoordinateIndexes, allactualCoordinateIndexes);
#actualCoordinate_to_predictedCoordinate = get_actualCoordinate_to_predictedCoordinate(allactualCoordinatepredictedCoordinateDistancesMatrix, allactualCoordinateIndexes);
#print(actualCoordinate_to_predictedCoordinate);
 
print("--Matched actualCoordinates to predictedCoordinates-- \n");
 
#----------------------------Write .CSV File----------------------------
file = open('actualCoordinatetopredictedCoordinate.csv', 'w')
writer = csv.writer(file)
 
writer.writerow(["actualCoordinate", "predictedCoordinate", "Distance"]);
                 
for i in range(len(actualCoordinate_to_predictedCoordinate)):
  print("Actual Coordinate", allactualCoordinateNumbers[actualCoordinate_to_predictedCoordinate[i][0]], "to Predicted Coordinate", allpredictedCoordinateNumbers[actualCoordinate_to_predictedCoordinate[i][1]], "with a Distance of", actualCoordinate_to_predictedCoordinate[i][2], "meters");
  writer.writerow(([allactualCoordinateNumbers[actualCoordinate_to_predictedCoordinate[i][0]], allpredictedCoordinateNumbers[actualCoordinate_to_predictedCoordinate[i][1]], actualCoordinate_to_predictedCoordinate[i][2]]));
print("\n");
 
file.close()
 
print("--Wrote .csv File-- \n");
 
print("--End-- \n");
