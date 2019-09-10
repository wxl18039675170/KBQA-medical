from jenademo.question_classifier import *
from jenademo.answer_search import *
from jenademo.question_parser import *
import json


class KBQA:
    def __init__(self):
        # self.entity = self.load_entity('../dict/md5_entity.json')
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    # def load_entity(self, path):
    #     with open(path, 'r', encoding='UTF-8') as fr:
    #         entity = json.load(fr)
    #     return entity

    def qa_main(self, question):
        question_classify = self.classifier.classify(question)
        # print(question_classify)
        if not question_classify:
            return '抱歉，小智暂时无法回答您的问题！'
        res_sql = self.parser.parser_main(question_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return '抱歉，小智暂时无法回答您的问题！'
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = KBQA()
    while 1:
        question = input('用户:')
        answer = handler.qa_main(question)
        print('小智:', answer)