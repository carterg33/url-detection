from math import log
import re
from urllib.parse import urlparse
from socket import gethostbyname
from pyquery import PyQuery
from whois import whois
import geoip2.webservice
import requests
from bs4 import BeautifulSoup

class URLFeatureGenerator:
    def __init__(self, url):
        self.url = url
        self.urlparse = urlparse(self.url)
        self.host = self.__get_ip()
        self.geoip = self.__get_geoip()
        self.content = self.__get_content()
        self.whois_dict = self.__get_whois()


    def __get_entropy(self, text):
        text = text.lower()
        probs = [text.count(c) / len(text) for c in set(text)]
        entropy = -sum([p * log(p) / log(2.0) for p in probs])
        return entropy

    def __get_ip(self):
        try:
            ip = self.urlparse.netloc if self.url_host_is_ip() else gethostbyname(self.urlparse.netloc)
            return ip
        except:
            return None
        
    def __get_geoip(self):
        try:
            with geoip2.webservice.Client(658304, 'w0i2b6H9dNXZMkq7', host = "geolite.info") as client:
                response = client.city(self.host)
                return response
        except:
            return None
    
    def __get_content(self):
        r = requests.get(self.url)
        content = BeautifulSoup(r.content, 'html.parser')
        return content

    def __get_whois(self):
        try:
            whois_dict = whois(self.host)
            return whois_dict
        except:
            return {}
    
    # extract lexical features
    def url_scheme(self):
        if self.urlparse.scheme == 'https':
            return True
        else:
            return False
        return self.urlparse.scheme

    def url_length(self):
        return len(self.url)

    def url_path_length(self):
        return len(self.urlparse.path)

    def url_host_length(self):
        return len(self.urlparse.netloc)

    def url_host_is_ip(self):
        host = self.urlparse.netloc
        pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        match = pattern.match(host)
        return match is not None

    def url_has_port_in_string(self):
        has_port = self.urlparse.netloc.split(':')
        return len(has_port) > 1 and has_port[-1].isdigit()

    def number_of_digits(self):
        digits = [i for i in self.url if i.isdigit()]
        return len(digits)

    def number_of_parameters(self):
        params = self.urlparse.query
        return 0 if params == '' else len(params.split('&'))

    def number_of_fragments(self):
        frags = self.urlparse.fragment
        return len(frags.split('#')) - 1 if frags == '' else 0

    def is_encoded(self):
        return '%' in self.url.lower()

    def num_encoded_char(self):
        encs = [i for i in self.url if i == '%']
        return len(encs)

    def url_string_entropy(self):
        return self.__get_entropy(self.url)

    def number_of_subdirectories(self):
        d = self.urlparse.path.split('/')
        return len(d)

    def number_of_periods(self):
        periods = [i for i in self.url if i == '.']
        return len(periods)

    def get_tld(self):
        return self.urlparse.netloc.split('.')[-1].split(':')[0]
    
    # host features
    def geo_loc(self):
        try:
            return self.geoip.country.name
        except:
            return None

    def whois_complete(self):
        if self.whois_dict.registrar:
            return True
        else:
            return False
    
    #content features
    def get_js_len(self):
        js=re.findall(r'<script>(.+)<\script>', str(self.content))
        complete_js=''.join(js)
        js_len = len(complete_js)
        return js_len

    def create_features(self):
        url_dict = {'url' : self.url}
        url_dict['https'] = self.url_scheme()
        url_dict['url_length'] = self.url_length()
        url_dict['url_path_length'] = self.url_path_length()
        url_dict['url_host_length'] = self.url_host_length()
        url_dict['url_host_is_ip'] = self.url_host_is_ip()
        url_dict['url_has_port_in_string'] = self.url_has_port_in_string()
        url_dict['number_of_digits'] = self.number_of_digits()
        url_dict['number_of_parameters'] = self.number_of_parameters()
        url_dict['number_of_fragments'] = self.number_of_fragments()
        url_dict['is_encoded'] = self.is_encoded()
        url_dict['num_encoded_char'] = self.num_encoded_char()
        url_dict['url_string_entropy'] = self.url_string_entropy()
        url_dict['number_of_subdirectories'] = self.number_of_subdirectories()
        url_dict['number_of_periods'] = self.number_of_periods()
        url_dict['tld'] = self.get_tld()
        url_dict['geo_loc'] = self.geo_loc()
        url_dict['js_len'] = self.get_js_len()
        url_dict['who_is'] = self.whois_complete()
        return url_dict