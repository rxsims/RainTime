import numpy as np

def normalize_vec(vec):
    # Find length of vectors.  If length = 0, set to 1 to return the original vector
    norms = get_vector_norm(vec)
    norms_rem0 = np.where(norms==0,1,norms)
    
    # If function calls for normalizing a single vector, do not broadcast norms array
    if type(norms) == np.float64:
        return vec / norms_rem0
    
    return vec / norms_rem0[:,np.newaxis]


def get_vector_norm(vec):
    return np.linalg.norm(vec, axis=-1)


def directional_vector(start, end):
    vec = end - start
    vec_n = normalize_vec(vec)
    return (vec, vec_n)


def angle_between_vectors(vec1, vec2):
    v1_norm = get_vector_norm(vec1)
    v2_norm = get_vector_norm(vec2)
    prod_norm = v1_norm*v2_norm
    prod_norm_rem0 = np.where(prod_norm==0, np.nan, prod_norm)
    
    cos_val = np.sum(vec1*vec2, axis=1)/prod_norm_rem0
    sin_val = (vec1[...,0]*vec2[...,1]-vec1[...,1]*vec2[...,0])/prod_norm_rem0
    
    return list(zip(cos_val, sin_val))
