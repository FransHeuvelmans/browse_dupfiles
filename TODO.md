# TODO list 

## Miscellaneous ideas
* Try using a dict instead of a tree and see what the data-usage is then
(separate branch)
* Add an option to not add and view the leaf nodes (requires 2 runs)
* First add a string to a node, then when it needs to be a Node, create a node
 (And encapsulate this properly in the tree instead of this leaky code)
* When separating leaf nodes, store full folder paths only as full strings
 (less memory, more )
* Use well tested libraries (take the non-hobby/non-silly route)
    * Tree library (anytree)
    * graph-db for smaller memory use (graphdb, graphite, cog)
    * Interface libraries (python-prompt-toolkit)

## Large new features

### Interaction
* Create a simple gui resembling a normal file-manager

### Performance
* Use a different datatype to make more valuable use of the space
(Cython or C bridge perhaps?) See miscellaneous ideas 

### Function
* Be able to send a duplicity command that retrieves a particular file
