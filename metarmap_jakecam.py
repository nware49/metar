import requests
from bs4 import BeautifulSoup
import board
import neopixel
import time
x = 0
y = 11
pixels = neopixel.NeoPixel(board.D18, 50)
pixels.fill((0,0,0))
pixels.fill((255,0,0))
time.sleep(2)
pixels.fill((0,0,255))
time.sleep(2)
pixels.fill((0,255,0))
time.sleep(2)
pixels.fill((0,255,255))
time.sleep(2)
pixels.fill((0,0,0))            
while y >= 10:
        #Airport 1
    try:
        url1 = 'https://metar-taf.com/KMXF'
        r1 = requests.get(url1)
        html1 = r1.text
        soup1 = BeautifulSoup(html1, 'html.parser')
        Reading1 = (soup1.find(class_= 'mb-0 align-self-center'))
        print(Reading1.text)
        RL1 =(Reading1.text)
        if RL1 == 'VFR':
          pixels[0] = (255,0,0)
        elif RL1 == 'MVFR':
          pixels[0] = (0,0,255)
        elif RL1 == 'IFR':
          pixels[0] = (0,255,0)
        elif RL1 =='LIFR':
          pixels[0] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 2
    try:
        url2 = 'https://metar-taf.com/KALX'
        r2 = requests.get(url2)
        html2 = r2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        Reading2 = (soup2.find(class_= 'mb-0 align-self-center'))
        print(Reading2.text)
        RL2 =(Reading2.text)
        if RL2 == 'VFR':
          pixels[2] = (255,0,0)
        elif RL2 == 'MVFR':
          pixels[2] = (0,0,255)
        elif RL2 == 'IFR':
          pixels[2] = (0,255,0)
        elif RL2 =='LIFR':
          pixels[2] = (0,255,255)
    except:
        print("Weather Not Found, Skipping") 
        #Airport 3
    try:
        url3 = 'https://metar-taf.com/KAUO'
        r3 = requests.get(url3)
        html3 = r3.text
        soup3 = BeautifulSoup(html3, 'html.parser')
        Reading3 = (soup3.find(class_= 'mb-0 align-self-center'))
        print(Reading3.text)
        RL3 =(Reading3.text)
        if RL3 == 'VFR':
          pixels[3] = (255,0,0)
        elif RL3 == 'MVFR':
          pixels[3] = (0,0,255)
        elif RL3 == 'IFR':
          pixels[3] = (0,255,0)
        elif RL3 =='LIFR':
          pixels[3] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 4
    try:
        url4 = 'https://metar-taf.com/KCSG'
        r4 = requests.get(url4)
        html4 = r4.text
        soup4 = BeautifulSoup(html4, 'html.parser')
        Reading4 = (soup4.find(class_= 'mb-0 align-self-center'))
        print(Reading4.text)
        RL4 =(Reading4.text)
        if RL4 == 'VFR':
          pixels[4] = (255,0,0)
        elif RL4 == 'MVFR':
          pixels[4] = (0,0,255)
        elif RL4 == 'IFR':
         pixels[4] = (0,255,0)
        elif RL4 =='LIFR':
         pixels[4] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 5
    try:
        url5 = 'https://metar-taf.com/KLGC'
        r5 = requests.get(url5)
        html5 = r5.text
        soup5 = BeautifulSoup(html5, 'html.parser')
        Reading5 = (soup5.find(class_= 'mb-0 align-self-center'))
        print(Reading5.text)
        RL5 =(Reading5.text)
        if RL5 == 'VFR':
          pixels[6] = (255,0,0)
        elif RL5 == 'MVFR':
          pixels[6] = (0,0,255)
        elif RL5 == 'IFR':
          pixels[6] = (0,255,0)
        elif RL5 =='LIFR':
          pixels[6] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 6
    try:
        url6 = 'https://metar-taf.com/KCCO'
        r6 = requests.get(url6)
        html6 = r6.text
        soup6 = BeautifulSoup(html6, 'html.parser')
        Reading6 = (soup6.find(class_= 'mb-0 align-self-center'))
        print(Reading6.text)
        RL6 =(Reading6.text)
        if RL6 == 'VFR':
          pixels[7] = (255,0,0)
        elif RL6 == 'MVFR':
          pixels[7] = (0,0,255)
        elif RL6 == 'IFR':
          pixels[7] = (0,255,0)
        elif RL6 =='LIFR':
          pixels[7] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 8
    try:
        url8 = 'https://metar-taf.com/KCTJ'
        r8 = requests.get(url8)
        html8 = r8.text
        soup8 = BeautifulSoup(html8, 'html.parser')
        Reading8 = (soup8.find(class_= 'mb-0 align-self-center'))
        print(Reading8.text)
        RL8 =(Reading8.text)
        if RL8 == 'VFR':
          pixels[8] = (255,0,0)
        elif RL8 == 'MVFR':
          pixels[8] = (0,0,255)
        elif RL8 == 'IFR':
          pixels[8] = (0,255,0)
        elif RL8 =='LIFR':
          pixels[8] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 9
    try:
        url9 = 'https://metar-taf.com/KCNI'
        r9 = requests.get(url9)
        html9 = r9.text
        soup9 = BeautifulSoup(html9, 'html.parser')
        Reading9 = (soup9.find(class_= 'mb-0 align-self-center'))
        print(Reading9.text)
        RL9 =(Reading9.text)
        if RL9 == 'VFR':
          pixels[10] = (255,0,0)
        elif RL9 == 'MVFR':
          pixels[10] = (0,0,255)
        elif RL9 == 'IFR':
          pixels[10] = (0,255,0)
        elif RL9 =='LIFR':
          pixels[10] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 10
    try:
        url10 = 'https://metar-taf.com/KRYY'
        r10 = requests.get(url10)
        html10 = r10.text
        soup10 = BeautifulSoup(html10, 'html.parser')
        Reading10 = (soup10.find(class_= 'mb-0 align-self-center'))
        print(Reading10.text)
        RL10 =(Reading10.text)
        if RL10 == 'VFR':
          pixels[11] = (255,0,0)
        elif RL10 == 'MVFR':
          pixels[11] = (0,0,255)
        elif RL10 == 'IFR':
          pixels[11] = (0,255,0)
        elif RL10 =='LIFR':
          pixels[11] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 11
    try:
        url11 = 'https://metar-taf.com/KATL'
        r11 = requests.get(url11)
        html11 = r11.text
        soup11 = BeautifulSoup(html11, 'html.parser')
        Reading11 = (soup11.find(class_= 'mb-0 align-self-center'))
        print(Reading11.text)
        RL11 =(Reading11.text)
        if RL11 == 'VFR':
          pixels[12] = (255,0,0)
        elif RL11 == 'MVFR':
          pixels[12] = (0,0,255)
        elif RL11 == 'IFR':
          pixels[12] = (0,255,0)
        elif RL11 =='LIFR':
          pixels[12] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 12
    try:
        url12 = 'https://metar-taf.com/KHMP'
        r12 = requests.get(url12)
        html12 = r12.text
        soup12 = BeautifulSoup(html12, 'html.parser')
        Reading12 = (soup12.find(class_= 'mb-0 align-self-center'))
        print(Reading12.text)
        RL12 =(Reading12.text)
        if RL12 == 'VFR':
          pixels[13] = (255,0,0)
        elif RL12 == 'MVFR':
          pixels[13] = (0,0,255)
        elif RL12 == 'IFR':
          pixels[13] = (0,255,0)
        elif RL12 =='LIFR':
          pixels[13] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 13
    try:
        url13 = 'https://metar-taf.com/K6A2'
        r13 = requests.get(url13)
        html13 = r13.text
        soup13 = BeautifulSoup(html13, 'html.parser')
        Reading13 = (soup13.find(class_= 'mb-0 align-self-center'))
        print(Reading13.text)
        RL13 =(Reading13.text)
        if RL13 == 'VFR':
          pixels[14] = (255,0,0)
        elif RL13 == 'MVFR':
          pixels[14] = (0,0,255)
        elif RL13 == 'IFR':
          pixels[14] = (0,255,0)
        elif RL13 =='LIFR':
          pixels[14] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 14
    try:
        url14 = 'https://metar-taf.com/KOPN'
        r14 = requests.get(url14)
        html14 = r14.text
        soup14 = BeautifulSoup(html14, 'html.parser')
        Reading14 = (soup14.find(class_= 'mb-0 align-self-center'))
        print(Reading14.text)
        RL14 =(Reading14.text)
        if RL14 == 'VFR':
          pixels[15] = (255,0,0)
        elif RL14 == 'MVFR':
          pixels[15] = (0,0,255)
        elif RL14 == 'IFR':
          pixels[15] = (0,255,0)
        elif RL14 =='LIFR':
          pixels[15] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 15
    try:
        url15 = 'https://metar-taf.com/K6A1'
        r15 = requests.get(url15)
        html15 = r15.text
        soup15 = BeautifulSoup(html15, 'html.parser')
        Reading15 = (soup15.find(class_= 'mb-0 align-self-center'))
        print(Reading15.text)
        RL15 =(Reading15.text)
        if RL15 == 'VFR':
          pixels[16] = (255,0,0)
        elif RL15 == 'MVFR':
          pixels[16] = (0,0,255)
        elif RL15 == 'IFR':
          pixels[16] = (0,255,0)
        elif RL15 =='LIFR':
          pixels[16] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 16
    try:
        url16 = 'https://metar-taf.com/KWRB'
        r16 = requests.get(url16)
        html16 = r16.text
        soup16 = BeautifulSoup(html16, 'html.parser')
        Reading16 = (soup16.find(class_= 'mb-0 align-self-center'))
        print(Reading16.text)
        RL16 =(Reading16.text)
        if RL16 == 'VFR':
          pixels[18] = (255,0,0)
        elif RL16 == 'MVFR':
          pixels[18] = (0,0,255)
        elif RL16 == 'IFR':
          pixels[18] = (0,255,0)
        elif RL16 =='LIFR':
          pixels[18] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 17
    try:
        url17 = 'https://metar-taf.com/KDBN'
        r17 = requests.get(url17)
        html17 = r17.text
        soup17 = BeautifulSoup(html17, 'html.parser')
        Reading17 = (soup17.find(class_= 'mb-0 align-self-center'))
        print(Reading17.text)
        RL17 =(Reading17.text)
        if RL17 == 'VFR':
          pixels[19] = (255,0,0)
        elif RL17 == 'MVFR':
          pixels[19] = (0,0,255)
        elif RL17 == 'IFR':
          pixels[19] = (0,255,0)
        elif RL17 =='LIFR':
          pixels[19] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 18
    try:
        url18 = 'https://metar-taf.com/KSBO'
        r18 = requests.get(url18)
        html18 = r18.text
        soup18 = BeautifulSoup(html18, 'html.parser')
        Reading18 = (soup18.find(class_= 'mb-0 align-self-center'))
        print(Reading18.text)
        RL18 =(Reading18.text)
        if RL18 == 'VFR':
          pixels[20] = (255,0,0)
        elif RL18 == 'MVFR':
          pixels[20] = (0,0,255)
        elif RL18 == 'IFR':
          pixels[20] = (0,255,0)
        elif RL18 =='LIFR':
          pixels[20] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 19
    try:
        url19 = 'https://metar-taf.com/KHQU'
        r19 = requests.get(url19)
        html19 = r19.text
        soup19 = BeautifulSoup(html19, 'html.parser')
        Reading19 = (soup19.find(class_= 'mb-0 align-self-center'))
        print(Reading19.text)
        RL19 =(Reading19.text)
        if RL19 == 'VFR':
          pixels[22] = (255,0,0)
        elif RL19 == 'MVFR':
          pixels[22] = (0,0,255)
        elif RL19 == 'IFR':
          pixels[22] = (0,255,0)
        elif RL19 =='LIFR':
          pixels[22] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 20
    try:
        url20 = 'https://metar-taf.com/KMLJ'
        r20 = requests.get(url20)
        html20 = r20.text
        soup20 = BeautifulSoup(html20, 'html.parser')
        Reading20 = (soup20.find(class_= 'mb-0 align-self-center'))
        print(Reading20.text)
        RL20 =(Reading20.text)
        if RL20 == 'VFR':
          pixels[24] = (255,0,0)
        elif RL20 == 'MVFR':
          pixels[24] = (0,0,255)
        elif RL20 == 'IFR':
          pixels[24] = (0,255,0)
        elif RL20 =='LIFR':
          pixels[24] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 21
    try:
        url21 = 'https://metar-taf.com/KCVC'
        r21 = requests.get(url21)
        html21 = r21.text
        soup21 = BeautifulSoup(html21, 'html.parser')
        Reading21 = (soup21.find(class_= 'mb-0 align-self-center'))
        print(Reading21.text)
        RL21 =(Reading21.text)
        if RL21 == 'VFR':
          pixels[26] = (255,0,0)
        elif RL21 == 'MVFR':
          pixels[26] = (0,0,255)
        elif RL21 == 'IFR':
          pixels[26] = (0,255,0)
        elif RL21 =='LIFR':
          pixels[26] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 22
    try:
        url22 = 'https://metar-taf.com/KLZU'
        r22 = requests.get(url22)
        html22 = r22.text
        soup22 = BeautifulSoup(html22, 'html.parser')
        Reading22 = (soup22.find(class_= 'mb-0 align-self-center'))
        print(Reading22.text)
        RL22 =(Reading22.text)
        if RL22 == 'VFR':
          pixels[27] = (255,0,0)
        elif RL22 == 'MVFR':
          pixels[27] = (0,0,255)
        elif RL22 == 'IFR':
          pixels[27] = (0,255,0)
        elif RL22 =='LIFR':
          pixels[27] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 23
    try:
        url23 = 'https://metar-taf.com/KAHN'
        r23 = requests.get(url23)
        html23 = r23.text
        soup23 = BeautifulSoup(html23, 'html.parser')
        Reading23 = (soup23.find(class_= 'mb-0 align-self-center'))
        print(Reading23.text)
        RL23 =(Reading23.text)
        if RL23 == 'VFR':
          pixels[28] = (255,0,0)
        elif RL23 == 'MVFR':
          pixels[28] = (0,0,255)
        elif RL23 == 'IFR':
          pixels[28] = (0,255,0)
        elif RL23 =='LIFR':
          pixels[28] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 24
    try:
        url24 = 'https://metar-taf.com/18AA'
        r24 = requests.get(url24)
        html24 = r24.text
        soup24 = BeautifulSoup(html24, 'html.parser')
        Reading24 = (soup24.find(class_= 'mb-0 align-self-center'))
        print(Reading24.text)
        RL24 =(Reading24.text)
        if RL24 == 'VFR':
          pixels[29] = (255,0,0)
        elif RL24 == 'MVFR':
          pixels[29] = (0,0,255)
        elif RL24 == 'IFR':
          pixels[29] = (0,255,0)
        elif RL24 =='LIFR':
          pixels[29] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 25
    try:
        url25 = 'https://metar-taf.com/KGMU'
        r25 = requests.get(url25)
        html25 = r25.text
        soup25 = BeautifulSoup(html25, 'html.parser')
        Reading25 = (soup25.find(class_= 'mb-0 align-self-center'))
        print(Reading25.text)
        RL25 =(Reading25.text)
        if RL25 == 'VFR':
          pixels[31] = (255,0,0)
        elif RL25 == 'MVFR':
          pixels[31] = (0,0,255)
        elif RL25 == 'IFR':
          pixels[31] = (0,255,0)
        elif RL25 =='LIFR':
          pixels[31] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 26
    try:
        url26 = 'https://metar-taf.com/KCEU'
        r26 = requests.get(url26)
        html26 = r26.text
        soup26 = BeautifulSoup(html26, 'html.parser')
        Reading26 = (soup26.find(class_= 'mb-0 align-self-center'))
        print(Reading26.text)
        RL26 =(Reading26.text)
        if RL26 == 'VFR':
          pixels[33] = (255,0,0)
        elif RL26 == 'MVFR':
          pixels[33] = (0,0,255)
        elif RL26 == 'IFR':
          pixels[33] = (0,255,0)
        elif RL26 =='LIFR':
          pixels[33] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 27
    try:
        url27 = 'https://metar-taf.com/KAJR'
        r27 = requests.get(url27)
        html27 = r27.text
        soup27 = BeautifulSoup(html27, 'html.parser')
        Reading27 = (soup27.find(class_= 'mb-0 align-self-center'))
        print(Reading27.text)
        RL27 =(Reading27.text)
        if RL27 == 'VFR':
          pixels[35] = (255,0,0)
        elif RL27 == 'MVFR':
          pixels[35] = (0,0,255)
        elif RL27 == 'IFR':
          pixels[35] = (0,255,0)
        elif RL27 =='LIFR':
          pixels[35] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 28
    try:
        url28 = 'https://metar-taf.com/KDZJ'
        r28 = requests.get(url28)
        html28 = r28.text
        soup28 = BeautifulSoup(html28, 'html.parser')
        Reading28 = (soup28.find(class_= 'mb-0 align-self-center'))
        print(Reading28.text)
        RL28 =(Reading28.text)
        if RL28 == 'VFR':
          pixels[36] = (255,0,0)
        elif RL28 == 'MVFR':
          pixels[36] = (0,0,255)
        elif RL28 == 'IFR':
          pixels[36] = (0,255,0)
        elif RL28 =='LIFR':
          pixels[36] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 29
    try:
        url29 = 'https://metar-taf.com/KDNN'
        r29 = requests.get(url29)
        html29 = r29.text
        soup29 = BeautifulSoup(html29, 'html.parser')
        Reading29 = (soup29.find(class_= 'mb-0 align-self-center'))
        print(Reading29.text)
        RL29 =(Reading29.text)
        if RL29 == 'VFR':
          pixels[38] = (255,0,0)
        elif RL29 == 'MVFR':
          pixels[38] = (0,0,255)
        elif RL29 == 'IFR':
          pixels[38] = (0,255,0)
        elif RL29 =='LIFR':
          pixels[38] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 30
    try:
        url30 = 'https://metar-taf.com/KRMG'
        r30 = requests.get(url30)
        html30 = r30.text
        soup30 = BeautifulSoup(html30, 'html.parser')
        Reading30 = (soup30.find(class_= 'mb-0 align-self-center'))
        print(Reading30.text)
        RL30 =(Reading30.text)
        if RL30 == 'VFR':
          pixels[40] = (255,0,0)
        elif RL30 == 'MVFR':
          pixels[40] = (0,0,255)
        elif RL30 == 'IFR':
          pixels[40] = (0,255,0)
        elif RL30 =='LIFR':
          pixels[40] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 31
    try:
        url31 = 'https://metar-taf.com/K4A6'
        r31 = requests.get(url31)
        html31 = r31.text
        soup31 = BeautifulSoup(html31, 'html.parser')
        Reading31 = (soup31.find(class_= 'mb-0 align-self-center'))
        print(Reading31.text)
        RL31 =(Reading31.text)
        if RL31 == 'VFR':
          pixels[42] = (255,0,0)
        elif RL31 == 'MVFR':
          pixels[42] = (0,0,255)
        elif RL31 == 'IFR':
          pixels[42] = (0,255,0)
        elif RL31 =='LIFR':
          pixels[42] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 32
    try:
        url32 = 'https://metar-taf.com/KGAD'
        r32 = requests.get(url32)
        html32 = r32.text
        soup32 = BeautifulSoup(html32, 'html.parser')
        Reading32 = (soup32.find(class_= 'mb-0 align-self-center'))
        print(Reading32.text)
        RL32 =(Reading32.text)
        if RL32 == 'VFR':
          pixels[44] = (255,0,0)
        elif RL32 == 'MVFR':
          pixels[44] = (0,0,255)
        elif RL32 == 'IFR':
          pixels[44] = (0,255,0)
        elif RL32 =='LIFR':
          pixels[44] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 33
    try:
        url33 = 'https://metar-taf.com/KASN'
        r33 = requests.get(url33)
        html33 = r33.text
        soup33 = BeautifulSoup(html33, 'html.parser')
        Reading33 = (soup33.find(class_= 'mb-0 align-self-center'))
        print(Reading33.text)
        RL33 =(Reading33.text)
        if RL33 == 'VFR':
          pixels[45] = (255,0,0)
        elif RL33 == 'MVFR':
          pixels[45] = (0,0,255)
        elif RL33 == 'IFR':
          pixels[45] = (0,255,0)
        elif RL33 =='LIFR':
          pixels[45] = (0,255,255)
    except:
        print("Weather Not Found, Skipping")
        #Airport 7
    x += 1
    print('End of loop ' + str(x) + ',going to sleep...')
    time.sleep(1800)
    print('End of sleep, New Weather Readings Imminient')
