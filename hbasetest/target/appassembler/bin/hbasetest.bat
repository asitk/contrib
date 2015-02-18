@REM ----------------------------------------------------------------------------
@REM  Copyright 2001-2006 The Apache Software Foundation.
@REM
@REM  Licensed under the Apache License, Version 2.0 (the "License");
@REM  you may not use this file except in compliance with the License.
@REM  You may obtain a copy of the License at
@REM
@REM       http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM  Unless required by applicable law or agreed to in writing, software
@REM  distributed under the License is distributed on an "AS IS" BASIS,
@REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM  See the License for the specific language governing permissions and
@REM  limitations under the License.
@REM ----------------------------------------------------------------------------
@REM
@REM   Copyright (c) 2001-2006 The Apache Software Foundation.  All rights
@REM   reserved.

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of arguments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
set BASEDIR=%~dp0\..

:repoSetup
set REPO=


if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=%BASEDIR%\repo

set CLASSPATH="%BASEDIR%"\etc;"%REPO%"\log4j\log4j\1.2.17\log4j-1.2.17.jar;"%REPO%"\commons-cli\commons-cli\1.2\commons-cli-1.2.jar;"%REPO%"\org\apache\zookeeper\zookeeper\3.4.6\zookeeper-3.4.6.jar;"%REPO%"\org\slf4j\slf4j-api\1.6.1\slf4j-api-1.6.1.jar;"%REPO%"\org\slf4j\slf4j-log4j12\1.6.1\slf4j-log4j12-1.6.1.jar;"%REPO%"\jline\jline\0.9.94\jline-0.9.94.jar;"%REPO%"\io\netty\netty\3.7.0.Final\netty-3.7.0.Final.jar;"%REPO%"\org\apache\hadoop\hadoop-core\1.2.1\hadoop-core-1.2.1.jar;"%REPO%"\xmlenc\xmlenc\0.52\xmlenc-0.52.jar;"%REPO%"\com\sun\jersey\jersey-core\1.8\jersey-core-1.8.jar;"%REPO%"\com\sun\jersey\jersey-json\1.8\jersey-json-1.8.jar;"%REPO%"\org\codehaus\jettison\jettison\1.1\jettison-1.1.jar;"%REPO%"\com\sun\xml\bind\jaxb-impl\2.2.3-1\jaxb-impl-2.2.3-1.jar;"%REPO%"\com\sun\jersey\jersey-server\1.8\jersey-server-1.8.jar;"%REPO%"\asm\asm\3.1\asm-3.1.jar;"%REPO%"\commons-io\commons-io\2.1\commons-io-2.1.jar;"%REPO%"\commons-httpclient\commons-httpclient\3.0.1\commons-httpclient-3.0.1.jar;"%REPO%"\commons-codec\commons-codec\1.4\commons-codec-1.4.jar;"%REPO%"\org\apache\commons\commons-math\2.1\commons-math-2.1.jar;"%REPO%"\commons-configuration\commons-configuration\1.6\commons-configuration-1.6.jar;"%REPO%"\commons-collections\commons-collections\3.2.1\commons-collections-3.2.1.jar;"%REPO%"\commons-digester\commons-digester\1.8\commons-digester-1.8.jar;"%REPO%"\commons-beanutils\commons-beanutils\1.7.0\commons-beanutils-1.7.0.jar;"%REPO%"\commons-beanutils\commons-beanutils-core\1.8.0\commons-beanutils-core-1.8.0.jar;"%REPO%"\commons-net\commons-net\1.4.1\commons-net-1.4.1.jar;"%REPO%"\org\mortbay\jetty\jetty\6.1.26\jetty-6.1.26.jar;"%REPO%"\org\mortbay\jetty\servlet-api\2.5-20081211\servlet-api-2.5-20081211.jar;"%REPO%"\org\mortbay\jetty\jetty-util\6.1.26\jetty-util-6.1.26.jar;"%REPO%"\tomcat\jasper-runtime\5.5.12\jasper-runtime-5.5.12.jar;"%REPO%"\tomcat\jasper-compiler\5.5.12\jasper-compiler-5.5.12.jar;"%REPO%"\org\mortbay\jetty\jsp-api-2.1\6.1.14\jsp-api-2.1-6.1.14.jar;"%REPO%"\org\mortbay\jetty\jsp-2.1\6.1.14\jsp-2.1-6.1.14.jar;"%REPO%"\ant\ant\1.6.5\ant-1.6.5.jar;"%REPO%"\commons-el\commons-el\1.0\commons-el-1.0.jar;"%REPO%"\net\java\dev\jets3t\jets3t\0.6.1\jets3t-0.6.1.jar;"%REPO%"\hsqldb\hsqldb\1.8.0.10\hsqldb-1.8.0.10.jar;"%REPO%"\oro\oro\2.0.8\oro-2.0.8.jar;"%REPO%"\org\eclipse\jdt\core\3.1.1\core-3.1.1.jar;"%REPO%"\org\codehaus\jackson\jackson-mapper-asl\1.8.8\jackson-mapper-asl-1.8.8.jar;"%REPO%"\org\apache\hadoop\hadoop-common\0.22.0\hadoop-common-0.22.0.jar;"%REPO%"\commons-logging\commons-logging\1.1.1\commons-logging-1.1.1.jar;"%REPO%"\org\mortbay\jetty\jsp-2.1-jetty\6.1.26\jsp-2.1-jetty-6.1.26.jar;"%REPO%"\org\mortbay\jetty\jsp-api-2.1-glassfish\2.1.v20091210\jsp-api-2.1-glassfish-2.1.v20091210.jar;"%REPO%"\org\mortbay\jetty\jsp-2.1-glassfish\2.1.v20091210\jsp-2.1-glassfish-2.1.v20091210.jar;"%REPO%"\org\eclipse\jdt\core\compiler\ecj\3.5.1\ecj-3.5.1.jar;"%REPO%"\net\sf\kosmosfs\kfs\0.3\kfs-0.3.jar;"%REPO%"\org\apache\avro\avro\1.5.3\avro-1.5.3.jar;"%REPO%"\com\thoughtworks\paranamer\paranamer\2.3\paranamer-2.3.jar;"%REPO%"\org\xerial\snappy\snappy-java\1.0.3.2\snappy-java-1.0.3.2.jar;"%REPO%"\org\apache\avro\avro-ipc\1.5.3\avro-ipc-1.5.3.jar;"%REPO%"\org\apache\hadoop\hadoop-tools\1.2.1\hadoop-tools-1.2.1.jar;"%REPO%"\org\apache\hadoop\hadoop-hdfs\0.22.0\hadoop-hdfs-0.22.0.jar;"%REPO%"\com\google\guava\guava\r09\guava-r09.jar;"%REPO%"\org\apache\hbase\hbase\0.94.14\hbase-0.94.14.jar;"%REPO%"\com\yammer\metrics\metrics-core\2.1.2\metrics-core-2.1.2.jar;"%REPO%"\com\github\stephenc\high-scale-lib\high-scale-lib\1.1.1\high-scale-lib-1.1.1.jar;"%REPO%"\commons-lang\commons-lang\2.5\commons-lang-2.5.jar;"%REPO%"\org\apache\thrift\libthrift\0.8.0\libthrift-0.8.0.jar;"%REPO%"\org\apache\httpcomponents\httpclient\4.1.2\httpclient-4.1.2.jar;"%REPO%"\org\apache\httpcomponents\httpcore\4.1.3\httpcore-4.1.3.jar;"%REPO%"\org\jruby\jruby-complete\1.6.5\jruby-complete-1.6.5.jar;"%REPO%"\org\mortbay\jetty\servlet-api-2.5\6.1.14\servlet-api-2.5-6.1.14.jar;"%REPO%"\org\codehaus\jackson\jackson-core-asl\1.8.8\jackson-core-asl-1.8.8.jar;"%REPO%"\org\codehaus\jackson\jackson-jaxrs\1.8.8\jackson-jaxrs-1.8.8.jar;"%REPO%"\org\codehaus\jackson\jackson-xc\1.8.8\jackson-xc-1.8.8.jar;"%REPO%"\org\jamon\jamon-runtime\2.3.1\jamon-runtime-2.3.1.jar;"%REPO%"\com\google\protobuf\protobuf-java\2.4.0a\protobuf-java-2.4.0a.jar;"%REPO%"\javax\xml\bind\jaxb-api\2.1\jaxb-api-2.1.jar;"%REPO%"\javax\activation\activation\1.1\activation-1.1.jar;"%REPO%"\stax\stax-api\1.0.1\stax-api-1.0.1.jar;"%REPO%"\com\hbasetest\core\hbasetest\1.0-SNAPSHOT\hbasetest-1.0-SNAPSHOT.jar

set ENDORSED_DIR=
if NOT "%ENDORSED_DIR%" == "" set CLASSPATH="%BASEDIR%"\%ENDORSED_DIR%\*;%CLASSPATH%

if NOT "%CLASSPATH_PREFIX%" == "" set CLASSPATH=%CLASSPATH_PREFIX%;%CLASSPATH%

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS%  -classpath %CLASSPATH% -Dapp.name="hbasetest" -Dapp.repo="%REPO%" -Dapp.home="%BASEDIR%" -Dbasedir="%BASEDIR%" com.hbasetest.core.App %CMD_LINE_ARGS%
if %ERRORLEVEL% NEQ 0 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=%ERRORLEVEL%

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@REM If error code is set to 1 then the endlocal was done already in :error.
if %ERROR_CODE% EQU 0 @endlocal


:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
