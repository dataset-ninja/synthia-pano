Dataset **SYNTHIA-PANO** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMzM1M19TWU5USElBLVBBTk8vc3ludGhpYXBhbm8tRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiNmpHcGI2NTJnTXB4ZXo2VnM2Vm83Uk5udVk0R0RmeVg4NlRyd01sYTFSST0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22synthiapano-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='SYNTHIA-PANO', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://drive.google.com/drive/folders/1loj19uFyDOQDYI1xwWM6FameR_fUxJnQ?usp=drive_link).