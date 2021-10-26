import requests
import json
import pandas as pd
#This API contains calls for many stocks from Wall Street Bets.
#It does not actually take any informtion
#The documentation URL is https://dashboard.nbshare.io/apps/reddit/api/
url = "https://dashboard.nbshare.io/api/v1/apps/reddit"


request =  requests.get(url=url)
WSB_json = json.loads(request.text)
WSB_df = pd.DataFrame(WSB_json)
WSB_df = WSB_df.set_index("no_of_comments")
WSB_df.to_csv("Wall_Street_Bets.csv")
