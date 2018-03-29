default_app_config = 'core.apps.CoreConfig'

from core.commit_input_handler import main
process_data = main.ProcessData()
process_data.run_consumer()
