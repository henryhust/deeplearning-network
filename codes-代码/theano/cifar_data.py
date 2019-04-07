import numpy as NP
import cPickle
# please put the cifar data in the folder cifar/
def load_cifar():
    ret = {}
    ret['train_data'] = []
    ret['train_label'] = []
    ret['test_data'] = []
    ret['test_label'] = []
    for i in xrange(1,6):
        f = open('cifar/data_batch_'+str(i), 'rb')
        t = cPickle.load(f)
        ret['train_data'].append(t['data'])
        ret['train_label'].append(t['labels'])
        f.close()

    ret['train_data'] = NP.concatenate(ret['train_data'], axis=0)
    ret['train_label'] = NP.concatenate(ret['train_label'], axis=0)
    f = open('cifar/test_batch', 'rb')
    t = cPickle.load(f)
    ret['test_data'] = 1.0*NP.asarray(t['data'])/255.0
    ret['test_label'] = NP.asarray(t['labels'])
    ret['valid_data'] = 1.0*NP.asarray(ret['train_data'][-1000:])/255.0
    ret['valid_label'] = NP.asarray(ret['train_label'][-1000:])
    ret['train_data'] = 1.0*NP.asarray(ret['train_data'][:-1000])/255.0
    ret['train_label'] = NP.asarray(ret['train_label'][:-1000])
    f.close()

    return ret
