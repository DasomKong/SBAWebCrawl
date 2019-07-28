#내장 모듈
from urllib.request import *
import sys

#외부 모듈
from bs4 import *
import matplotlib.pyplot as p
import matplotlib

# 중간의 id 를 제외하고 공용이므로 전역으로 뺌.
webUrl = "https://m.entertain.naver.com/tvBrand/%s/broadcastInfo/ratingCard"
colors = ['r','g','b','c','m','y','k','w']

def CheckRatings(tgDict):
    RatingDict = dict()
    # 예시로 하나만.. 만약 여러 개의 프로그램을 보여주려고 한다면, range의 값을 수정하면 됨.
    # 추가할 id는 참고하는 홈페이지에서 골라서 밑의 'inputDrama' 함수에 넣어서 반환해주세요.
    
    # 타깃리스트에 들어있는 id 값 갯수만큼 반복해서 dict에 대입
    for drama_name, drama_id in tgDict.items():
        # wPage 변수는 타깃리스트에 들어있는 id를 대입해서 완성한 url
        wPage = urlopen(webUrl % drama_id)

        # print(webUrl % page) # 확인하려면 앞의 주석을 지워서 확인
        soup = BeautifulSoup(wPage, 'html.parser')
    
        # 시청률 값은 tag가 'em' 이고 아래와 같이 find_all 하면 해당 페이지에서 찾을 수 있음.
        emList = soup.find_all('em', {'class': 'rating_grp_percent_num'})
        
        # 시청률값을 담기 위한 임시 리스트
        tmpList = list()
        for em in emList:
            tmpList.append(float(em.get_text()))  # 값만 나옴
        # 리스트를 뒤집어서 첫회차가 가장 앞으로 올 수 있게
        tmpList.reverse()
        RatingDict[drama_name] = tmpList
            
    return RatingDict


def inputDrama():
    print("방송 정보를 출력합니다.")

    tmpTargetDict = dict()
    
    # 슈돌 id : 675566 #미션 id:5930336
    
    tmpTargetDict['Superman comeback']='675566'
    tmpTargetDict['Mr.sunshine']='5930336'
   
    # # 기간이 0일 경우 하루만 출력
    # if (inputNumber.isdigit() and int(inputNumber) >= 0):
    #     days = int(inputNumber)
    # else:
    #     print("잘못된 입력입니다. 프로그램을 종료합니다.")
    #     sys.exit()


    return tmpTargetDict


def drawGraph(pDict):
    matplotlib.rcParams['font.family']='Malgun Gothic'
    matplotlib.rcParams['axes.unicode_minus']=False
    
    # 구해온 자료들을 여기서 세팅과 출력
    i = 0
    for dramaname, dramalist in pDict.items():
        #전역변수로 선언한 colors[] list
        p.plot(dramalist, colors[i], label=dramaname)
        i += 1

        #그래프의 레이블 및 비주얼 효과 생성
    p.title('시청률 그래프')    
    p.xlabel('회차')
    p.ylabel('시청률 %')
    
    p.grid(True)
    p.legend(['슈퍼맨이 돌아왔다', '미스터 션샤인'],loc='upper left')
    p.show()

    return


# main start

TargetDict = inputDrama()  # 드라마 선택

ResultDict = CheckRatings(TargetDict)  # 시청률 추출

drawGraph(ResultDict)  # 그리기

# end of main