import configparser
import requests


def getXmlValue(dom, node):
    try:
        return dom.getElementsByTagName(node)[0].firstChild.nodeValue
    except Exception as e:
        # return e.args[0]
        return "ERROR"


def getConfigReader():
    config = configparser.ConfigParser()
    config.read('datas/config.ini')

    try:
        baud_rate = config['Reader']['baud_rate']
        com_port = config['Reader']['com_port']
        bc_prefix = config['Reader']['bc_prefix']
        timeout = float(config['Reader']['timeout'])
        switch_pairs = int(config['Reader']['rfid_switch_pairs'])
        convert_to_dec = int(config['Reader']['rfid_convert_to_dec'])
    except Exception as error:
        raise RuntimeError('config Reader parameter missing') from error

    return [baud_rate, com_port, bc_prefix, timeout, switch_pairs, convert_to_dec]


def getConfigRequestParams():
    config = configparser.ConfigParser()
    config.read('datas/config.ini')

    try:
        url = config['Request']['url']
        user = config['Request']['user']
        password = config['Request']['password']
        timeout = int(config['Request']['timeout'])
    except Exception as error:
        raise RuntimeError('config Request parameter missing') from error

    # ----- Config Read URL Parameters -----
    url_barcode = ''
    url_rfid = ''
    url_params = ''
    param = ''

    for i in range(1, 10):
        try:
            param = config['Request']['req_param_' + str(i)]
        except:
            pass
        finally:
            if (param != ''):
                if (url_params == ''):
                    url_params = '?'
                else:
                    url_params += '&'

            url_params += param
            param = ''

    try:
        url_barcode = config['Request']['req_barcode']
    except:
        pass

    try:
        url_rfid = config['Request']['req_rfid']
    except:
        pass

    return [url, user, password, timeout, url_params, url_barcode, url_rfid]
    # ----- Config Read URL Parameters -----


def GetRequest(req_params, barcode, rfid):
    if (len(req_params) < 7):
        raise RuntimeError('config parameter Error')

    url = req_params[0]
    user = req_params[1]
    password = req_params[2]
    timeout = req_params[3]
    url_params = req_params[4]
    url_barcode = req_params[5]
    url_rfid = req_params[6]

    # Make Request URL
    if (url_barcode != '' and barcode != ''):
        if (url_params == ''):
            url_params = '?' + url_barcode + '=' + barcode
        else:
            url_params += '&' + url_barcode + '=' + barcode

    if (url_rfid != '' and rfid != ''):
        if (url_params == ''):
            url_params = '?' + url_rfid + '=' + rfid
        else:
            url_params += '&' + url_rfid + '=' + rfid

    try:
        r = requests.get(url + url_params,
                         auth=(user, password), timeout=timeout)
    except requests.exceptions.Timeout as error:
        raise RuntimeError('Timeout') from error
    except requests.exceptions.HTTPError as error:
        raise RuntimeError('HTTP Error') from error
    except requests.exceptions.ConnectionError as error:
        raise RuntimeError('Connection Error') from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError('RequestException Error') from error
    except Exception as err:
        raise RuntimeError('Other Error') from error

    if r.status_code != 200:
        raise RuntimeError('Status Code:' + r.status_code)

    return r.text


def getHostConfig():
    config = configparser.ConfigParser()
    config.read('datas/config.ini')

    try:
        url = config['GetHost']['url']
        username = config['GetHost']['username']
        password = config['GetHost']['password']
    except Exception as error:
        raise RuntimeError('getHostConfig parameter missing') from error

    return [url, username, password]
