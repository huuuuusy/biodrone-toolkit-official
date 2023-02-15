from __future__ import absolute_import, print_function

import os
import glob
import numpy as np
import six
import json


class BioDrone(object):
    r"""BioDrone Dataset.
    
    Args:
        root_dir (string): Root directory of dataset where ``train``,
            ``val`` and ``test`` folders exist.
        subset (string, optional): Specify ``train``, ``val`` or ``test``
            subset of BioDrone.
    """
    def __init__(self, root_dir, subset):
        super(BioDrone, self).__init__()
        self.root_dir = root_dir
        self.subset = subset

        f = open(os.path.join(os.path.split(os.path.realpath(__file__))[0],'biodrone_info.json'),'r',encoding='utf-8')
        self.infos = json.load(f)['all']            
        f.close() 

        self.seq_names = self.infos[self.subset]

        self.seq_dirs = [os.path.join(root_dir,'data',self.subset,'frame_{}'.format(s)) for s in self.seq_names]
        self.anno_files = [os.path.join(root_dir,'attribute','groundtruth','{}.txt'.format(s)) for s in self.seq_names]
        self.restart_files = [os.path.join(root_dir,'attribute', 'restart','{}.txt'.format(s)) for s in self.seq_names]
        
    
    def __getitem__(self, index):
        r"""        
        Args:
            index (integer or string): Index or name of a sequence.
        
        Returns:
            tuple:
                (img_files, anno, restart_flag), where ``img_files`` is a list of
                file names, ``anno`` is a N x 4 (rectangles) numpy array
        """
        if isinstance(index, six.string_types):
            if not index in self.seq_names:
                raise Exception('Sequence {} not found.'.format(index))
            index = self.seq_names.index(index)

        img_files = sorted(glob.glob(os.path.join(
            self.seq_dirs[index], '*.jpg')))
        anno = np.loadtxt(self.anno_files[index], delimiter=',')
        restart_flag = np.loadtxt(self.restart_files[index], delimiter=',', dtype=int)

        return img_files, anno, restart_flag
        

    def __len__(self):
        return len(self.seq_names)

