#  RAT7M Dataset 

RAT7M is an animal (rat) pose estimation database containing nearly 7 million frames with 2D & 3D keypoints acquired from motion capture, with a diverse variety of rodent poses. This dataset was initially used in our paper [Geometric deep learning enables 3D kinematic profiling across species and environments (Dunn et al. 2021, Nat Methods)](https://www.nature.com/articles/s41592-021-01106-6), i.e. [DANNCE (code release)](https://github.com/spoonsso/dannce).

![RAT7M Overview](commons/rat7m.jpeg)

Given the massive number of available frames in the dataset, we offer this additional instruction for generating a smaller subset of 2D training and test frames. The scripts in this repository enable automatically downloading, frame extraction and annotation processing of the original RAT7M release, making it easy for training algorithms used in rodents.

## Prerequisites
It is expected to run the following in a **Python3** environment, with extra dependencies on:
* opencv-python
* urllib3

## Download
To download the dataset, run `python download_all.py`, which yields 3 new folders under the current directory:
* `video_sequences` containing all *.mp4 video sequences (n=2028).
    * Each video is named with the fashion of `{subject_id}-{recording-day}-{camera_id}-{starting_frame_idx}.mp4` and should each contain at most 3500 frames.
* `annnotations` with motion capture annotation data and camera parameters.
* (`zips` containing all original data in zip format; can be safely deleted if needed.)

## Extract training & test frames from videos
### Overview
This training/test subset of RAT7M contains N=112730 data samples/timesteps extracted from the available video sequences. 
* Notice that each data sample DOES NOT correspond to one single image, but 6 from different synchronized camera views. 
* Details in the split:
    * Train: n = 88194
        * s1-d1: 17812
        * s2-d1: 17441
        * s2-d2: 19728
        * s3-d1: 19845
        * s4-d1: 13368
    * Test: n = 24536
        * s5-d1: 10445
        * s5-d2: 14091


### Download additional annotation
Use the Google Drive link to download [rat7m_train_test_annotation.pkl](https://drive.google.com/file/d/1sZwwX2v0NGkT9j3I5-QCetCxCKEZk5U-/view?usp=sharing). 

* This annotation file is organized as a nested dictionary:
    ```javascript
    annot_dict = {
        "cameras": dict[subject_idx][day_idx][camera_name] // camera poses
        "camera_names": numpy.ndarray // "Camera1"

        "table": {
            "subject_idx": numpy.ndarray //subject ID (1, 2, 3, 4, 5)
            "day_idx": numpy.ndarray //recording day (1, 2)
            "train_test": numpy.darray //"train" or "test"
            "frame_idx": dict[camera_name] //video frame index
            "image_path": dict[camera_name] //relative path to right image "images_unpacked/s1-d1/camera1/frame_000014.jpg"
            "2D_keypoints": dict[camera_name]  //2D keypoints w.r.t each camera, with shape [20, 2]
            "2D_com": dict[camera_names]  //2D (x, y) center of mass
            "3D_keypoints": numpy.ndarray //3D keypoints with shape [20, 3]   
    }
    ```
    * In specific, `"cameras"` provides information regarding `
        'rotationMatrix',
        'translationVector',
        'TangentialDistortion',
        and 'RadialDistortion'`.
    * `"table"` is another nested dictionary where each entry's last level is designated as one **numpy.array of size N=112730**, the total number of data samples in this training/test subset. This organization makes data fetching easier with common deep learning frameworks.
* Several examples about how to use this annotation file:
    * Camera poses for the s4-d1 recordings: `annot_dict['cameras'][4][1]`
    * Name of the 4th camera: `annot_dict['camera_names'][3]`
    * Find data samples corresponding to s5-d1: `np.logical_and(annot_dict['table']['subject_idx'] == 5, annot_dict['table']['day_idx'] == 1)`
    * 2D keypoint coordinates for the i-th data point from camera 4: `annot_dict['table']['2D_keypoints']['Camera4'][i-1]`

### Frame extraction
Run `python extract_frames.py`, which should yield
* `images_unpacked` containing all unpacked frames. It is organized as follows:
```
- images_unpacked/
    - s1-d1/
        - camera1/
            - frame_00014.png
            - ....
        - camera2/
        - camera3/
        - camera4/
        - camera5/
        - camera6/
    - s2-d1/
    - s2-d2/
    - s3-d1/
    - s4-d1/
    - s5-d1/
```
### Sanity check by visualization
Open `visualization.ipynb` and follow the instructions inside. If everything works correctly, you should be seeing an image similar to 

![sample_frame](commons/sample_frame.png)

## (Optional) Compute validation metric with predictions
### Common metrics used in 3D pose estimation
* Mean Per-Joint Position Error (MPJPE): mean Euclidean/L2 distances between predicted keypoints and ground truth.
* PA-MPJPE (Procrustes Analysis, i.e. MPJPE after rigid alignment with the ground truth skeletons after translation, rotation and scale).
* Normalized MPJPE (N-MPJPE), which only evaluates the scale.

### One example
* The script `metrics.py` contains helper functions that compute the above metrics. To use, simply add `from metrics import mpjpe, pa_mpjpe, n_mpjpe` to your evaluation script.
* Each function expects two arguments:
    * `predicted`: numpy.darray of shape (n_samples, n_joints, 2/3)
    * `target`: numpy.darray of shape (n_samples, n_joints, 2/3)

    and returns:
    * numpy.darray of shape (n_sample, )
## Now you may start your own project with RAT7M!
If you use this dataset, please kindly cite:

**Dunn, T.W., Marshall, J.D., Severson, K.S., Aldarondo, D.E., Hildebrand, D.G., Chettih, S.N., Wang, W.L., Gellis, A.J., Carlson, D.E., Aronov, D. and Freiwald, W.A., 2021. Geometric deep learning enables 3D kinematic profiling across species and environments. Nature methods, 18(5), pp.564-573.**