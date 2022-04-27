import datetime
import requests
from ast import literal_eval

import dns.resolver
from ping3 import ping
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView, Response


SHA_TZ = datetime.timezone(
    datetime.timedelta(hours=8),
    name='Asia/Shanghai',
)

def get_ip46_address(address):
    req = requests.get(address).text
    data = literal_eval(req)
    return data.get("ip")
    
class DomainCheckView(APIView):

    def get(self, request):

        domain = request.query_params.get('domain')

        ipv4_url = "http://testipv6.cn/ip/?callback="
        ipv6_url = "http://ipv6.testipv6.cn/ip/?callback="
        cdn_url = "https://cdn.poizon.com/node-common/2aa395c3c2257c5010d0c17569f794af.png"
        status = HTTP_200_OK
        cur_date = datetime.datetime.now(SHA_TZ).strftime('%Y-%m-%d %H:%M:%S')

        ipv4, ipv6, dns_value, pinginfo, cdn_str = "", "", "", "", ""
        try:
            ipv4 = get_ip46_address(ipv4_url)
            ipv6 = get_ip46_address(ipv6_url)

            dns_resolver = dns.resolver.Resolver()
            dns_value = dns_resolver.nameservers[0]
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
                
            pinginfo = round((sum(times) / count) * 1000) if times else "域名PING超时"
            
            data = {"status":  HTTP_200_OK}

        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            data = {
                "status": HTTP_400_BAD_REQUEST,
                "msg": "获取IP地址失败",
            }

        data["data"] = {
                "ipv4": ipv4,
                "ipv6": ipv6,
                "localdns": dns_value,
                "pinginfo": pinginfo,
                "checktime": cur_date,
                "mediacdn": cdn_str
            }

        return Response(status=status, data = data)