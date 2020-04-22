import numpy  as np
import pandas as pd

class Score:
    '''
    This is a class to score and evaluate algorithms and predictions.
    
    Public methods:
        correct:  returns the number of correct predictions,
        accuracy: returns the accuracy of the predictions,
        error:    returns the difference between the true values and the predictions
        error2:   returns the squared difference between the true values and the predictions
    '''
    
    def __init__(self,
                 y_true,
                 y_pred,
                 rounding=None
                ):
        '''
        Constructor of the class.
        
        Required arguments:
            y_true:   the true values,
            y_pred:   the predicted values.
        
        Optional arguments:
            rounding: the function used to approximate the predictions.
        '''
        
        self.rounding = rounding
        self.y_true   = np.array(y_true)
        
        # process the predictions
        self.y_pred   = np.array(self.rounding(y_pred)) if self.rounding is not None else np.array(y_pred)
        
    def correct(self):
        '''
        Compute the number of correct predictions.
        
        Returns:
            the number of correct predictions.
        '''
        
        return np.sum(self.y_true == self.y_pred)
    
    def accuracy(self):
        '''
        Compute the accuracy of the predictions.
        
        Returns:
            the accuracy.
        '''
        
        return self.correct() / np.shape(self.y_true)[0]
    
    def error(self):
        '''
        Compute the difference between the true value and the predictions.
        
        Returns:
            y_true - y_pred.
        '''
        
        return self.y_true - self.y_pred
    
    def error2(self):
        '''
        Compute the squared difference of the errors.
        
        Returns:
            (y_true - y_pred)**2
        '''
        return self.error()**2

class ViewCV:
    '''
    This class retrieves and manipulates the cross-validation results of a Scikit estimator.
    
    Public methods:
        results:         returns a Pandas dataframe with the complete cross-validation results,
        best_results:    returns a Pandas dataframe with the best cross-validation results,
        test_mean:       returns the mean value of the test score,
        test_std:        returns the standard deviation of the test score.
        
    Attributes:
        best_parameters: the best parameters of the estimator.
    '''
    
    def __init__(self,
                 estimator
                ):
        '''
        Constructor of the class.
        
        Required arguments:
            estimator: the Scikit estimator.
        '''
        
        self.estimator       = estimator
        self.best_parameters = self.estimator.best_params_
        
    def results(self):
        '''
        Retrieves the cross-validation results of the estimator.
        
        Returns:
            a Pandas dataframe with the cross-validation results.
        '''
        
        return pd.DataFrame(self.estimator.cv_results_)
    
    def best_results(self):
        '''
        Retrieves the cross-validation results of the estimator.
        
        Returns:
            a Pandas dataframe with the cross-validation results.
        '''
        
        df = self.results()
        
        return df.loc[df['params'] == self.best_parameters]
    
    def test_mean(self):
        '''
        Returns the mean of the test score.
        
        Return:
            the mean of the test score.
        '''
        
        return self.best_results.loc[:, 'mean_test_score'].values[0]
    
    def test_std(self):
        '''
        Returns the standard deviation of the test score.
        
        Return:
            the mean of the test score.
        '''
        
        return self.best_results.loc[:, 'std_test_score'].values[0]
    
def accuracy(y_true, y_pred, rounding=None):
    '''
    Compute the accuracy (functional interface).
    
    Required arguments:
        y_true: the true values,
        y_pred: the predictions.
        
    Optional arguments:
        rounding: the function used to approximate the predictions.
    '''
    
    return Score(y_true=y_true,
                 y_pred=y_pred,
                 rounding=rounding
                ).accuracy()