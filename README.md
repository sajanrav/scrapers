# scrapers

| Ser. No. | Script Name	| Test Run 	| Sample Output ( if any ) | 
|----------|--------------|-----------|--------------------------|
| 1	       | get_indian_express_opinion_articles.py	| python get_indian_express_opinion_articles.py test_dir indian_express_opinion_sample.csv 5 | indian_express_opinion_sample.csv | 
| 2	       | get_mendocino_county_documents.py	| python get_mendocino_county_documents.py test_dir 10	| Set of 10 documents downloaded from the site | 
| 3	       | get_red_fit_data.py	  | python get_red_fit_data.py test_dir red_fit_sample.csv 2	 | red_fit_sample.csv | 
| 4	       | get_social_media_links_from_page.py	| python get_social_media_links_from_page.py https://stackoverflow.com	| {'facebook': 'https://www.facebook.com/officialstackoverflow/', 'twitter': 'https://twitter.com/stackoverflow', 'linkedin': 'https://linkedin.com/company/stack-overflow'} |
| 5            | get_cfbanalytics_data.py | python get_cfbanalytics_data.py 2012 ratings cfba_2012_ratings.csv output-dir sample_config/url_config_file | cfba_2012_ratings.csv |
| 6 	       | get_famous_quotes.py  | python get_famous_quotes.py famous_quotes.csv output-dir 	| famous_quotes.csv |
| 7            | get_uspto_patent_data.py | python get_uspto_patent_data.py test_dir uspto_patent_list.csv uspto_patent_info.csv | uspto_patent_info.csv |
| 8            | get_terms_from_dhatus.py | python get_terms_from_dhatus.py karmani | out_karmani.txt |
| 9            | get_eia_data.py | python get_eia_data.py | henry_hub_daily_gas_prices.csv |
|10            | get_bmc_dashboard.py | python get_bmc_dashboard.py | bmc_war_room_dashboard_20201002.pdf |