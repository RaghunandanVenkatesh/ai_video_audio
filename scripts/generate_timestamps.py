import csv
import math

def generate_timestamps(input_csv, output_csv, words_per_second=2):
    """
    Generates start and end times for subtitles based on word count.
    Assumes an average reading speed of words_per_second.
    """
    current_time = 0  # Start at the beginning of the video
    with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Id', 'Prompts', 'Facts', 'Start Time', 'End Time']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            fact = row['Facts']
            words = len(fact.split())
            duration = math.ceil(words / words_per_second)
            start_time = current_time
            end_time = current_time + duration

            writer.writerow({
                'Id': row['Id'],
                'Prompts': row['Prompts'],
                'Facts': row['Facts'],
                'Start Time': start_time,
                'End Time': end_time
            })

            current_time = end_time  # Move to next timestamp

if __name__ == "__main__":
    input_csv = 'data/facts_2.csv'
    output_csv = 'data/facts_with_timestamps.csv'
    generate_timestamps(input_csv, output_csv)
