import datetime
import requests
from ast import literal_eval

import dns.resolver
from ping3 import ping
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView, Response

def get_ip46_address(address):
    req = requests.get(address).text
    data = literal_eval(req)
    return data.get("ip")
    
class DomainCheckView(APIView):

    def get(self, request):

        domain = request.query_params.get('domain')

        ipv4 = "http://testipv6.cn/ip/?callback="
        ipv6 = "http://ipv6.testipv6.cn/ip/?callback="
        cdn_url = "https://cdn.poizon.com/node-common/2aa395c3c2257c5010d0c17569f794af.png"
        status = HTTP_200_OK
        
        try:
            dns_resolver = dns.resolver.Resolver()
            # 获取cdn
            cdn = requests.get(cdn_url, stream = True)
            ip_port = cdn.raw._connection.sock.getpeername()
            address = "{}:{}".format(ip_port[0], ip_port[1])
            cdn_str = "status_code:{}\nx-cache:{}\neagleid:{}\ndata:{}\naddress:{}".format(
                            cdn.status_code,
                            cdn.headers.get("X-Cache"),
                            cdn.headers.get("EagleId"),
                            None,
                            address
                        )
            # 获取ping值
            count, times = 1, []
            res = ping(domain)
            if res:
                times.append(res)

            data = {
                "status":  HTTP_200_OK,
                "data": {
                    "ipv4": get_ip46_address(ipv4),
                    "ipv6": get_ip46_address(ipv6),
                    "localdns": dns_resolver.nameservers[0],
                    "pinginfo": sum(times) / count if times else "域名PING超时",
                    "checktime": datetime.datetime.utcnow().isoformat(),
                    "mediacdn": cdn_str
                }
            }

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            data = {
                "status": HTTP_400_BAD_REQUEST,
                "msg": "获取IP地址失败",
                "data": {
                    "ipv4": "",
                    "ipv6": "",
                    "localdns": "",
                    "pinginfo": "",
                    "checktime": datetime.datetime.utcnow().isoformat(),
                    "mediacdn": ""
                }
            }

        return Response(status=status, data = data)