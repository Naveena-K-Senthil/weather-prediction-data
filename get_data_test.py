from kfp.components import OutputPath


def get_data_test(output_path: OutputPath()):
    import urllib.request
    print("starting download...")
    url = "https://github.com/Naveena-K-Senthil/weather-prediction-data/blob/main/data/jfk_weather.csv"
    urllib.request.urlretrieve(url, output_path)
    print("done")

