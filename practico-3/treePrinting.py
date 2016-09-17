from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle

def testExample():
	exampleTree = {'Outlook': {'Overcast': 'Yes', 'Sunny': {'Humidity': {'High': 'No', 'Normal': 'Yes'}}, 'Rain': {'Wind': {'Strong': 'No', 'Weak': 'Yes'}}}}
	printTree(exampleTree)

attributeTypeNodeColor = "red"
attributeValueNodeColor = "green"
classificationNodeColor = "blue"

def printTree(treeDict):
	#Estilo del arbol.
	ts = TreeStyle()
	#No se agregan nombres de hoja automaticamente.
	ts.show_leaf_name = False
	#Usar este layout custom.
	ts.layout_fn = my_layout
	tree = getPrintableTree(treeDict)
	#Muestro arbol usando el layout establecido.
	tree.show(tree_style=ts)		

def my_layout(node):
    if node.is_leaf():
         #Si el nodo es terminal, se muestra su nombre.
         name_face = AttrFace("name")
    else:
         #Si el nodo es interno, se muestra su nombre con menor escala.
         name_face = AttrFace("name", fsize=10)
    #Adds the name face to the image at the preferred position.
    faces.add_face_to_node(name_face, node, column=0, position="branch-right")

def getPrintableTree(treeDict):
	if (isinstance(treeDict,dict)):
		nodeName = treeDict.keys()[0]
		node = Tree(name=str(nodeName))
		#Seteo color de este nodo (de tipo de atributo).
		nstyle = NodeStyle()
		nstyle["fgcolor"] = attributeTypeNodeColor
		nstyle["size"] = 5
		node.set_style(nstyle)
		if (isinstance(treeDict[nodeName],dict)):
			children = treeDict[nodeName]
			for key in children.keys():
				childrenNode = Tree(name=str(key))
				childrenNode.add_child(getPrintableTree(children[key]))
				#Seteo color de este nodo (de valor de atributo).
				nstyle = NodeStyle()
				nstyle["fgcolor"] = attributeValueNodeColor
				nstyle["size"] = 5
				childrenNode.set_style(nstyle)
				#Agrego este subarbol al nodo padre.
				node.add_child(childrenNode)
		return node
	else:
		classificationNode = Tree(name=str(treeDict))
		#Seteo color de este nodo (valor de clasificacion).
		nstyle = NodeStyle()
		nstyle["fgcolor"] = classificationNodeColor
		nstyle["size"] = 5
		classificationNode.set_style(nstyle)
		return classificationNode