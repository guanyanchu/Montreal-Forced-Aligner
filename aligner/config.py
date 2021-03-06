import os

TEMP_DIR = os.path.expanduser('~/Documents/MFA')


def make_safe(value):
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


class MonophoneConfig(object):
    '''
    Configuration class for monophone training

    Scale options defaults to::

        ['--transition-scale=1.0', '--acoustic-scale=0.1', '--self-loop-scale=0.1']

    If ``align_often`` is True in the keyword arguments, ``realign_iters`` will be::

        [1, 5, 10, 15, 20, 25, 30, 35, 38]

    Otherwise, ``realign_iters`` will be::

        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 23, 26, 29, 32, 35, 38]

    Attributes
    ----------
    num_iters : int
        Number of training iterations to perform, defaults to 40
    scale_opts : list
        Options for specifying scaling in alignment
    beam : int
        Default beam width for alignment, defaults = 10
    retry_beam : int
        Beam width to fall back on if no alignment is produced, defaults to 40
    max_iter_inc : int
        Last iter to increase #Gauss on, defaults to 30
    totgauss : int
        Total number of gaussians, defaults to 1000
    boost_silence : float
        Factor by which to boost silence likelihoods in alignment, defaults to 1.0
    realign_iters : list
        List of iterations to perform alignment
    stage : int
        Not used
    power : float
        Exponent for number of gaussians according to occurrence counts, defaults to 0.25
    do_fmllr : bool
        Specifies whether to do speaker adaptation, defaults to False
    do_lda_mllt : bool
        Spacifies whether to do LDA + MLLT transformation, default to True
    '''

    def __init__(self, **kwargs):
        self.num_iters = 40

        self.scale_opts = ['--transition-scale=1.0',
                           '--acoustic-scale=0.1',
                           '--self-loop-scale=0.1']
        self.beam = 10
        self.retry_beam = 40
        self.max_gauss_count = 1000
        self.boost_silence = 1.0
        if kwargs.get('align_often', False):
            self.realign_iters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14,
                                  16, 18, 20, 23, 26, 29, 32, 35, 38]
        else:
            self.realign_iters = [1, 5, 10, 15, 20, 25, 30, 35, 38]
        self.stage = -4
        self.power = 0.25

        self.do_fmllr = False
        self.do_lda_mllt = False

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def max_iter_inc(self):
        return self.num_iters - 10

    @property
    def inc_gauss_count(self):
        return int((self.max_gauss_count - self.initial_gauss_count) / self.max_iter_inc)


class TriphoneConfig(MonophoneConfig):
    '''
    Configuration class for triphone training

    Scale options defaults to::

        ['--transition-scale=1.0', '--acoustic-scale=0.1', '--self-loop-scale=0.1']

    If ``align_often`` is True in the keyword arguments, ``realign_iters`` will be::

        [1, 5, 10, 15, 20, 25, 30, 35, 38]

    Otherwise, ``realign_iters`` will be::

        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 23, 26, 29, 32, 35, 38]

    Attributes
    ----------
    num_iters : int
        Number of training iterations to perform, defaults to 35
    scale_opts : list
        Options for specifying scaling in alignment
    beam : int
        Default beam width for alignment, defaults = 10
    retry_beam : int
        Beam width to fall back on if no alignment is produced, defaults to 40
    max_iter_inc : int
        Last iter to increase #Gauss on, defaults to 30
    totgauss : int
        Total number of gaussians, defaults to 1000
    boost_silence : float
        Factor by which to boost silence likelihoods in alignment, defaults to 1.0
    realign_iters : list
        List of iterations to perform alignment
    stage : int
        Not used
    power : float
        Exponent for number of gaussians according to occurrence counts, defaults to 0.25
    do_fmllr : bool
        Specifies whether to do speaker adaptation, defaults to False
    do_lda_mllt : bool
        Spacifies whether to do LDA + MLLT transformation, default to False
    num_states : int
        Number of states in the decision tree, defaults to 3100
    num_gauss : int
        Number of gaussians in the decision tree, defaults to 50000
    cluster_threshold : int
        For build-tree control final bottom-up clustering of leaves, defaults to 100
    '''

    def __init__(self, **kwargs):
        defaults = {'num_iters': 35,
                    'initial_gauss_count': 3100,
                    'max_gauss_count': 50000,
                    'cluster_threshold': 100,
                    'do_lda_mllt': False}
        defaults.update(kwargs)
        super(TriphoneConfig, self).__init__(**defaults)


