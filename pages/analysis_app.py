import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns


feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))

st.set_page_config(page_title="viz_demo")

st.title("Analysis")

new_df = pd.read_csv("datasets/data_viz1.csv")
new_df1 = pd.read_csv("datasets/updated_data.csv")


group_df = new_df[['sector','price','price_per_sqft','built_up_area'
                   ,'latitude','longitude']].groupby('sector').mean()



# Plotly scatter mapbox
st.header("Sector Price per Sqft Geomap")
plotly_fig = px.scatter_mapbox(
    group_df, 
    lat="latitude", 
    lon="longitude", 
    color="price_per_sqft", 
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire, 
    zoom=10,
    mapbox_style="open-street-map",
    width=1200, 
    height=700,
    hover_name=group_df.index
)
st.plotly_chart(plotly_fig, use_container_width=True)

# Matplotlib WordCloud
st.header("Features Wordcloud")
wordcloud = WordCloud(
    width=800, 
    height=800, 
    background_color='white', 
    stopwords=set(['s']),  
    min_font_size=10
).generate(feature_text)

fig_wc, ax = plt.subplots(figsize=(8, 8))  # new Matplotlib figure
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)
st.pyplot(fig_wc)  # pass Matplotlib figure here



# Scatter plot
st.header("Area Vs Price")

# Column name where property type is stored
property_type_column = "property_type"

# Selected property type from dropdown
selected_type = st.selectbox("Select Property Type", ['flat', 'house'])

# Filter DataFrame
filtered_df = new_df[new_df[property_type_column] == selected_type]

# Plot
plotly_fig1 = px.scatter(
    filtered_df,
    x="built_up_area", 
    y="price", 
    color="bedRoom", 
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(plotly_fig1, use_container_width=True)





# creating the pie chart
st.header("BHK Pie Chart")

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
selected_sector = st.selectbox('Select Sector',sector_options)

if selected_sector == 'overall':
    fig2 = px.pie(new_df,names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector],names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)


# #4rth plot side by side box plot
st.header("Side by Side BHK price comparision")

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price')
st.plotly_chart(fig3, use_container_width=True)


# 5th plot dist plot
st.header("Side by Side Distplot for property type")

fig4 = plt.figure(figsize=(10,4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label = 'house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'],label = 'flat')
plt.legend()
st.pyplot(fig4)
