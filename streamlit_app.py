import streamlit as st
import pandas as pd
import numpy as np
from src import module
from pathlib import Path

st.title("Pemilu DPRP DKI Jakarta 2019")
st.title("Sainte Lague Simulation 🗳️")
st.markdown("This app simulates the Pemilu DPRP DKI Jakarta 2019")
st.markdown("You can change the vote for each partai and calon")

# load dataframes
path = Path.cwd() / "output/vote_result.xlsx"
df = pd.read_excel(path)

with st.sidebar:
    # set dapil selector
    dapil = st.radio(
        "Select dapil 👇",
        [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
        ],
        captions=[
            'Jakarta Pusat',
            'Kepulauan Seribu dan Jakarta Utara',
            'Jakarta Utara',
            'Jakarta Timur',
            'Jakarta Timur',
            'Jakarta Timur',
            'Jakarta Selatan',
            'Jakarta Selatan',
            'Jakarta Barat',
            'Jakarta Barat',
        ],
        key="dapil_no",
    )