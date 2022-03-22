### Install
Install conda or miniconda and after
```
conda create --name tensorflow
conda activate tensorflow
conda install --file requirements.txt

mkdir out_klines
mkdir markets
```

### Uninstall
```uninstall
conda remove --name tensorflow
conda env remove --name tensorflow
```

### Commands
```
conda activate tensorflow   
conda deactivate

python klines-dump.py && python klines-read.py 
python markets-dump.py

```