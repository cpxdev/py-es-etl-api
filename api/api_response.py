
class APIResponse(object):
        
    def build_insert_response(self, data):
        if len(data) > 0:        
            return {
                "statusCode" : 0,
                "message" : "Data added",
                "data" : data
            };
        else:
            return {
                "statusCode" : 1,
                "message" : "Data not added",
                "data" : ""
            };

    def build_search_response(self, data):
        if len(data) > 0:        
            return {
                "statusCode" : 0,
                "message" : "Data found",
                "data" : data
            };
        else:
            return {
                "statusCode" : 1,
                "message" : "Data not found",
                "data" : ""
            };
            
    def build_delete_response(self, count):
        return {
            "statusCode" : 0,
            "message" : str(count) + " record(s) deleted"
        };
        
    def build_bulk_insert_response(self, response):
        records_inserted = response[0]
        errors = response[1]
        return {
            "statusCode" : 0,
            "message" : str(records_inserted) + " record(s) inserted with " + str(len(errors)) + " errors",
            "errors" : errors
        };