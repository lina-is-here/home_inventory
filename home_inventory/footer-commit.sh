#!/bin/bash
NOW=`date +"%Y-%m-%d"`
sed -i '' 's@<p id="commit-date-id".*@<p id="commit-date-id" class="text-center text-muted">Last change:\ '"$NOW"'</p>@g' home_inventory/inventory/templates/footer.html
exit 0
