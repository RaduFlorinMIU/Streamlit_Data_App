# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:00:48 2023

@author: angel
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_data():
    """
    Returns
    -------
    temp_data : DataFrame
        This function is used to load the data about 'Sleep Health and Lifestyle'.
        THe data is put in a cache so it dosen't have to be loaded at each 
        query from the app.
    """
    temp_data = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
    return temp_data


@st.cache_data
def load_data_clean_data():
    data_frame = load_data()
    data_frame = data_frame.fillna("None")
    return data_frame

@st.cache_data
def sleep_disorder(x):
    temp = x["Sleep Disorder"].unique().tolist()
    return temp

def create_distribution_plots(data_to_plot):
    """
    Parameters
    ----------
    data_to_plot : Data Frame from we will create plots from

    Returns
    -------
    Seavorn plot.

    """

    figure, axes = plt.subplots(1, 2, sharex=True)

    sns.boxplot(ax=axes[0],
                data=data_to_plot,
                x="Sleep Disorder",
                y="Quality of Sleep",
                )

    sns.boxplot(ax=axes[1],
                data=data_to_plot,
                x="Sleep Disorder",
                y="Sleep Duration",
                )

    for ax in axes:
        ax.tick_params(axis="x", labelrotation=45)

    figure.suptitle("Distribution per Sleep Disorder")

    figure.tight_layout()

    st.pyplot(figure)

def filter_exloratory_plots (data_to_plot):
    fig_1 = plt.figure()
    sns.scatterplot(x="Age", 
                    y="Sleep Duration", 
                    data = data_to_plot, 
                    hue = "Sleep Disorder"
                    )
    plt.title("Evolution of Sleep")
    st.pyplot(fig_1)
    
    fig_2 = plt.figure()
    sns.set_theme(style="ticks")
    sns.boxplot(data = data_to_plot,
                x = "Occupation", 
                y = "Sleep Duration",
                )
    plt.title("Distribution of sleep based on occupation")
    plt.xticks(rotation = 90)
    sns.despine(trim=True)
    st.pyplot(fig_2)
    
    fig_3 = plt.figure()
    
    sns.countplot(data=temp_data,
                x="Quality of Sleep",
                hue="Sleep Disorder"
        )
    
    st.pyplot(fig_3)
    
    fig_4 = plt.figure()
    sns.countplot(data=data_to_plot,
                x="Quality of Sleep", 
                hue="Sleep Disorder"
        )
    st.pyplot(fig_4)


def main():

    # Display Title
    st.title("Advanced Python for Data Science")

    # Display Header
    st.header("Individual Project : creation of an app")

    # Display Subheader
    st.subheader("Sleep Health and Lifestyle analysis")

    # Display a sample of the dataset
    sleep_data_frame = load_data_clean_data()

    # Display sample of Data
    st.write(sleep_data_frame.head())

    # Creating disorder filtering option
    sleep_disorder_option = sleep_disorder(sleep_data_frame)
    sleep_disorder_option = ["All"] + sleep_disorder_option

    
    # Creating a Side bar 
    with st.sidebar:
        st.subheader("Exploratory Data Analysis")
        menu_selected = st.selectbox("Choose a page",["Page 1", "Page 2"])
    
    if menu_selected == "Page 1" : 
        # Display plot
        create_distribution_plots(sleep_data_frame)

    else :
        select_disorder = st.selectbox("Choose a Sleep Disorder to filter the graphics",
                               sleep_disorder_option)
        
        # Applyng the filtering disorder option :
        if select_disorder == "All":
            filter_data_frame = sleep_data_frame
        else:
            filter_data_frame = sleep_data_frame[
                sleep_data_frame['Sleep Disorder'] == select_disorder 
                ]
        
        filter_exloratory_plots(filter_data_frame)



if __name__ == '__main__':
    main()
