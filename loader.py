import json

def from_json(path):
	return json.load(open(path))

def is_function(node):
	return node['_nodetype'] == 'Decl' and node['type']['_nodetype'] == 'FuncDecl'

def is_typedef(node):
	return node['_nodetype'] == 'Typedef' and node['type']['_nodetype'] == 'TypeDecl' and node['type']['type']['_nodetype'] != 'Struct'

def typedef(node):
	return {
		'name': node['name'],
		'type': node['type']['type']['names'][0]
	}

def function_name(node):
	return node['name']

def function_return_type(func_node):
	ret_type = func_node['type']
	if is_pointer(func_node['type']):
		return ret_type['type']['type']['type']['names'][0]
	else:
		return ret_type['type']['type']['names'][0]

def is_pointer(argument):
	return argument['type']['_nodetype'] == 'PtrDecl'

def function_arguments(node):
	res = []
	if node['type']['args'] is None:
		return []
	for arg in node['type']['args']['params']:
		if is_pointer(arg):
			if is_pointer(arg['type']):
				print("Skipping")
				continue
			res.append({
				'name': arg['type']['type']['declname'],
				'type': arg['type']['type']['type']['names'][0],
				'pointer': True,
			})
		else:
			res.append({
				arg['type']['declname']:
				arg['type']['type']['names'][0],
			})
	return res

def to_internal(ast):
	res = {
		'functions': {},
		'typedefs': {}
	}
	for node in ast['ext']:
		if is_typedef(node):
			if '/' in node['coord']:
				continue
			td = typedef(node)
			res['typedefs'][td.pop('name')] = td['type']
		if is_function(node):
			info = function_info(node)
			res['functions'][info.pop('name')] = info
	return res

def function_info(func_node):
	return {
			'name': function_name(func_node),
		'return_type': function_return_type(func_node),
		'arguments': function_arguments(func_node),
	}

if __name__ == '__main__':
	loaded = from_json('out')
	functions = [i for i in loaded['ext'] if is_function(i)]
	res = to_internal(loaded)
	import yaml
	yaml.dump(res, open('bass.yml', 'w'))
	import pprint
	#pprint.pprint(res)
