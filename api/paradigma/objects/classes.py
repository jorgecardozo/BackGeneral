import math

class DataTransferResultSet:
    rows = []
    int_rows = 0
    int_total_rows = 0
    int_total_rows_filtered = 0
    int_page = 0
    int_total_pages = 0
    int_page_size = 0

    def __init__(self, 
        rows,
        int_total_rows_filtered, 
        int_total_rows, 
        int_page, 
        int_page_size):

        self.rows = rows
        self.int_total_rows = int_total_rows
        self.int_total_rows_filtered = int_total_rows_filtered
        self.int_page = int_page
        self.int_page_size = int_page_size
        
        self.int_rows = len(rows)
        self.int_total_pages = int(math.ceil(int_total_rows_filtered / int_page_size))

    def GetMeta(self):
        meta = {
            'rows': self.int_rows,
            'totalRows': self.int_total_rows,
            'totalRowsFiltered': self.int_total_rows_filtered,
            'page': self.int_page,
            'totalPages': self.int_total_pages,
            'pageSize': self.int_page_size,
        }
        return meta