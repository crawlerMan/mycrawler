import networkx as nx
import matplotlib.pyplot as plt

from pymongo import MongoClient
client = MongoClient('localhost')
db = client.followers


ghraph = db.graphtree.aggregate([{ "$match": { "name": "sara" } } ,{ "$graphLookup": { 'from': "graphtree", 'startWith': "$follower_list" , 'connectFromField': "user_id",'connectToField': "follower_list",'as': "mutul_friend"}}])






node=[]
#
for i in ghraph:
	name = i['name']
	x = i["mutul_friend"]


for v in x:
	node.append(v['name'])



edges = []

j = 0
for e in node:

	if j==0:
		pass

	else:
		edges.append([j,e])

	j = e




g = nx.Graph(edges)
nx.draw_networkx(g,node_color='red',node_size=800,directed = True)
plt.savefig(fname="/Users/vahid/Downloads/test")
plt.show()


# g.add_nodes_from(node)
# for h in edges:
# 	g.add_nodes_from(h)




# nx.draw(g,with_labels=True)
# plt.draw()
# plt.show()
# plt.savefig()
