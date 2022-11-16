from dataaclasses import dataaclass 

@dataaclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    