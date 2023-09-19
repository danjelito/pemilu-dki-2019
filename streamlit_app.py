import streamlit as st
import pandas as pd
from src import module
from pathlib import Path

# set page configuration
st.set_page_config(
    page_title="Sainte Lague Simulation",
    page_icon="🗳️",
    initial_sidebar_state="expanded",
    layout="wide",
)


def reset():
    """Reset editable DF."""
    st.session_state.key += 1


@st.cache_data
def load_data():
    """Load DF with caching."""
    path = Path.cwd() / "output/vote_result.xlsx"
    df = pd.read_excel(path)
    return df


df = load_data()

# title and markdown
st.markdown("### Pemilu DPRP DKI Jakarta 2019" "\n# Sainte Lague Simulation 🗳️")
st.markdown("This app simulates the Pemilu DPRP DKI Jakarta 2019.")
st.markdown("You can change the vote each calon and see if they become selected or not.")
st.markdown("##### Open in PC for best experience.")
st.divider()

# set dapil selector
with st.sidebar:
    st.markdown("# Select dapil here 👇")
    dapil = st.radio(
        label="Select dapil here 👇",
        label_visibility="hidden",
        options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        captions=[
            "Jakarta Pusat",
            "Kepulauan Seribu dan Jakarta Utara",
            "Jakarta Utara",
            "Jakarta Timur",
            "Jakarta Timur",
            "Jakarta Timur",
            "Jakarta Selatan",
            "Jakarta Selatan",
            "Jakarta Barat",
            "Jakarta Barat",
        ],
        key="dapil_no",
    )

# get dataframe based on dapil
dapil_no = int(dapil)
df_dapil = df.loc[df["dapil_no"] == dapil_no]
num_calon_selected = df_dapil.loc[:, "terpilih"].sum()

# prepare dataframe for display
df_dapil = df_dapil.assign(
    dapil=lambda df_: df_["dapil_no"].astype(str) + " " + df_["dapil_nama"]
)

# show editable DF
st.markdown("## Input Data")
st.markdown("#### This table is *sortable* and *changeable*.")
st.markdown("1️⃣ Double click the number of calon vote to change.")
st.markdown("2️⃣ Click table header to sort.")
st.markdown("3️⃣ Scroll on the right side of the table to see more.")
st.markdown("4️⃣ Click reset button below table to reset calon vote to the original.")

if "key" not in st.session_state:
    st.session_state.key = 0

edited_df_dapil = st.data_editor(
    df_dapil,
    width=1000,
    height=450,
    column_order=["dapil", "partai", "partai_vote", "no_urut", "nama", "vote"],
    column_config={
        "dapil": "Dapil",
        "partai": "Partai",
        "partai_vote": "Suara Partai",
        "no_urut": "No Urut Calon",
        "nama": "Nama",
        "vote": "Suara Calon (changeable 👇)",
    },
    disabled=["dapil", "partai", "partai_vote", "no_urut", "nama"],
    hide_index=True,
    key=f"editor_{st.session_state.key}",
)
st.button("Reset", type="primary", on_click=reset)

# sainte lague calculation
# use editable df to get the elected valon
partai_vote, calon_vote = module.get_dapil_data(edited_df_dapil, dapil_no)
selected_partai = module.get_selected_partai(
    partai_vote=partai_vote, num_selected=num_calon_selected, with_rank=True
)
selected_calon = module.get_selected_calon(
    calon_vote=calon_vote, selected_partai=selected_partai, with_partai=True
)

# display the selected calon
st.markdown("## Result - Elected Calon")
st.markdown('#### This is the *result of the simulation*, sorted by "Terpilih Di Ronde".')
st.markdown("1️⃣ Click table header to sort.")
selected_calon = pd.DataFrame(selected_calon, columns=["partai", "nama"])
selected_calon = (selected_calon
    .assign(
        suara_partai_calon=lambda df_: df_["partai"].map(partai_vote),
        terpilih_di_ronde=list(range(1, len(selected_calon) + 1))
    )
    .merge(calon_vote, left_on="nama", right_on="nama", how="left")
    .drop(columns=["partai_y"])
    .rename(columns={
        "suara_partai_calon": "suara_partai_+_calon",
        "vote": "suara_calon", 
        "rank": "ranking_calon_di_partainya"}
    )
    .rename(columns=lambda c: c.replace("_x", "").title().replace("_", " "))
    .loc[:, ["Partai", "Suara Partai + Calon", "Nama", "Suara Calon", 
             "Ranking Calon Di Partainya", "Terpilih Di Ronde"]]
    .sort_values("Terpilih Di Ronde")
)       
selected_calon.index = selected_calon.index + 1
df_len = len(selected_calon)
df_height = (df_len + 1) * 35 + 3
st.dataframe(selected_calon, width=1000, height=df_height, hide_index=False)
