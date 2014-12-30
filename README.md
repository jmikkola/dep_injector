# Dep injector

![](https://api.travis-ci.org/jmikkola/dep_injector.svg)

Allows expressing dependency graphs and getting dependencies from them.

This is potentially useful for dependency injection.

## Example:

```python
from injector import Dependencies

def value_source():
	return 'Result of a {}'.format('computation')

def both_source_and_dependant(computed_value, another_value):
	return len(computed_value) + another_value

class UsesInjector:
	def __init__(self, computed_value, len_value):
		self.s = computed_value
		self.l = len_value

	def __str__(self):
		return 'UsesInjector({}, {})'.format(self.s, self.l)

# register dependencies
deps = Dependencies()
# You can register a class as a factory
deps.register_factory(
	'uses-injector',
	UsesInjector,
	dependencies=['computed_value', 'len_value'],
)
# or a function
deps.register_factory(
	'len_value',
	both_source_and_dependant,
	dependencies=['computed_value', 'another_value'],
)
deps.register_factory('computed_value', value_source)
# You can also register plain values
deps.register_value('another_value', 10000)

# Get the injector - this finalizes the dependencies and checks to make sure
# that the dependencies are all correct.
inj = deps.build_injector()

print(inj.get_dependency('uses-injector'))
print(inj.get_dependency('len_value'))

# You can also inject new functions (just not register more values)
def uses_computed_value(computed_value):
	return ''.join(set(computed_value))

print(inj.inject(uses_computed_value, ['computed_value']))
```

## Development

Run this:

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r dev-requirements.txt
nosetests .
```
