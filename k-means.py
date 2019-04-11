import numpy as np
import random
import scipy
from scipy import spatial
import argparse

def gen_dummy_data(N_dim, N_points):
    '''
    Generate dummy data - N_points number of points of N_dim dimension.
    Points are sampled from uniform distribution U(a,b) = U(0,50) and saved to a text file.

    Arguments:
        N_dim: Dimensionality of coordinate space.
        N_points: Number of points to be returned.
    '''

    arr = np.random.uniform(0,50,(N_points,N_dim))
    np.savetxt('dummy_data.txt',arr)

def distance(Xa, Xb):
    '''
    Returns Euclidean distance between each pair of two collection/arrays of inputs.

    Arguments:
        Xa - One set of inputs. Ex. Array of data points in the dataset.
        Xb - Second set of inputs. Ex. Array of centroids. 
    
    Returns:
        A distance matrix of shape (M_a by M_b) returned. 
        For each i-th and j-th point in Xa and Xb, respectively, the metric dist(u=Xa[i], v=Xb[j]) is computed
        and stored in the th entry.
    '''
    
    dist_array = scipy.spatial.distance.cdist(Xa, Xb, metric='euclidean')
    return dist_array

def k_means(gen_data):
    '''
    Finds the clusters and their centroids given input file containing data points in N-th dimensional space 
    and specified number of clusters.

    Arguments:
        gen_data - Helps the script decide if user wants to evaluate on dummy data that can be generated by function gen_dummy_data
        or enter their own dataset text file. 
    '''
    
    #get input file path
    if (gen_data == 'Y' or gen_data == 'y'):
        n_dim = int(input('Enter dimension of data points: '))
        n_points = int(input('Enter number of points that you want to generate: '))
        gen_dummy_data(n_dim,n_points)
        data_file_path = 'dummy_data.txt'
    
    elif (gen_data == 'N' or gen_data == 'n'):
        data_file_path = input('Enter path of the dataset text file: ')
    
    else:
        print('Enter a valid choice next time - Y/y or N/n')
        exit()

    data_arr = np.array(np.loadtxt(data_file_path))#load text file as numpy array
    k = int(input('Enter the number of clusters: ')) #take number of clusters as input from user
    dim = data_arr.shape[-1] #find the dimensionality of given points
    
    indices = np.random.choice(data_arr.shape[0], k, replace=False)
    centroids_curr = np.array([data_arr[i] for i in indices]) #randomly select any data points from the input file as current centroids
    centroids_old = np.zeros(centroids_curr.shape)
    error = distance(centroids_curr, centroids_old)
    cumulative_error = np.sum([error[i][i] for i in range(k)])

    #Iterate until the error between centroids_old and centroids_curr converges
    while not(cumulative_error == 0):
        #assign cluster
        distance_array = distance(data_arr, centroids_curr)
        cluster_array = np.argmin(distance_array, axis=1)
 
        #find new centroid
        centroids_old = centroids_curr
        for i in range(k):
            cluster_i = np.array([data_arr[j] for j in range(len(cluster_array)) if cluster_array[j] == i])
            centroid_i = np.mean(cluster_i, axis=0)
            if i == 0:
                temp_centroids_curr = np.array([centroid_i])
            else:
                temp_centroids_curr = np.append(temp_centroids_curr, [centroid_i], axis=0)
        centroids_curr = temp_centroids_curr
        
        #find error   
        error = distance(centroids_curr, centroids_old)
        cumulative_error = np.sum([error[i][i] for i in range(k)])

    #save centroids
    np.savetxt('output.txt',centroids_curr,fmt='%.5f')

    print("Centroids have been saved in \"output.txt\" !")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('generate_data', help='Enter Y/y if you want to first generate dummy data. To use any other dataset, enter N/n')
    args = parser.parse_args()

    k_means(args.generate_data)