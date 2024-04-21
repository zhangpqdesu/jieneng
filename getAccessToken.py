import requests

#文档地址：https://ai.baidu.com/ai-doc/REFERENCE/Lkru0zoz4
def main():
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={yourAccessToken}"
    
    payload='detect_direction=false&paragraph=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()
