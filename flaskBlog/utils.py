from datetime import datetime
from flaskBlog import app

# --------------------------------------------------
# IL s'agit ici de creer nos propres filtres ...   |
# --------------------------------------------------

@app.template_filter('date_format')
def date_format_fr(datetime: datetime):
    return datetime.strftime("%A, %d %B %Y")