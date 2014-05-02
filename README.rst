==========
PyApiMaker
==========

*disclaimer: written in some kind of 3 years old kid english*


*PyApiMaker* provides utilities to easily create aplications
or modules that must interact with functions.
*PyApiFunction* encloses a python function and collects data,
doc, and annotations of it. Then a *PyApi* stores all functions and
manages them by context. One can also get a *PyApiContext* to 
easily acces the functions. 
Some simple usage looks like this::

    #!/usr/bin/env python

    from PyApiMaker import PyApi

    api = PyApi()

    @api.add()
    def foo(a, b, c):
    	return a * b + c

    with api.context("web"):
    	@api.add()
    	def foo(a, b):
    		return a + b

    if __name__ == "__main__":
    	with context("web") as web:
    		print(web.foo())


Index
=====

1. For what the hell is this?
	- Some unusefull questions

2. PyApi
	- Create an api
	- Defining functions
	- Searching the api
	- Api context

3. PyApiRpc
	- PyApiRpcServer
	- PyApiRpcBlueprint
	- PyApiRpcTerminal

4. PyApiParser
	- Use with PyApiRpcTerminal


For what the hell is this?
==========================

All that you dont wanna know.

Some unusefull questions
------------------------

*-What can I get from this?*

Yep, what can you get from something that only catalloge
your functions? Really not so much, but commodity.

Basically this was tought for applications that needs some
kind of interaction, with the user or with another app.
Think of this like a big and ordered bag where store your
functions, and later you can access them throught one PyApi 
object.

When you have large applications you also need to organize 
all that scrap, and this is where the context came in.
When you add functions to your big bag you can specify a 
context where to add them. Then, in another remote place of
your code, you can get that context and acces all that
functions. 

*-So, everything is fine and stuff but, I can use a dict or 
organize all my functions in my own way.*

Yep again, but, its not bad to just forget how do that stuff and
just do it. So for one second remember all the time you lost 
writing command line interface applications which change 
everytime from app to app, and tedoius http APIs where you 
never standarize your output.

There is when all the automagical optional tools came in.
Basically you have some utilities to make all this stuff 
with just a few lines. 


PyApi
=====

Basically, a *how to* use the api.

Create an api
-------------

You can create an api object ready to go on just from *PyApi()*
In some confortable place of your code you can just do this::

	from pyapimaker import PyApi

	myapi = PyApi()

Also you can create your own class and inherit from PyApi (TODO: 
explain PyApi internally)

Defining functions
------------------

To define and add functions to your brand new shiny api you must 
use the simple function *add()* provided in your api. Its simple
enough to just put a decorator::

	@api.add()
	def foo(a, b):
	"""returns the sum of a and b"""
		return a + b

Now the function is stored in *api* with the name "foo", also (for now)
it goes to a context called "none" (but this will be changed in the
future with the addition of a tree context structure).

When the function is added the decorator replaces the function with
a *PyApiFunction* object which wrapps the original function. Then *PyApi* 
sets a *key*, a *name* and a *context* attribute. They are basically::

	>>> foo.key 
	"none.foo"
	>>> foo.name
	"foo"
	>>> foo.context
	"none"

Also *PyApi* saves the docstring and the argspecs (and signature in some distant future) of
the function in *doc* and *args*. You can easily access then with::

	>>> foo.doc 
	"returns the sum of a and b"
	>>> foo.args
	["a", "b"]

So, this is nothing new, but its just a wrapper to oragnize the functions. 

Also when you add functions you can specify the name and/or context where add the
function. Just simple like this::

	@api.add(name="eggs", context="spam")
	def someFoo(a, b, c)
		pass

And there are some useful functions (also used by some *PyApi* utils) like a fancy
*\_\_repr\_\_* and a *toJson()* function::

	>>> someFoo
	<spam.eggs(a, b, c)>
	>>> someFoo.toJson()
	{'context': 'spam', 'args': ['a', 'b', 'c'], 'name': 'eggs'}

And finally with the api *context(),* you can easily open and close a 
context and do not write the same in each function::

	with api.context("spam"):
		@api.add()
		def eggs(a, b):
			pass

	with api.context("more_spam"):
		@api.add()
		def eggs(a, b):
			pass

		@api.add()
		def more_eggs(a, b):
			pass

In the context section its a little bit better explained.


Searching the api
-----------------

When you just have defined all your junk, you will need a way to get all the functions from
the automagical big bag. 

You can use *getFunction* to get one function which matches the specs 
or *findFunctions* to return a list of functions. Its easier with an example.
Consider the last defined functions::

	>>> api.getFunction("eggs")
	None
	>>> api.getFunction("eggs", context="spam")
	<spam.eggs(a, b)>

The fist attempt doesn't return nothing because ive told you about the "none" context.
By default you are in this context and by default *getFunction* returns the function
of the actual context, similary does *findFunctions*::

	>>> api.findFunctions()
	[]
	>>> api.findFunctions(context="more_spam")
	[<more_spam.eggs(a, b)> <more_spam.more_eggs(a, b)>]

And then wildcards appear::

	>>> api.findFunctions(context="*", name="eggs")
	[<spam.eggs(a, b)>, <more_spam.eggs(a, b)>]

And very prehistorical regexes::

	>>> api.findFunctions(context="more_spam", name="eggs|more_eggs")
	[<more_spam.eggs(a, b)>, <more_spam.more_eggs(a, b)>]

There is room for improvement. For now you can have only one function
with the same name in one context. One idea is to have many, with
different argspecs, but it sounds more like C function override.


Api context
-----------

Searching the functions is not cool. But getting the functions that you need from
some magical object its really cool. And there the *PyApiContext* came in.

Your *PyApi* object has a stack (a LIFO) of of contextes. When you call *enterContext*
you just add a context and set it like the actual context, and when you call *exitContext*
you just go to the last context. Another example::

	api.enterContext("bar")

	@api.add()
	def foo():
		pass

	api.exitContext()

And then magically::

	>>> foo
	<bar.foo()>

But opening the context like this is kinda tedious. So there is a PyApiContext 
object, which implements *\_\_enter\_\_* and *\_\_exit\_\_* so you can easily use
it with the *with* keyword::

	with api.context("web"):
		@api.add()
		def foo():
			pass

Actually the *context* function returns a *PyApiContext* object::

	ctx = api.context()

And by default if its called without args it gives the actual context.

The really confortable stuff is that *PyApiContext* contains all the api functions
that the specified context contains, and you can access them easily::

	>>> ctx.someFoo
	<someContext.someFoo(a, b, c)>

Also you can get the object with *with .. as,* kinda like this::

	with api.context("web") as web:
		web.foo("mosquito")

When you call some function which uses another context inside, you have nothing to
worry about. If the function exits the context that she had opened the magical context
lifo makes shure that you return to where you was.


PyApiRpc
========

The fun stuff

PyApiRpcServer
--------------

WIP

PyApiRpcBlueprint
-----------------
WIP

PyApiRpcTerminal
----------------

WIP

PyApiParser
===========

WIP

Use with PyApiRpcTerminal
-------------------------

WIP
