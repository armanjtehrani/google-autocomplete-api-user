import requests
import html

from graphviz import Graph
from graphviz import Digraph


class GraphBuilder:
    def __init__(self):
        self.all = []

    def get_suggestions(self, my_str):
        if my_str not in self.all:
            self.all.append(my_str)
        res = requests.get(
            'https://www.google.com/complete/search?'
            'client=psy-ab&hl=en-IR&gs_rn=64&gs_ri=psy-ab&pq=str to binary&cp=6&gs_id=23n&q='
            + str(my_str) + '&xhr=t')
        json_data = res.json()
        data = {'basic': my_str, 'more': []}
        more = json_data[1]
        for m in more:
            msg = html.unescape(m[0]).replace('<b>', '').replace('</b>', '')
            if msg not in self.all:
                data['more'].append(msg)
                self.all.append(msg)
        return data

    def build_level(self, my_str, level):
        data = self.get_suggestions(my_str)
        print('new data:', data)
        if level <= 1:
            for d in range(len(data['more'])):
                d_str = data['more'][d]
                dm = {'basic': d_str, 'more': []}
                data['more'][d] = dm
                self.all = []
        else:
            for sub_str_index in range(len(data['more'])):
                sub_str = data['more'][sub_str_index]
                sub_str_data = self.build_level(sub_str, level-1)
                data['more'][sub_str_index] = sub_str_data
        return data

    def visualize_data(self, my_str, level, file_name):
        data = self.build_level(my_str, level)
        dot = Digraph('unix', filename='unix.gv')
        acc = [data]
        print('acc:', acc[0])
        while acc:
            basic = acc[0]['basic']
            childs = acc[0]['more']
            print('new acc:', basic)
            for ch in childs:
                chb = ch['basic']
                print('new ch:', chb)
                dot.node(chb)
                dot.edge(basic, chb)
                acc.append(ch)
            dot.node(basic)
            del acc[0]
        print('dot:', dot)
        dot.view()
        dot.render('output/' + str(file_name), view=True)

    def another_visual(self, my_str, level, file_name):
        data = self.build_level(my_str, level)
        dot = Graph('G', filename='process.gv', engine='sfdp')
        acc = []
        acc.append(data)
        print('acc:', acc[0])
        while (acc):
            basic = acc[0]['basic']
            childs = acc[0]['more']
            print('new acc:', basic)
            for ch in childs:
                chb = ch['basic']
                print('new ch:', chb)
                dot.node(chb)
                dot.edge(basic, chb)
                acc.append(ch)
            dot.node(basic)
            del acc[0]
        print('dot:', dot)
        dot.view()
        dot.render('output/' + str(file_name), view=True)


class Doer:
    graph_builder = GraphBuilder()

    def do(self):
        while True:
            my_str = input("write string:")
            level = input("write level:")
            file_name = input("write file name:")
            level = int(level)
            self.graph_builder.visualize_data(my_str, level, file_name)


Doer().do()




