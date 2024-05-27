SPIDER_MODULES = ["website_scraper.spiders"]

ITEM_PIPELINES = {
    "website_scraper.pipelines.MogiPipeline": 300,
    # "website_scraper.pipelines.CSVExportPipeline": 400,
}
