import sys

CODE_HOSTS = (
    ("github", "GitHub"),
    ("bitbucket", "BitBucket"),
    ("google", "GoogleCode"),
)

def get_host(host):
    if host in CODE_HOSTS:
        path = 'codehost.hosts.%s.%s' % (host, CODE_HOSTS[host])
    else:
        path = host
    __import__(path)
    return sys.modules[path]