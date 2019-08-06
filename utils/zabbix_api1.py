import json
import requests
import time


class ZabbixAPI:
  def __init__(self):
    self.__url = 'http://134.175.221.4/zabbix/api_jsonrpc.php'
    self.__user = 'logadmin'
    self.__password = '542ab7772a73'
    self.__header = {"Content-Type": "application/json-rpc"}
    self.__token_id = self.UserLogin()

  def get_token_id(self):
    return self.__token_id
  
  # 登陆获取token
  def UserLogin(self):
    data = {
      "jsonrpc": "2.0",
      "method": "user.login",
      "params": {
        "user": self.__user,
        "password": self.__password
      },
      "id": 0,
    }
    return self.PostRequest(data)

  # 推送请求
  def PostRequest(self, data):
    result = requests.post(self.__url, headers = self.__header, json=data).content.decode('utf-8')
    #print(result)
    #string type response
    if result=='':
        return result
    # '' can't be loaded
    response = json.loads(result)
    try:
      return response.get('result', None)
    except KeyError:
      raise KeyError

  # hosts lists
  def HostGet(self, hostid=None, hostip=None):
    data = {
      "jsonrpc":"2.0",
      "method":"host.get",
      "params": {
        "with_simple_graph_items": True,      
        "output": [
            "hostid",
            "host"
        ]
    },  
      "auth": self.__token_id,
      "id":0,
    }

    if hostid:
      data['params'] = {
        "output": "extend",
        "hostids": hostid,
        "sortfield": "name"
      }
    return self.PostRequest(data)

  # hosts list
  def HostCreate(self, hostname, hostip, groupid=None, templateid=None):
    data = {
      "jsonrpc":"2.0",
      "method":"host.create",
      "params": {
        "host": hostname,
        "interfaces": [
          {
          "type": 1,
          "main": 1,
          "useip": 1,
          "ip": hostip,
          "dns": "",
          "port": "10050"
          }
        ],
        "groups": [
          {
          "groupid": groupid
          }
        ],
        "templates": [
          {
          "templateid": templateid
          }
        ]
      },
      "auth": self.__token_id,
      "id":1,
    }
    return self.PostRequest(data)
  # 主机组列表
  def HostGroupGet(self, hostid=None, itemid=None):
    data = {
      "jsonrpc":"2.0",
      "method":"hostgroup.get",
      "params":{
        "output": "extend",
        "hostids": hostid,
        "itemids": itemid,
        "sortfield": "name"
      },
      "auth": self.__token_id,
      "id":1,
    }
    return self.PostRequest(data)
  # 监控项列表
  def ItemGet(self, hostid=None):
    data = {
      "jsonrpc":"2.0",
      "method": "item.get",
      "params": {
        "output": "itemid",
        "hostids": hostid,
        "sortfield": "name"
      },
      "auth": self.__token_id,
      "id":1,
    }
    return self.PostRequest(data)

  # 模板列表
  def TemplateGet(self, hostid=None, templateid=None):
    data = {
      "jsonrpc":"2.0",
      "method": "template.get",
      "params": {
        "output": "extend",
        "hostids": hostid,
        "templateids": templateid,
        "sortfield": "name"
      },
      "auth": self.__token_id,
      "id":1,
    }
    return self.PostRequest(data)

  # 图像列表
  def GraphGet(self, hostid=None, graphid=None):
    data = {
      "jsonrpc":"2.0",
      "method": "graph.get",
      "params": {
        "output": "extend",
        "hostids": hostid,
        "graphids": graphid,
        "sortfield": "name"
      },
      "auth": self.__token_id,
      "id":1,
    }
    return self.PostRequest(data)

  # 历史数据
  def History(self, hostid=None, itemid=None):
    timestart = time.time() - 60 * 60 *4
    data = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
      "output": "extend",
      #"history": 2,
      #"itemids": itemid,
      "hostids": hostid,
      "time_from": timestart,
      "sortfield": "clock",
      "sortorder": "DESC",
      "limit": 10
    },
    "auth": self.__token_id,
    "id": 2
    }
    return self.PostRequest(data)
   
  def Alert(self, hostid=None, itemid=None, actionid=None):
       data = {
        "jsonrpc": "2.0",
        "method": "alert.get",
        "params": {
        "output": "extend",
        "actionids": actionid,
        # "hostids": hostid,
        },
        "auth": self.__token_id,
        "id": 1
       }
       return self.PostRequest(data)
  
  def Problem(self, hostid=None,objectid=None):
        data = {
        "jsonrpc": "2.0",
        "method": "problem.get",
        "params": {
         "output": "extend",
         "selectAcknowledges": "extend",
         "selectTags": "extend",
         #"hostids": hostid,
         "objectids": objectid,
         "recent": "true",
         "sortfield": ["eventid"],
         "sortorder": "DESC"
         },
         "auth": self.__token_id,
         "id": 1
        }
        return self.PostRequest(data)

def main():
  zapi = ZabbixAPI()
  token = zapi.get_token_id()
  print('token:', token)
  
  hostid = zapi.HostGet()
  print('token2:', zapi.get_token_id())
  print('hostid:', hostid)


if __name__=="__main__":
  zapi = ZabbixAPI()
  token = zapi.get_token_id()
  print('token:', token)
  
  hostids = zapi.HostGet() 
  #print('hostid:', hostid)
  '''
  # 查看前100台机器的hostid和host name, 顺便把每台机器的所有itemid放到data中
  data = []
  host_name = []
  host_id = []
  for idx, host in enumerate(hostids):
      hostidc = host['hostid']   # 10084
      host_id.append(hostidc)
      host_name.append(host['host'])
      itemids = zapi.ItemGet(hostidc)
      for item in itemids:
          data.append(item['itemid'])
      #print('host {}:\n {}'.format(hostidc, itemids))
      if idx>100:
          break
  print(len(set(data)))
  
  # null
  print(zapi.History(hostid=host_id[1]))
  '''
  
  print(zapi.Problem(objectid='15112'))