import numpy as NP
import theano
import theano.tensor as T
import theano.tensor.nnet as NN
from cifar_data import *
from wrapper import * # a simple tool for theano, get it from my github TheanoWrapper

batch_size= 32
var_lr = theano.shared(NP.asarray(1e-2).astype(theano.config.floatX))
drop1 = Dropout(shape=(batch_size, 32, 16, 16), prob=0.25)
drop2 = Dropout(shape=(batch_size, 64, 8, 8), prob=0.25)
drop3 = Dropout(shape=(batch_size, 512), prob=0.5)
img_in = T.tensor4()
label_in = T.ivector()

def get_expression(model, train, img_in, label_in):
    conv1 = relu(model.conv(img_in, name='conv1', shape=(32, 3, 3, 3, 1, 1)))
    conv2 = relu(model.conv(conv1, name='conv2', shape=(32, 32, 3, 3, 1, 1)))
    pool1 = model.pooling(conv2, name='pool1', shape=(2,2))
    if train:
        pool1 = drop1.drop(pool1)

    conv3 = relu(model.conv(pool1, name='conv3', shape=(64, 32, 3, 3, 1, 1)))
    conv4 = relu(model.conv(conv3, name='conv4', shape=(64, 64, 3, 3, 1, 1)))
    pool2 = model.pooling(conv4, name='pool2', shape=(2,2))
    if train:
        pool2 = drop2.drop(pool2)

    pool2 = pool2.reshape((batch_size, -1))
    fc1 = relu(model.fc(pool2, name='fc1', shape=(4096, 512)))
    if train:
        fc1 = drop3.drop(fc1)
    fc2 = softmax(model.fc(fc1, name='fc2', shape=(512, 10)))

    loss = T.mean(NN.categorical_crossentropy(fc2, label_in))

    if train:
        grads = rmsprop(loss, model.get_params(), lr=var_lr, epsilon=var_lr**2, return_norm=False)
        return loss, fc2, grads
    else:
        return loss, fc2

print 'Compile'
model = Model()
l, o, g = get_expression(model, True, img_in, label_in)

train_func = theano.function([img_in, label_in], [l,o], updates=g, allow_input_downcast=True)

l, o = get_expression(model, False, img_in, label_in)
test_func = theano.function([img_in, label_in], [l,o], allow_input_downcast=True)

print 'Training'
cifar_data = load_cifar()
last_acc = 2e10
for ep in xrange(200):
    avg_loss = []
    for i in xrange(len(cifar_data['train_data'])/batch_size):
        loss, net_out = train_func(cifar_data['train_data'][i*batch_size:(i+1)*batch_size].reshape((batch_size, 3, 32, 32)), cifar_data['train_label'][i*batch_size:(i+1)*batch_size])
        print 'Epoch = {0:}, Batch = {1:}, Loss = {2:}'.format(ep, i, loss)
        avg_loss.append(loss)

    
    avg_loss = []
    acc = []
    for i in xrange(len(cifar_data['test_data'])/batch_size):
        loss, net_out = test_func(cifar_data['test_data'][i*batch_size:(i+1)*batch_size].reshape((batch_size, 3, 32, 32)), cifar_data['test_label'][i*batch_size:(i+1)*batch_size])
        avg_loss.append(loss)
        acc.append(cifar_data['test_label'][i*batch_size:(i+1)*batch_size]==NP.argmax(net_out, axis=1))

    if NP.mean(acc)>last_acc:
        var_lr.set_value((var_lr.get_value()*0.8).astype('float32'))
    last_acc = NP.mean(acc)
    print 'Epoch = {0:}, Test AVG Loss = {1:.4f}, ACC = {2:.4f}'.format(ep, NP.mean(avg_loss), NP.mean(acc))
    model.save('cifar_save_'+str(ep))

