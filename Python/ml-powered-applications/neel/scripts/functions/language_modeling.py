def nlp_red(_nlp, list_vectors, name):

    # function to generate word embeddings for a given non-nan list
    import pandas as pd
    
    # Error handling
    if (type(list_vectors) != type([])) or (type(name) != type("")):
        raise Exception('TypeError: Incompatible argument type supplied.')

    # initializations
    embeddings = {}
    _data = {}

    # convert list to pandas dataframe
    _data[name] = list_vectors

    _df = pd.DataFrame(_data)
    _vectors = _df.loc[:, name]
    
    # Produce embdeddings
    embeddings[name] = _vectors.apply(lambda x: _nlp(x).vector)

    return embeddings

def umap_red(vec_emb):

    # function to perform a umap dimension reduction on a list of vector embeddings
    import umap

    _reducer = umap.UMAP()
    _umap = _reducer.fit_transform(vec_emb)
    return {
        "_reducer": _reducer, 
        "_umap_vectors"   : _umap
        }

def get_kmeans_clusters(vec_emb_list, n_clusters, _params, random_state=10):
    
    # function to return kmeans clusteral predictions from a list of vectors
    from sklearn.cluster import KMeans
    from joblib import load

    # print("optimal_clusters: {}".format(n_clusters))

    # load a pretrained model and assign each vector to a cluster
    _clus = load(_params['pretrained_models']['kmeans']['model_location']) 
    _cluster_labels = _clus.fit_predict(vec_emb_list)

    return {
        "_kmeans": _clus,
        "_cluster_predictions": _cluster_labels
    }

def optimize_kmeans_cluster(vec_emb_list, random_state=10):

    # function to provide the number of clusters on a kmeans model using the silhouette_score
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed clusters

    from sklearn.metrics import silhouette_score
    from sklearn.cluster import KMeans
    import pandas as pd

    # initialization
    range_n_clusters = [2, 3, 4, 5, 6]
    _clusters = []
    _silscores = []

    
    for n_clusters in range_n_clusters:
        
        # perform clustering operations
        _clus = KMeans(n_clusters=n_clusters, random_state=random_state)
        _clus_predictions = _clus.fit_predict(vec_emb_list)
        
        # determine silhouette_avg scores
        silhouette_avg = silhouette_score(vec_emb_list, _clus_predictions, metric='cosine')
        
        # save data
        _clusters.append(n_clusters) 
        _silscores.append(silhouette_avg)
        
    # evaluate performance and select best performing cluster
    _df = pd.DataFrame(
        data={
            "clusters": _clusters,
            "silhoutte_scores": _silscores
        }
    )
    
    return str(_df.sort_values("silhoutte_scores", ascending=False).loc[0, "clusters"])