import time, os
import cv2
import numpy as np

##################################################################################################################
# HELPER FUNCTION
##################################################################################################################
def unpack_video_into_frames(subjectID, dayID, cameraID, frame_indices):    
    video_prefix = 's{}-d{}-camera{}'.format(subjectID, dayID, cameraID)
    video_seq_list = sorted(os.listdir('video_sequences'))
    selected_video_list = sorted([vid for vid in video_seq_list if video_prefix in vid])

    output_root = 'images_unpacked/s{}-d{}'.format(subjectID, dayID)
    output_dir = os.path.join(output_root, 'Camera{}'.format(cameraID))
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    count = 0
    for vid in selected_video_list:
        start_frame = vid.split('-')[-1].split('.mp4')[0]
        vidcap = cv2.VideoCapture(os.path.join('video_sequences', vid))

        success, image = vidcap.read()
        current_frame = int(start_frame)
        while success:
            if current_frame == frame_indices[count]:
                save_path = os.path.join(output_dir, 'frame_{}.jpg'.format(str(current_frame).zfill(6)))
                cv2.imwrite(save_path, image)
                count += 1
                  
            success, image = vidcap.read()
            current_frame += 1
            
    print('Unpacking for {} is completed.'.format(video_prefix))

##################################################################################################################
#EXPS = [(1, 1), (2, 1), (2, 2), (3, 1), (4, 1), (5, 1), (5, 2)]
EXPS = [(5, 2)]
# load annotation
annot_path = 'rat7m_train_test_annotation.pkl'
annot_dict = np.load(annot_path, allow_pickle=True)

for exp in EXPS:
    indicator = np.logical_and(annot_dict['table']['subject_idx'] == exp[0], 
                               annot_dict['table']['day_idx'] == exp[1])

    # extract frames for each recording
    for camID in range(1, 7):
        start = time.time()
        frame_indices = annot_dict['table']['frame_idx']['Camera{}'.format(camID)][indicator]
        unpack_video_into_frames(exp[0], exp[1], camID, frame_indices)
        end = time.time()
        print('Finished with frame unpacking for s{}-d{}-camera{}: {}'.format(exp[0], exp[1], camID, end-start))