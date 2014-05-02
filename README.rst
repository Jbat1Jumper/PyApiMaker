==========
PyApiMaker
==========

``Written in: python 3``


*Disclaimer: written in some kind of 3 years old kid english (while hitting the head to the keyboard (while ...))*


*PyApiMaker* provides utilities to easily create aplications
or modules that must interact with functions.
*PyApiFunction* encloses a python function and collects data,
doc, and annotations of it. Then a *PyApi* stores all functions and
manages them by context. One can also get a *PyApiContext* to 
easily access the functions of a given context.
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

So, this is nothing new, but its just a wrapper to organize the functions. 

Also when you add functions you can specify the name and/or context where add the
function. Just simple like this::

	@api.add(name="eggs", context="spam")
	def someFoo(a, b, c)
		pass

And there are some useful functions (also used by some *PyApi* utils) like a fancy
*\_\_repr\_\_* and a *to_json()* function::

	>>> someFoo
	<spam.eggs(a, b, c)>
	>>> someFoo.to_json()
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

You can use *get_function* to get one function which matches the specs 
or *find_functions* to return a list of functions. Its easier with an example.
Consider the last defined functions::

	>>> api.get_function("eggs")
	None
	>>> api.get_function("eggs", context="spam")
	<spam.eggs(a, b)>

The fist attempt doesn't return nothing because ive told you about the "none" context.
By default you are in this context and by default *get_function* returns the function
of the actual context, similary does *find_functions*::

	>>> api.find_functions()
	[]
	>>> api.find_functions(context="more_spam")
	[<more_spam.eggs(a, b)>, <more_spam.more_eggs(a, b)>]

And then wildcards appear::

	>>> api.find_functions(context="*", name="eggs")
	[<spam.eggs(a, b)>, <more_spam.eggs(a, b)>]

And very prehistorical regexes::

	>>> api.find_functions(context="more_spam", name="eggs|more_eggs")
	[<more_spam.eggs(a, b)>, <more_spam.more_eggs(a, b)>]

There is room for improvement. For now you can have only one function
with the same name in one context. One idea is to have many, with
different argspecs, but it sounds more like C function override.


Api context
-----------

Searching the functions is not cool. But getting the functions that you need from
some magical object its really cool. And there the *PyApiContext* came in.

Your *PyApi* object has a stack (a LIFO) of contexts. When you call *enter_context*
you just add a context and set it like the actual context, and when you call *exit_context*
you just go to the last context. Another example::

	api.enter_context("bar")

	@api.add()
	def foo():
		pass

	api.exit_context()

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

	>>> ctx.some_foo
	<some_context.some_foo(a, b, c)>

Also you can get the object with *with .. as,* kinda like this::

	with api.context("web") as web:
		web.foo("mosquito")

When you call some function which uses another context inside, you have nothing to
worry about. If the function exits the context that she had opened the magical context
lifo makes sure that you return to where you were.


PyApiRpc
========

The fun stuff.

*PyApiRpc* provides a web interface to your api functions.

This utility uses Flask as a web server, so you need to have Flask installed.


PyApiRpcServer
--------------

This is actually a wrapper around a Flask app. When you create it you can
specify a name, an ip, a port, like any othere server. Also you can pass a debug=True
for the enable de Flask debug mode (autorefresh and web stacktrace).
This is the *PyApiRpcServer* init by default::

	PyApiRpcServer(name="PyRpcServer", ip="127.0.0.1", port=5000, debug=False)

Theres no magic around this, its only a server setup line. You can also specify
the values later like::

	server = PyApiRpcServer()
	server.ip = "0.0.0.0"
	server.port = 80

There is no difference. 

The *PyApiRpcServer* is only a Flask server which only serves components (Actually Flask Blueprints)
of the PyApiRpc kind.
You can add this components with the *add* function::

	server.add(some_component)

And then when you builded all you just must run the server::

	server.run()

And there is it, up and running.


PyApiRpcBlueprint
-----------------

This is an *PyApiRpc* component made to run in a *PyApiRpcServer*.
This is some kind of a function container. It groups functions of your api and 
serves them in a url. 

To use it you just must create it, fill it with functions, and add it to an *PyApiRpcServer*.
Just like this::

	bp = PyApiRpcBlueprint(prefix="/rpc")
	functions = myapi.findFunctions(context="web|chat|file_share")
	bp.add(functions)
	server.add(bp)

And then the server will serve all that functions in "ip:port/rpc"

How it will serve the functions is the question. Actually the blueprint makes an action 
to the specified functions, by default the action is "call" but it can be:

:call:           call the given function with the given args.
:fancy_call:     same as above but the response gets formatted to look good in the browser.
:help:           return the doc of the given function.
:fancy_help:     same as above but looks good.

The format in which it serves the functions is ``ip:port/prefix/<foo>?args=val``.

By default it stores the functions in a dict using function key as key. You can change 
this specifying ``only_names=True``. Be careful of adding functions with the same name.
(Dont know if to throw an exception or just replace with the new function, the second will
work better for future *on fly api changing*).

One pattern can be, to use prefix ``/rpc/call`` for calling functions and ``/rpc/help``
for retriving de documentation.

The output (for now) its only a JSON response which wrapps the actual return of the function.
The response always have the attributes *content*, *had_errors*, *error_code* and *error_desc*.
And looks like any other JSON object::

	{
		"content": 42,
		"error_code": 0,
		"error_desc": "",
		"had_errors": false
	}

In the *content* its where the return value will go. The *had_errors* its a boolean showing
that everything went ok, turns false if there were exceptions. The *error_code* its something 
that its not finished yet (the idea is that you can throw exceptions with error numbers), and 
*error_desc* shows the exception msg.

The arguments for the functions can be passed by name and also in order, but for now you cant
mix the two forms. Passing the arguments by name its nothing but the same POST or GET call, 
using the same names for the arguments. Passing them in order its some kind of a hack in which
you can pass the args in order with the names ``arg0=`` ``arg1=`` . . ``arg#=`` and so on.

Note that passing values by args its something not good for compatibility on code changes, and
for your health.



PyApiRpcTerminal
----------------

This is an *PyApiRpc* component made to run in a *PyApiRpcServer*.
This is a complete terminal embedded in a web page. It uses *JQuery*, *JQueryTerminal*
and *JQueryMouseWheel*, and they are embedded in the package and served in the server, so you
can use this in a local network and dont worry about them.

It can be used with not only with the api, but also you can reuse it for everything you need
just defining a function.

Its usage is similar to the *PyApiRpcBlueprint* but instead of adding functions you define only 
one function which is called when someone write something in the console.

To use it just do de same::

	term = PyApiRpcTerminal(prefix="/terminal")
	term.handler = 	some_function
	server.add(term)

In this case ``some_function`` must recive only a string with the text written in the conosle
and do whatever it want. Maybe a::

	def some_function(cmd):
		if cmd == "spam":
			return "eggs"
		return "sorry"

And there you have your interactive web shell, but its a pain to writte all the parser. So just 
keep reading.


PyApiParser
===========

This is just a parser, which automagically integrates with your api, and its the cherry of the py.
You can add 


Use with PyApiRpcTerminal
-------------------------

WIP


---------------------

Thanks to nosemeocurrenada for nada