class TriphoneFmllrConfig(TriphoneConfig):
    '''
    Configuration class for speaker-adapted triphone training

    Scale options defaults to::

        ['--transition-scale=1.0', '--acoustic-scale=0.1', '--self-loop-scale=0.1']

    If ``align_often`` is True in the keyword arguments, ``realign_iters`` will be::

        [1, 5, 10, 15, 20, 25, 30, 35, 38]

    Otherwise, ``realign_iters`` will be::

        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 23, 26, 29, 32, 35, 38]

    ``fmllr_iters`` defaults to::

        [2, 4, 6, 12]

    Attributes
    ----------
    num_iters : int
        Number of training iterations to perform, defaults to 35
    scale_opts : list
        Options for specifying scaling in alignment
    beam : int
        Default beam width for alignment, defaults = 10
    retry_beam : int
        Beam width to fall back on if no alignment is produced, defaults to 40
    max_iter_inc : int
        Last iter to increase #Gauss on, defaults to 30
    totgauss : int
        Total number of gaussians, defaults to 1000
    boost_silence : float
        Factor by which to boost silence likelihoods in alignment, defaults to 1.0
    realign_iters : list
        List of iterations to perform alignment
    stage : int
        Not used
    power : float
        Exponent for number of gaussians according to occurrence counts, defaults to 0.25
    do_fmllr : bool
        Specifies whether to do speaker adaptation, defaults to True
    do_lda_mllt : bool
        Spacifies whether to do LDA + MLLT transformation, default to False
    num_states : int
        Number of states in the decision tree, defaults to 3100
    num_gauss : int
        Number of gaussians in the decision tree, defaults to 50000
    cluster_threshold : int
        For build-tree control final bottom-up clustering of leaves, defaults to 100
    fmllr_update_type : str
        Type of fMLLR estimation, defaults to ``'full'``
    fmllr_iters : list
        List of iterations to perform fMLLR estimation
    fmllr_power : float
        Defaults to 0.2
    silence_weight : float
        Weight on silence in fMLLR estimation
    '''

    def __init__(self, align_often=True, **kwargs):
        defaults = {'do_fmllr': True,
                    'do_lda_mllt': False,
                    'fmllr_update_type': 'full',
                    'fmllr_iters': [2, 4, 6, 12],
                    'fmllr_power': 0.2,
                    'silence_weight': 0.0}
        defaults.update(kwargs)
        super(TriphoneFmllrConfig, self).__init__(**defaults)

