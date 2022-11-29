from py2neo import Graph
import json


def nodep(nodeList:list, parent_id:str, g:Graph):
    for node in nodeList:
        id = node['id']
        cls = node['class']
        command = f"""CREATE (:Device:{cls} 
                {{id:'{id}', 
                    description:'{node.get('description', '')}',
                    product:'{node.get('product', '')}'
                }})"""
        g.run(command.strip())
        if parent_id:
            command = f"""
                MATCH (p:Device {{id: '{parent_id}'}}), (c:Device {{id: '{id}'}})
                CREATE (p) -[:PART]-> (c)
            """
            g.run(command.strip())
        if "children" in node:
            nodep(node['children'], id, g)


g = Graph("bolt://localhost:7688", name="neo4j")

data = json.load(open("lshw.json", "rt"))
nodep(data, None, g)


# Commands
# GET PARENT:
#   MATCH (d:Device) WHERE NOT (:Device)-[:PART]->(d:Device) return d

