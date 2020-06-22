import allure
import pytest
from common.config import *
from common.base import *
class Test_checkD():
    sql="select distinct(era) from teleplay_record_info"
    @pytest.mark.parametrize('par', [{"recordInfoType": '电视剧'}, ])
    @allure.story("年代和题材比对")
    def test_01(self,par):
        content = get_mth(host1 + addr1, par)
        ##数据库获取年代数据
        content1=sqlcheck(self.sql)
        length = len(content1)
        aa=[]
        ##获取接口的年代数据由字典转为列表格式
        bb=list(content['content'].keys())
        ##获取各个年代下以及各个年代下的题材数据
        for i in range(0,length):
            #print(content1)
            aa.append(content1[i][0])
            ##接口下的各个年代下的题材列表
            content_theme1=list(content['content'][aa[i]])
            sql_type="select distinct(theme) from public.teleplay_record_info  where  era='"+aa[i]+"'"
            content2 = sqlcheck(sql_type)
            content_theme=[]
            ##数据库下的各个题材转为列表形式
            for j in range(0, len(content2)):
                content_theme.append(content2[j][0])
            print(content_theme)
            print(content_theme1)
            assert content_theme.sort()==content_theme1.sort()
        assert aa.sort()==bb.sort()




    @allure.story("年代+题材+年份搜索")
    @pytest.mark.parametrize('year', ['2020', '2019',])
    def test_02(self,year):
        ##数据库查询出所有的年代
        content1=sqlcheck(self.sql)
        length = len(content1)
        aa = []
        content_theme = []
        for i in range(0, length):
            ##追加到查询出来年代到aa列表里
            aa.append(content1[i][0])
            ##利用遍历每个年代去查询年代下的对应题材
            sql_type = "select distinct(theme) from public.teleplay_record_info  where  era='" + aa[i] + "'"
            content2 = sqlcheck(sql_type)
            for j in range(0, len(content2)):
                ##将题材追加到列表里
                content_theme.append(content2[j][0])
                ##用遍历的每个年代题材去查询对应的条数
                sql_count="select count(*) from  public.teleplay_record_info  where  era='"+aa[i]+"' and theme='"+content_theme[j]+"'and public_year='"+year+"'"
                content3 = sqlcheck(sql_count)
                ##获取数据库的条数count
                count=content3[0][0]
                data = {
                    "dramaType": "全部",
                    "keyword": "",
                    "movieRecordType": "全部",
                    "page": 1,
                    "publicMonthBegin": 0,
                    "publicMonthEnd": 0,
                    "publicYear": year,
                    "quarter": 0,
                    "recordInfoType": "电视剧",
                    "rows": 10,
                    "teleTheme": content_theme[j],
                    "teleTime": aa[i]
                }

                content_api = post_mth(host1 + addr, data=data,headers=headers)
                count_api=content_api['content']["count"]
                print(year + aa[i] + content_theme[j] + ',数据库数据' + str(count) + ',接口数据' + str(count_api))
                assert count==count_api




    @allure.story('关键字搜索如证号,坐落,剧名,报备机构,梗要')
    @pytest.mark.parametrize("keyword",['甲第075','黑龙江','双喜临门','哈尔滨电视台','让客人们真正体验到了哈尔滨'])
    def test_03(self,keyword):
        sql="select count(*) from  public.teleplay_record_info  where   name like '%"+keyword+"%' or synopsis like '%"+keyword+"%' or producer like '%"+keyword+"%' or  location like '%"+keyword+"%' or license like '%"+keyword+"%'"
        content=sqlcheck(sql)
        count=content[0][0]
        data = {
            "dramaType": "全部",
            "keyword": keyword,
            "movieRecordType": "全部",
            "page": 1,
            "publicMonthBegin": 0,
            "publicMonthEnd": 0,
            "publicYear": 0,
            "quarter": 0,
            "recordInfoType": "电视剧",
            "rows": 10,
            "teleTheme": "全部",
            "teleTime": "全部"
        }
        content_api=post_mth(host1+addr,data=data,headers=headers)
        count_api=content_api['content']['count']
        print(keyword+':数据库数据'+str(count)+',接口数据'+str(count_api))
        assert count==count_api






    @allure.story('关键字+年份+年代+题材搜索')
    @pytest.mark.parametrize('keyword,year,teleTime,teleTheme',[('上海','2019','近代','传奇'),])
    def test_04(self,keyword,year,teleTime,teleTheme):
        sql_total="select count(*) from (select * from  public.teleplay_record_info  where   name like '%"+keyword+"%' or synopsis like '%"+keyword+"%' or producer like '%"+keyword+"%' or  location like '%"+keyword+"%' or license like '%"+keyword+"%')aa where  aa.public_year='"+year+"'and aa.era='"+teleTime+"' and aa.theme='"+teleTheme+"'"
        print(sql_total)
        ##获取数据库的数量
        content=sqlcheck(sql_total)
        count=content[0][0]
        data = {
            "dramaType": "全部",
            "keyword": keyword,
            "movieRecordType": "全部",
            "page": 1,
            "publicMonthBegin": 0,
            "publicMonthEnd": 0,
            "publicYear": year,
            "quarter": 0,
            "recordInfoType": "电视剧",
            "rows": 10,
            "teleTheme": teleTheme,
            "teleTime": teleTime
        }
        content_api = post_mth(host1 + addr, data=data, headers=headers)
        ##获取接口的数量
        count_api=content_api['content']['count']
        print('时间:'+year+ ',关键字:'+keyword+',年代:'+teleTime+",题材:"+teleTheme+',数据库数据:'+str(count)+',接口数据:'+str(count_api))
        assert  count==count_api





    @allure.story('5年备案数据')
    #@pytest.mark.parametrize('beginYear,endYear,recordInfoType',['2016','2020','电影'],)
    def test_05(self):
        data ={"beginYear":2016,"category":"全部","endYear":2020,"era":"全部","networkDramaType":"全部","recordInfoType":'电视剧'}
        #获取接口数据
        content_api=post_mth(host1+addr2,data,headers)
        print(len(content_api['content']))
        list=[]
        value=[]
        dict={}
        #遍历获取接口数据年份，备案数量，加载到数组里
        for i in range(0,len(content_api['content'])):
            a=content_api['content'][i]['year']
            b=content_api['content'][i]['sum']
            list.append(a)
            value.append(b)
            dict[list[i]]=value[i]
        print(dict)
        ##数据库查询电视剧5年备案数据
        sql_curve="select sum(num),year  from public.record_summary  where type='电视剧'  and  year between '2016' and '2020' group by year"
        content=sqlcheck(sql_curve)
        #print(content)
        list1=[]
        value1=[]
        dict1={}
        ##遍历数据库数据的年份，数量，加载到数组里
        for j in range(0,len(content)):
            a1=content[j][1]
            b1=content[j][0]
            list1.append(a1)
            value1.append(b1)
            dict1[list1[j]]=value1[j]
        print(dict1)
        assert dict==dict1




    @allure.story('具体年份的备案数据')
    @pytest.mark.parametrize('year',['2020','2019',])
    def test_06(self,year):
        par={"recordInfoType":"电视剧","year":year}
        content_api=get_mth(host1+addr3,par)
        ##获取接口数据content下的键值即年代
        a=list(content_api['content'].keys())
        ##遍历接口，遍历每个年代下的备案是占比和备案数量
        for i in range(0,len(a)):
            #c指的是取出每个年代
            c=a[i]
            era1=c[0:2]
            category1=c[2:]
            #print(era1,category1)
            proportions_api=content_api['content'][a[i]]["proportions"]
            nums_api=content_api['content'][a[i]]["nums"]
            #print(proportions_api,nums_api)
            count_proportions=[]
            count_nums=[]
            ##获取数据库中每个年代（从接口遍历取），对应的备案数量和备案数量占比
            for j in range(1,13):
                sql_propor="select SUM(proportion)   from public.record_summary  where type='电视剧' and year='"+year+"' and era='"+era1+"'  and category='"+category1+"' and month='"+str(j)+"'"
                #print(sql_propor)
                sql_nums ="select SUM(num)   from public.record_summary  where type='电视剧' and year='" + year + "' and era='" + era1 + "'  and category='" + category1 + "' and month='" + str(j) + "'"
                content=sqlcheck(sql_propor)
                #print(content)
                content1=sqlcheck(sql_nums)
                ##将获取到的年代每月的备案数量和占比追加到列表里
                if content[0][0] == None:
                    count_proportions.append(0)
                else:
                    count_proportions.append(content[0][0])
                if content1[0][0] == None:
                    count_nums.append(0)
                else:
                    count_nums.append(content1[0][0])
            print(year+a[i]+'接口备案数量占比：'+str(proportions_api)+'，数据库备案数量占比：'+str(count_proportions))
            print(year+ a[i] + '接口备案数量占比：' + str(nums_api) + '，数据库备案数量占比：' + str(count_nums))
            ##比对接口数据和数据库的数据
            assert  count_proportions == proportions_api
            assert   count_nums == nums_api





if __name__=="__main__":
    #pytest.main(['-s','test_checkD.py','--reruns','2','--reruns-delay','3'])
    pytest.main(['-s', 'test_checkD.py'])


