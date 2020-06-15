import numpy as np
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_tensorflow_log(path_mi, path_nmi):

    # Loading too much data is slow...
    tf_size_guidance = {
        'compressedHistograms': 10,
        'images': 0,
        'scalars': 300,
        'histograms': 1
    }

    event_acc_mi = EventAccumulator(path_mi, tf_size_guidance)
    event_acc_mi.Reload()
    event_acc_nmi = EventAccumulator(path_nmi, tf_size_guidance)
    event_acc_nmi.Reload()

    kl_mi = event_acc_mi.Scalars('vae/vae_kl_categorical_loss')
    kl_nmi = event_acc_nmi.Scalars('vae/vae_kl_categorical_loss')

    steps = len(kl_mi)
    x = np.arange(steps)
    y = np.zeros([steps, 2])

    for i in range(steps):
        y[i, 0] = kl_mi[i][2] # value
        y[i, 1] = kl_nmi[i][2] # value

    plt.plot(x, y[:,0], label='MI maximization')
    plt.plot(x, y[:,1], label='Vanilla VAE')

    plt.grid(True, lw = 0.5, ls = '-')

    plt.xlabel("Training Iterations")
    plt.ylabel("KL divergence estimate")
    plt.title("KL divergence estimate comparison")
    plt.legend(loc='lover right', frameon=True)
    plt.show()
    plt.savefig('kl_comparison.png')


if __name__ == '__main__':
    log_file_nmi = "/home/andrew/projects/info_vaegan/logs_cat/mnistcat_vae04/events.out.tfevents.1557323451.breil-schmidhuber" 
    log_file_mi  = "/home/andrew/projects/info_vaegan/logs_cat/mnistcat_qvae64/events.out.tfevents.1558008643.breil-schmidhuber"
    plot_tensorflow_log(log_file_mi, log_file_nmi)
