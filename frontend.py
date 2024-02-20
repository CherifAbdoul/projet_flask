import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier


st.write('''
         # App pour le reporting des outputs des modeles data
         Cette application permet de faire des reportings graphiques
         ''')


st.sidebar.header("les parametres d'entrée")


# streamlit run main.py