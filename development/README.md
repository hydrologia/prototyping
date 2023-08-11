
<br>

### Development Notes

This repository's virtual environment is created via

```shell
    # Environment
    conda create --prefix .../miscellaneous
    conda activate miscellaneous
    
    # Python
    conda install -c anaconda python==3.11.3
    
    # Dask
    conda install -c anaconda dask==2023.5.1
                              toolz==0.12.0
                              cloudpickle==2.2.1    
                              python-graphviz==0.20.1
    # Jupyterlab
    conda install -c anaconda jupyterlab==3.6.3 nodejs==18.16.0 pywin32
    
    # Testing, Code Analysis
    conda install -c anaconda pytest coverage pylint pytest-cov flake8
    
    # Geography
    pip install geopandas    
    conda install -c anaconda folium
    pip install geopy
    
    # Replaces the anaconda channel version, which has a vulnerability
    conda install -c conda-forge requests
    
    # And
    conda install -c seaborn
    
```

The [filter.txt](/docs/filter.txt) document lists the core libraries of [requirements.txt](/requirements.txt).  Thus

```shell
    pip freeze -r docs/filter.txt > requirements.txt
```

Subsequently, retain `numpy`, `pandas`, and `yaml` within the second part of `requirements.txt`.  To generate the dotfile that [`pylint`](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html) - the static code analyser - will use for analysis, run

```shell
    pylint --generate-rcfile > .pylintrc
```

<br>
<br>

### Docker

A few references:

* [The best Docker base image for your Python application (March 2023)](https://pythonspeed.com/articles/base-image-python-docker-images/) by Itamar Turner-Trauring
* [Docker Official Images: Python](https://hub.docker.com/_/python/)

<br>
<br>

### Snippets

```python
import datetime

datetime.date.today() - datetime.timedelta(days=1)
```


<br>
<br>


### References

* [conda](https://docs.conda.io/projects/conda/en/stable/)
  * `conda search -i ....`
* [pip](https://pip.pypa.io/en/stable/)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
