# Branch and Bound algorithm for Feature Selection

### Usage:
```
$ python bb.py [-h] -f ... -d ...
```
* -h or --help --> __Optional__ Used to display help information
* -f or --features= --> __Required__ Used to supply feature values, comma-separated without spaces (_Ex: -f 1,2,3,4,5_)
* -d or --desired= --> __Required__ Used to supply the count of desired number of features to select (_Ex: -d 2_)

__Note:__
* If you want to use a different criterion function, change to code for function __criterion_function__ in __bb.py__ file
* This code is written in __Python3__
* You may want to install __python-graphviz__ module (For Anaconda: ```$ conda install -c conda-forge python-graphviz```)

###### References:
* https://www.youtube.com/watch?v=hG7IVK_waNQ&t=4s
* http://dataaspirant.com/2017/04/21/visualize-decision-tree-python-graphviz/
