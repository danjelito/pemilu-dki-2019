# Sainte Lague Simulation

This project is a Streamlit web application designed for simulating the Pemilu DPRP DKI Jakarta 2019 election using the Sainte-Laguë method. The application allows users to interactively change the vote count for each candidate and view the results based on the Sainte-Laguë calculation. 

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)

## Overview

The Sainte-Laguë Simulation web application allows users to simulate the Pemilu DPRP DKI Jakarta 2019 election results based on the Sainte-Laguë method. Key features of the application include:

- Selection of Dapil (Daerah Pemilihan) to simulate election results for a specific constituency.
- Interactive table for changing the vote count for each candidate.
- Calculation of elected candidates based on the Sainte-Laguë method.
- Display of election results sorted by the "Terpilih Di Ronde" (Elected in Round) column.
- Option to reset the vote counts to the original data.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- `aiofiles==22.1.0`
- `aiosqlite==0.18.0`
- `altair==5.1.1`
- `arrow-cpp==11.0.0`
- `asttokens==2.0.5`
- `attrs==22.1.0`
- `beautifulsoup4==4.12.2`
- `bleach==4.1.0`
- `click==8.1.7`
- `cryptography==41.0.3`
- `fontconfig==2.14.1`
- `freetype==2.12.1`
- `grpc-cpp==1.48.2`
- `jupyterlab==3.6.3`
- `lxml==4.9.2`
- `matplotlib==3.7.2`s
- `numpy==1.25.2`
- `openpyxl==3.0.10`
- `pandas==2.0.3`
- `pillow==9.4.0`
- `pyarrow==11.0.0`
- `scipy==1.11.1`
- `seaborn==0.12.2`
- `streamlit==1.26.0`
- `xlsxwriter==3.1.1`

## Usage

Upon running the application, you will see a sidebar where you can select the Dapil (constituency) you want to simulate the election for.

In the main content area, you will find an editable table displaying the election data. You can double-click on the number of votes for each candidate to change the vote count. You can also click on the table header to sort the data.

After making changes to the vote counts, click the "Reset" button to revert to the original data.

The application will calculate and display the elected candidates based on the Sainte-Laguë method. The results will be sorted by the "Terpilih Di Ronde" column.