import os
import urllib.parse
from flask import Flask, make_response, request, redirect
import tweepy

app = Flask(__name__)

twitterCounter = 0
bearerToken = [os.getenv("TWITTER_BEARER"), os.getenv("TWITTER_BEARER2")]

oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="https://givewithporuka.pythonanywhere.com/callback"
    )

dummyRet = {
  "result": {
    "0x1plus": {
      "id": 733478230779428865,
      "img": "https://pbs.twimg.com/profile_images/1464101452889141261/gOa1d5vm_normal.jpg"
    },
    "0xMacroDAO": {
      "id": 1460980132194177030,
      "img": "https://pbs.twimg.com/profile_images/1519831935643791364/0n_tlDQQ_normal.jpg"
    },
    "0xPolygon": {
      "id": 914738730740715521,
      "img": "https://pbs.twimg.com/profile_images/1549781337028308992/P-J04JMx_normal.jpg"
    },
    "0xjackson_": {
      "id": 978297310210752513,
      "img": "https://pbs.twimg.com/profile_images/1570607429813149702/88Tmq2DB_normal.jpg"
    },
    "0xjenil": {
      "id": 1410286200,
      "img": "https://pbs.twimg.com/profile_images/1547613486502408194/nu4m8w-6_normal.jpg"
    },
    "0xmasamasa": {
      "id": 1374005060217184258,
      "img": "https://pbs.twimg.com/profile_images/1569374842620678145/EG5K_kxf_normal.jpg"
    },
    "0xtiagofneto": {
      "id": 1452248234592714755,
      "img": "https://pbs.twimg.com/profile_images/1528443860761952257/jhW13sCN_normal.jpg"
    },
    "101dotxyz": {
      "id": 1318652008828600320,
      "img": "https://pbs.twimg.com/profile_images/1502096534740951044/clDUEYj4_normal.jpg"
    },
    "1kxnetwork": {
      "id": 978008453225496576,
      "img": "https://pbs.twimg.com/profile_images/1548000177717317633/SNs-gWNj_normal.jpg"
    },
    "2xic_": {
      "id": 1416633667,
      "img": "https://pbs.twimg.com/profile_images/1530922876223819782/6ebIBQyh_normal.jpg"
    },
    "6thManVentures": {
      "id": 1182327328061497344,
      "img": "https://pbs.twimg.com/profile_images/1554996414387716096/v5Oll1ey_normal.jpg"
    },
    "7FFFnft": {
      "id": 1495317020325609475,
      "img": "https://pbs.twimg.com/profile_images/1566030493123940353/VXZVbHbf_normal.jpg"
    },
    "AJEhrenberg_": {
      "id": 703342311158255616,
      "img": "https://pbs.twimg.com/profile_images/1549102435305668610/iaqnKBbl_normal.png"
    },
    "AaronCarpenter": {
      "id": 1088207396,
      "img": "https://pbs.twimg.com/profile_images/1491493279308955651/5mrd493H_normal.jpg"
    },
    "AdamDraper": {
      "id": 34055382,
      "img": "https://pbs.twimg.com/profile_images/1547324187588538370/tKLmbxhc_normal.jpg"
    },
    "AzucaCo": {
      "id": 14925641,
      "img": "https://pbs.twimg.com/profile_images/1537119874778124288/hHfmCxKv_normal.jpg"
    },
    "Balance_io": {
      "id": 730509234614341633,
      "img": "https://pbs.twimg.com/profile_images/1492243500158500864/jklHpaIK_normal.jpg"
    },
    "BanklessHQ": {
      "id": 1225557966142820354,
      "img": "https://pbs.twimg.com/profile_images/1559689397288706048/uO6uah2X_normal.jpg"
    },
    "BasiaKubicka1": {
      "id": 1107049867275325440,
      "img": "https://pbs.twimg.com/profile_images/1107050528167657475/lYiAuXr__normal.jpg"
    },
    "BerBlockWeek": {
      "id": 1004377150990974978,
      "img": "https://pbs.twimg.com/profile_images/1022950880490840064/Z7lA-5Sc_normal.jpg"
    },
    "BhatiaKishore": {
      "id": 879196999,
      "img": "https://pbs.twimg.com/profile_images/639120724200853505/mpAAzJUr_normal.jpg"
    },
    "BrantlyMillegan": {
      "id": 518918278,
      "img": "https://pbs.twimg.com/profile_images/1484254155124396034/RJ8uoGSV_normal.png"
    },
    "BraytonKey": {
      "id": 270197351,
      "img": "https://pbs.twimg.com/profile_images/1477361157413347328/baUiajdX_normal.jpg"
    },
    "BrennerSpear": {
      "id": 3031068356,
      "img": "https://pbs.twimg.com/profile_images/1562994677346840577/m7OBRRwK_normal.png"
    },
    "BrianKnier": {
      "id": 377012564,
      "img": "https://pbs.twimg.com/profile_images/1553495059453992961/Q9mZaMf7_normal.jpg"
    },
    "BrunoZell": {
      "id": 1125046777181364224,
      "img": "https://pbs.twimg.com/profile_images/1480006120286552064/nk_Sui9e_normal.jpg"
    },
    "CJarnefur": {
      "id": 1520097969206349830,
      "img": "https://pbs.twimg.com/profile_images/1535253004580012044/raaMZng8_normal.jpg"
    },
    "CReckhow": {
      "id": 2584156840,
      "img": "https://pbs.twimg.com/profile_images/1453714758583132162/A5mAalCB_normal.jpg"
    },
    "CandyDAO_eth": {
      "id": 1353559604827836417,
      "img": "https://pbs.twimg.com/profile_images/1499750333777682436/NYoWbiFY_normal.jpg"
    },
    "CandyDAO_leaf": {
      "id": 1360084437086609409,
      "img": "https://pbs.twimg.com/profile_images/1529128674737459201/9J6wZvo6_normal.jpg"
    },
    "CarlKVogel": {
      "id": 1332729339188817929,
      "img": "https://pbs.twimg.com/profile_images/1507866756865478658/ILPyilCk_normal.png"
    },
    "CharleyMa": {
      "id": 18996396,
      "img": "https://pbs.twimg.com/profile_images/1545288304471547904/VLIouCbr_normal.png"
    },
    "ChrisTurdd": {
      "id": 983521823596924928,
      "img": "https://pbs.twimg.com/profile_images/1563943519961620481/tWPIhPR9_normal.jpg"
    },
    "CodyDisch": {
      "id": 214650515,
      "img": "https://pbs.twimg.com/profile_images/1525786377752829952/krSwvwzD_normal.jpg"
    },
    "CoinviseCo": {
      "id": 1322826777383694337,
      "img": "https://pbs.twimg.com/profile_images/1555069405935022080/nTpd6Wb1_normal.jpg"
    },
    "Conste11ation": {
      "id": 851902232903766016,
      "img": "https://pbs.twimg.com/profile_images/1567217978415976449/kUf8P49s_normal.png"
    },
    "CryptoGamr": {
      "id": 730086612,
      "img": "https://pbs.twimg.com/profile_images/1491077616572456965/mF3_-Yqu_normal.jpg"
    },
    "CryptoMondaysNY": {
      "id": 1468425485172588546,
      "img": "https://pbs.twimg.com/profile_images/1468425660272193538/B-hC2_S1_normal.png"
    },
    "CultDaoInfinite": {
      "id": 1511760914210598916,
      "img": "https://pbs.twimg.com/profile_images/1554887940236517376/DkTCutEp_normal.jpg"
    },
    "DGHEvents": {
      "id": 1479129668049686528,
      "img": "https://pbs.twimg.com/profile_images/1486018585181003776/qIDNZ6hz_normal.png"
    },
    "DIAdata_org": {
      "id": 1026772462296547328,
      "img": "https://pbs.twimg.com/profile_images/1568277474445778944/ibfVuuLz_normal.jpg"
    },
    "DeFi_Conference": {
      "id": 1420844255698989066,
      "img": "https://pbs.twimg.com/profile_images/1546165385040363521/DXu-Y6tz_normal.jpg"
    },
    "Dopeness007": {
      "id": 1408498124268703748,
      "img": "https://pbs.twimg.com/profile_images/1564602520705671168/-zJu8r21_normal.jpg"
    },
    "ELVEricLay": {
      "id": 3219608602,
      "img": "https://pbs.twimg.com/profile_images/1521635933191229440/40VKz8Xe_normal.jpg"
    },
    "ETHBerlin": {
      "id": 973460227130646529,
      "img": "https://pbs.twimg.com/profile_images/1546798251042607105/x4BJz7DX_normal.png"
    },
    "ETHBrno": {
      "id": 1431700224779735046,
      "img": "https://pbs.twimg.com/profile_images/1555325967043907595/f0xZ23EG_normal.jpg"
    },
    "ETHIndiaco": {
      "id": 964919649837056000,
      "img": "https://pbs.twimg.com/profile_images/1506575392614023172/MpQnHp1P_normal.png"
    },
    "ETHWarsaw": {
      "id": 1323595037591150593,
      "img": "https://pbs.twimg.com/profile_images/1516030725727920130/IcQtKMX9_normal.png"
    },
    "ElastosInfo": {
      "id": 897748073501278208,
      "img": "https://pbs.twimg.com/profile_images/1402816234438209536/oH2NiuBC_normal.jpg"
    },
    "ElastosWeb3": {
      "id": 1472243648377114631,
      "img": "https://pbs.twimg.com/profile_images/1476627975412109315/o5D9MtFB_normal.jpg"
    },
    "ElectricCapital": {
      "id": 994440544657928193,
      "img": "https://pbs.twimg.com/profile_images/995890561478545408/NmJ6Mbpw_normal.jpg"
    },
    "EmpireDao": {
      "id": 1445206614286512137,
      "img": "https://pbs.twimg.com/profile_images/1481694682421858309/jzHr1rSE_normal.jpg"
    },
    "EthCC": {
      "id": 738485554048860160,
      "img": "https://pbs.twimg.com/profile_images/1544304761658277888/rQ0lofL7_normal.jpg"
    },
    "EthCCweek": {
      "id": 1086282726255353856,
      "img": "https://pbs.twimg.com/profile_images/1534833314472787970/jeZHYovF_normal.jpg"
    },
    "EthereumPhone": {
      "id": 1467635854143336453,
      "img": "https://pbs.twimg.com/profile_images/1544337107203809280/Htnt5DHV_normal.jpg"
    },
    "FranktheFTank": {
      "id": 851096468727492608,
      "img": "https://pbs.twimg.com/profile_images/1504914624180854786/3xOSawXt_normal.jpg"
    },
    "GeoffreyHorwitz": {
      "id": 1445873553824378880,
      "img": "https://pbs.twimg.com/profile_images/1537223062399070208/bbo4z08s_normal.png"
    },
    "HailTheArt": {
      "id": 1470610743678619655,
      "img": "https://pbs.twimg.com/profile_images/1505595077724446725/XeKaoUM2_normal.jpg"
    },
    "HowardChiao1": {
      "id": 1584878540,
      "img": "https://pbs.twimg.com/profile_images/873243362458914816/HCkEaPA6_normal.jpg"
    },
    "IDriss_xyz": {
      "id": 1416199220978089987,
      "img": "https://pbs.twimg.com/profile_images/1488654051562688512/U_KfDBz0_normal.jpg"
    },
    "INFcryptoNFT": {
      "id": 4878019133,
      "img": "https://pbs.twimg.com/profile_images/1540749936647716864/iNJQuH5c_normal.jpg"
    },
    "Irrelephantoops": {
      "id": 1150415077301981188,
      "img": "https://pbs.twimg.com/profile_images/1535695547704778752/SclwdxSi_normal.png"
    },
    "JamesLemkin": {
      "id": 3230118097,
      "img": "https://pbs.twimg.com/profile_images/1566781648343105539/GAbdjec8_normal.jpg"
    },
    "JarisJames": {
      "id": 1372182489914040322,
      "img": "https://pbs.twimg.com/profile_images/1535233955833716737/QNUVix0y_normal.jpg"
    },
    "JdWhitty": {
      "id": 80641510,
      "img": "https://pbs.twimg.com/profile_images/1560357399025700865/KnFonAqr_normal.png"
    },
    "Jeff_Crypto2012": {
      "id": 1449086502928007176,
      "img": "https://pbs.twimg.com/profile_images/1504437836661108740/Y58cOlUP_normal.jpg"
    },
    "Jierlich": {
      "id": 1140853128054493184,
      "img": "https://pbs.twimg.com/profile_images/1531338812076457984/O21UXwsH_normal.jpg"
    },
    "KevinCargon": {
      "id": 1192486562476544003,
      "img": "https://pbs.twimg.com/profile_images/1562102036417634305/Qx3LYV5B_normal.jpg"
    },
    "KrisJ_Official": {
      "id": 285315957,
      "img": "https://pbs.twimg.com/profile_images/1256465155082211329/gD-ThiX1_normal.jpg"
    },
    "KyivTechSummit": {
      "id": 1501374404856582149,
      "img": "https://pbs.twimg.com/profile_images/1559298535341920258/S9yYWTAl_normal.jpg"
    },
    "LedgerMail": {
      "id": 1045227798237827072,
      "img": "https://pbs.twimg.com/profile_images/1421381051797045257/scvbiS3P_normal.jpg"
    },
    "LensProtocol": {
      "id": 1478109975406858245,
      "img": "https://pbs.twimg.com/profile_images/1490782523701481474/DtyJ_8ej_normal.jpg"
    },
    "LordONence": {
      "id": 2553004051,
      "img": "https://pbs.twimg.com/profile_images/1522565681178370051/sELcWCra_normal.jpg"
    },
    "MKBHD": {
      "id": 29873662,
      "img": "https://pbs.twimg.com/profile_images/1468001914302390278/B_Xv_8gu_normal.jpg"
    },
    "MacBudkowski": {
      "id": 3163739973,
      "img": "https://pbs.twimg.com/profile_images/1492924579194580998/_rJC76y3_normal.png"
    },
    "MajaCholewka": {
      "id": 1475208529040580610,
      "img": "https://pbs.twimg.com/profile_images/1568943943160578052/QGdT2Jqu_normal.jpg"
    },
    "MashAppNFT": {
      "id": 1501654652810670085,
      "img": "https://pbs.twimg.com/profile_images/1548818547371118592/LNBKT-Tf_normal.jpg"
    },
    "MetaMask": {
      "id": 3278906401,
      "img": "https://pbs.twimg.com/profile_images/1514275943300284417/2Ubgzfgg_normal.jpg"
    },
    "Metagame": {
      "id": 1453867148514926600,
      "img": "https://pbs.twimg.com/profile_images/1458507640800268300/RObt94dZ_normal.png"
    },
    "MidwitMilhouse": {
      "id": 461174650,
      "img": "https://pbs.twimg.com/profile_images/1569758810096410625/ljh_KNjI_normal.jpg"
    },
    "MikeFraietta": {
      "id": 17256825,
      "img": "https://pbs.twimg.com/profile_images/1532766732863037444/6mtdB5Kb_normal.jpg"
    },
    "MithosCULT": {
      "id": 2155794606,
      "img": "https://pbs.twimg.com/profile_images/1533339510020444160/wWs_TAuT_normal.jpg"
    },
    "MollOfAmerika": {
      "id": 836414253217136640,
      "img": "https://pbs.twimg.com/profile_images/1438242677250736130/INbUTdKW_normal.jpg"
    },
    "MrOmodulus": {
      "id": 1484209042356531201,
      "img": "https://pbs.twimg.com/profile_images/1533044046515654656/VI5yZchV_normal.jpg"
    },
    "MrUncleD": {
      "id": 1356373002217259010,
      "img": "https://pbs.twimg.com/profile_images/1538623310371725315/oFu4NGSQ_normal.jpg"
    },
    "NYCBlockchainN1": {
      "id": 1417945675522838532,
      "img": "https://pbs.twimg.com/profile_images/1417946229539999746/IeojvMxV_normal.jpg"
    },
    "NamebaseHQ": {
      "id": 1017470147940966401,
      "img": "https://pbs.twimg.com/profile_images/1570287582336126976/yXBgfYCw_normal.jpg"
    },
    "NathanSexer": {
      "id": 569478101,
      "img": "https://pbs.twimg.com/profile_images/1569981453034823680/B7HSJkj5_normal.png"
    },
    "NikinTharan": {
      "id": 1487890932930424834,
      "img": "https://pbs.twimg.com/profile_images/1524737600229158915/iZwPfBDo_normal.jpg"
    },
    "NodarJ": {
      "id": 569183068,
      "img": "https://pbs.twimg.com/profile_images/1537255501397909504/xrpyh26U_normal.jpg"
    },
    "Nogoodtwts": {
      "id": 4805642293,
      "img": "https://pbs.twimg.com/profile_images/1490031652940230656/2SysVIEA_normal.jpg"
    },
    "NormanQian": {
      "id": 2197003290,
      "img": "https://pbs.twimg.com/profile_images/1436750242091782145/wPS6d_rV_normal.jpg"
    },
    "OpenZeppelin": {
      "id": 765981595383857152,
      "img": "https://pbs.twimg.com/profile_images/1509629320649658380/9QINcb2f_normal.jpg"
    },
    "OrangeProtocol": {
      "id": 1440983608865411077,
      "img": "https://pbs.twimg.com/profile_images/1440988448752500742/3Zqg4r4p_normal.jpg"
    },
    "OurielOhayon": {
      "id": 918711,
      "img": "https://pbs.twimg.com/profile_images/1561381946516725762/r97jkd88_normal.png"
    },
    "OzzTheChris": {
      "id": 603738454,
      "img": "https://pbs.twimg.com/profile_images/1445790779004399616/7TE534Sl_normal.jpg"
    },
    "POKTnetwork": {
      "id": 789201646685392896,
      "img": "https://pbs.twimg.com/profile_images/1395858515156156421/Q7Wa_y4C_normal.jpg"
    },
    "ParallelTCG__": {
      "id": 1362289791379898370,
      "img": "https://pbs.twimg.com/profile_images/1491123866051043334/F97r-w8__normal.png"
    },
    "ParkerCardwell": {
      "id": 1487154020946898946,
      "img": "https://pbs.twimg.com/profile_images/1570415539121491971/3fxSjV_-_normal.jpg"
    },
    "Piotr_Saczuk": {
      "id": 1440352815403069447,
      "img": "https://pbs.twimg.com/profile_images/1534118040928927746/SeZV6VE6_normal.jpg"
    },
    "Potterlee222": {
      "id": 976600361464197120,
      "img": "https://pbs.twimg.com/profile_images/1467987168903581700/_g-MMsyG_normal.jpg"
    },
    "QomResearch": {
      "id": 1456987957223698441,
      "img": "https://pbs.twimg.com/profile_images/1561105367869923330/Y3_Go1BP_normal.jpg"
    },
    "RyanLucchese": {
      "id": 3886114574,
      "img": "https://pbs.twimg.com/profile_images/1542540332851757059/lL1ZL2vc_normal.jpg"
    },
    "SOCRATESxWEB3": {
      "id": 1141285766066106368,
      "img": "https://pbs.twimg.com/profile_images/1560102936415330304/Y_srzHwc_normal.jpg"
    },
    "SOLDIERweb3": {
      "id": 1513543578680803331,
      "img": "https://pbs.twimg.com/profile_images/1539174396643926017/KaJH311w_normal.jpg"
    },
    "STO_verse": {
      "id": 1460600482217537539,
      "img": "https://pbs.twimg.com/profile_images/1513833060613169156/shpvv10X_normal.jpg"
    },
    "Safaryclub": {
      "id": 1481775252594069505,
      "img": "https://pbs.twimg.com/profile_images/1533533844694913026/CpJYK1en_normal.png"
    },
    "SmEllen_Fresh": {
      "id": 906424448,
      "img": "https://pbs.twimg.com/profile_images/943549781334519809/63pdakJg_normal.jpg"
    },
    "SnowX_Thomas": {
      "id": 1312703919173242881,
      "img": "https://pbs.twimg.com/profile_images/1555281095683297280/QRV8NmND_normal.jpg"
    },
    "TJStone25": {
      "id": 1461814765664276481,
      "img": "https://pbs.twimg.com/profile_images/1544158825468633088/kTmM5_P8_normal.jpg"
    },
    "TalentProtocol": {
      "id": 1383059435111780352,
      "img": "https://pbs.twimg.com/profile_images/1507710515564498949/RKhV4OMv_normal.jpg"
    },
    "TallyCash": {
      "id": 1346646594314244097,
      "img": "https://pbs.twimg.com/profile_images/1448857004794159105/7QR2OL79_normal.jpg"
    },
    "TheDerrek": {
      "id": 25463841,
      "img": "https://pbs.twimg.com/profile_images/1457777649451864075/3eHr_NoM_normal.jpg"
    },
    "TheDivijGupta": {
      "id": 1379143382098907143,
      "img": "https://pbs.twimg.com/profile_images/1532533817545990144/-xoa7JhQ_normal.png"
    },
    "TheWitzCarlton": {
      "id": 426841535,
      "img": "https://pbs.twimg.com/profile_images/1548672387578732545/ghsDef9Y_normal.jpg"
    },
    "TimDraper": {
      "id": 20884310,
      "img": "https://pbs.twimg.com/profile_images/712463875975680000/yUVhpujj_normal.jpg"
    },
    "Timccopeland": {
      "id": 953233327238021120,
      "img": "https://pbs.twimg.com/profile_images/1550036770670125056/V2WXlOf__normal.jpg"
    },
    "VanessaGrellet_": {
      "id": 3166953201,
      "img": "https://pbs.twimg.com/profile_images/1557166815696093184/YS-hnnwN_normal.png"
    },
    "VitalikButerin": {
      "id": 295218901,
      "img": "https://pbs.twimg.com/profile_images/977496875887558661/L86xyLF4_normal.jpg"
    },
    "WalletConnect": {
      "id": 977233881668648960,
      "img": "https://pbs.twimg.com/profile_images/1549006291502243841/Lx0GJtn0_normal.png"
    },
    "WealtthS": {
      "id": 1237929416262639616,
      "img": "https://pbs.twimg.com/profile_images/1237929978097958914/orBfLqSo_normal.jpg"
    },
    "Web3Essentials": {
      "id": 1438668420971696130,
      "img": "https://pbs.twimg.com/profile_images/1438673722567798787/GbOvzr-I_normal.jpg"
    },
    "WoahBoyMusic": {
      "id": 150510571,
      "img": "https://pbs.twimg.com/profile_images/1504447004906303489/Pfz7jOhj_normal.jpg"
    },
    "XanteFi": {
      "id": 1431310663297613825,
      "img": "https://pbs.twimg.com/profile_images/1486508008121278467/r1t8aum7_normal.jpg"
    },
    "_TMVU": {
      "id": 1466798412582379521,
      "img": "https://pbs.twimg.com/profile_images/1562580758211862528/TzWtLQiZ_normal.jpg"
    },
    "_erfie": {
      "id": 1193413268,
      "img": "https://pbs.twimg.com/profile_images/1569075543466983425/UYTvm3ST_normal.jpg"
    },
    "_franzihei": {
      "id": 494256932,
      "img": "https://pbs.twimg.com/profile_images/1561013730711949313/vQWaLNG8_normal.jpg"
    },
    "_tessr": {
      "id": 107837944,
      "img": "https://pbs.twimg.com/profile_images/1487007256222785536/YhgPkFvO_normal.jpg"
    },
    "aadityak968": {
      "id": 775325928742236160,
      "img": "https://pbs.twimg.com/profile_images/1433552063619870724/eFIl6BAA_normal.jpg"
    },
    "aaronmkern": {
      "id": 181372550,
      "img": "https://pbs.twimg.com/profile_images/1212453858573737984/8cLpaqnE_normal.jpg"
    },
    "abal_eth": {
      "id": 1370428085531729937,
      "img": "https://pbs.twimg.com/profile_images/1516777298820743172/mD3nnviV_normal.jpg"
    },
    "ai": {
      "id": 13949232,
      "img": "https://pbs.twimg.com/profile_images/1485050791488483328/UNJ05AV8_normal.jpg"
    },
    "alaahd": {
      "id": 101467732,
      "img": "https://pbs.twimg.com/profile_images/1509297056292167682/LgMoPWgd_normal.jpg"
    },
    "alsoknownasLJ": {
      "id": 309276185,
      "img": "https://pbs.twimg.com/profile_images/1514898169536172034/gzfaV_RU_normal.jpg"
    },
    "anandx": {
      "id": 1490871,
      "img": "https://pbs.twimg.com/profile_images/1216580701807677440/sTxkIjUm_normal.jpg"
    },
    "andrewhong5297": {
      "id": 801246156340740096,
      "img": "https://pbs.twimg.com/profile_images/1436370413173592079/0yuubs2F_normal.jpg"
    },
    "anna_shakola": {
      "id": 1486316143992356866,
      "img": "https://pbs.twimg.com/profile_images/1486316335894351873/AhHpindM_normal.jpg"
    },
    "arbitrum": {
      "id": 1332033418088099843,
      "img": "https://pbs.twimg.com/profile_images/1490751860461953029/046qIxwT_normal.jpg"
    },
    "armanvaziri": {
      "id": 1492026984062337024,
      "img": "https://pbs.twimg.com/profile_images/1516928118144962560/BhLHlsYD_normal.jpg"
    },
    "banklessDAO": {
      "id": 1380589844838055937,
      "img": "https://pbs.twimg.com/profile_images/1389400052448247816/qsOU0pih_normal.jpg"
    },
    "bchesky": {
      "id": 12901712,
      "img": "https://pbs.twimg.com/profile_images/680250513951084544/yFwa_Sjd_normal.jpg"
    },
    "be0the1change": {
      "id": 1521240061437792259,
      "img": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
    },
    "blakeburrito": {
      "id": 25715899,
      "img": "https://pbs.twimg.com/profile_images/1565127210532487168/AyoYAEbx_normal.jpg"
    },
    "blindballer_": {
      "id": 453742743,
      "img": "https://pbs.twimg.com/profile_images/1324407065742368770/_DVAIwE0_normal.jpg"
    },
    "blockv_io": {
      "id": 879705117641117697,
      "img": "https://pbs.twimg.com/profile_images/1495755289936773121/f8qq-NTg_normal.jpg"
    },
    "boutellier_yves": {
      "id": 1380593146971762690,
      "img": "https://pbs.twimg.com/profile_images/1569028930421547009/9zNux1Gc_normal.jpg"
    },
    "bowensanders": {
      "id": 18119203,
      "img": "https://pbs.twimg.com/profile_images/1488568312661307398/hLsHeswL_normal.jpg"
    },
    "brian_armstrong": {
      "id": 14379660,
      "img": "https://pbs.twimg.com/profile_images/1516832438818770944/n77EwnKU_normal.png"
    },
    "brianjcho": {
      "id": 19317055,
      "img": "https://pbs.twimg.com/profile_images/1571184531998396417/pGkxOGBJ_normal.jpg"
    },
    "buddyofcult": {
      "id": 15530655,
      "img": "https://pbs.twimg.com/profile_images/1531674954529329152/c8D3PGOp_normal.jpg"
    },
    "cameron": {
      "id": 250980843,
      "img": "https://pbs.twimg.com/profile_images/1486881423160221696/WXgrwZ-o_normal.jpg"
    },
    "castig": {
      "id": 5352542,
      "img": "https://pbs.twimg.com/profile_images/1512314402254385155/_ArJ2M-5_normal.jpg"
    },
    "chapterone": {
      "id": 787810160513200129,
      "img": "https://pbs.twimg.com/profile_images/1523331584656506880/XTtnfEmx_normal.jpg"
    },
    "chlolands": {
      "id": 560784614,
      "img": "https://pbs.twimg.com/profile_images/1561809249230938112/KCrln0Wo_normal.jpg"
    },
    "cody_mccauley": {
      "id": 813853325556875264,
      "img": "https://pbs.twimg.com/profile_images/1546514727945310210/DsdefrLJ_normal.jpg"
    },
    "coinbase": {
      "id": 574032254,
      "img": "https://pbs.twimg.com/profile_images/1484586799921909764/A9yYenz3_normal.png"
    },
    "cooldaram": {
      "id": 1432694110075428868,
      "img": "https://pbs.twimg.com/profile_images/1560297139666026497/JEPyyhvC_normal.jpg"
    },
    "dappcon_berlin": {
      "id": 999979500543897600,
      "img": "https://pbs.twimg.com/profile_images/1493918791922860034/ACmpNYkZ_normal.jpg"
    },
    "davidesilverman": {
      "id": 1967549388,
      "img": "https://pbs.twimg.com/profile_images/1385255657121648642/wH8x29FW_normal.jpg"
    },
    "ddasattack": {
      "id": 848600268807733250,
      "img": "https://pbs.twimg.com/profile_images/1479716713570529282/D4P-ubxL_normal.jpg"
    },
    "defi_jay": {
      "id": 1428336893415075845,
      "img": "https://pbs.twimg.com/profile_images/1558271275159650306/f_wTRaVG_normal.jpg"
    },
    "dgmason": {
      "id": 137425713,
      "img": "https://pbs.twimg.com/profile_images/1450459906709020681/Ue6ssLvO_normal.jpg"
    },
    "dgvisuals_ai": {
      "id": 885680070,
      "img": "https://pbs.twimg.com/profile_images/1561783099121442819/6yyb0kUV_normal.jpg"
    },
    "eastban120": {
      "id": 137137265,
      "img": "https://pbs.twimg.com/profile_images/1459625371058458633/O5u0XxMS_normal.jpg"
    },
    "elonmusk": {
      "id": 44196397,
      "img": "https://pbs.twimg.com/profile_images/1569943778198437888/iy7_UX5j_normal.jpg"
    },
    "esthercrawford": {
      "id": 14501624,
      "img": "https://pbs.twimg.com/profile_images/1525477181811351552/nNfADJjP_normal.jpg"
    },
    "ethsign": {
      "id": 1366569623303254021,
      "img": "https://pbs.twimg.com/profile_images/1366600332420079616/obK54dle_normal.jpg"
    },
    "ethtomato": {
      "id": 87379433,
      "img": "https://pbs.twimg.com/profile_images/1523384275290128384/PsQ-iFD5_normal.png"
    },
    "f_biviano": {
      "id": 2738942788,
      "img": "https://pbs.twimg.com/profile_images/1483033737814323203/OhqSolTo_normal.jpg"
    },
    "fedetabakman": {
      "id": 153072350,
      "img": "https://pbs.twimg.com/profile_images/876501946475180032/ioRW8KCR_normal.jpg"
    },
    "fortmatic": {
      "id": 996029264444121093,
      "img": "https://pbs.twimg.com/profile_images/1293288961800933376/rtDOqMXY_normal.jpg"
    },
    "francescoswiss": {
      "id": 4260074967,
      "img": "https://pbs.twimg.com/profile_images/1442572387921235969/SEmY9Fu-_normal.jpg"
    },
    "galaxy_adams": {
      "id": 3433627179,
      "img": "https://pbs.twimg.com/profile_images/1569330438652452864/4x2NiQvO_normal.jpg"
    },
    "geoist_": {
      "id": 169163425,
      "img": "https://pbs.twimg.com/profile_images/1505949793180336130/y4wdakzl_normal.jpg"
    },
    "getpipcom": {
      "id": 1454084218368057351,
      "img": "https://pbs.twimg.com/profile_images/1454086230556430336/qE35Vvc4_normal.jpg"
    },
    "gitcoin": {
      "id": 856446453157376003,
      "img": "https://pbs.twimg.com/profile_images/1565017773453049857/HErNeU2S_normal.jpg"
    },
    "gmdotxyz": {
      "id": 1321899068591906816,
      "img": "https://pbs.twimg.com/profile_images/1465684492304191491/UAhrXE4i_normal.jpg"
    },
    "hatskier_me": {
      "id": 1422971459148951554,
      "img": "https://pbs.twimg.com/profile_images/1527441532873236490/T12uv8Q7_normal.jpg"
    },
    "headcpx": {
      "id": 559618987,
      "img": "https://pbs.twimg.com/profile_images/1510977376456351746/_C5LXRQg_normal.jpg"
    },
    "henryboldi": {
      "id": 524914455,
      "img": "https://pbs.twimg.com/profile_images/1461786745805094912/DivzHN6C_normal.jpg"
    },
    "hexxy0x": {
      "id": 1060578150013435905,
      "img": "https://pbs.twimg.com/profile_images/1554290299949686784/KRlpKT_T_normal.jpg"
    },
    "hey_wallet": {
      "id": 1429076224756916228,
      "img": "https://pbs.twimg.com/profile_images/1517216245573115906/2RD9YphA_normal.jpg"
    },
    "heyitscbh": {
      "id": 700929919,
      "img": "https://pbs.twimg.com/profile_images/1477720121317773313/8_mOTzEF_normal.jpg"
    },
    "iSpeakComedy": {
      "id": 255168531,
      "img": "https://pbs.twimg.com/profile_images/1561696278551187458/4TmvdlJj_normal.jpg"
    },
    "ianlapham": {
      "id": 887744028023894017,
      "img": "https://pbs.twimg.com/profile_images/1567268843936010240/y_aG2iKD_normal.jpg"
    },
    "issa_john_": {
      "id": 4727035637,
      "img": "https://pbs.twimg.com/profile_images/753628092275494912/T-231ZvD_normal.jpg"
    },
    "itstimconnors": {
      "id": 273565626,
      "img": "https://pbs.twimg.com/profile_images/1507395617743532037/-J0l8tqp_normal.jpg"
    },
    "j0xseph": {
      "id": 1483370488239992834,
      "img": "https://pbs.twimg.com/profile_images/1483371283404492800/-yZg1QD6_normal.jpg"
    },
    "jafetsc": {
      "id": 37240063,
      "img": "https://pbs.twimg.com/profile_images/1550496644948451330/LsWKMgfR_normal.jpg"
    },
    "jazzthebear": {
      "id": 753223959672397824,
      "img": "https://pbs.twimg.com/profile_images/1016776647352176645/3J_APEy9_normal.jpg"
    },
    "jbrukh": {
      "id": 14592709,
      "img": "https://pbs.twimg.com/profile_images/1484518891938275328/fnnyCQOR_normal.jpg"
    },
    "jessicasmw": {
      "id": 2903026983,
      "img": "https://pbs.twimg.com/profile_images/1521022283300622336/MxQzzWHz_normal.jpg"
    },
    "kazsatamai": {
      "id": 273527453,
      "img": "https://pbs.twimg.com/profile_images/1557535992298369025/-xVz9wO0_normal.jpg"
    },
    "keinan_ziv": {
      "id": 938691774549291009,
      "img": "https://pbs.twimg.com/profile_images/1222554078888308736/NzaSjWHZ_normal.jpg"
    },
    "kennethchongeth": {
      "id": 1266388393,
      "img": "https://pbs.twimg.com/profile_images/1564791985684242434/U-4IuBxc_normal.jpg"
    },
    "kit_eth": {
      "id": 1247116962603266049,
      "img": "https://pbs.twimg.com/profile_images/1534950683157356545/OJ-aicWj_normal.jpg"
    },
    "kudztaziva": {
      "id": 178018088,
      "img": "https://pbs.twimg.com/profile_images/1515658476533403648/bEgOat8U_normal.jpg"
    },
    "kunal_modi": {
      "id": 166871945,
      "img": "https://pbs.twimg.com/profile_images/1498355725369630721/Lay-ABCf_normal.jpg"
    },
    "larfy_rothwell": {
      "id": 1116253713511768064,
      "img": "https://pbs.twimg.com/profile_images/1528140885275332608/BCppI8QM_normal.jpg"
    },
    "letsraave": {
      "id": 1448638253070966789,
      "img": "https://pbs.twimg.com/profile_images/1570400706435158018/mv6wHOrD_normal.jpg"
    },
    "levychain": {
      "id": 2351123413,
      "img": "https://pbs.twimg.com/profile_images/1528864539680178176/mK4w3AFY_normal.jpg"
    },
    "loukerner": {
      "id": 46920783,
      "img": "https://pbs.twimg.com/profile_images/1495115230765936642/C6_op3kP_normal.jpg"
    },
    "magdalenakala": {
      "id": 259028293,
      "img": "https://pbs.twimg.com/profile_images/1502693195234304002/vE350uvP_normal.jpg"
    },
    "matt_doggo": {
      "id": 1524739036224659457,
      "img": "https://pbs.twimg.com/profile_images/1556645833419984899/8AYP5qrM_normal.jpg"
    },
    "matthewegould": {
      "id": 1215564264,
      "img": "https://pbs.twimg.com/profile_images/1542914271503192064/waMF_tPR_normal.jpg"
    },
    "mattysino": {
      "id": 14206218,
      "img": "https://pbs.twimg.com/profile_images/1569833016595300353/wEI_wJJ3_normal.jpg"
    },
    "mbarboza80": {
      "id": 1461830599296135169,
      "img": "https://pbs.twimg.com/profile_images/1561082993896292360/yHb1sF6N_normal.jpg"
    },
    "mdhoffschmidt": {
      "id": 1205032076384329729,
      "img": "https://pbs.twimg.com/profile_images/1528750078638399491/jWbPUsex_normal.jpg"
    },
    "mdudas": {
      "id": 7184612,
      "img": "https://pbs.twimg.com/profile_images/1563930379471437825/s1_ZQKm8_normal.jpg"
    },
    "mhluongo": {
      "id": 16179805,
      "img": "https://pbs.twimg.com/profile_images/1519710359254405121/DJ2c1Mnk_normal.jpg"
    },
    "mikeaz1": {
      "id": 21429841,
      "img": "https://pbs.twimg.com/profile_images/1519382237627785224/YzHLGR6M_normal.jpg"
    },
    "mikemcg0": {
      "id": 4700470641,
      "img": "https://pbs.twimg.com/profile_images/1510973090578280450/vIwY4RJH_normal.jpg"
    },
    "missteencrypto": {
      "id": 1253392898638450688,
      "img": "https://pbs.twimg.com/profile_images/1541523027225198595/3ojCn4cS_normal.jpg"
    },
    "mitchelljhammer": {
      "id": 1225944444865826820,
      "img": "https://pbs.twimg.com/profile_images/1546937990324387845/a0ppFLTZ_normal.jpg"
    },
    "mkamoako": {
      "id": 1469132076633014274,
      "img": "https://pbs.twimg.com/profile_images/1534626786746695682/XoWfJfgM_normal.jpg"
    },
    "mongolraider": {
      "id": 4679024540,
      "img": "https://pbs.twimg.com/profile_images/1569543289547661312/GefzzQ58_normal.jpg"
    },
    "mydomexyz": {
      "id": 1519331742980706306,
      "img": "https://pbs.twimg.com/profile_images/1531370535673860096/KfWsaaQ2_normal.jpg"
    },
    "naxsun3301": {
      "id": 949235658224230400,
      "img": "https://pbs.twimg.com/profile_images/1331902606512435203/vb0jesTs_normal.jpg"
    },
    "oderint_eth": {
      "id": 1532117469628071936,
      "img": "https://pbs.twimg.com/profile_images/1553060231743422464/AQIagTNc_normal.jpg"
    },
    "ohhshiny": {
      "id": 1318987223232999424,
      "img": "https://pbs.twimg.com/profile_images/1569657135377829889/XnrokTkd_normal.jpg"
    },
    "optimismFND": {
      "id": 1044836083530452992,
      "img": "https://pbs.twimg.com/profile_images/1510410375140945927/JtpX95Rt_normal.jpg"
    },
    "pcbo": {
      "id": 19069127,
      "img": "https://pbs.twimg.com/profile_images/1565808871184244736/4mKCLGxb_normal.jpg"
    },
    "pedrolandinx": {
      "id": 1493313768717119489,
      "img": "https://pbs.twimg.com/profile_images/1545372610795634690/uF-RU5-i_normal.jpg"
    },
    "pedrouid": {
      "id": 823546213,
      "img": "https://pbs.twimg.com/profile_images/1494048200013094914/WFTsIGEr_normal.jpg"
    },
    "pimpstar_2": {
      "id": 1429214135590526982,
      "img": "https://pbs.twimg.com/profile_images/1445491494140272647/tOdbk2sS_normal.jpg"
    },
    "pmpinedo": {
      "id": 78065213,
      "img": "https://pbs.twimg.com/profile_images/1562467424745959425/GDAs-nRS_normal.png"
    },
    "poapxyz": {
      "id": 1096560334880399361,
      "img": "https://pbs.twimg.com/profile_images/1531393031022202881/06ZFPE_b_normal.jpg"
    },
    "polygonscan": {
      "id": 1394982824243957763,
      "img": "https://pbs.twimg.com/profile_images/1405837960298196999/afEOtglW_normal.jpg"
    },
    "ppeplinsky": {
      "id": 1487924011384381442,
      "img": "https://pbs.twimg.com/profile_images/1562541444589559812/l7Nn-h8O_normal.jpg"
    },
    "proctar": {
      "id": 291605058,
      "img": "https://pbs.twimg.com/profile_images/1443162336932605957/qr-I6zEP_normal.jpg"
    },
    "rabbithole_gg": {
      "id": 1254192452522696705,
      "img": "https://pbs.twimg.com/profile_images/1438893096998146051/rcnWPNuz_normal.jpg"
    },
    "ranjan3118": {
      "id": 700851955,
      "img": "https://pbs.twimg.com/profile_images/1554752928975425536/FrWrtxdI_normal.jpg"
    },
    "rasha_hantash": {
      "id": 1222314809481400320,
      "img": "https://pbs.twimg.com/profile_images/1427486779590987778/lzq-gXNI_normal.jpg"
    },
    "redstone_defi": {
      "id": 1294053547630362630,
      "img": "https://pbs.twimg.com/profile_images/1405602838915522562/jf6E8c-K_normal.png"
    },
    "rekmarks": {
      "id": 716072631871606784,
      "img": "https://pbs.twimg.com/profile_images/986010009954869253/BzUPbXWq_normal.jpg"
    },
    "rjrushmore": {
      "id": 16150398,
      "img": "https://pbs.twimg.com/profile_images/1283495054565310465/0jKTI5uq_normal.jpg"
    },
    "ruhelahmed95": {
      "id": 996870858626002946,
      "img": "https://pbs.twimg.com/profile_images/1212892517873659904/2ZZAtFMi_normal.jpg"
    },
    "safe": {
      "id": 8467082,
      "img": "https://pbs.twimg.com/profile_images/1566773491764023297/IvmCdGnM_normal.jpg"
    },
    "salondaonyc": {
      "id": 1504160483468849158,
      "img": "https://pbs.twimg.com/profile_images/1506051967520550916/JgY45LaB_normal.jpg"
    },
    "samscamspam": {
      "id": 1275408279863275521,
      "img": "https://pbs.twimg.com/profile_images/1559998056967405573/Ju4iamvX_normal.jpg"
    },
    "sandeepnailwal": {
      "id": 100798845,
      "img": "https://pbs.twimg.com/profile_images/1569822111132258306/xGNuwmk3_normal.jpg"
    },
    "scstar": {
      "id": 60646144,
      "img": "https://pbs.twimg.com/profile_images/1380921144375656449/eIs9wSQt_normal.jpg"
    },
    "shanvasion": {
      "id": 1438575484368007173,
      "img": "https://pbs.twimg.com/profile_images/1529265929934217219/_E7jBVlD_normal.jpg"
    },
    "sjdthree1": {
      "id": 947213688464990208,
      "img": "https://pbs.twimg.com/profile_images/1532796066210324480/FZ4gOTLd_normal.jpg"
    },
    "sslisen": {
      "id": 826617226623057920,
      "img": "https://pbs.twimg.com/profile_images/1564064236451418113/0bxuCqzV_normal.jpg"
    },
    "straightupjac": {
      "id": 573352242,
      "img": "https://pbs.twimg.com/profile_images/1473489725323243522/Oc8dN20B_normal.jpg"
    },
    "sui414": {
      "id": 767119245851459584,
      "img": "https://pbs.twimg.com/profile_images/1560055518701334528/37BQdJSz_normal.jpg"
    },
    "sys1221": {
      "id": 1237415288389287936,
      "img": "https://pbs.twimg.com/profile_images/1525888105596653568/CY76n53T_normal.jpg"
    },
    "takuyakitagawa": {
      "id": 80660347,
      "img": "https://pbs.twimg.com/profile_images/1044015435581140993/EIXWSkpR_normal.jpg"
    },
    "terkastarostova": {
      "id": 1369003317301551108,
      "img": "https://pbs.twimg.com/profile_images/1369003500739452933/FKGxUd_6_normal.jpg"
    },
    "theNFThinker": {
      "id": 1412886659583119363,
      "img": "https://pbs.twimg.com/profile_images/1454245157327544320/LLw9Fjpr_normal.jpg"
    },
    "thegoodzombies": {
      "id": 734807498570534912,
      "img": "https://pbs.twimg.com/profile_images/1472638491351736323/9cRfbdXJ_normal.jpg"
    },
    "treecz": {
      "id": 158622600,
      "img": "https://pbs.twimg.com/profile_images/1294532489558589440/I8V3MDXC_normal.jpg"
    },
    "tropoFarmer": {
      "id": 16273846,
      "img": "https://pbs.twimg.com/profile_images/1547001359622438912/1tITuXmH_normal.png"
    },
    "tyler": {
      "id": 24222556,
      "img": "https://pbs.twimg.com/profile_images/1489425592739053570/RafStk7c_normal.jpg"
    },
    "unbankdco": {
      "id": 2880107732,
      "img": "https://pbs.twimg.com/profile_images/1047947429222346752/wwGq5FMn_normal.jpg"
    },
    "unionprotocol": {
      "id": 1204625363353001984,
      "img": "https://pbs.twimg.com/profile_images/1491891244376772616/5W2BAk92_normal.png"
    },
    "unstoppableweb": {
      "id": 1101647425867902976,
      "img": "https://pbs.twimg.com/profile_images/1494097574613057541/gATQxSnP_normal.jpg"
    },
    "valentinaaro": {
      "id": 1260685961693978637,
      "img": "https://pbs.twimg.com/profile_images/1410459473425014789/xP6wRS20_normal.jpg"
    },
    "venturecounsl": {
      "id": 1377711845054816257,
      "img": "https://pbs.twimg.com/profile_images/1381383816661643264/51pxR_Ts_normal.jpg"
    },
    "wabisabidao": {
      "id": 1404159484239429643,
      "img": "https://pbs.twimg.com/profile_images/1504885837204492289/Lrudrpex_normal.jpg"
    },
    "wanye68394762": {
      "id": 1371602128146403328,
      "img": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"
    },
    "wearecultdao": {
      "id": 1482787383418499075,
      "img": "https://pbs.twimg.com/profile_images/1482793670688575492/quxZPrbC_normal.jpg"
    },
    "web3talks": {
      "id": 1452383632933392393,
      "img": "https://pbs.twimg.com/profile_images/1521251540241207300/8EGZEiH8_normal.png"
    },
    "witnet_io": {
      "id": 955794358242029568,
      "img": "https://pbs.twimg.com/profile_images/1539931396944322560/mnYGgJbY_normal.png"
    },
    "worthalter": {
      "id": 14739890,
      "img": "https://pbs.twimg.com/profile_images/1544690687714672640/3TxH8_vW_normal.jpg"
    },
    "zapper_fi": {
      "id": 1208076242366283776,
      "img": "https://pbs.twimg.com/profile_images/1554215313251749889/nwriicTp_normal.jpg"
    },
    "zerion_io": {
      "id": 895030804383969283,
      "img": "https://pbs.twimg.com/profile_images/1545425456199045121/CEciqDtp_normal.jpg"
    },
    "zoebringsjoy": {
      "id": 967983575554449408,
      "img": "https://pbs.twimg.com/profile_images/1421740080280965131/wmWzAAXL_normal.jpg"
    },
    "zypsycom": {
      "id": 965302183179636736,
      "img": "https://pbs.twimg.com/profile_images/1408322649915199489/CkI1RPoI_normal.jpg"
    }
  }
}

