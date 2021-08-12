from os import pathsep
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
    st.header("Clustered requirements from the PDF-file System-Lastenheft Automotive System Cluster (ELC und ACC)")
    st.write("The chart below contains 2 dimensional representations of all requirements contained in the PDF-file ")


    language_model = st.selectbox('Which pre-trained Language Model should be used?',('Roberta (Ger & Eng)' , 'Mpnet Base Multilingual V2'))
    dimension_reduce = st.selectbox('Which Algorithm for dimension reduction should be used?',('TSNE', 'UMAP'))
    clustering_alg = st.selectbox('Which Clustering Algorithm should be used?',('K-Means++', 'HDBSCAN (min sample = None)', 'HDBSCAN (min sample = 1)', 'Agglomerative Clustering'))


  




    if language_model == 'Roberta (Ger & Eng)':

      if clustering_alg == 'K-Means++':
        path = pathlib.Path("assets/roberta/all_req_data.pkl")
      
      elif clustering_alg == 'HDBSCAN (min sample = None)':
        path = pathlib.Path("assets/roberta/all_req_data_umap_hdbscan_minsample_none.pkl")

      elif clustering_alg == 'HDBSCAN (min sample = 1)':
        path = pathlib.Path("assets/roberta/all_req_data_umap_hdbscan_minsample_1.pkl")

      elif clustering_alg == 'Agglomerative Clustering':
        path = pathlib.Path("assets/roberta/all_req_data_umap_agg_cluster.pkl")
    
    elif language_model == 'Mpnet Base Multilingual V2':
      if clustering_alg == 'K-Means++':
        path = pathlib.Path("assets/mpnet/all_req_data.pkl")
      
      elif clustering_alg == 'HDBSCAN (min sample = None)':
        path = pathlib.Path("assets/mpnet/all_req_data_umap_hdbscan_minsample_none.pkl")

      elif clustering_alg == 'HDBSCAN (min sample = 1)':
        path = pathlib.Path("assets/mpnet/all_req_data_umap_hdbscan_minsample_1.pkl")

      elif clustering_alg == 'Agglomerative Clustering':
        path = pathlib.Path("assets/mpnet/all_req_data_umap_agg_cluster.pkl")



    all_viz_data = pickler(filename=path , mode='unpickle')

    
    if clustering_alg == 'K-Means++':
      sil_score_list = []
      for k in range(4,50,2):
        cluster = all_viz_data[k]
        sil_score_list.append((k, cluster['silhoette Score'][0]))
      sil_best_score = max(sil_score_list,key=lambda item:item[1])


     
      st.write("The suggested K Value (By Silhuette Method) is K = " , sil_best_score[0], " with a Value of = ", sil_best_score[1])

      number_of_clusters = st.slider("number of clusters to display", min_value=4, max_value=48, step=2, value=10)
      source_df = all_viz_data[number_of_clusters]      
      source = source_df
      st.write("This Silhuette Score for ", number_of_clusters , " clusters is: ", source['silhoette Score'][0] )


    else:
      source = all_viz_data

    if dimension_reduce == 'TSNE':
      dim_x = 'tsne_dim_1'
      dim_y = 'tsne_dim_2'

    elif dimension_reduce == 'UMAP':
      dim_x = 'umap_dim_1'
      dim_y = 'umap_dim_2'

    chart = alt.Chart(source).mark_circle(size=60).encode(
        x=dim_x,
        y=dim_y,
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
    if dimension_reduce == 'TSNE':
        source = source.drop(columns=['umap_dim_1', 'umap_dim_2'])


    elif dimension_reduce == 'UMAP':
        source = source.drop(columns=['tsne_dim_1', 'tsne_dim_2'])



    cluster_col  = source["cluster_id"]
    cluster_max = cluster_col.max()    
    cluster_min = cluster_col.min()
    

    cluster_col_list = cluster_col.tolist()
    cluster_col_list = list(dict.fromkeys(cluster_col_list))
    cluster_col_list.sort()

    container = st.beta_container()
 
    
  
   # 
    selected_all = st.checkbox('Select all Clusters', value=True)




    if selected_all:
      selected_cluster_list = st.multiselect( 'Select Cluster you want to filter for',cluster_col_list,cluster_col_list)
      filtered_source = source
    else:
      selected_cluster_list = st.multiselect( 'Select Cluster you want to filter for',cluster_col_list)
      filtered_source = source[source['cluster_id'].isin(selected_cluster_list)]

    filtered_source_copy = filtered_source

    sort_by = st.selectbox( 'Sort by: ',('ID', 'Cluster'))

    if sort_by == 'ID':
      filtered_source = filtered_source_copy
    elif sort_by == 'Cluster':
      filtered_source = filtered_source_copy.sort_values(by=['cluster_id'])



    st.table(filtered_source.style.set_precision(2))

    
