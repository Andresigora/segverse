import pandas_gbq
from google.oauth2 import service_account

CREDENTIALS = service_account.Credentials.from_service_account_file(filename='credentials/bigquery.json')
SEGMENTATION_SCHEMA = "segverse"

class BigQueryConnector():
    def __init__(self, credentials, segmentation_schema):
        self.credentials = credentials
        self.segmentation_schema = segmentation_schema
    
    def query(self, sql):
        res = pandas_gbq.read_gbq(sql,
                                 self.credentials.project_id,
                                 credentials=self.credentials,
                                 progress_bar_type=None
                                 )
        return res

    def get_segmentation(self, table_name, entity_id, segmentation_col):
        sql = """select CAST({entity_id} as STRING) as {entity_id},
                        {segmentation_col} as {segmentation_col}
                        from `{schema}.{table}`""".format(entity_id=entity_id, 
                                                         segmentation_col=segmentation_col,
                                                         schema=self.segmentation_schema,
                                                         table=table_name   
                                                        )
        seg = self.query(sql)
        return seg