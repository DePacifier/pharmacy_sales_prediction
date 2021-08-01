from scripts.data_manipulation import DataManipulator
from scripts.data_cleaner import DataCleaner
from numpy.core.records import array
import streamlit as st
import mlflow
from pickle import load
import pandas as pd
import numpy as np
import sys
import datetime
sys.path.insert(0, '../scripts')

from scripts.results_pickler import ResultPickler
from scripts.data_loader import load_df_from_csv

def read_csv_without_index(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print("file read as csv")
        return df
    except FileNotFoundError:
        print("file not found")


# def datToAndAfterHoliday(df, Column, holidays):

#     to = []
#     after = []
#     for a in df[Column]:
#         index = bisect.bisect(holidays, a)
#         if len(holidays) == index:
#             to.append(pd.Timedelta(0, unit='d'))
#             after.append(a - holidays[index-1])
#         else:
#             after.append(holidays[index] - a)
#             to.append(a - holidays[index-1])
#     return to, after


# def startMidEndMonth(x):
#     if x < 10:
#         return 0
#     elif x < 20:
#         return 1
#     else:
#         return 2


# def isWeekend(x):
#     if x < 6:
#         return 0
#     else:
#         return 1


# def dateExplode(df, column):
#     try:
#         df['Year'] = pd.DatetimeIndex(df[column]).year
#         df['Month'] = pd.DatetimeIndex(df[column]).month
#         df['Day'] = pd.DatetimeIndex(df[column]).day
#     except KeyError:
#         print("Column couldn't be found")
#         return
#     return df


# def generate_features(df):

#     df["Date"] = pd.to_datetime(df["Date"])

#     df["weekend"] = df["DayOfWeek"].apply(isWeekend)
#     df["MonthState"] = df["Day"].apply(startMidEndMonth)
#     with open('dates.pickle', 'rb') as handle:
#         dates = pickle.load(handle)
#     df["To"], df["After"] = datToAndAfterHoliday(df, "Date", dates)

#     df["After"] = pd.to_timedelta(df["After"])

#     df["To"] = pd.to_timedelta(df["To"])

#     df["After"] = pd.to_numeric(df['After'].dt.days, downcast='integer')
#     df["To"] = pd.to_numeric(df['To'].dt.days, downcast='integer')

#     return df


# def predict(model, csv):
#     csv_copy = csv.copy()
#     csv_copy.drop("Store", axis=1, inplace=True)

#     csv_copy.drop("Id", axis=1, inplace=True)

#     csv_copy.drop("Date", axis=1, inplace=True)
#     print(csv_copy.columns)
#     prediction = model.predict(csv_copy)

#     pred_df = csv.copy()

#     pred_df["Sales-Prediction"] = prediction
#     pred_df['Date'] = pd.to_datetime(pred_df['Date'])
#     return pred_df


# def man_predict(model, csv):

#     csv_copy = csv.copy()
#     csv_copy.drop("Store", axis=1, inplace=True)

#     csv_copy.drop("Date", axis=1, inplace=True)

#     prediction = model.predict(csv_copy)
#     pred_df = csv.copy()

#     pred_df["Sales-Prediction"] = prediction
#     pred_df['Date'] = pd.to_datetime(pred_df['Date'])
#     return pred_df

def get_model_columns():
    # Create Result Pickler Object
    results = ResultPickler()
    results.load_data('./models/column_reference.pkl')

    return results.get_data()['model_input_columns']

def import_model(columns=None):
    '''Import from mlflow if possible or get saved model'''
    try:
        if(columns != None):
            model = 'runs:/2d6250149bd746ab84c41372792902b4/model'
            # Load model as a PyFuncModel.
            model = mlflow.pyfunc.load_model(model)
            data = pd.DataFrame(columns=columns)

            # a_series = pd.Series(a["data"], index=data.columns)
            # data = data.append(a_series, ignore_index=True)
        else:
            with open('../models/01-08-2021-21-23-15-74.17%.pkl', 'rb') as handle:
                model = load(handle)

            # model.predict([a['data']])

        return model

    except Exception as e:
        print('Failed to load model')

def dayofweek(data):
    values = []
    try:
        for index, row in data.iterrows():
            day = datetime.date(row['Year'],row['Month'],row['Day']).weekday()
            values.append(day + 1)
        data['DayOfWeek'] = values

    except:
        print("Failed to create day of week")

def get_season(month):
    if(month <= 2 or month == 12):
        return 2
    elif(month > 2 and month <= 5):
        return 1
    elif(month > 5 and month <= 8):
        return 0
    else:
        return 3

def add_season(data):
    date_index = data.columns.get_loc("Month")
    data.insert(date_index + 1, 'Season',data['Month'].apply(get_season))


def encode_holiday(x):
    if x == 'Public Holiday':
        return 1
    elif x == 'Easter':
        return 2
    elif x == 'Christmas':
        return 3
    else:
        return 0

def change_holiday(data):
    data['StateHoliday'] = data['StateHoliday'].apply(encode_holiday)

def day_to_after_holiday(data, holidays):
    days_to = []
    days_after = []
    holidays = holidays.sort_values(by=['Month','Day'], ascending='True')
    print(holidays)

    for index, row1 in data.iterrows():
        lower_month = 12
        lower_day = 26
        actual_month = 0
        month = row1['Month']
        day = row1['Day']
        for index, row in holidays.iterrows():
            if(month >= row['Month'] and day > row['Day']):
                lower_month = row["Month"]
                lower_day = row['Day']
            elif(month > row['Month']):
                lower_month = row["Month"]
                lower_day = row['Day']
            elif(month <= row['Month'] and day < row['Day']):
                actual_month = row['Month']
                actual_day = row['Day']
                break
                
        if(lower_month == 12):
            date1 = datetime.date(2009, lower_month, lower_day)
            date2 = datetime.date(2010, month, day)
            date3 = datetime.date(2010, actual_month, actual_day)
        else:
            date1 = datetime.date(2010, lower_month, lower_day)
            date2 = datetime.date(2010, month, day)
            date3 = datetime.date(2010, actual_month, actual_day)

        days_to_holiday = date2 - date1
        days_after_holiday = date3 - date2
        
        days_to.append(days_to_holiday.days)
        days_after.append(days_after_holiday.days)

    data['DaysToHoliday'] = days_to
    data['DaysAfterHoliday'] = days_after

def create_additional_datas(data):
    # Load Holiday References
    holiday_reference = load_df_from_csv('./models/holiday_reference.csv')

    # Classifiy Date
    data_cleaner = DataCleaner(data)
    data_cleaner.change_column_to_date_type('Date')
    data_cleaner.separate_date_column(date_column='Date')

    # Create Day of Week
    dayofweek(data)

    # Create WeekDay
    data_manipulator = DataManipulator(data)
    data_manipulator.add_week_day('DayOfWeek')

    # Create Season
    add_season(data)

    # change holiday
    change_holiday(data)

    # Create Month Timing
    data_manipulator.add_month_timing('Day')

    # Create Days to and after holiday
    day_to_after_holiday(data, holiday_reference)

    data = data[['DayOfWeek', 'WeekDay', 'Year', 'Month', 'Season', 'Day', 'MonthTiming', 'Open', 'Promo', 'StateHoliday', "DaysAfterHoliday","DaysToHoliday", "SchoolHoliday"]]

    return data

def app():

    # Load model column input reference
    model_columns = get_model_columns()

    # Import Model for the predicition
    model = import_model()

    # Load Store References
    store_reference = load_df_from_csv('./models/store_reference.csv')
    store_reference.drop('Store', axis=1, inplace=True)

    # Load Saved Results Data
    # model = load(filename='./models/satisfaction_scorer_model.pkl')

    st.title("Store Sales Predictor")

    method = st.radio("Options", ('Upload File', 'Manual'))

    if(method == 'Upload File'):
        test_file = st.file_uploader("Upload csv files", type=['csv'])
        test_csv = None

        if (test_file):
            test_csv = read_csv_without_index(test_file)
            st.dataframe(test_csv)
            # st.write(test_csv)

            if st.button('Predict'):
                st.write("Predict clicked")
                # dateExplode(test_csv,column="Date")
                # test_store=merge_store(test_csv)
                # test_store=generate_features(test_store)
                # # st.write(test_csv)
                # prediction=predict(model,test_store)
                # st.write(prediction)
                
    else:

        store_id = int(st.selectbox(
            "Store Id", [i for i in range(1, 1116)]))
        # DayOfWeek	Date	Open	Promo	StateHoliday	SchoolHo
        date = st.date_input('Sale date')
        # sate_hoilday = st.selectbox(
        #     "Sate Holiday", list(holidays.keys()))
        state_hoilday = st.selectbox("Sate Holiday", ["Public Holiday", "Easter", "Christmas", "None"])
        school_holiday = int(st.checkbox("School Holiday"))
        promo = int(st.checkbox("Promotion Running"))
        is_open = int(st.checkbox("Store Open"))

        if st.button('Predict'):
            st.write('predict button clicked')
            # Create dataframe with the values
            pred_value = pd.DataFrame(columns=model_columns)
            store_values = store_reference.iloc[store_id + 1,:]
            data = {'Date': [date], 'StateHoliday': [state_hoilday],'SchoolHoliday': [school_holiday], 'Promo':[promo], 'Open':[is_open]}
            initial_data = pd.DataFrame(data=data)
            train_data = create_additional_datas(initial_data)
            st.dataframe(train_data)
            # final_data = pd.concat(
            #     [train_data, store_values], axis=1, ignore_index=True)
            # st.dataframe(final_data)
                        
            # st.write(f"{pred['Sales-Prediction'].to_list()[0]:.2f}")

