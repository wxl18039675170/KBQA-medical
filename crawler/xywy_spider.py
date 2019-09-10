import urllib.request
import urllib.parse
from lxml import etree
import pymongo


'''爬取寻医问药网站数据，解析后存入放入python字典，然后存入mongodb'''
class XYWYSpider:
    def __init__(self):
        self.conn = pymongo.MongoClient() # 默认打开localhost数据库，端口27017
        self.db = self.conn['xywy']  # 数据库名字
        self.col = self.db['jib']   # 集合名字

    '''根据url，模拟浏览器请求'''
    def request_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    def get_gaishu_info(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        title = html_tree.xpath('//title/text()')[0]
        category = html_tree.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        desc = html_tree.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        ps = html_tree.xpath('//div[@class="mt20 articl-know"]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
            infobox.append(info)
        gaishu_data = {}
        gaishu_data['category'] = category
        gaishu_data['name'] = title.split('的简介')[0]
        gaishu_data['desc'] = desc
        gaishu_data['attributes'] = infobox
        return gaishu_data

    def cause_prevent_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        ps = html_tree.xpath('//p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    '''treat_infobox治疗解析'''
    def treat_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        ps = html_tree.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ',
                                                                                                        '').replace(
                '\t', '')
            infobox.append(info)
        return infobox

    '''treat_infobox治疗解析'''
    def drug_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        drugs = [i.replace('\n', '').replace('\t', '').replace(' ', '') for i in
                 html_tree.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
        return drugs

    '''food治疗解析'''
    def food_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        divs = html_tree.xpath('//div[@class="diet-img clearfix mt20"]')
        try:
            food_data = {}
            food_data['good'] = divs[0].xpath('./div/p/text()')
            food_data['bad'] = divs[1].xpath('./div/p/text()')
            food_data['recommand'] = divs[2].xpath('./div/p/text()')
        except:
            return {}

        return food_data

    '''症状信息解析'''
    def symptom_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        symptoms = html_tree.xpath('//a[@class="gre" ]/text()')
        ps = html_tree.xpath('//p')
        detail = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ',
                                                                                                        '').replace(
                '\t', '')
            detail.append(info)
        symptoms_data = {}
        symptoms_data['symptoms'] = symptoms
        symptoms_data['symptoms_detail'] = detail
        return symptoms, detail

    '''检查信息解析'''
    def inspect_spider(self, url):
        html = self.request_html(url)
        html_tree = etree.HTML(html)
        inspects = html_tree.xpath('//li[@class="check-item"]/a/@href')
        return inspects

    def run(self):
        for page in range(1, 10139):
            try:
                gaishu_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm' % page
                cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm' % page
                prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm' % page
                symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm' % page
                inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm' % page
                treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm' % page
                food_url = 'http://jib.xywy.com/il_sii/food/%s.htm' % page
                drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm' % page
                spider_data = {}
                spider_data['url'] = gaishu_url
                # gaishu_url = 'http://jib.xywy.com/il_sii/gaishu/10900.htm'
                spider_data['gaishu_info'] = self.get_gaishu_info(gaishu_url)  # 概述
                desc_len = len(spider_data['gaishu_info']['desc'][0])     # 概述文本的长度

                spider_data['cause_info'] = self.cause_prevent_spider(cause_url)
                spider_data['prevent_info'] = self.cause_prevent_spider(prevent_url)

                spider_data['symptom_info'] = self.symptom_spider(symptom_url)
                spider_data['inspect_info'] = self.inspect_spider(inspect_url)
                spider_data['treat_info'] = self.treat_spider(treat_url)
                spider_data['food_info'] = self.food_spider(food_url)
                spider_data['drug_info'] = self.drug_spider(drug_url)
                if desc_len > 10:
                    print(page, gaishu_url)
                    self.col.insert(spider_data)
            except Exception as e:
                print(e, page)
        return


if __name__ == '__main__':
    spider = XYWYSpider()
    spider.run()