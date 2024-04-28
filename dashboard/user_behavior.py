import os, sys
from dotenv import load_dotenv

rpath = os.path.abspath('/home/user/Documents/10/w1/tellco')

if rpath not in sys.path:
    sys.path.insert(0, rpath)
       
import utils.data_manager as dataManager
import script.user_engagement_analysis as analysis




    

def getTopCustomers():
    load_dotenv()
    database_uri = os.getenv("CLEANED_DATABASE_URI")
    dataM = dataManager.DataManager(database_uri)
    data = dataM.read_table_to_dataframe('xdr_data')    
    userEngagement = analysis.UserEngagementAnalyzer(data)
    aggregate_engagement_metrics= userEngagement.aggregate_engagement_metrics({
        'Bearer Id': 'count',
        'Dur. (ms)': 'sum',
        'Total UL (Bytes)': 'sum',
        # 'Total DL (Bytes)': 'sum'
    },"MSISDN/Number")
    return aggregate_engagement_metrics.nlargest(10, 'Bearer Id')
 