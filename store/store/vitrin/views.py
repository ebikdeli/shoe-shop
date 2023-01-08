from django.shortcuts import render, HttpResponse
import requests


def users_view(request):
    res = requests.get('http://127.0.0.1:8000/api/user/')
    data = res.json()
    print(res)
    print(data)
    return HttpResponse(f'<div align="center"><h1>Hello store part!</h1></br><h2>data: {data}</h2></div>')
