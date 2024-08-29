from azureml.datadrift import DataDriftDetector, AlertConfiguration
from azureml.core import Dataset, Workspace

ws = Workspace.from_config()

baseline_dataset = Dataset.get_by_name(ws, name='baseline-data')
target_dataset = Dataset.get_by_name(ws, name='new-data')

drift_detector = DataDriftDetector.create_from_datasets(ws, 'drift-detector', baseline_dataset, target_dataset)
drift_detector.run()

alert_config = AlertConfiguration(['charotamine@gmail.com'])
drift_detector.set_alert(alert_config)
