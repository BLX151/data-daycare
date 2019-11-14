@ECHO OFF

ECHO %1

IF %1==on GOTO ON
IF %1==off GOTO OFF
GOTO ERR

:ON 
CALL %cd%\pyenv\scripts\activate
SET FLASK_APP=dd
SET FLASK_ENV=development
CLS
ECHO DD Activated
GOTO DONE

:OFF
CALL %cd%\pyenv\scripts\deactivate
CLS
ECHO DD Deactivated
GOTO DONE

:ERR
ECHO "Format: dd on; dd off"
GOTO DONE

:DONE