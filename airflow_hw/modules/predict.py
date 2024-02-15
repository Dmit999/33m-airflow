import pandas as pd
import json
import datetime as dt
import os
import dill


def predict():
    path = os.environ.get('PROJECT_PATH', '.')
    path_pikl = path + '/data/models/'
    path_json = path + '/data/test/'
    path_to_save = path + '/data/predictions/'

    def last_pikl():
        dates = []
        for files in os.listdir(path_pikl):
            dates = dates + [files.split('_')[-1].split('.')[0]]
        return os.listdir(path_pikl)[dates.index(max(dates))]

    def get_model():
        model_filename = path_pikl + last_pikl()
        with open(model_filename, 'rb') as file:
            model = dill.load(file)
        return model

    model = get_model()
    result_df = pd.DataFrame()
    for files in os.listdir(path_json):
        if files.split('.')[-1] == 'json':
            path_file = path_json + files
            with open(path_file, 'r') as j:
                contents = json.load(j)
            json_list = [contents]
            data = pd.DataFrame(json_list)
            data['preds'] = model.predict(data)
            data = data[['id', 'price', 'preds']]
            result_df = pd.concat([result_df, data], axis=0)
            file_name_to_save = f'preds_{dt.datetime.now().strftime("%Y%m%d%H%M")}.csv'
            result_df.to_csv(path_to_save + file_name_to_save, index=False)


if __name__ == '__main__':
    predict()
