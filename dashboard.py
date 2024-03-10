import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns

# Fungsi Label di plot bar
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# Fungsi untuk menghitung total pemesanan masing-masing user
def cnt_user(df):
    casual = df['casual'].sum()
    registered = df['registered'].sum()
    count = df['count'].sum()
    return casual,registered,count

# Fungsi membuat line plot
def make_Line_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df_x,df_y)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    st.pyplot(fig)

# Fungsi untuk menghitung total pemesanan masing-masing time category
def cnt_timecat(df):
    data = df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    if data.empty:
        Morning=0
        Afternoon=0
        Evening=0
        Night=0
    else:
        Morning = data.loc[data['time_category']=='Morning','count'].values[0]        
        Afternoon = data.loc[data['time_category']=='Afternoon','count'].values[0]
        Evening = data.loc[data['time_category']=='Evening','count'].values[0]
        Night = data.loc[data['time_category']=='Night','count'].values[0]
    return Morning, Afternoon, Evening, Night

# Fungsi membuat bar plot
def make_bar_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    figx, ax = plt.subplots(figsize=(6, 6))
    ax.bar(df_x, df_y, color='#72BCD4')
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    addlabels(df_x,df_y)
    st.pyplot(figx)

# Baca File csv
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# mengolah data
day_df.sort_values(by="rental_date", inplace=True)
hour_df.sort_values(by="rental_date", inplace=True)
day_df['rental_date'] = pd.to_datetime(day_df['rental_date'])
hour_df['rental_date'] = pd.to_datetime(hour_df['rental_date'])

# Membuat Sidebar 
min_date = hour_df["rental_date"].min()
max_date = hour_df["rental_date"].max()
with st.sidebar:
    st.image("dashboard/logo.png")

    # Membuat filter rentang tanggal
    start_date, end_date = st.date_input(
        label='time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mengolah data sesuai rentang tanggal yang diinput
main_day_df = day_df[(day_df["rental_date"] >= str(start_date)) & (day_df["rental_date"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["rental_date"] >= str(start_date)) & (hour_df["rental_date"] <= str(end_date))]

# Dashboard
st.title('Welcome To Rental Bersama IMA :sparkles:')
st.markdown("""---""")

# Membuat Grafik pemesanan harian
st.header('Daily Rentals :date:')
tab1, tab2, tab3 = st.tabs(["ALL","holiday", "working day"])
# Grafik jumlah rental di semua hari (sesuai rentang yang diinput)
with tab1:
    casual,registered,count = cnt_user(main_day_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(main_day_df['rental_date'],main_day_df['count'],None,None,45) 
# Grafik jumlah rental di hari libur (sesuai rentang yang diinput)
with tab2:
    df_holiday = main_day_df[main_day_df['holiday']==1]
    casual,registered,count = cnt_user(df_holiday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(df_holiday['rental_date'],df_holiday['count'],None,None,45)
# Grafik jumlah rental di hari kerja (sesuai rentang yang diinput)
with tab3:
    df_workday = main_day_df[main_day_df['workingday']==1]
    casual,registered,count = cnt_user(df_workday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(df_workday['rental_date'],df_workday['count'],None,None,45)

# Membuat Grafik pemesanan berdasarkan kategori waktu (Pagi, Siang, Sore, Malam)
st.markdown("""---""")
st.header('Hourly Rentals :clock1:')
tab1, tab2, tab3 = st.tabs(["ALL","holiday", "working day"])
# Grafik jumlah rental di semua hari (sesuai rentang yang diinput)
with tab1:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        hourly_cnt_df.sort_values(by='count', ascending=False,inplace=True)
        hourly_cnt_df=hourly_cnt_df.reset_index()
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)
# Grafik jumlah rental di hari libur (sesuai rentang yang diinput)
with tab2:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[main_hour_df['holiday']==1]
    hourly_cnt_df = hourly_cnt_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        hourly_cnt_df.sort_values(by='count', ascending=False,inplace=True)
        hourly_cnt_df=hourly_cnt_df.reset_index()
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)
# Grafik jumlah rental di hari kerja (sesuai rentang yang diinput)
with tab3:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[main_hour_df['workingday']==1]
    hourly_cnt_df = hourly_cnt_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        hourly_cnt_df.sort_values(by='count', ascending=False,inplace=True)
        hourly_cnt_df=hourly_cnt_df.reset_index()
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)


# Membuat Grafik pemesanan berdasarkan kategori musim
st.markdown("""---""")
st.header('Seasonly Rentals 🍂')

season_rental = main_day_df[['count','season']].groupby(by='season').sum().reset_index()
season_map = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}
season_rental['season'] = season_rental['season'].map(season_map)
season_rental.sort_values(by='count', ascending=False,inplace=True)
season_rental = season_rental.reset_index()
col1, col2, col3 = st.columns([1,4,1])
with col2:
    make_bar_Plot(season_rental["season"],season_rental["count"],None,'count',45)

# Membuat Grafik perbandingan pemesanan pada hari kerja dan libur
st.markdown("""---""")
st.header('Rental in Holiday vs Workingday')
tab1, tab2 = st.tabs(["by time","by user"])
with tab1:
    col1, col2,col3 = st.columns([1,5,1])
    with col2:
        time_rental = main_hour_df[['time_category','count','workingday']].groupby(['workingday','time_category']).sum().reset_index()
        time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
        time_rental['time_category'] = pd.Categorical(time_rental['time_category'], categories=time_order, ordered=True)
        fig, ax = plt.subplots()
        ax = sns.barplot(x='workingday', y='count', hue='time_category', data=time_rental, )
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.xlabel(None)
        plt.ylabel('Total')
        plt.xticks([1, 0], ['Workingday', 'Holiday'], rotation=0)
        plt.legend(loc='upper left')
        st.pyplot(fig)
with tab2:
    col1, col2,col3 = st.columns([1,5,1])
    with col2:
        workingday_rental = main_day_df[['workingday','casual','registered','count']].groupby(by='workingday').sum().reset_index()
        fig, ax = plt.subplots()
        ax = workingday_rental.plot(kind='bar', x='workingday', y=['casual', 'registered', 'count'], ax=ax)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.ylabel('Total')
        plt.xlabel(None)
        plt.xticks([1, 0], ['Workingday', 'Holiday'], rotation=0)
        plt.legend(['Casual', 'Registered', 'count'])
        st.pyplot(fig)


# Membuat Grafik korelasi temperature dan count rental
st.markdown("""---""")
st.header('Temperature Correlation :thermometer:')
col1,col2=st.columns([7,1])
with col1:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.scatter(x=main_day_df['temp'],  y=main_day_df['count'])
    ax.set_ylabel('Count Rental')
    ax.set_xlabel('Temperature')
    st.pyplot(fig)
with col2:
    corr = main_day_df['temp'].corr(main_day_df['count'])
    st.metric(label="Korelasi", value=round(corr,2))
