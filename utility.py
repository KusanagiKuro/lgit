#!/usr/bin/env python3


def try_and_pass_function(function, error, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        pass
