
I have created a directed graph nx.DiGraph() using networkx in python.

for example, like this:
```python
...
graph.add_node(
    x,
    name=x,
    node_type="entity",                                 
)
...
graph.add_edge(
     subj,
     obj,
     relationship=pred,
)
...
``` 

I have exported the graph to JSON using
```python 
... 
json.dump(      
    nx.readwrite.json_graph.node_link_data(
        graph,
        edges="edges"
    ),      
    file,
) 
```  

I am hosting this JSON data and you can assume that it is available at:  
```javascript
const jsonURL = `${window.location.origin}/knowledge_graph_data.json`;
```  

Please write me a single html file which draws a force network graph using d3js (the latest stable version). The graph MUST show:
- Node attributes on hover (the node attributes which I defined in python networkx), 
- Directed edges
- Node labels (the node attribute "name")
- Edge labels (the edge attribute "relationship")

