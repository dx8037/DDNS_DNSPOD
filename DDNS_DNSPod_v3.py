#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,commands
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

try:
    cred = credential.Credential("api用户名称", "用户授权码")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    req = models.DescribeRecordRequest()
    params = {
        "Domain": "主域名",
        "RecordId": 二级域名ID，可在web控制台日志获得
    }
    req.from_json_string(json.dumps(params))

    resp = client.DescribeRecord(req)
#    print(resp.to_json_string())
    json_dict = json.loads(resp.to_json_string())
    ss = commands.getoutput("/sbin/ip -6 addr show eth0|/bin/grep 2409|/bin/awk '{print $2}'|/bin/awk -F'/' '{print $1}'")
    #此处过滤语句可按各种需求进行变动，命令请写绝对路径，不然报错
    newip = ss.replace("'","")
    oldip = json_dict['RecordInfo']['Value']
    if newip == oldip:
        print('not updata')
    else:
        req1 = models.ModifyRecordRequest()
        params = {
            "Domain": "主域名",
            "SubDomain": "记录内容",
            "RecordType": "记录类型",
            "RecordLine": "线路",
            "Value": newip,
            "RecordId": 级域名ID，可在web控制台日志获得
        }
        req1.from_json_string(json.dumps(params))
        resp1 = client.ModifyRecord(req1)
        print(resp1.to_json_string())
except TencentCloudSDKException as err:
    print(err)
