# Branch and Bound algorithm for Feature Selection

### Usage:
```
$ python bb.py [-h | --help] [-d | --defaults] -f | --features ... -d | --desired ...
```

* Example usage: `$ python bb.py -f 1,2,3,4,5 -d 2` or `$ python bb.py --features 1,2,3,4,5 --desired 2`
* -h or --help --> __Optional__ Used to display help information
* -d or --defaults --> __Optional/Requried__ Required to specify the use of default values for unspecified arguments. Optional if all the required arguments are specified. 
* -f or --features --> __Required__ Used to supply feature values, comma-separated without spaces (_Ex: -f 1,2,3,4,5_)
* -d or --desired --> __Required__ Used to supply the desired number of features to select (_Ex: -d 2_)

__Note:__
* If you want to use a different criterion function, update __criterion_function__ in __bb.py__ file, with the required functionality
* You may want to install __python-graphviz__ module (For Anaconda: ```$ conda install -c conda-forge python-graphviz```)
* This code is written in __Python3__

###### References:
* https://www.youtube.com/watch?v=hG7IVK_waNQ&t=4s
* http://dataaspirant.com/2017/04/21/visualize-decision-tree-python-graphviz/
