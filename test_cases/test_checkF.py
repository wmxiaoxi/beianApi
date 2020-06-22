import allure
import pytest
from common.config import *
from common.base import *
class Test_checkF():
    @allure.story("电影类型比对")
    @pytest.mark.parametrize('sql_ftype',["select  distinct (category)  from public.record_summary where type='电影'"],)
    @pytest.mark.parametrize('par',[{"recordInfoType":'电影'},])
    def test_02(self,sql_ftype,par):
        try:
            content=get_mth(host1+addr1,par)
            count1=len(content["content"])
            count2 = sqlcheck(sql_ftype)
            #print(content["content"],count2)
            list = []
            n = 0
            while n < len(count2):
                list.append(count2[n][0])
                n = n + 1
            else:
                print(list)
                list.sort()
            assert count1==len(count2)
            assert content["content"] == list
        except Exception as e:
            raise e


    @pytest.mark.parametrize('sql_ftype', ["select  distinct (category)  from public.record_summary where type='电影'"], )
    @allure.story("电影按各类型查询数据比对")
    def test_03(self,sql_ftype):
        try:
            count2 = sqlcheck(sql_ftype)
            print(count2)
            n = 0
            while n < len(count2):
                self.data = {
                    "dramaType": "全部",
                    "keyword": "",
                    "movieRecordType": count2[n][0],
                    "page": 1,
                    "publicMonthBegin": 0,
                    "publicMonthEnd": 0,
                    "publicYear": 0,
                    "quarter": 0,
                    "recordInfoType": "电影",
                    "rows": 10,
                    "teleTheme": "全部",
                    "teleTime": "全部"
                }
                count1 = post_mth(host1 + addr, self.data, headers)
                sql = "select count(*) from public.movie_record_info  where movie_type='" + count2[n][0] + "'"
                count3 = sqlcheck(sql)
                print(count1["content"]["count"], count3[0][0])
                assert count1["content"]["count"] == count3[0][0]
                n = n + 1
        except Exception as e:
            raise e



    @allure.story("电影年份查询")
    @pytest.mark.parametrize("year",['2020','2019','2018','2017','2016'])
    def test_04(self,year):
        try:
            self.data = {
                "dramaType": "全部",
                "keyword": "",
                "movieRecordType": "全部",
                "page": 1,
                "publicMonthBegin": 0,
                "publicMonthEnd": 0,
                "publicYear": year,
                "quarter": 0,
                "recordInfoType": "电影",
                "rows": 10,
                "teleTheme": "全部",
                "teleTime": "全部"
            }
            count1 = post_mth(host1 + addr, self.data, headers)
            sql = "select count(*) from public.movie_record_info  where public_year='" + year + "'"
            count2 = sqlcheck(sql)
            assert count1["content"]["count"] == count2[0][0]

        except Exception as e:
            raise e




    @allure.story("电影关键字查询--用电影标题，立项号，编剧，备案单位，梗概，备案地")
    @pytest.mark.parametrize("keyword",['太极拳','第018号','王鸿铭','山东繁耀文化传媒','对于弘扬中国传统文化','山东'])
    def test_05(self,keyword):
        try:
            self.data = {
                "dramaType": "全部",
                "keyword": keyword,
                "movieRecordType": "全部",
                "page": 1,
                "publicMonthBegin": 0,
                "publicMonthEnd": 0,
                "publicYear": 0,
                "quarter": 0,
                "recordInfoType": "电影",
                "rows": 10,
                "teleTheme": "全部",
                "teleTime": "全部"
            }
            count1 = post_mth(host1 + addr, self.data, headers)
            sql = "select count(*) from public.movie_record_info  where name like '%" + keyword + "%'  or company_name like '%" + keyword + "%'   or  location like '%" + keyword + "%' or record_item_number like '%" + keyword + "%' or synopsis like '%" + keyword + "%' or screenwriter like '%" + keyword + "%'"
            count2 = sqlcheck(sql)
            assert count1["content"]["count"] == count2[0][0]
        except Exception as e:
            raise e



    @allure.story("组合查询")
    @pytest.mark.parametrize("keyword,movieRecordType,publicYear",[('上海',"合拍片",'2019'),])
    def test_06(self,keyword,movieRecordType,publicYear):
        try:
            self.data = {
                "dramaType": "全部",
                "keyword": keyword,
                "movieRecordType": movieRecordType,
                "page": 1,
                "publicMonthBegin": 0,
                "publicMonthEnd": 0,
                "publicYear": publicYear,
                "quarter": 0,
                "recordInfoType": "电影",
                "rows": 10,
                "teleTheme": "全部",
                "teleTime": "全部"
            }
            count1 = post_mth(host1 + addr, self.data, headers)
            sql = "select count(*) from (select public_year,movie_type from  public.movie_record_info  where name like '%" + keyword + "%'  or company_name like '%" + keyword + "%'   or  location like '%垃圾%' or record_item_number like '%" + keyword + "%' or synopsis like '%" + keyword + "%' or screenwriter like '%" + keyword + "%' )aa  where  aa.movie_type='" + movieRecordType + "' and  aa.public_year='" + publicYear + "'"
            count2 = sqlcheck(sql)
            assert count1["content"]["count"] == count2[0][0]
        except Exception as e:
            raise e



    @allure.story('5年备案数据查询')
    @pytest.mark.parametrize('beginYear,endYear',[(beginYear,endYear),])
    def test_07(self,beginYear,endYear):
        self.data = {
            "beginYear": beginYear,
            "category": "全部",
            "endYear": endYear,
            "era": "全部",
            "networkDramaType":"全部",
            "recordInfoType": "电影"
        }
        count1 = post_mth(host1 + addr2, self.data, headers)
        print(len(count1['content']))
        n=0
        list=[]
        summry=[]
        while n<len(count1['content']):
            list.append(count1['content'][n]["year"])
            summry.append(count1['content'][n]["sum"])
            n=n+1
        print(list, summry)
        sqlcount=[]
        while str(beginYear)<=endYear:
            sql="select count(*) from public.movie_record_info  where    public_year='"+str(beginYear)+"'"
            count2 = sqlcheck(sql)
            sqlcount.append(count2[0][0])
            beginYear=int(beginYear)+1
        print(sqlcount)
        assert summry==sqlcount




    #@pytest.mark.parametrize('par',[{"recordInfoType":'电影',"year":"2019"},])

    par = {"recordInfoType": '电影', "year": "2019"}

    #@pytest.mark.webtest
    @allure.story('按年份各分类备案数量')
    @pytest.mark.parametrize('type',['特种影片','合拍片','故事影片','纪录影片','动画影片','科教影片'],)

    def test_08(self,type):
        content=get_mth(host1+addr3,self.par)
        print(content['content'])
        banum=content['content'][type]["nums"]
        bazb=content['content'][type]["proportions"]
        n=1
        list=[]
        pro=[]
        while n<=12:
            sql="select sum(num)  from public.record_summary where type='电影'  and category='"+type+"'and year='2019' and month="+str(n)
            sql1= "select SUM(proportion)  from public.record_summary where type='电影'  and category='" + type + "'and year='2019' and month=" + str(n)
            count2 = sqlcheck(sql)
            count3=sqlcheck(sql1)
            if count2[0][0] != None:
                list.append(count2[0][0])
            else:
                list.append(0)
            if count3[0][0] != None:
                pro.append(count3[0][0])
            else:
                pro.append(0)

            n=n+1
        print(list,banum,pro)
        assert list==banum
        assert  bazb==pro




if __name__=="__main__":
    #pytest.main(['-s','test_checkF.py','--reruns','2','--reruns-delay','3'])
    #pytest.main(["-s", "test_checkF.py", "-m=webtest"])
    pytest.main(['-s', 'test_checkF.py'])

