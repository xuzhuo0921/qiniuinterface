#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json,sys
from qiniuinterface import apitest,cli_request



def index(request):
    if request.method == "GET":
        return render(request,"index.html",{"body":'请求示例 :{"key":"test123"}'})
    if request.method == "POST":
        data=""
        ak="4m63nv_dnnHyqqA_mn5xs_F57D_Dt9w8DXl7k0ah"
        sk="v86EoezR9Zw9mhC8-zQmqSTpGVpcoYqa6DoGXd8G"
        url=request.POST.get('apiurl',None).replace( ' ' , '' )
        method=request.POST.get('method',None)
        body=request.POST.get('testbody',None).replace( ' ' , '' )
        fun=request.POST.get('fun',None)
        response=""
        if request.POST.get('ak'):
            ak=request.POST.get('ak')
        if request.POST.get('sk'):
            sk=request.POST.get('sk')
        if method == "post":
            b=""
            try:
                b=json.loads(body)
            except:
                mes="body格式错误:"+body
                return render(request,"index.html",{"apiurl":url,"body":mes,"data":data})  
            data=apitest.apitest_post(url, method, b, ak, sk)
            if fun == "True":
                res=cli_request.cli_post(url, method,b, ak, sk)
                response="\"status_code\":"+str(res.status_code) + ",\"body\":" + str(res.content) + ",\"header\":\"" + str(res.headers)+"\""
        if method == "get":
            data=apitest.apitest_get(url, method, ak, sk)
            if fun == "True":
                res=cli_request.cli_get(url,method,ak,sk)
                response="\"status_code\":"+str(res.status_code) + ",\"body\":" + str(res.content) + ",\"header\":\"" + str(res.headers)+"\""
        return render(request,"index.html",{"apiurl":url,"body":body,"data":data,"response":response})
