# Assignment 3 for ISP

##### Digital signature 
---  

## Preparation

### Linux

#### Create virtual environment
```shell
mkdir oqs
cd oqs
python3 -m venv venv
. venv/bin/activate
python3 -m ensurepip --upgrade
```
#### Install liboqs-python. 
```shell
git clone --depth=1 https://github.com/open-quantum-safe/liboqs-python
cd liboqs-python
pip install .
```
#### Extract or copy ```oqs_real_estates``` to ```liboqs-python/```.

## Run the code  
```shell
cd oqs_real_estates/demo
python3 sign_verify.py 
```
 The result should be like this 
 ![image](img.png)
