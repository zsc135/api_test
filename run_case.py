import unittest
from HTMLTestRunner import HTMLTestRunner
from setting import TEST_REPOET_PATH



if __name__ == '__main__':

    suite = unittest.TestLoader().discover('./cases','test*.py')


    with open(TEST_REPOET_PATH,'wb') as e:

        runner = HTMLTestRunner(e,title='测试报告')
        runner.run(suite)