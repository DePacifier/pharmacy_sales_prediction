from numpy.core.records import array
import streamlit as st
from pickle import load
import numpy as np
import sys
sys.path.insert(0, '../scripts')

def app():

    # Load Saved Results Data
    # model = load(filename='./models/satisfaction_scorer_model.pkl')

    st.title("Store Sales Predictor")

    st.header("Insert Values to get the Store's Current Sales")
    st.subheader("Is the Store Open (0,1): ")
    store_open = st.number_input('Enter Status', key='a')

    st.subheader("How much distance between the store and its competition(m): ")
    distance = st.number_input('Enter total distance', key='b')

    st.subheader("Is Promo in effect (0,1): ")
    promo = st.number_input('Enter Promo Status', key='v')

    st.subheader("Since when did the competition began (Year): ")
    comp_year = st.number_input('Enter the year in number', key='c')

    st.subheader("Since when did the competition began (Month): ")
    comp_month = st.number_input('Enter the month in number', key='d')

    st.subheader("What Day of the week is it: ")
    week_val = st.number_input('Enter week in number', key='e')

    st.subheader("What week did Promo2 started: ")
    promo2_start_week = st.number_input('Enter Promo start week in number', key='f')

    st.subheader("What is the type of the store (0 - 3 for a - d): ")
    store_type = st.number_input('Enter type', key='g')

    st.subheader("What day is it: ")
    day_val = st.number_input('Enter day in number', key='h')

    st.subheader("What month is it: ")
    month_val = st.number_input('Enter month in number', key='i')

    st.subheader("What year did Promo2 Start: ")
    promo2_year = st.number_input('Enter year in number', key='j')

    st.subheader("What is the Assortment of the store (0 - 2 for a - c): ")
    store_assortment = st.number_input('Enter assortment type', key='k')

    st.subheader("How many days left to holiday: ")
    rem_days_holiday = st.number_input('Enter remaining days in number', key='l')

    st.subheader("What is the Promo Interval: ")
    promo_interval = st.number_input('Enter promo interval', key='m')

    st.subheader("What year is it: ")
    year_val = st.number_input('Enter year in number', key='n')

    st.subheader("How many days after the holiday: ")
    day_after_hol = st.number_input('Enter days after the holiday', key='o')

    st.subheader("Is Promo2 in effect (0,1): ")
    promo2_status = st.number_input('Enter Status of Promo2', key='p')

    st.subheader("Is it a week-day or not (0,1): ")
    weekday_val = st.number_input('Enter Status', key='q')

    st.subheader("Is it a school holiday or not (0,1): ")
    school_hol = st.number_input('Enter Status', key='r')

    st.subheader("What season is it (0-3 for Winter-Spring): ")
    season_val = st.number_input('Enter season', key='s')

    st.subheader("What is the month timing (0-2 for Before,During or After): ")
    month_timing = st.number_input('Enter month timing', key='t')

    st.subheader("Is it a state holiday or not (0,1): ")
    state_hol_stat = st.number_input('Enter status', key='u')

    if st.button('Predict Satisfaction'):	
        try:
            array = [week_val, weekday_val, year_val, month_val, season_val, day_val, month_timing, store_open,
                     promo, state_hol_stat, day_after_hol, rem_days_holiday, school_hol, store_type, store_assortment,
                     distance, comp_month, comp_year, promo2_status, promo2_start_week,
                     promo2_year, promo_interval]
            # val = model.predict([array])
            # satisfaction = [i[0] for i in val][0]
            # st.write(
                # 'The predicted satisfaction score of the user is: {:.3f}'.format(satisfaction))
        except:
            print('Need more inputs')
