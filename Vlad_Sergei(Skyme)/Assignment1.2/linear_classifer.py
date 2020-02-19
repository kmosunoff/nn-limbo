import numpy as np


def softmax(predictions):
    '''
    Computes probabilities from scores

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output

    Returns:
      probs, np array of the same shape as predictions - 
        probability for every class, 0..1
    '''
    # TODO implement softmax
    # Your final implementation shouldn't have any loops
    p_dim = predictions.ndim
    predictions = np.array(predictions)
    if predictions.ndim == 1:
      predictions = predictions[np.newaxis, :]
    predictions -= np.max(predictions, axis=1)[:, np.newaxis]
    #probs = np.zeros_like(predictions)
    
    probs = np.exp(predictions) / np.sum(np.exp(predictions), axis=1)[:, np.newaxis]

    if p_dim == 1:
      return probs[0]
    else:
      return probs
    #raise Exception("Not implemented!")


def cross_entropy_loss(probs, target_index):
    '''
    Computes cross-entropy loss

    Arguments:
      probs, np array, shape is either (N) or (batch_size, N) -
        probabilities for every class
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss: single value
    '''
    # TODO implement cross-entropy
    # Your final implementation shouldn't have any loops
    if (type(target_index) == int):
      loss = - np.log(probs)[target_index]
    else:
      loss = - np.mean(np.log(probs[range(len(target_index)), target_index]))
    
    return loss
    #raise Exception("Not implemented!")


def softmax_with_cross_entropy(predictions, target_index):
    '''
    Computes softmax and cross-entropy loss for model predictions,
    including the gradient

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss, single value - cross-entropy loss
      dprediction, np array same shape as predictions - gradient of predictions by loss value
    '''
    # TODO implement softmax with cross-entropy
    # Your final implementation shouldn't have any loops
    #if type(target_index) == type(np.array([])):
    #  t = target_index.copy()
    #else:
    #  t = np.array([target_index])
    #p = predictions.copy()
    

    #s_m = softmax(softmax(p))
    #s_m = soft_max.reshape(-1, 1)
    #dprediction = np.diagflat(s_m) - np.dot(s_m, s_m.T)
    #loss = cross_entropy_loss(p, t)

    #return loss, dprediction
    zeros = np.zeros_like(predictions)
    if predictions.ndim > 1:  # batch case
      sumlog = np.log(np.exp(predictions).sum(axis=1)) 
      x_i = np.array([predictions[i, target_index[i]] for i in range(target_index.shape[0])])
      for i in range(target_index.shape[0]):
        zeros[i, target_index[i]] = 1
    else:
      sumlog = np.log(np.exp(predictions).sum()) 
      x_i = predictions[target_index]
      zeros[target_index] = 1

    # print(sumlog.shape, x_i.shape)
    loss = sumlog - x_i.T
    grad = softmax(predictions)
    grad -= zeros

    if predictions.ndim > 1:
      grad /= predictions.shape[0]
    return loss.mean(), grad
    #raise Exception("Not implemented!")


def l2_regularization(W, reg_strength):
    '''
    Computes L2 regularization loss on weights and its gradient

    Arguments:
      W, np array - weights
      reg_strength - float value

    Returns:
      loss, single value - l2 regularization loss
      gradient, np.array same shape as W - gradient of weight by l2 loss
    '''

    # TODO: implement l2 regularization and gradient
    # Your final implementation shouldn't have any loops
    #raise Exception("Not implemented!")
    loss = reg_strength*(W**2).sum()
    grad = 2 * reg_strength * W

    return loss, grad
    

def linear_softmax(X, W, target_index):
    '''
    Performs linear classification and returns loss and gradient over W

    Arguments:
      X, np array, shape (num_batch, num_features) - batch of images
      W, np array, shape (num_features, classes) - weights
      target_index, np array, shape (num_batch) - index of target classes

    Returns:
      loss, single value - cross-entropy loss
      gradient, np.array same shape as W - gradient of weight by loss

    '''
    predictions = np.dot(X, W)

    # TODO implement prediction and gradient over W
    # Your final implementation shouldn't have any loops
    #raise Exception("Not implemented!")
    loss, dW = softmax_with_cross_entropy(predictions, target_index)
    dW = np.dot(X.T, dW)
    
    return loss, dW


class LinearSoftmaxClassifier():
    def __init__(self):
        self.W = None

    def fit(self, X, y, batch_size=100, learning_rate=1e-7, reg=1e-5,
            epochs=1):
        '''
        Trains linear classifier
        
        Arguments:
          X, np array (num_samples, num_features) - training data
          y, np array of int (num_samples) - labels
          batch_size, int - batch size to use
          learning_rate, float - learning rate for gradient descent
          reg, float - L2 regularization strength
          epochs, int - number of epochs
        '''

        num_train = X.shape[0]
        num_features = X.shape[1]
        num_classes = np.max(y)+1
        if self.W is None:
            self.W = 0.001 * np.random.randn(num_features, num_classes)

        loss_history = []
        loss = 0
        for epoch in range(epochs):
            shuffled_indices = np.arange(num_train)
            np.random.shuffle(shuffled_indices)
            sections = np.arange(batch_size, num_train, batch_size)
            batches_indices = np.array_split(shuffled_indices, sections)

            # TODO implement generating batches from indices
            # Compute loss and gradients
            # Apply gradient to weights using learning rate
            # Don't forget to add both cross-entropy loss
            # and regularization!
            #raise Exception("Not implemented!")
            for batch_index in batches_indices:
              loss, dW = linear_softmax(X[batch_index], self.W, y[batch_index])
              reg_loss, dW_dR = l2_regularization(self.W, reg)
              self.W -= learning_rate * (dW+dW_dR)
              loss_history.append(loss)

            # end
            print("Epoch %i, loss: %f" % (epoch, loss))

        return loss_history

    def predict(self, X):
        '''
        Produces classifier predictions on the set
       
        Arguments:
          X, np array (test_samples, num_features)

        Returns:
          y_pred, np.array of int (test_samples)
        '''
        y_pred = np.zeros(X.shape[0], dtype=np.int)
        predictions = np.dot(X, self.W)
        # TODO Implement class prediction
        # Your final implementation shouldn't have any loops
        #raise Exception("Not implemented!")

        y_pred = np.argmax(predictions, axis=1)
        return y_pred
        #return y_pred

