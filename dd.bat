@ECHO OFF

IF %1==on GOTO ON
IF %1==off GOTO OFF
GOTO ERR

:ON 
@ECHO OFF
CALL %cd%\pyenv\scripts\activate
SET FLASK_APP=dd
SET FLASK_ENV=development
ECHO == DD Activated ==
GOTO DONE

:OFF
@ECHO OFF
CALL %cd%\pyenv\scripts\deactivate
ECHO  == DD Deactivated ==
GOTO DONE

:ERR
@ECHO OFF
ECHO "Format: dd on; dd off"
GOTO DONE

:DONE