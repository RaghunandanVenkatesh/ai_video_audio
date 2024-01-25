pip install stable_diffusion_videos
pip install gdown
pip install tqdm
pip install matplotlib
pip install nemo-text-processing
pip install soundfile
pip install g2p-en
pip install accelerate
pip install scipy
pip install torch
pip install git+https://github.com/Zulko/moviepy.git@bc8d1a831d2d1f61abfdf1779e8df95d523947a5
pip install --quiet imageio==2.25.1
apt install imagemagick
cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml
pip install TTS
pip install git+https://github.com/suno-ai/bark.git