class Pagination:
    def __init__(self, data, items_on_page):
        if items_on_page < 0:
            raise Exception("items on page must be greater than zero")
        self.data = data
        self.items_on_page = items_on_page
        self.book = [data[i:i+items_on_page] for i in range(0, len(data), items_on_page)]

    @property
    def page_count(self):
        return len(self.book)

    @property
    def item_count(self):
        return len(self.data)

    def count_items_on_page(self, page_number):
        if page_number < len(self.book):
            return len(self.book[page_number])
        else:
            raise Exception("Invalid index. Page is missing")

    def find_page(self, data):
        if not data:
            raise Exception("Invalid data")
        needed = data.lower()
        found = []
        full_text = self.data.lower()

        if needed not in full_text:
            raise Exception(f"'{data}' is missing on the pages")

        indices = []
        index = full_text.find(needed)
        while index != -1:
            indices.append(index)
            index = full_text.find(needed, index + 1)

        for ind in indices:
            start_page = ind // self.items_on_page
            end = (ind + len(data) -1) // self.items_on_page
            for page in range(start_page, end+1):
                if page not in found:
                    found.append(page)

        return found

    
    def display_page(self, page_number):
        if page_number < len(self.book):
            return self.book[page_number]
        else:
            raise Exception("Invalid index. Page is missing")


if __name__ == "__main__":
    pass