import allure
import pytest
from common.config import *
from common.base import *
class Test_checkA():
    sql_f1='select count(*) from public.movie_record_info'
    sql_d1='select count(*) from  public.teleplay_record_info'
    sql_w1= 'select count(*) from public.online_drama_info'
    sql_w2= "select count(*) from public.online_drama_info where drama_type='网络剧'"
    sql_w3= "select count(*) from public.online_drama_info where drama_type='网络动画'"
    sql_w4= "select count(*) from public.online_drama_info where drama_type='网络电影'"
    @allure.story("电影，电视剧，网络剧的全部数据")
    @pytest.mark.parametrize('dramaType,recordInfoType,sql',[("全部","电影",sql_f1),("全部","电视剧",sql_d1),("全部","网络剧",sql_w1),("网络剧","网络剧",sql_w2),("网络动画","网络剧",sql_w3),("网络电影","网络剧",sql_w4),])
    def test_01(self,dramaType,recordInfoType,sql):
        try:
            self.data = {
                "dramaType": dramaType,
                "keyword": "",
                "movieRecordType": "全部",
                "page": 1,
                "publicMonthBegin": 0,
                "publicMonthEnd": 0,
                "publicYear": 0,
                "quarter": 0,
                "recordInfoType": recordInfoType,
                "rows": 10,
                "teleTheme": "全部",
                "teleTime": "全部"
            }
            count1 = post_mth(host1 + addr, self.data, headers)
            count2 = sqlcheck(sql)
            assert count1["content"]["count"] == count2[0][0]
        except Exception as e:
            raise e



if __name__=="__main__":
    pytest.main(["-s","test_checkAll.py"])