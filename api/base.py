
# 主要功能：实现所有接口的请求

import requests
from loguru import logger
from setting import BASE_URL
from cacheout import Cache
cache = Cache()
class Base():

    # 实现url拼接
    def get_url(self,path,params=None):
        """
        eg1:http://121.196.13.152:8080/admin/auth/login
        eg2:http://121.196.13.152:8080/admin/admin/list?page=1&limit=20&sort=add_time&order=desc
        :param path:接口路径，比如/admin/auth/login
        :param params:查询参数，比如page=1&limit=20
        :return:
        """
        if params:
            full_path = BASE_URL + path + params
            return full_path
        return BASE_URL + path

    # 实现所有头信息的管理
    def get_headers(self):
        """
        作用：返回头信息
        eg:{'Content-Type':'application/json','X-Litemall-Admin-Token':'xxxx-xxxx-xxxx'}
        :return:
        """
        headers = {'Content-Type':'application/json'}

        # 提取token
        token = cache.get("token")
        if token:
            headers.update({'X-Litemall-Admin-Token':token})
        logger.warning("请求头信息返回数据:{},注意多数接口需要带token".format(headers))
        return headers




    # 实现get方法
    def get(self,url):
        """
        作用：get方法
        :param url:接收的接口地址
        :return: 返回的是请求后的结果
        """
        result = None
        response = requests.get(url,headers=self.get_headers())
        try:
            result = response.json()
            logger.info("请求get方法返回结果：{}".format(result))
            return result
        except Exception as e:
            logger.error("请求get方法异常,返回数据:{}".format(result))


    # 实现post方法
    def post(self,url,data):
        """
        作用：get方法
        :param url:接收的接口地址
        :param data：传递接口的请求体
        :return: 返回的是请求后的结果
        """
        result = None
        response = requests.post(url,json=data,headers=self.get_headers())
        try:
            result = response.json()
            logger.info("请求post方法返回结果：{},请求接口路径：{}".format(result,url))
            return result
        except Exception as e:
            logger.error("请求post方法异常,返回数据:{}".format(result))


    # 实现登录
    def login(self,username,password):

        login_path = "/admin/auth/login"
        login_url = self.get_url(login_path)
        login_data = {'username':username,'password':password}
        result = self.post(login_url,login_data)

        try:
            if 0 == result.get('errno'):
                logger.info("请求登录接口成功")
                token = result.get('data').get('token')
                cache.set("token",token)
            else:
                logger.warning("登录返回失败：{}".format(result))
                return None
        except Exception as e:
            logger.error("请求登录接口异常，异常数据{}".format(result))





if __name__ == '__main__':

    base = Base()
    print(base.login('admin123','admin123'))
