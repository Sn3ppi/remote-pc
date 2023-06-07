from math import ceil

class Button(dict):
    '''Конструктор кнопки.'''
    def __init__(self,
            text: str=None,
            callback_data: str=None,
            url: str=None
        ) -> None:
        super().__init__()
        self.update(text=b"\x00".decode("utf-8") if text is None else text)
        if url is None:
            self.update(callback_data=b"\x00".decode("utf-8") if callback_data is None else callback_data)
        else:
            self.update(url=url)    

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
    
    def __getitem__(self, key):
        return super().__getitem__(key)


class Row(list):
    '''Конструктор ряда кнопок.'''
    def __init__(self, *args) -> None:
        super().__init__()
        self._size = len(args)
        self._max_size = 5
        if self._size > self._max_size:
            raise ValueError(f"Row can not contain more items than {self._max_size}")
        else:
            self.extend(args)


class Keyboard(list):
    '''Конструктор клавиатуры.'''
    def __init__(self) -> None:
        super().__init__()
        self.depth = None
        self.current_menu = None
        self.previous_menu = None
        self.home_menu = None
        self.rows_per_page = None
        self._current_page = None
        self._max_pages = None
        self._upper_bar = []
        self._lower_bar = []
        self._static_rows = []
        self._dynamic_rows = []
        self._row_bound = None
        self._static_rows_count = None
        self._start_static_bound = None
        self._end_static_bound = None
        self._dynamic_rows_count = None
        self._start_dynamic_bound = None
        self._end_dynamic_bound = None
        self._total_rows_count = None
        self._start_idx = None
        self._end_idx = None
        self._start_static_idx = None
        self._end_static_idx = None
        self._start_dynamic_idx = None
        self._end_dynamic_idx = None
        self._dynamic_rows_generator = None
        self._dynamic_row_template = None     
        
    def add_static_items(self, rows: list) -> None:
        self._static_rows.extend(rows) 
        self._static_rows_count = len(rows)
        
    def add_dynamic_items(self, generator, template_row: list, count: int) -> None:
        self._dynamic_row_template = template_row
        self._dynamic_rows_generator = generator
        self._dynamic_rows_count = count
        
    def get_page(self, page: int=1) -> None:
        self._current_page = page
        if self._static_rows_count is None and self._dynamic_rows_count is not None:
            self._row_bound = 0
            self._total_rows_count = self._dynamic_rows_count
        elif self._dynamic_rows_count is None and self._static_rows_count is None:
            self._row_bound = 0
            self._total_rows_count = 0
        elif self._dynamic_rows_count is None and self._static_rows_count is not None:
            self._row_bound = max(self._static_rows_count - 1, 0)
            self._total_rows_count = self._static_rows_count
        elif self._dynamic_rows_count is not None and self._static_rows_count is not None:
            self._row_bound = max(self._static_rows_count - 1, 0)
            self._total_rows_count = self._static_rows_count + self._dynamic_rows_count
            
        self._max_pages = ceil(self._total_rows_count / self.rows_per_page)
        self._start_idx = (self._current_page - 1) * self.rows_per_page
        self._end_idx = max(min(self._current_page * self.rows_per_page, self._total_rows_count)-1, 0)
        
        if self._static_rows_count is not None:
            self._start_static_bound = 0
            self._end_static_bound = self._row_bound
        if self._dynamic_rows_count is not None:
            self._start_dynamic_bound = self._row_bound + 1
            self._end_dynamic_bound = self._end_idx
        
        if self._dynamic_rows_count is None:
            self._start_static_idx = self._start_idx
            self._end_static_idx = self._end_idx

        elif self._static_rows_count is None:
            self._start_dynamic_idx = self._start_idx
            self._end_dynamic_idx = self._end_idx

        elif self._end_idx < self._start_dynamic_bound:
            self._start_static_idx = self._start_idx
            self._end_static_idx = min(self._end_static_bound, self._end_idx)

        elif self._start_idx >= self._start_static_bound and self._start_idx <= self._end_static_bound and self._end_idx > self._end_static_bound:
            self._start_static_idx = self._start_idx
            self._end_static_idx = self._end_static_bound
            self._start_dynamic_idx = self._start_dynamic_bound - self._start_dynamic_bound
            self._end_dynamic_idx = min(self._end_idx, self._end_dynamic_bound) - self._start_dynamic_bound

        elif self._start_idx > self._end_static_bound:
            self._start_dynamic_idx = self._start_idx - self._start_dynamic_bound
            self._end_dynamic_idx = self._end_idx - self._start_dynamic_bound
        if self._dynamic_rows_count is not None and self._dynamic_rows_count:
            for data in self._dynamic_rows_generator(self._start_dynamic_idx, self._end_dynamic_idx):
                self._dynamic_rows.append(self._dynamic_row_template(data))      
        if self.depth > 1:      
            self._upper_bar.extend(
                Row(
                    Button(text="⬅️ Назад", callback_data=f"{self.previous_menu}.pg_1"),
                    Button(text="🏠 Домой", callback_data=f"{self.home_menu}.pg_1") if self.depth > 2 else Button()
                )
            )
        if self._max_pages > 1:
            self._lower_bar.extend(
                Row(
                    Button(text="⬅️⬅️", callback_data=f"{self.current_menu}.pg_1") if self._current_page > 2 else Button(),
                    Button(text="⬅️", callback_data=f"{self.current_menu}.pg_{self._current_page-1}") if self._current_page > 1 else Button(),
                    Button(text=f"{self._current_page}/{self._max_pages}"),
                    Button(text="➡️", callback_data=f"{self.current_menu}.pg_{self._current_page+1}") if self._max_pages >= self._current_page + 1 else Button(),
                    Button(text="➡️➡️", callback_data=f"{self.current_menu}.pg_{self._max_pages}") if self._max_pages > self._current_page + 1 else Button()
                )
            )  
            
        if self._upper_bar:
            self.append(self._upper_bar)
        if self._static_rows:
            for row in self._static_rows[self._start_static_idx:self._end_static_idx+1]:
                for button in row:
                    if button.get('callback_data') and button['callback_data'] != '\x00' and "pg_1" not in button['callback_data']:
                        button["callback_data"] += f".pg_{page}"
                self.append(row)  
        if self._dynamic_rows:
            for row in self._dynamic_rows:
                for button in row:
                    if button.get('callback_data') and button['callback_data'] != '\x00' and "pg_1" not in button['callback_data']:
                        button["callback_data"] += f".pg_{page}"
                self.append(row)
        if self._lower_bar:
            self.append(self._lower_bar)
        return self