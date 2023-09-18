import streamlit as st
import pandas as pd
import numpy as np
from src import module
from pathlib import Path
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("Pemilu DPRP DKI Jakarta 2019")
st.title("Sainte Lague Simulation 🗳️")
st.markdown("This app simulates the Pemilu DPRP DKI Jakarta 2019")
st.markdown("You can change the vote for each partai and calon")

# load dataframes
@st.cache_data
def load_data():
    path = Path.cwd() / "output/vote_result.xlsx"
    df = pd.read_excel(path)
    return df
df = load_data()

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

# get dataframe based on dapil
dapil_no = int(dapil)
df_dapil = df.loc[df["dapil_no"] == dapil_no]
num_calon_selected = df_dapil.loc[:, 'terpilih'].sum()

# prepare dataframe for display
df_dapil = (df_dapil
            .assign(dapil=lambda df_: df_["dapil_no"].astype(str) + " " + df_["dapil_nama"])
            )

# starting from here, use editable DF
edited_df_dapil = st.data_editor(
    df_dapil,
    width=800, 
    height=1200, 
    column_order=["dapil", "partai", "partai_vote", "no_urut", "nama", "vote"],
    column_config={
        "dapil": "Dapil",
        "partai": "Partai",
        "partai_vote": "Suara Partai",
        "no_urut": "No Urut Calon",
        "nama": "Nama",
        "vote": "Suara Calon",
    },
    disabled=["dapil", "partai", "partai_vote", "no_urut", "nama"],
    hide_index=True,
)

# use editable df to get the elected valon
partai_vote, calon_vote = module.get_dapil_data(edited_df_dapil, dapil_no) 
selected_partai = module.get_selected_partai(partai_vote, num_calon_selected, with_rank=True) 
selected_calon = module.get_selected_calon(calon_vote, selected_partai, with_partai=True)
# module.verify_if_selected(df, selected_calon, dapil_no)
# selected_calon.sort(key=lambda x: x[0])

# display the selected calon
selected_calon = pd.DataFrame(selected_calon, columns=["partai", "nama"])
selected_calon = (selected_calon
    .assign(
        terpilih_di_ronde=list(range(1, len(selected_calon) + 1))
    )
    .merge(calon_vote, left_on="nama", right_on="nama", how="left")
    .drop(columns=["partai_y"])
    .rename(columns={"vote": "suara_calon", "rank": "ranking_calon_di_partainya"})
    .rename(columns=lambda c:c.replace("_x", "").title().replace("_", " "))
)
selected_calon.index = selected_calon.index + 1
st.dataframe(selected_calon, width=800, hide_index=False)
