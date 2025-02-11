from scrapy.exceptions import DropItem


class CleanDataPipeline:
    def process_item(self, item, spider):
        raw_data = item.get('raw_data', [])
        cleaned_data = [line.strip() for line in raw_data if line.strip()]
        formatted_data = "\n".join(cleaned_data)
        return item