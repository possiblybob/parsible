import re
import urlparse

def parse_nginx_collect(line):
    regex = re.compile("(?P<ip_address>\S*)\s-\s(?P<requesting_user>\S*)\s\[(?P<timestamp>.*?)\]\s\"(?P<method>\S*)\s*(?P<request>\S*)\s*(HTTP\/)*(?P<http_version>.*?)\"\s(?P<response_code>\d{3}).*")
    r = regex.search(line)
    result_set = {}
    if r:
        for k, v in r.groupdict().iteritems():
            if v is None or v is "-":
                continue
            if "request" in k:
                if "?" not in v:
                    continue
                request = v.partition("?")
                path = request[0]
                query = request[2]
                result_set["path"] = path
                result_set["query"] = query

                # get querystring
                info = {}
                qs_values = urlparse.parse_qs(query)
                for tag, value in qs_values.iteritems():
                    val = value[0]
                    if tag.lower() == 'ref':
                        try:
                            val = urlparse.urlparse(val).netloc
                        except:
                            # invalid URL
                            continue
                    info[tag] = val
                result_set["info"] = info

                r.groupdict().pop(k)

            result_set[k] = r.groupdict().pop(k)
    return result_set