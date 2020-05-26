import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

# remove the outliers from a Pandas dataset
class RemoveOutliers(BaseEstimator, TransformerMixin):
    '''
    Remove outlying data given a dataset and a dictionary containing the intervals for each class.
    
    E.g.: if the two classes are 'h11' and 'h21', the dictionary will be: {'h11': [1, 16], 'h21': [1, 86]}.
    
    Public methods:
        fit:           unused method,
        transform:     remove data outside the given interval,
        fit_transform: equivalent to transform(fit(...)).
    '''

    def __init__(self, filter_dict=None):
        '''
        Constructor of the class.
        
        Optional arguments:
            filter_dict: the intervals to retain in the data.
        '''
        
        self.filter_dict = filter_dict

    def fit(self, X, y=None):
        '''
        Unused method.
        '''

        return self

    def transform(self, X):
        '''
        Transform the input by deleting data outside the interval.
        
        Required arguments:
            X: the dataset.
            
        Returns:
            the transformed dataset.
        '''

        x = X.copy() #-------------------------------------------- avoid overwriting

        if self.filter_dict is not None:
            for key in self.filter_dict:
                x = x.loc[x[key] >= self.filter_dict[key][0]] #--- keep only if > then smallest value
                x = x.loc[x[key] <= self.filter_dict[key][1]] #--- keep only if < then largest value

        return x

# extract the tensors from a Pandas dataset
class ExtractTensor(BaseEstimator, TransformerMixin):
    '''
    Extract a dense tensor from sparse input from a given dataset.
    
    Public methods:
        fit:           unused method,
        transform:     extract dense tensor,
        fit_transform: equivalent to transform(fit(...)),
        get_shape:     compute the shape of the tensor.
    '''

    def __init__(self, flatten=False, shape=None):
        '''
        Constructor of the class.
        
        Optional arguments:
            flatten: whether to flatten the output or keep the current shape,
            shape:   force the computation with a given shape.
        '''

        self.flatten = flatten
        self.shape   = shape

    def fit(self, X, y=None):
        '''
        Unused method.
        '''

        return self

    def transform(self, X):
        '''
        Compute the dense equivalent of the sparse input.
        
        Required arguments:
            X: the dataset
            
        Returns:
            the transformed input.
        '''

        x = X.copy() #----------------------------------------------------- avoid overwriting
        if self.shape is None:
            self.shape = x.apply(np.shape).max() #------------------------- get the shape of the tensor

        if len(self.shape) > 0: #------------------------------------------ apply padding to vectors and tensors
            offset = lambda s : [ (0, self.shape[i] - np.shape(s)[i]) for i in range(len(self.shape)) ]
            x      = x.apply(lambda s: np.pad(s, offset(s), mode='constant'))

        if self.flatten and len(self.shape) > 0:
            return list(np.stack(x.apply(np.ndarray.flatten).values))
        else:
            return list(np.stack(x.values))

    def get_shape(self):
        '''
        Compute the shape of the tensor.
        
        Returns:
            the shape of the tensor.
        '''
        
        return self.shape
