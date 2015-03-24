import urlparse

def app(environ, start_response):
	data = '<html><body><h1>Hello World!</h1>\n<h2>Parameters:</h2>\n'
	
	#check if request body is empty
	try:
		requestBodySize = int(environ.get('CONTENT_LENGTH', 0))
	except:
		requestBodySize = 0

	#parse get and post content
	post_parameters = urlparse.parse_qs(environ['wsgi.input'].read(requestBodySize))
	get_parameters = urlparse.parse_qs(environ['QUERY_STRING'])

	#get parameters treatment
	data += '\n<h3>GET:</h3>\n<ul>'
	for key in get_parameters.keys():
		for value in get_parameters[key]:
			data += "\n\t<li>" + key + ' = ' + value + '</li>\n'
	data += '</ul>'

	#post parameters treatment
	data += '\n<h3>POST:</h3>\n<ul>'
	for key in post_parameters.keys():
		for value in post_parameters[key]:
			data += "\n\t<li>" + key + ' = ' + value + '</li>\n'
	data += '</ul>'
	data += '\n</body></html>'

	status = '200 OK'
	response_headers = [
    	('Content-type','text/html'),
    	('Content-Length', str(len(data)))
    ]
	start_response(status, response_headers)

	return data