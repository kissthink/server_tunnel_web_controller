#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from subprocess import call

config_file_path = '/root/tunnels'

html = """
<!DOCTYPE html>
<head>
	<meta charset="UTF-8">
	<title>端口转发配置工具</title>
	<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
</head>
<body>
	<script>
		var port_config_raw = "%s";
		$(document).ready(function(){
			reload_ui();
		});
		function reload_ui() {
			if (port_config_raw.substr(port_config_raw.length-1,1) == '|') {
				port_config_raw = port_config_raw.slice(0, port_config_raw.length-1);
			}
			if (port_config_raw.substr(0,1) == "|") {
				port_config_raw = port_config_raw.slice(1, port_config_raw.length);
			}
			var config_array = port_config_raw.split("|");
			$("#config_content").html('');
			for (var index in config_array) {
				if (config_array[index].length==0) {
					continue;
				}
				line_config = config_array[index].split(":");
				$("#config_content").append('外网端口：'+ line_config[1] + ' 内网IP：' + line_config[2] + ' 内网端口：' + line_config[3] + '<button onclick="remove_config(\\'' + config_array[index] + '\\')">删除</button><br/>');
			}
		}
		function add_config() {
			var new_outbound_port = $('#new_outbound_port').val().trim();
			var new_lan_ip = $('#new_lan_ip').val().trim();
			var new_lan_port = $('#new_lan_port').val().trim();
			if (new_outbound_port=='' || new_lan_ip=='' || new_lan_port=='') {
				alert("请填写完整！");
				return;
			}
			var line_config_raw = "0.0.0.0:" + new_outbound_port + ":" + new_lan_ip + ":" + new_lan_port;
			port_config_raw = port_config_raw + "|" + line_config_raw;
			port_config_raw = port_config_raw.replace(/\|\|/g,'|');
			reload_ui();
		}
		function remove_config(str) {
			port_config_raw = port_config_raw.replace(str, '');
			port_config_raw = port_config_raw.replace(/\|\|/g,'|');
			reload_ui();
		}
		function save() {
			window.location.href="/"+encodeURIComponent(port_config_raw);
		}
	</script>
	<div>
		<input type="text" placeholder="外网端口" id="new_outbound_port" >
		<input type="text" placeholder="内网IP" id="new_lan_ip" >
		<input type="text" placeholder="内网端口" id="new_lan_port" >
		<button onclick="add_config()">增加</button>
	</div>
	<div id="config_content" style="margin-top:10px;margin-bottom:10px;">
		
	</div>
	<div>
		公网域名：syslab.ddns.us<br/>
		注意：仅支持TCP映射，外网端口范围30001-34999，外网31000端口可部署内网web服务，通过http://syslab.ddns.us可访问<br/>
		<button onclick="save()">保存设置</button>
		<button onclick="window.location.reload()">重置</button>
		<p>
			作者：不是司机
		</p>
	</div>
</body>
"""

html_success = """
<!DOCTYPE html>
<head>
	<meta charset="UTF-8">
	<title>端口转发配置工具</title>
</head>
<body>
保存成功！
<script>
setTimeout(function(){
	window.location.href="/";
	},2000);
</script>
</body>
"""

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    if (environ['PATH_INFO'][1:] and str(environ['PATH_INFO'][1:]).find(':') != -1):
    	open(config_file_path, "w+").write(str(environ['PATH_INFO'][1:]).replace('<','').replace('>','').replace('|','\n'))
    	call(["/root/run_tunnel"])
    	return html_success
    else:
    	return html % open(config_file_path,"r").read().replace('\n','|');

call(["/root/run_tunnel"])
httpd = make_server('', 8080, application)
print("Serving HTTP on port 8080...")
httpd.serve_forever()
