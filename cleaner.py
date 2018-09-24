import pickle

class Cleaner:
    def __init__(self, data):
        self.data = data
        self.obj = {}

    def _clean_html(self):
        # remove uncessary html
        self.data = self.data.replace('\n', '')
        self.data = self.data.replace('\t', '')
        self.data = self.data.split('<br>')
        self.data = [i for i in self.data if i is not '']

    def _extract_garment_measurements(self):
        # cleaning garment measurement data
        garment_measurements_data = self.data[::]
        garment_measurements_data = [i.split(' ') for i in garment_measurements_data]
        garment_measurements_data = garment_measurements_data[1:5]
        for garment_data in garment_measurements_data:
            garment_data[0] = garment_data[0].replace('”', '')
            garment_data[0] = garment_data[0].replace('“', '')

        for data in garment_measurements_data:
            self.obj[data[1]] = data[0]


    def _extract_model_measurements(self):
        model_measurement_data = self.data[::]
        model_measurement_data = model_measurement_data[7:]
        # size, height, chest, waist, fit notes, sizing notes
        self.obj['size'] = model_measurement_data[0].split('size')[1].replace('.', '').replace(' ', '')
        for i, measurement in enumerate(model_measurement_data[1].split('|')):
            try:
                if i == 0:
                    self.obj['model-height-feet'] = measurement.split(' ')[2].replace('"', '')
                elif i == 1:
                    self.obj['model-chest-inches'] = measurement.split(" ")[1].replace('”', '')
                elif i == 2:
                    self.obj['model-waist-inches'] = measurement.split(" ")[1].replace('”', '')
            except:
                pass
        
    
    def _reformat_obj(self):
        self.obj['leg-opening'] = self.obj.pop('leg')
    
    def start(self):
        self._clean_html()
        self._extract_garment_measurements()
        self._extract_model_measurements()
        self._reformat_obj()
        return self.obj

if __name__ == '__main__':
    with open('dump.pkl', 'rb') as f:
        data = pickle.load(f)

    cc = Cleaner(data)
    cc.start()
    print(cc.obj)