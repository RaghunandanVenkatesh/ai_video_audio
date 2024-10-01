from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import csv
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


def apply_subtitles(video_path, subtitle_path, output_path):
    # Load the video
    video = VideoFileClip(video_path)

    # List to hold the subtitles clips
    subtitles = []

    # Read the subtitles from the CSV file
    with open(subtitle_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fact = row['Facts']
            start_time = float(row['Start Time'])
            end_time = float(row['End Time'])

            # Create a TextClip for the subtitle
            subtitle = TextClip(fact, fontsize=24, font="Arial", color='white', bg_color='black')
            subtitle = subtitle.set_position(('center', 'bottom')).set_duration(end_time - start_time)
            subtitle = subtitle.set_start(start_time)

            # Add to the list of subtitles
            subtitles.append(subtitle)

    # Overlay subtitles on the video
    final = CompositeVideoClip([video] + subtitles)

    # Write the result to a file
    final.write_videofile(output_path, fps=video.fps)

if __name__ == "__main__":
    video_path = 'output/PixabayTTV/1.mp4'  # Input video
    subtitle_path = 'data/facts_with_timestamps.csv'  # Subtitles with timestamps
    output_path = 'output/final_video_with_subtitles.mp4'  # Output video with subtitles
    apply_subtitles(video_path, subtitle_path, output_path)
