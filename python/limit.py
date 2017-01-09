import os

#在Linux下面部署应用的时候，有时候会遇上Socket/File: Can’t open so many files的问题；这个值也会影响服务器的最大并发数，其实Linux是有文件句柄限制的，而且Linux默认不是很高，一般都是1024，生产服务器用其实很容易就达到这个数量。
#修改配置文件的方式如下（执行完这个脚本之后需要重启才能生效）
# use 'ulimit -a' to lookup the size
# use 'ulimit -n num' to set the size



value = '409600'
str_conf = ['*                hard    nofile          ' + value + '\n',
	   '*                soft    nofile          ' + value + '\n',
           'root             hard    nofile          ' + value + '\n',
           'root             soft    nofile          ' + value + '\n']
str_pro = 'ulimit -SHn ' + value +'\n'


def set_limit():
    set_conf()
    set_pro()

def set_conf():
    conf = open('/etc/security/limits.conf', 'r+')
    lines = conf.readlines()    
    for i in range(len(lines)):
        if (lines[i].startswith(str_conf[0].split(value)[0])):
            lines[i] = '' 
        if (lines[i].startswith(str_conf[1].split(value)[0])):
            lines[i] = ''
        if (lines[i].startswith(str_conf[2].split(value)[0])):
            lines[i] = ''
        if (lines[i].startswith(str_conf[3].split(value)[0])):
            lines[i] = ''
    for s in str_conf:
        lines.append(s) 
    conf = open('/etc/security/limits.conf', 'w+')
    for l in lines:     
        conf.writelines(l)
    conf.close()

def set_pro():
    pro = open('/etc/profile', 'r+')
    lines = pro.readlines()
    for i in range(len(lines)):
        if 'ulimit -SHn' in lines[i]:
            lines[i] = ''
    lines.append(str_pro)         
    pro = open('/etc/profile', 'w')
    for l in lines:    
        pro.writelines(l)
    pro.close()



set_limit()
