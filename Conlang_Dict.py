import streamlit as st
import pandas as pd
from glob import glob
from pathlib import Path

def df_helper(df):
    st.dataframe(
        df,
        column_config={
            'Conlang': st.column_config.Column(
                'Conlang Word:',
                width='medium',
                required=True
            ),
            'English': st.column_config.Column(
                'English Word:',
                width='large',
                required=True
            )
        },
        hide_index=True
    )

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

if __name__ == "__main__":
    st.set_page_config(
        page_icon='random',
        page_title='Conlang Dict!',
        layout='wide'
    )
    st.title('Conlang Dictionary')
    tab1, tab2 = st.tabs(['Vocab', 'Grammar Rules'])
    diction = pd.read_json('Diction.json')
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col2:
            search = st.text_input(label="Search")
            with st.form('New Word', clear_on_submit=True):
                st.write('Add A New Word:')
                eng = st.text_input(label='English Word/s:')
                con = st.text_input(label='Conlang Word:')
                submitted = st.form_submit_button('Submit')
            if submitted:
                if eng not in diction['English'].unique() and con not in diction['Conlang'].unique():
                    newLine = {'English': eng, 'Conlang': con}
                    diction = pd.read_json('Diction.json')
                    lengt = diction.shape[0]
                    diction = pd.concat([diction, pd.DataFrame(newLine, index=[str(lengt + 1)])])
                    diction.to_json('Diction.json')
                elif eng in diction['English'].unique() and con not in diction['Conlang'].unique():
                    st.error('English word already exists!')
                elif eng not in diction['English'].unique() and con in diction['Conlang'].unique():
                    st.error('Conlang word already exists!')
                else:
                    st.error('Entry already exists!')
            st.download_button('Download Full Dictionary', diction.to_json(), file_name='Diction.json')
        with col1:
            if search != None:
                diction = diction[diction['English'].str.contains(search) | diction['Conlang'].str.contains(search)]
                df_helper(diction)
            else:
                df_helper(diction)
    with tab2:
        for f in glob('./Conlang Notes/*'):
            st.markdown(read_markdown_file(f), unsafe_allow_html=True)