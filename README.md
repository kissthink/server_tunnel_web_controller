#Server Tunnel

#简介

SysLab 3408的百兆电信宽带经过多层NAT并且无网关控制权限，为了方便在工作室内搭建临时开发服务器，我写了这个基于SSH反向隧道的端口映射脚本，可以将内网IP的某个服务端口映射到SysLab公共服务器的服务端口上，同时提供Web配置页面方便临时设置，Web基于Python WSGI。

该脚本运行于3408极路由上。

#使用方法

* 连接上3408极路由后，登录 http://192.168.3.1:8080 配置

* 为避免与公共服务器已有服务冲突，外网端口可配置范围为30001-34999，且不可与已配置的外网端口重复，如默认下极路由SSH服务映射到了公共服务器的30001端口上，则不可再填写30001

* 内网IP填写3408的需要映射的服务器的内网IP，如192.168.3.123，内网端口为需要映射的服务器提供服务的TCP端口，如web服务则一般为80

* SysLab公共服务器地址为： syslab.ddns.us

* 示例：填写如下配置，外网端口：30100，内网IP：192.168.3.123，内网端口：80。则访问 http://syslab.ddns.us:30100 即可访问IP为192.168.3.123的内网机器的80端口上的Web服务。

#注意

* 外网端口30001,30002,30003,31000分别映射了：极路由SSH服务、3408服务器SSH服务、3408服务器ShadowSocks服务、3408服务器Web服务，该几个端口保留，请尽量不要使用（特别是30001极路由SSH端口，若删除了这个，外部就完全失去对极路由的控制）。

* 外网端口31000可用于Web服务映射。在SysLab公共服务器上已通过Nginx配置好虚拟主机+反向代理，通过 http://syslab.ddns.us 即可访问该Web服务。但是请尽量通过在3408服务器上配置Nginx反代的形式使用该端口，如果确实需要占用该端口，使用后请恢复原设置（外网端口：31000，内网IP：192.168.2.100，内网端口：80）。

* 由于未知原因，将该脚本放在极路由自启动目录中虽能自动启动Web配置页服务，但无法自动发起SSH隧道连接（SSH命令貌似执行失败，但通过重定向未发现错误回显）。因此请尽量不要重启极路由。

* 如果不可避免地需要重启极路由，重启后请在极路由上手动运行该脚本。具体操作为：以root身份SSH进极路由（192.168.3.1），后台运行```~/tunnel_config_web.py``` (推荐在screen中跑，方便随时查询log)

* 网络维护：邓司机 出了问题给我甩锅 _(:з」∠)_
