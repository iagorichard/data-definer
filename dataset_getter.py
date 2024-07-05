import os
import glob
import cv2
import argparse

def get_mkv_files(directory):
    """Recursively finds all .mkv files in the specified directory."""
    return glob.glob(os.path.join(directory, '**', '*.mkv'), recursive=True)

def crop_img(img, init_point, end_point):
    """Crops the image based on the given initial and end points."""
    return img[init_point[0]:end_point[0], init_point[1]:end_point[1], :]

def extract_frames(video_path, frame_skip, output_dir):
    """Extracts and saves frames from the video at the specified intervals."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_name = os.path.basename(video_path)
    
    subject, activity, routine = parse_video_name(video_path)
    
    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_index % frame_skip == 0:
            imgs = crop_frame(frame)
            save_cropped_images(imgs, frame_index, subject, activity, routine, output_dir)
        
        frame_index += 1
    
    cap.release()

def parse_video_name(video_path):
    """Parses the video file path to extract subject, activity, and routine numbers."""
    parts = os.path.normpath(video_path).split(os.sep)
    #print(parts)
    subject = parts[-3].replace('subject', '')
    activity = parts[-2].replace('activity', '')
    #print(subject, activity, )
    #routine = parts[-1].split('_')[1].split('.')[0]
    routine = int(parts[-1].split(".")[0].replace('routine', ''))
    return subject, activity, routine

def crop_frame(frame):
    """Crops the frame into four sub-images for each camera."""
    return [
        crop_img(frame, (0, 0), (720, 1280)),        # Camera 1
        crop_img(frame, (0, 1320), (720, 2600)),     # Camera 2
        crop_img(frame, (780, 0), (1500, 1280)),     # Camera 3
        crop_img(frame, (780, 1320), (1500, 2600))   # Camera 4
    ]

def save_cropped_images(images, frame_number, subject, activity, routine, output_dir):
    """Saves the cropped images to the specified output directory."""
    for i, img in enumerate(images, start=1):
        filename = f"{subject}_{activity}_{routine}_{frame_number}_{i}.jpg"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img)

def main():
    parser = argparse.ArgumentParser(description="Process .mkv files and extract frames.")
    parser.add_argument('--directory', type=str, required=True, help='Directory containing .mkv files')
    parser.add_argument('--frame_skip', type=int, required=True, help='Number of frames to skip between extractions')

    args = parser.parse_args()
    
    mkv_files = get_mkv_files(args.directory)
    
    output_dir = 'out'
    os.makedirs(output_dir, exist_ok=True)
    
    for mkv_file in mkv_files:
        extract_frames(mkv_file, args.frame_skip, output_dir)

if __name__ == "__main__":
    main()
