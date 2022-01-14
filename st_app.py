import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title ('Testing streamlit')

st.text('Using Pandas & Seaborn')

sns.set_style ('whitegrid')
#('white' | 'dark' | 'whitegrid' | 'darkgrid' | 'ticks')

st.text('This is a dataset from Seaborn, loaded using')
st.code("df = sns.load_dataset('flights')" )
df = sns.load_dataset('flights') # Jan 1949 - Dec 1960
df

st.header('Catagorical Grouping')
grouper = { }
months =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',]
gr = st.multiselect ('Use this Multiselect to pick which months can have snow.', months, months[0:3])
for m in months:
    if m in gr:
        grouper[m]="Snow"
    else:
        grouper[m]="No Snow"
if st.checkbox('Show the resulting grouper dictionary'):
    st.text('This is the resulting grouper dictionary.')
    grouper

st.text("Use the grouper to create a new column")
st.code("df['snow'] = df.month.map(grouper)")
df['snow'] = df.month.map(grouper)
st.write(df.head())

st.text("Use Pandas groupby to sum or count")
st.code("df_summed = df.groupby(['year','snow']).sum(['passengers'])")
df_summed = df.groupby(['year','snow']).sum(['passengers'])
st.write(df_summed)

g = sns.relplot(x='year', y='passengers',
                data=df_summed,
                hue='snow',
                #col='snow',
                aspect=1.7,
                height=3,
                palette=['blue', 'orange'],
                kind='line'
               )
#g.set_titles(col_template="")
g.set_xlabels("Year")
g.set_ylabels('Passengers');
g.legend.set_title('Snow or Not')
g.fig.suptitle('Grouping Categorical Columns')
st.pyplot(g)

if st.checkbox('Show code for chart'):
    st.subheader('Chart Code')
    st.code("""
        g = sns.relplot(x='year', y='passengers',
                        data=df_summed,
                        hue='snow',
                        #col='snow',
                        aspect=1.7,
                        height=3,
                        palette=['blue', 'orange'],
                        kind='line'
                       )
        #g.set_titles(col_template="")
        g.set_xlabels("Year")
        g.set_ylabels('Passengers');
        g.legend.set_title('Snow or Not')
        g.fig.suptitle('Grouping Categorical Columns')
        st.pyplot(g)
    """)

st.header('Distribution based Grouping')

cutoff = st.slider('Use the slider to set the cutoff for a Good Month', min_value=100, max_value=500, value=400, step = 50)
st.text("Add a column to hold the categories & a column for counting")
st.code("""
    df['ranking']='Bad'
    df.loc [ df['passengers'] > 500, ['ranking'] ] = 'Best'
    df.loc [ df['passengers'].between(cutoff,500,inclusive='both'),['ranking']] = 'Good'
    df['to_count']=1
""")
df['ranking']='Bad'
df.loc [ df['passengers'] > 500, ['ranking'] ] = 'Best'
df.loc [ df['passengers'].between(cutoff,500,inclusive='both'),['ranking']] = 'Good'
df['to_count']=1
st.write(df.head(2))

st.text("""As above, group and count using Pandas""")
st.code("""    df_ranked = df.groupby(['year','ranking']).sum('to_count')""")
df_ranked = df.groupby(['year','ranking']).sum('to_count')
st.write(df_ranked.head(2))

f2 = sns.relplot(x='year', y='to_count',
                data=df_ranked,
                hue='ranking',
                #col='snow',
                aspect=1.7,
                height=3,
                kind='line'
               )
#g.set_titles(col_template="")
f2.set_xlabels("Year")
f2.set_ylabels('Months');
f2.legend.set_title('Ranking')
f2.fig.suptitle('Grouping based on distribution criteria')
f2 = st.pyplot(f2)
