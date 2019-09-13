from py2neo import Graph
from jenademo.jena_spqrql_endpoint import *
import json
class AnswerSearcher:
    def __init__(self):
        self.fuseki = JenaFuseki()
        self.num_limit = 30
        self.md5_entity = self.load_entity('../dict/md5_entity.json')
    def load_entity(self, path):
        with open(path, 'r', encoding='UTF-8') as fr:
            entity = json.load(fr)
        return entity

    '''执行sparql查询，并返回相应结果'''
    def search_main(self, sparqls):
        final_answers = []
        for sparql_ in sparqls:
            question_type = sparql_['question_type']
            queries = sparql_['sql']
            answers = []
            for query in queries:
                # ress = self.g.run(query).data()
                result = self.fuseki.get_sparql_result(query)
                answers.append(result)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            object_name = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            final_answer = '{0}的症状包括：{1}'.format(subject_name, '；'.join(list(set(object_name))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            object_name = self.md5_entity[answers[0]['results']['bindings'][0]['o']['value'][4:]]
            subject_name = [self.md5_entity[item['s']['value'][4:]] for item in answers[0]['results']['bindings']]
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(object_name, '；'.join(list(set(subject_name))[:self.num_limit]))

        elif question_type == 'disease_cause':
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}可能的成因有：{1}'.format(subject_name, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            # desc = [';'.join(i['m.cure_way']) for i in answers]
            # subject = answers[0]['m.name']
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_getway':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}的传播方式为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc1 = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            desc2 = [self.md5_entity[item['s']['value'][4:]] for item in answers[1]['results']['bindings']]
            desc = [i for i in desc1 + desc2 if i != subject_name]
            final_answer = '{0}的并发症包括：{1}'.format(subject_name, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_can_eat':
            # desc = [answers[0]['m.can_eat']]
            # subject = answers[0]['m.name']
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            desc = [item['o']['value'] for item in answers[0]['results']['bindings']]
            if desc:
                final_answer = '{0}可以吃/喝：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            object_name = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject_name, '；'.join(list(set(object_name))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            do_desc = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            recommand_desc = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            final_answer = '{0}推荐{1}\n推荐食谱包括有：{2}'.format(subject_name, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [self.md5_entity[item['s']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['o']['value'][4:]]
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject_name)

        elif question_type == 'food_do_disease':
            desc = [self.md5_entity[item['s']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['o']['value'][4:]]
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject_name)

        elif question_type == 'disease_drug':
            desc = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject_name = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject_name, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [self.md5_entity[item['s']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['o']['value'][4:]]
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [self.md5_entity[item['o']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['s']['value'][4:]]
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [self.md5_entity[item['s']['value'][4:]] for item in answers[0]['results']['bindings']]
            subject = self.md5_entity[answers[0]['results']['bindings'][0]['o']['value'][4:]]
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # print("final_answer: ",final_answer)
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()