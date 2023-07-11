import json

def getVectors(distance, combustion, electric):
  # print('combustion: ', combustion)
  # print('electric: ', electric)
  with open('data_files/intersection.json', "r") as file:
    data = json.load(file)
  diferencia = [e1 - e2 for e1, e2 in zip(combustion, electric)] # make the subtraction between the lists combustion and electric
  # print('diferencia: ', diferencia)
  j = 0
  for x in diferencia:
    if x < 0:
      j+=1
    else:
      break
  # print('j: ', j)
  if j < 10:
    data[str(distance)] = {
        'combustion': [j-1, combustion[j-1], j, combustion[j]],
        'electric': [j-1, electric[j-1], j, electric[j]],
    }
  else:
    data[str(distance)] = {
        'combustion': 'NO possible solution',
        'electric': 'NO possible solution',
    }
  with open('data_files/intersection.json', 'w') as outfile:
    json.dump(data, outfile)