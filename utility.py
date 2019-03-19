#!/usr/bin/env python3


def try_and_pass_function(function1, error, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        pass
