# Implementation of Branch and Bound algorithm for feature selection

### Usage:
```
$ python bb.py [-h] -f ... -d ...
```
* -h or --help --> __Optional__ Used to display help information
* -f or --features= --> __Required__ Used to supply feature values, comma-separated without spaces (_Ex: -f 1,2,3,4,5_)
* -d or --desired= --> __Required__ Used to supply the count of desired number of features to select (_Ex: -d 2_)

__Note:__ If you want to use a different criterion function, change to code for function _criterion_function()_ in _bb.py_ file.