@app.route("/auth", methods=["GET"])
def twitterauth():
    """
    Start Twitter Authentication process.

    Returns:
    url (string): Twitter authorization url. Open so that user can confirm application.

    """

    global oauth1_user_handler
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SEC"),
        callback="https://givewithporuka.pythonanywhere.com/callback"
    )

    url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

    response = make_response({"url": url}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/callback")
def callback():
    """
    Twitter callback handler.

    Returns:
    redirect: bring user back to index, now with Twitter account information

    """

    global oauth1_user_handler
    global twitterCounter
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        request.args['oauth_verifier']
    )

    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SEC"),
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    id_ = client._get_authenticating_user_id(oauth_1=True)
    clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
    user = clientT.get_user(id=id_, user_fields=["username", "id", "profile_image_url"])
    twitterCounter += 1
    profile_image_url = user.data.profile_image_url
    username = user.data.username
    params = {"id": id_, "username": username, "img": profile_image_url}

    return redirect("https://poruka-new.vercel.app/connect?"+urllib.parse.urlencode(params))


@app.route("/v1/getTwitterIDs", methods=["GET"])
def getTwitterIDs():
    """
    Translate Twitter usernames to Twitter IDs.

    IDriss Twitter handles are translated to IDs so that a given
    link does not disappear whenever someone changes the Twitter username.

    Parameters:
    names (string): comma-separated list of Twitter usernames. Max-length: 100 names.

    Returns:
    result (dict): Key-Value pairs of Twitter usernames and Twitter IDs.

    """
    try:
        global twitterCounter
        clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        twitter_ids = clientT.get_users(usernames=",".join([x.strip("@") for x in request.args["names"].split(",")]), user_fields=["id"])
        twitterCounter += 1
        res_ids = {u.username: u.id for u in twitter_ids.data}
    except Exception as e:
        print(str(e))
        res_ids = "No ids found"
    response = make_response({"result": res_ids}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/v1/getTwitterNames", methods=["GET"])
def getTwitterNames():
    """
    Translate Twitter IDs to Twitter usernames.

    IDriss Twitter handles are translated to IDs so that a given
    link does not disappear whenever someone changes the Twitter username.
    Translation from IDs to usernames is needed after reverse resolving.

    Parameters:
    ids (string): comma-separated list of Twitter user IDs. Max-length: 100 IDs.

    Returns:
    result (dict): Key-Value pairs of Twitter IDs and Twitter usernames.

    """
    try:
        global twitterCounter
        clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        twitter_names = clientT.get_users(ids=",".join([str(x) for x in request.args["ids"].split(",")]), user_fields=["username"])
        twitterCounter += 1
        res_names = {u.id: u.username for u in twitter_names.data}
    except Exception as e:
        print(str(e))
        res_names = "No names found"
    response = make_response({"result": res_names}, 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/getFollowing', methods=["GET"])
def get_follower():
    """
    Retrieve user information of people a given user is following.

    Call after Twitter username of user is known
    (sign-in with Twitter or IDriss reverse resolving) and
    display a list of contacts.

    Parameters:
    id (string): Twitter user ID of given (verified) user.

    Returns:
    result (dict): Nested Key-Value pairs of Twitter usernames to Twitter IDs and profile picture source.
    Example:
        {
            "givewithporuka": {
                "id": "1570867755661889541",
                "img": "https://pbs.twimg.com/profile_images/1570925543473684480/GF3RTo7W_bigger.jpg"
            }
        }

    Warning: Rate limits 15 requests per 15 mins

    """
    try:
        # following = {}
        # global twitterCounter
        # clientT = tweepy.Client(bearerToken[twitterCounter % len(bearerToken)])
        # for response in tweepy.Paginator(clientT.get_users_following, request.args["id"], user_fields=["username", "id", "profile_image_url"], max_results=1000):
        #     if response.data:
        #         following = {**following, **{u.username: {"id": u.id, "img": u.profile_image_url} for u in response.data}}
        # twitterCounter += 1
        response = make_response(dummyRet, 200)
    except Exception as e:
        print(e)
        following = {}
        response = make_response({"result": following}, 429)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)
