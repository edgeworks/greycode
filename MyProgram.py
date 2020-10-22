import sys, web
from test import Test

testinstance = Test

urls = (
       '/(.*)', 'testinstance'
)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
