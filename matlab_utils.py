import scipy.io as sio
import numpy as np

def load_cameras(path):
    d = sio.loadmat(path, struct_as_record=False)
    dataset = vars(d["cameras"][0][0])

    camnames = dataset['_fieldnames']

    cameras = {}
    for i in range(len(camnames)):
        cameras[camnames[i]] = {}
        cam = vars(dataset[camnames[i]][0][0])
        fns = cam['_fieldnames']
        for fn in fns:
            if fn == 'rotationMatrix':
                cameras[camnames[i]]['RotationMatrix'] = cam[fn]
            elif fn == 'translationVector':
                cameras[camnames[i]]['TranslationVector'] = cam[fn]
            else:
                cameras[camnames[i]][fn] = cam[fn]

    return cameras


def load_mocap(path):
    d = sio.loadmat(path, struct_as_record=False)
    dataset = vars(d["mocap"][0][0])

    markernames = dataset['_fieldnames']

    mocap = []
    for i in range(len(markernames)):
        mocap.append(dataset[markernames[i]])

    return np.stack(mocap, axis=2)

def load_mat(path):
    d = sio.loadmat(path, struct_as_record=False)
    return d