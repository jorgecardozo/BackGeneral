start cmd /k "git submodule foreach git checkout -- * & git submodule foreach git checkout -f release & git submodule foreach git pull origin release & exit"