# For nnets
class LdaMlltConfig(object):
    '''
    Configuration class for LDA + MLLT training

    Scale options defaults to::

        ['--transition-scale=1.0', '--acoustic-scale=0.1', '--self-loop-scale=0.1']

    Attributes
    ----------
    num_iters : int
        Number of training iterations to perform
    do_fmllr : bool
        Specifies whether to do speaker adaptation, defaults to False
    do_lda_mllt : bool
        Spacifies whether to do LDA + MLLT transformation, default to True
    scale_opts : list
        Options for specifying scaling in alignment
    num_gauss : int
        Number of gaussians in the decision tree, defaults to 50000
    beam : int
        Default beam width for alignment, defaults = 10
    retry_beam : int
        Beam width to fall back on if no alignment is produced, defaults to 40
    cluster_threshold : int
        For build-tree control final bottom-up clustering of leaves, defaults to 100
    boost_silence : float
        Factor by which to boost silence likelihoods in alignment, defaults to 1.0
    realign_iters : list
        List of iterations to perform alignment
    stage : int
        Not used
    power : float
        Exponent for number of gaussians according to occurrence counts, defaults to 0.25
    randprune : float
        Approximately the ratio by which we will speed up the LDA and MLLT calculations via randomized pruning
    '''
    def __init__(self, **kwargs):
        self.num_iters = 13
        self.do_fmllr = False
        self.do_lda_mllt = True

        self.scale_opts = ['--transition-scale=1.0',
                           '--acoustic-scale=0.1',
                           '--self-loop-scale=0.1']
        self.num_gauss = 5000
        self.beam = 10
        self.retry_beam = 40
        self.initial_gauss_count = 5000
        self.cluster_threshold = -1
        self.max_gauss_count = 10000
        self.boost_silence = 1.0
        self.realign_iters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.stage = -5
        self.power = 0.25

        self.dim = 40
        self.careful = False
        self.randprune = 4.0
        self.splice_opts = ['--left-context=3', '--right-context=3']
        self.cluster_thresh = -1
        self.norm_vars = False

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def max_iter_inc(self):
        return self.num_iters

    @property
    def inc_gauss_count(self):
        return int((self.max_gauss_count - self.initial_gauss_count) / self.max_iter_inc)

class DiagUbmConfig(object):
    '''
    Configuration class for diagonal UBM training

    Attributes
    ----------
    num_iters : int
        Number of training iterations to perform
    num_gselect : int
        Number of Gaussian-selection indices to use while training the model
    num_gauss : int
        Number of Gaussians after clustering down.

    '''
    def __init__(self, **kwargs):
        self.num_iters = 4
        self.num_gselect = 30
        self.num_frames = 400000
        self.num_gauss = 256

        self.num_iters_init = 20
        self.initial_gauss_proportion = 0.5
        self.subsample = 2
        self.cleanup = True
        self.min_gaussian_weight = 0.0001

        self.remove_low_count_gaussians = True
        self.num_threads = 32
        self.splice_opts = ['--left-context=3', '--right-context=3']

class iVectorExtractorConfig(object):
    '''
    Configuration class for i-vector extractor training

    Attributes
    ----------
    ivector_dim : int
        Dimension of the extracted i-vector
    ivector_period : int
        Number of frames between i-vector extractions
    num_iters : int
        Number of training iterations to perform
    num_gselect : int
        Gaussian-selection using diagonal model: number of Gaussians to select
    posterior_scale : float
        Scale on the acoustic posteriors, intended to account for inter-frame correlations
    min_post : float
        Minimum posterior to use (posteriors below this are pruned out)
    subsample : int
        Speeds up training; training on every x'th feature
    max_count : int
        The use of this option (e.g. --max-count 100) can make iVectors more consistent for different lengths of utterance, by scaling up the prior term when the data-count exceeds this value. The data-count is after posterior-scaling, so assuming the posterior-scale is 0.1, --max-count 100 starts having effect after 1000 frames, or 10 seconds of data.
    '''
    def __init__(self, **kwargs):
        self.ivector_dim = 100
        self.ivector_period = 10
        self.num_iters = 10
        self.num_gselect = 5
        self.posterior_scale = 0.1

        self.min_post = 0.025
        self.subsample = 2
        self.max_count = 0

        self.num_threads = 4
        self.num_processes = 4

        self.splice_opts = ['--left-context=3', '--right-context=3']
        self.compress = False

