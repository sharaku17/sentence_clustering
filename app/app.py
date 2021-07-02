import pathlib
import streamlit as st
import altair as alt
import pickle
import pandas
import numpy



def pickler(obj=None, filename: str= None, mode: str = 'pickle'):
  """
  pickles the file to filename, or 
  unpickles and returns the file

  (to save the result of long running calculations)

  Parameters
  ----------
  obj : 
    the object to pickle
  filename : str
    file to pickle to
  mode:
    one of 'pickle' or 'depickle'
  """
  unpickled = None
  
  if mode == 'pickle':
    pickle.dump(obj, open(filename,'wb'))

  elif mode == 'unpickle':
    unpickled = pickle.load(open(filename,'rb'))
  
  return unpickled


if __name__ == "__main__":
    all_viz_data = pickler(filename=pathlib.Path("assets/all_req_data.pkl"), mode='unpickle')

    st.header("Clustered requirements from the PDF-file System-Lastenheft Automotive System Cluster (ELC und ACC)")
    st.write("The chart below contains 2 dimensional representations of all requirements contained in the PDF-file ")


    number_of_clusters = st.slider("number of clusters to display", min_value=4, max_value=28, step=2, value=10)
    source_df = all_viz_data[number_of_clusters]
    
    source = source_df
  

    chart = alt.Chart(source).mark_circle(size=60).encode(
        x='tsne_dim_1',
        y='tsne_dim_2',
        color=alt.Color('cluster_id', scale=alt.Scale(scheme='category20')) ,
        tooltip=['cluster_id','requirement']
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=700,
        height=500,
    ).interactive()


    st.altair_chart(chart)
