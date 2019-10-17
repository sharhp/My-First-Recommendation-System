import numpy as np
from numpy import random as rand
from scipy import sparse as sps
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
import os
# DO NOT CHANGE THE NAME OF THIS METHOD OR ITS INPUT OUTPUT BEHAVtst_X_Xftst_X_Xftst_X_XfIOR

# INPUT CONVENTION
# X: n x d matrix in csr_matrix format containing d-dim (sparse) features for n test data points
# k: the number of recommendations to return for each test data point in ranked order

# OUTPUT CONVENTION
# The method must return an n x k numpy nd-array (not numpy matrix or scipy matrix) of labels with the i-th row 
# containing k labels which it thinks are most appropriate for the i-th test point. Labels must be returned in 
# ranked order i.e. the label yPred[i][0] must be considered most appropriate followed by yPred[i][1] and so on

# CAUTION: Make sure that you return (yPred below) an n x k numpy (nd) array and not a numpy/scipy/sparse matrix
# The returned matrix will always be a dense matrix and it terribly slows things down to store it in csr format
# The evaluation code may misbehave and give unexpected results if an nd-array is not returned

def getReco( X, k ):
    # Find out how many data points we have
    n = X.shape[0]
    L = 3400
    # Load and unpack the dummy model
    # The dummy model simply stores the labels in decreasing order of their popularity
    in_path=""
    out_path="sandbox/data/Assn2/"
    goto_dir=""
    lol="shallow/"
    model_dir = "sandbox/results/Assn2/"
    print("Test Data Dump Started")
    dump_food(X,in_path,out_path)
    print("Test Data Dump Completed")
    print(" ")
    print("Prediction Sarted.")
    os.system("bash shallow/sample_run.sh")

    filename = model_dir + "score_mat"

    Xp, _ = load_svmlight_file( "%s.txt" %filename, multilabel = True, n_features = L, offset = 1 )

    yPred = np.zeros( (n, k), dtype=int )
    for ind, user in enumerate(Xp):
        d = user.data
        i = user.indices
        xf = np.vstack( (i, d) ).T
        xf = xf[xf[:,1].argsort()[::-1]]
        # print("Sorted array: ", xf)
        for j in range(0,k):
            yPred[ind][j]=xf[j][0]

    print(yPred)
    print(yPred.shape)

    '''
    # Let us predict a random subset of the 2k most popular labels no matter what the test point
    shortList = model[0:2*k]
    # Make sure we are returning a numpy nd-array and not a numpy matrix or a scipy sparse matrix
    yPred = np.zeros( (n, k) )
    for i in range( n ):
        yPred[i,:] = rand.permutation( shortList )[0:k]
    '''
    return yPred


def dump_food( matrix_test, in_path, out_path):
    (n, d) = matrix_test.shape
    dummy = sps.csr_matrix( (n, 1) )
    dump_svmlight_file( matrix_test, dummy, "test_data.X", multilabel = True, zero_based = True, comment = "%d %d" % (n, d) )   

    test_ws=open(in_path+"test_data.X","r")
    test_is=open(out_path+"tst_X_Xf.txt","w")

    for i in range(0,3):
        test_ws.readline(); 

    lines=test_ws.readlines()

    lines[0]=lines[0][2:]
    test_is.write(lines[0])
    for i in range(1,len(lines)):
        lines[i]=lines[i][1:]
        test_is.write(lines[i])

    test_is.close()
