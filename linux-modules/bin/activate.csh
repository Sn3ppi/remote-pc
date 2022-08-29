# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; test "\!:*" != "nondestructive" && unalias deactivate'

# Unset irrelevant variables.
deactivate nondestructive

setenv VIRTUAL_ENV "/media/sneppi/0094C07094C06A2C/Users/racer/AppData/Roaming/Sneppi-PC_bot/remote_pc/linux-modules"

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    if ("linux-modules" != "") then
        set env_name = "linux-modules"
    else
        if (`basename "VIRTUAL_ENV"` == "__") then
            # special case for Aspen magic directories
            # see https://aspen.io/
            set env_name = `basename \`dirname "$VIRTUAL_ENV"\``
        else
            set env_name = `basename "$VIRTUAL_ENV"`
        endif
    endif
    set prompt = "[$env_name] $prompt"
    unset env_name
endif

alias pydoc python -m pydoc

rehash
