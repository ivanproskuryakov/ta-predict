
https://developer.apple.com/forums/thread/697658

https://www.mrdbourke.com/setup-apple-m1-pro-and-m1-max-for-machine-learning-and-data-science/
conda install -c apple tensorflow-depspython -m pip install tensorflow-macos
conda create --prefix ./env python=3.8
conda activate ./env
conda install -c apple tensorflow-deps
python -m pip install tensorflow-macos
python -m pip install tensorflow-metal


conda install -c conda-forge ta-lib
conda install -c conda-forge seaborn

----




conda create --name tensorflow python=3.8
conda activate tensorflow   
conda deactivate


conda list -e > requirements.txt
conda create --name tensorflow --file requirements.txt


conda remove --name tensorflow
conda env remove --name tensorflow