class NnetBasicConfig(object):
    '''
    Configuration class for neural network training

    Attributes
    ----------
    num_epochs : int
        Number of epochs of training; number of iterations is worked out from this
    iters_per_epoch : int
        Number of iterations per epoch
    realign_times : int
        How many times to realign during training; this will equally space them over the iterations
    beam : int
        Default beam width for alignment
    retry_beam : int
        Beam width to fall back on if no alignment is produced
    initial_learning_rate : float
        The initial learning rate at the beginning of training
    final_learning_rate : float
        The final learning rate by the end of training
    pnorm_input_dim : int
        The input dimension of the pnorm component
    pnorm_output_dim : int
        The output dimension of the pnorm component
    p : int
        Pnorm parameter
    hidden_layer_dim : int
        Dimension of a hidden layer
    samples_per_iter : int
        Number of samples seen per job per each iteration; used when getting examples
    shuffle_buffer_size : int
        This "buffer_size" variable controls randomization of the samples on each iter.  You could set it to 0 or to a large value for complete randomization, but this would both consume memory and cause spikes in disk I/O.  Smaller is easier on disk and memory but less random.  It's not a huge deal though, as samples are anyway randomized right at the start. (the point of this is to get data in different minibatches on different iterations, since in the preconditioning method, 2 samples in the same minibatch can affect each others' gradients.
    add_layers_period : int
        Number of iterations between addition of a new layer
    num_hidden_layers : int
        Number of hidden layers
    randprune : float
        Speeds up LDA
    alpha : float
        Relates to preconditioning
    mix_up : int
        Number of components to mix up to
    prior_subset_size : int
        Number of samples per job for computing priors
    update_period : int
        How often the preconditioning subspace is updated
    num_samples_history : int
        Relates to online preconditioning
    preconditioning_rank_in : int
        Relates to online preconditioning
    preconditioning_rank_out : int
        Relates to online preconditioning

    '''
    def __init__(self, **kwargs):
        self.num_epochs = 4
        self.num_epochs_extra = 5
        self.num_iters_final = 20
        self.iters_per_epoch = 2
        self.realign_times = 0

        self.beam = 10
        self.retry_beam = 15000000

        self.initial_learning_rate=0.32
        self.final_learning_rate=0.032
        self.bias_stddev = 0.5

        self.pnorm_input_dim = 3000
        self.pnorm_output_dim = 300
        self.p = 2

        self.shrink_interval = 5
        self.shrink = True
        self.num_frames_shrink = 2000

        self.final_learning_rate_factor = 0.5
        self.hidden_layer_dim = 50

        self.samples_per_iter = 200000
        self.shuffle_buffer_size = 5000
        self.add_layers_period = 2
        self.num_hidden_layers = 3
        self.modify_learning_rates = False

        self.last_layer_factor = 0.1
        self.first_layer_factor = 1.0

        self.splice_width = 3
        self.randprune = 4.0
        self.alpha = 4.0
        self.max_change = 10.0
        self.mix_up = 12000 # From run_nnet2.sh
        self.prior_subset_size = 10000
        self.boost_silence = 0.5

        self.update_period = 4
        self.num_samples_history = 2000
        self.max_change_per_sample = 0.075
        self.precondition_rank_in = 20
        self.precondition_rank_out = 80

class MfccConfig(object):
    '''
    Configuration class for MFCC generation

    The ``config_dict`` currently stores one key ``'use-energy'`` which
    defaults to False

    Parameters
    ----------
    output_directory : str
        Path to directory to save configuration files for Kaldi
    kwargs : dict, optional
        If specified, updates ``config_dict`` with this dictionary

    Attributes
    ----------
    config_dict : dict
        Dictionary of configuration parameters
    '''

    def __init__(self, output_directory, job=None, kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.job = job
        self.config_dict = {'use-energy': False, 'frame-shift': 10}
        self.config_dict.update(kwargs)
        self.output_directory = output_directory
        self.write()

    def update(self, kwargs):
        '''
        Update configuration dictionary with new dictionary

        Parameters
        ----------
        kwargs : dict
            Dictionary of new parameter values
        '''
        self.config_dict.update(kwargs)
        self.write()

    @property
    def config_directory(self):
        path = os.path.join(self.output_directory, 'config')
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def path(self):
        if self.job is None:
            f = 'mfcc.conf'
        else:
            f = 'mfcc.{}.conf'.format(self.job)
        return os.path.join(self.config_directory, f)

    def write(self):
        '''
        Write configuration dictionary to a file for use in Kaldi binaries
        '''
        with open(self.path, 'w', encoding='utf8') as f:
            for k, v in self.config_dict.items():
                f.write('--{}={}\n'.format(k, make_safe(v)))
