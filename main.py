from yt_ai import yt_ai
import dotwiz

core = yt_ai.Core("configs/config_2.json")
core.run()  # This will run the whole process including video generation with subtitles
print("Completed")