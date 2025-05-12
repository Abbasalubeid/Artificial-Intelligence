# Supervised Deep Learning

**Answers to the questions from lab 3**

1.  We calculate the gradient of the loss (which is the sum of squared
    errors) with respect to the *parameters* (the model’s intercept and
    slope) using `tape.gradient(loss, parameters)` from TensorFlow’s
    `GradientTape`. This helps update the parameters to reduce the loss.

2.  To find the total number of parameters in the first `Dense` layer,
    we look at the following:

    -   The input to the layer is a flattened vector from a 28 × 28
        image, which gives us 28 × 28 = 784 input features.

    -   The first `Dense` layer has 128 neurons, and each neuron has a
        weight for each input feature, plus one bias term.

    So, for each neuron, the number of parameters is:
    Parameters per neuron = 784 (weights) + 1 (bias) = 785

    Since there are 128 neurons in the first dense layer, the total
    number of parameters is:
    Total parameters = 785 × 128 = 100480

3.  In this experiment, we evaluated how different mini-batch sizes
    affect the training time and accuracy of a neural network. We
    trained the network using batch sizes of 1, 10, 100, 1000, and
    60000, recording the training time and accuracy for each run. After
    each training, the parameters were reset to ensure consistency
    across batch sizes. The training time and accuracy for each batch
    size were saved and plotted to visualize the trade-offs.

    ![Training Results](https://github.com/Abbasalubeid/Artificial-Intelligence/raw/main/lab3-deep-learning/training_time_accuracy_vs_batch_size.png)

    The results showed that smaller batch sizes (1, 10, and 100) took
    longer to train but generally yielded higher accuracy while larger
    batch sizes (1000 and 60000) trained faster but resulted in lower
    accuracy. In this case, a batch size of 10 produced the highest
    accuracy (82.71%) with a reasonable training time of 20 seconds
    which shows that for this dataset and model, a batch size of 10
    provides a good balance between accuracy and training efficiency.
