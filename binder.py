from attr import attr, attributes, Factory
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath=".")
template_env = jinja2.Environment(loader=templateLoader)
template_env.trim_blocks = True
template_env.lstrip_blocks = True

@attributes
class CDeclaration:
	name = attr()
	type = attr()

@attributes
class CFunctionArgument(CDeclaration):
	default_value = attr(default=None)

@attributes
class CFunction:
	name = attr()
	return_type = attr()
	arguments = attr(default=Factory(list))


@attributes
class Library:
	name = attr()
	typedefs = attr(default=Factory(list))
	functions = attr(default=Factory(list))

def render(library, language):
	template = template_env.get_template(language + '.template')
	return template.render(library=library)


