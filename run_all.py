import pytest
def test_main():
    # pytest.main(['-v', '-s', 'test_cases/', '--html=report/report.html', '--self-contained-html'])
     pytest.main(['-q', '-s', './test_cases/', '--alluredir', './result','--reruns','3','--reruns-delay','3'])     #切换到相应目录去执行allure serve result
if __name__=="__main__":
    test_main()
