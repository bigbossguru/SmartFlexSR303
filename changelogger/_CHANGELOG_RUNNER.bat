git log --date=format:"%%d-%%m-%%Y" --pretty="## [%%h] - %%ad -%%s" > CHANGELOG_orig.md
python change_log_creater.py
mv CHANGELOG.md ../