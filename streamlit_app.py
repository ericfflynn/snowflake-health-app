# Import python packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import datetime 

st.set_page_config(
    page_title="Personal Health App",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
st.title("Eric Flynn's Personal Health Application :man-lifting-weights:")
st.markdown("""---""")

raw_df = pd.read_csv("./raw_data.csv")
raw_df['DATE'] = raw_df['DATE'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
rep = raw_df.METRIC.unique()
raw_df.replace(rep,['Body Fat %','BMI','Calcium','Carbohydrates','Cholesterol','Dietary Calories','Fiber','Sugar','Mono-Fat','Potassium','Vitamin C','Iron','Sodium','Fat','Poly-Fat','Protein','Saturated Fat','Exercise Time','Step Count','Weight','Exercise Calories'], inplace=True)

start_date = st.sidebar.date_input('Start Date',min(raw_df['DATE']))
end_date = st.sidebar.date_input('End Date',max(raw_df['DATE']))
metric = st.sidebar.selectbox("Metric", raw_df.METRIC.unique(), index=5)


base_df = raw_df.query("DATE >= @start_date & DATE <= @end_date")

line_data = base_df[base_df['METRIC'] == metric]
line_unit = line_data['UNITS'].unique()[0]

macros = base_df[base_df['METRIC'].isin(['Protein','Carbohydrates','Fat'])].groupby('METRIC').mean()
active_mins = int(base_df[base_df['METRIC'] == 'Exercise Time']['QTY'].mean())

avg_cals = int(base_df[base_df['METRIC'] == 'Dietary Calories']['QTY'].mean())
last_recorded_weight = base_df.loc[base_df['METRIC'] == 'Weight'].QTY.iloc[-1]
avg_daily_protein = macros.loc['Protein'].iloc[0]

col1_1, col1_2, col1_3, col1_4 = st.columns(4)
with col1_1:
    st.metric(label="Average Daily Calories", value=f'{avg_cals:,} Kcal', delta=(avg_cals-2800))
with col1_2:
    st.metric(label="Average Daily Activity", value=f"{active_mins} Min", delta=(active_mins-30))
with col1_3:
    st.metric(label="Average Daily Protein", value=f"{avg_daily_protein:,.1f} Grams", delta=f'{(avg_daily_protein-last_recorded_weight):,.1f}')
with col1_4:
    st.metric(label="Last Recorded Weight", value=f"{last_recorded_weight} lbs", delta=(last_recorded_weight-180))

st.markdown("")
st.markdown("")
col1_2, col2_2= st.columns([.6, .4])

with col1_2:
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(line_data.DATE, line_data.QTY, marker='o', color='r');
    plt.title(f"{metric}", fontsize=20);
    # plt.xlabel('Date', fontsize=15);
    plt.ylabel(line_unit, fontsize=15);
    plt.xticks(rotation=90, fontsize=10);
    st.pyplot(fig)
with col2_2:
    # fig, ax = plt.subplots(figsize=(5,5))
    # plt.title("Average Macronutrient Distrubution")
    # ax.pie(macros['QTY'], labels=['Carbohydrates', 'Protein', 'Fat'], autopct='%1.1f%%');
    # st.pyplot(fig)

    # buf = BytesIO()
    # fig.savefig(buf, format="png")
    # st.image(buf)
    sizes = macros['QTY']
    colors = ['#ff9999','#66b3ff','#99ff99']
    fig1, ax1 = plt.subplots(figsize=(5,5))
    plt.title("Average Macronutrient Distrubution")
    ax1.pie(sizes, colors = colors, labels=['Carbohydrates', 'Protein', 'Fat'], autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0,0),0.80,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')  
    plt.tight_layout()
    st.pyplot(fig)

