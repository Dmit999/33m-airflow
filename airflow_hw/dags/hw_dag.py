import datetime as dt
import os
import sys

import pandas as pd
import json
import datetime
import os
import dill

from airflow.models import DAG
from airflow.operators.python import PythonOperator

import logging
from datetime import datetime

from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import json


path = os.path.expanduser('~/airflow_hw')
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

from modules.pipeline import pipeline
# <YOUR_IMPORTS>
from modules.predict import predict

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2024, 1, 9),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=2),
    'depends_on_past': True,
}

with DAG(
        dag_id='car_price_prediction',
        schedule="00 15 * * *",
        default_args=args,
) as dag:
    pipeline_step = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
    )
    # предсказание
    predict_step = PythonOperator(
        task_id='predict',
        python_callable=predict,
    )
    # Порядок выполнения тасок
    pipeline_step >> predict_step
