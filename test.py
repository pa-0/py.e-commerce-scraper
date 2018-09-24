import pickle

with open('dump.pkl', 'rb') as f:

    obj = {}

    data = pickle.load(f)

    # remove uncessary html
    data = data.replace('\n', '')
    data = data.replace('\t', '')
    data = data.split('<br>')
    data = [i for i in data if i is not '']

    # cleaning garment measurement data
    garment_measurements_data = data[::]
    garment_measurements_data = [i.split(' ') for i in data]
    garment_measurements_data = garment_measurements_data[1:5]
    for data in garment_measurements_data:
        data[0] = data[0].replace('”', '')
        data[0] = data[0].replace('“', '')


    model_measurement_data = data[::]

    # adding to obj
    for data in garment_measurements_data:
        obj[data[1]] = data[0]

    obj['leg-opening'] = obj.pop('leg')
    
    # remove unecessary data
    data = data[1:]



    print("GARMENT DATA:", obj)