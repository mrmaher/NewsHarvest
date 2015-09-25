# NewsHarvest

Package for collecting headlines and news stories from the Associated Press, Bloomberg, and Reuters

Collect headlines and cooresponding data with this code:

```
from NewsHarvest.NewsHarvest import AssocitedPress, Reuters, Bloomberg
from NewsHavest.utilities import *

ap_data = AssociatedPress().get_data()
reuters_data = Reuters().get_data()
bloomberg_data = Bloomberg().get_data()
```

The get_data() method accepts these arguments:
* ```get_content=True``` - This determines whether or not you wish to scrape all visible text from the headlines' url
* ```sleep=True``` - This determines whether there is a one second pause between each headline scrape
* ```json_format=False``` - When set to True, it will output data into json format
* ```include_headings=False``` - When set to True, it will include the column headings in the output. This is espciall helpful when writing the output to a CSV file 

All news sources return these data points:
* Source
* Headline
* URL
* Exceprt
* Location (location is blank for Bloomberg)
* Publish_time
* Date
* Page_content (unless get_content is set to False)


Feedback is welcome at: mdgithub@gmail.com

## Associated Press

Sources within Associated Press: headlines (or home), business, US, world, sports, entertainment, health, science, politics

#### Example:
```
from NewsHarvest.NewsHarvest import AssocitedPress
from NewsHavest.utilities import *

ap_sources = ['headlines', 'business', 'us', 'world']
output = []
for source in ap_sources:
    source_data = AssociatedPress(source=source).get_data()
    for news_item in source_data:
        output.append(news_item)

write_to_csv(output, 'associatepress.csv')
```

## Reuters

Sources within Reuters: businessNews, wealth, bankruptcyNews, bondsNews, deals, economy, globalmarketsNews, hedgefunds, hotStocksNews, mergersNews,governmentfilingsNews, summitNews, USdollarreportNews, usmarkets

#### Example:

```
from NewsHarvest.NewsHarvest import Reuters
from NewsHavest.utilities import *

reuters_sources = ['businessNews', 'wealth', 'deals', 'economy']
output = []
for source in reuters_sources:
    source_data = Reuters(source=source).get_data()
    for news_item in source_data:
        output.append(news_item)

write_to_csv(output, 'reuters.csv')
```


## Bloomberg

Sources within Bloomberg: top news, markets

```
from NewsHarvest.NewsHarvest import Bloomberg
from NewsHavest.utilities import *

output = []
source_data = Bloomberg(source='top news').get_data()
for news_item in source_data:
    output.append(news_item)

write_to_csv(output, 'bloomberg.csv')
```

## Utilities Module

This module contains many functions that are used as helper functions in the NewsHarvest module. 

But it also contains many functions that should aid in exporting and importing data:

```
from NewsHarvest.NewsHarvest import AssocitedPress
from NewsHavest.utilities import *

data = AssociatedPress(source='headlines').get_data()
write_to_csv(data, 'outpt_file.csv')
write_to_txt(data, 'outpt_file.csv')

data = AssociatedPress(source='headlines').get_data()
append_to_csv(data, 'file_name.csv')

data = AssociatedPress(source='headlines').get_data(json_format=True)
write_json(data, 'output_file.csv')
```