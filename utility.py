#from cv_tuner import App
import cv_tuner as cv
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

def print(message):
    #global ex
    __builtin__.print('abc')
    __builtin__.print(message)
    if hasattr(cv.ex, 'message_console'):
        __builtin__.print('def')
        cv.ex.message_console.append(message)
        cv.ex.message_console.moveCursor(QTextCursor.End)
    # if hasattr(App, 'message_console'):
        # __builtin__.print('def')
        # App.message_console.append(message)
        # App.message_console.moveCursor(QTextCursor.End)