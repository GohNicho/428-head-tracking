@echo off
set curr=%cd%
if "%1" == "antiquorum" GOTO start
if "%1" == "worker" GOTO worker
if "%1" == "server" GOTO server
if "%1" == "" GOTO end
:start
    start cmd /k " %curr%\start_db.cmd worker "
    start cmd /k " %curr%\start_db.cmd server "
    TIMEOUT 30
    ::start "" "http://localhost:3000/"
    GOTO end
:server
    rails s
    GOTO end
:worker
    rake jobs:work
:end

::mongod.exe --dbpath ".\db"
::mongod.exe 
:: populate a test database (unnecessary but always good to see)
::use head_tracker &
::db.head_tracking.insertOne( { grav:0, x_rot:0, y_rot:0, z_rot:0 } ); &
::db.client_session.insertOne( { first_name: "Test", last_name: "Test", choice1: "Choice 1b", choice1time: 5.0, choice2: "Choice 5a", choice2time: 7.1, choice3: "Choice 6b", choice3time: 4.4 } ); &
::db.head_tracking.find().pretty() &
::db.client_session.find().pretty() &