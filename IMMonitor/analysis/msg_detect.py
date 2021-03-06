import json
from urllib.parse import urlencode
import requests
from aip import AipSpeech
import base64
# from IMMonitor.analysis import ACCESS_TOKEN, DETECT_URL_IMG, DETECT_URL_TEXT

APP_ID = '15674182'
API_KEY = 'X4gVrgxTl4KbqjAtOnMf0BCs'
SECRET_KEY = 'ofOfsvyKXlNpxEIADp2MkNbZitm6kDRL'
ACCESS_TOKEN = '24.ad351b35b33ecadfead85aec0b556ebf.2592000.1554274477.282335-15674182'
DETECT_URL_IMG = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/user_defined"
DETECT_URL_TEXT = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam'

def detect_image(image):
    """
    图像检测
    :param image: 二进制图像
    :param access_token: 百度AI平台access_token
    :return:
    成功返回：
    log_id:请求唯一id,必须
    rtype:Long

    conclusion:审核结果描述，成功才返回，失败不返回，可取值 1.合规, 2.不合规, 3.疑似, 4.审核失败，不必须
    rtype:string

    conclusionType:审核结果标识，成功才返回，失败不返回，可取值1:合规, 2:不合规, 3:疑似, 4:审核失败，不必须
    rtype:uint64

    data:审核项详细信息，响应成功并且conclusion为疑似或不合规时才返回，响应失败或conclusion为合规是不返回。不必须
    rtype:object[]

    +type:审核类型，1：色情、2：性感、3：暴恐、4:恶心、5：水印码、6：二维码、7：条形码、8：政治人物、9：敏感词、10：自定义敏感词,不必须
    rtype:Integer

    +msg:不合规项描述信息,不必须
    rtype:String

    +probability:不合规项置信度,不必须
    rtype:double

    +stars:政治人物列表数组，只有政治人物审核不通过才有,不必须
    rtype:object[]

    +words:审核不通过敏感词，只有敏感词审核不通过才有，不必须
    rtype:string

    失败返回：
    error_code:错误提示码，失败才返回，成功不返回,不必须
    rtype:uint64

    error_msg:错误提示信息，失败才返回，成功不返回，不必须
    rtype:string

    +error_code:内层错误提示码，底层服务失败才返回，成功不返回，不必须
    rtype:uint64

    +error_msg:内层错误提示信息，底层服务失败才返回，成功不返回，不必须
    rtype:string

    """
    # 待审核图片Base64编码字符串
    f = open(image, 'rb')
    image = base64.b64encode(f.read())
    # 二进制方式打开图片文件
    params = {"image": image}
    params = urlencode(params)

    # 百度人工智能API请求
    request_url = DETECT_URL_IMG + "?access_token=" + ACCESS_TOKEN
    res = requests.post(request_url, data=params)
    res_data = res.content.decode('utf-8')
    res_dict = json.JSONDecoder().decode(res_data)
    return res_dict


def detect_text(text, access_token):
    """
    文字检测
    :param text: 检测文字
    :param access_token: 百度AI平台access_token
    :return:
    成功返回：
    logid:正确调用生成的唯一标识码，用于问题定位
    rtype:uint64

    result:包含审核结果详情
    rtype:object

    +spam:请求中是否包含违禁，0表示非违禁，1表示违禁，2表示建议人工复审
    rtype:int

    +reject:审核未通过的类别列表与详情
    rtype:array

    +review:待人工复审的类别列表与详情
    rtype:array

    +pass:审核通过的类别列表与详情
    rtype:array

    ++label:请求中的违禁类型,1:暴恐违禁，2：文本色情，3：政治敏感，4：恶意推广，5：低俗辱骂，6：低质灌水
    rtype:int

    ++score:违禁检测分，范围0~1，数值从低到高代表风险程度的高低
    rtype:float

    ++hit:违禁类型对应命中的违禁词集合，可能为空
    rtype:array

    失败返回：
    error_code:错误提示码，失败才返回，成功不返回,不必须
    rtype:uint64

    error_msg:错误提示信息，失败才返回，成功不返回，不必须
    rtype:string
    """
    params = {"content": text}
    params = urlencode(params)
    # 百度人工智能API请求示例
    request_url = DETECT_URL_TEXT + "?access_token=" + ACCESS_TOKEN
    res = requests.post(request_url, data=params)
    res_data = res.content.decode('utf-8')
    res_dict = json.JSONDecoder().decode(res_data)
    return res_dict.get('result')
	
def recognize_speech(voice):
    """
    语音识别
    :param voice:语音文件的格式，pcm 或者 wav 或者 amr
    :param access_token: 百度AI平台access_token
    :return:
    --------------------------------------------------------------------------------------------
    参数	    |  类型	|是否一定输出	| 描述
    err_no	|  int	|    是	    | 错误码
    err_msg	|  int	|    是	    | 错误码描述
    sn	    |  int	|    是	    | 语音数据唯一标识，系统内部产生，用于 debug
    result	|  int	|    是	    | 识别结果数组，提供1-5 个候选结果，string 类型为识别的字符串， utf-8 编码
    --------------------------------------------------------------------------------------------
    成功返回：
    {
    "err_no": 0,
    "err_msg": "success.",
    "corpus_no": "15984125203285346378",
    "sn": "481D633F-73BA-726F-49EF-8659ACCC2F3D",
    "result": ["北京天气"]
    }
    失败返回：
    {
    "err_no": 2000,
    "err_msg": "data empty.",
    "sn": null
    }
    """
    data = 'ffmpeg -y  -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm'%(voice,voice)
    os.popen(data)
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 读取文件
    with open(voice + ".pcm", 'rb') as fp:
        # return fp.read()
        res_dict = client.asr(fp.read(),'pcm',16000, {'dev_pid': '1537'})
        if "result" not in res_dict:
            return res_dict
        else:
            result = res_dict["result"][0]
            return result